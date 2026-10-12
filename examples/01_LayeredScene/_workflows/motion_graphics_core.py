"""Widget-free, deterministic motion model shared by baking and live Kit playback.

JSON is data, never executable code. Distances are scene centimetres, time seconds.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import uuid

PROFILE = 'CC-MOTION-01/0.1.1'
CONTROL_PRIM = '/World/MotionGraphControls'
CLONER = '/World/MotionGraphics/Cloner'
TOPOLOGY = {'rows': 32, 'columns': 32, 'seed': 7}
# One definition supplies validation, JSON comments, IDE schema and the Kit panel.
NUMBERS = {
    'strength': (1.0, 0, 1, 'Overall animated effect strength; zero gives the neutral cloner.'),
    'spacing_cm': (160.0, 50, 500, 'Grid spacing or spacing between rings.'),
    'amplitude_cm': (220.0, 0, 1500, 'Wave height.'),
    'wavelength_cm': (1600.0, 100, 10000, 'Distance between wave crests. Try 1800; near/below clone spacing the pattern can look irregular.'),
    'speed_hz': (0.25, -2, 2, 'Cycles per second, not percent. Try 0.5 (one cycle every 2 seconds); negative reverses travel; 0 freezes the wave.'),
    'phase_degrees': (0.0, -360, 360, 'Wave phase offset.'),
    'direction_degrees': (25.0, -180, 180, 'Direction in degrees; affects plane waves only.'),
    'base_scale': (0.7, 0.1, 3, 'Neutral clone scale multiplier.'),
    'scale_wave': (0.45, 0, 0.9, 'Wave-driven scale modulation relative to base scale.'),
    'rotation_degrees': (35.0, 0, 180, 'Wave-driven clone tilt.'),
    'spin_degrees_per_second': (45.0, -360, 360, 'Continuous clone spin.'),
    'noise_cm': (25.0, 0, 500, 'Deterministic per-clone bobbing amplitude.'),
    'noise_speed_hz': (0.5, 0, 2, 'Noise oscillation speed.'),
    'falloff_radius_cm': (4500.0, 100, 20000, 'Effect fades to zero at this radius. Try 12000 so most clones move; a small radius leaves outer clones still.'),
    'color_cycle_hz': (0.375, 0, 2, 'Prototype steps per second among three shared material configurations.'),
}
CHOICES = {'layout': ('grid', 'rings', 'spiral'), 'wave_mode': ('plane', 'radial', 'swirl')}


def control_hints():
    return {'live_preview': 'true = live JSON; false = saved animation (other JSON controls then have no effect).',
            'layout': 'Choose "grid", "rings" or "spiral". Keep the quotes.',
            'wave_mode': 'Choose "plane", "radial" or "swirl". Keep the quotes.',
            **{name: f'Range {lo} to {hi}; default {val}. {help_text}'
               for name, (val, lo, hi, help_text) in NUMBERS.items()}}


def annotated_controls(controls):
    """JSON has no comment syntax: optional string fields carry adjacent hints."""
    return {key: value for name, hint in control_hints().items()
            for key, value in ((f'_comment_{name}', hint), (name, controls[name]))}


def default_document():
    return {
        'controls': annotated_controls({'live_preview': True, 'layout': 'grid', 'wave_mode': 'radial',
                     **{name: item[0] for name, item in NUMBERS.items()}}),
        'schema_version': 1,
        'topology': dict(TOPOLOGY),
        '_help': {'edit': 'Edit the values after each _comment_ hint and SAVE, or use the Motion Graphics Controls panel. Hints are ignored by motion evaluation.',
                  'syntax': 'Keep commas between entries and quotes around text. Use decimal numbers like 0.5, not 500. No // comments or literal line breaks inside strings.',
                  'topology': 'Fixed 32 x 32 for stable IDs; changing topology requires a separate rebuild.',
                  'live_preview': 'false removes the temporary runtime layer and resumes the saved animation.',
                  'layout': 'grid, rings, spiral', 'wave_mode': 'plane, radial, swirl',
                  'bake': 'Saved clip is 8 seconds at 60 time codes/s, sampled every 2 frames. JSON changes are live only until explicitly baked.',
                  'fields': {name: item[3] for name, item in NUMBERS.items()}},
    }


def control_schema():
    hints = control_hints()
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': PROFILE, 'type': 'object', 'additionalProperties': False,
            'required': ['controls', 'schema_version', 'topology'],
            'properties': {
                '$schema': {'type': 'string'}, '_help': {'type': 'object'},
                'schema_version': {'const': 1}, 'topology': {'const': TOPOLOGY},
                'controls': {'type': 'object', 'additionalProperties': False,
                    'required': list(hints),
                    'properties': {
                        'live_preview': {'type': 'boolean', 'description': hints['live_preview']},
                        **{name: {'enum': list(choices), 'description': hints[name]} for name, choices in CHOICES.items()},
                        **{name: {'type': 'number', 'default': val, 'minimum': lo, 'maximum': hi,
                                  'description': hints[name]}
                           for name, (val, lo, hi, _) in NUMBERS.items()},
                        **{f'_comment_{name}': {'type': 'string', 'readOnly': True, 'description': 'Documentation only; ignored by the motion model.'}
                           for name in hints}}}}}


def validate(document):
    if not isinstance(document, dict) or type(document.get('schema_version')) is not int or document['schema_version'] != 1:
        raise ValueError('Expected schema_version 1 JSON object.')
    if set(document) - {'controls', 'schema_version', 'topology', '_help', '$schema'}:
        raise ValueError('Unknown top-level field; only controls are live editable.')
    if document.get('topology') != TOPOLOGY:
        raise ValueError('Topology must remain 32 x 32, seed 7; live resizing is unsupported.')
    controls = document.get('controls')
    required = {'live_preview', 'layout', 'wave_mode', *NUMBERS}
    hints = {f'_comment_{name}' for name in required}
    if not isinstance(controls, dict) or not required <= controls.keys() or controls.keys() - required - hints:
        raise ValueError(f'Controls require {sorted(required)}; only their optional _comment_ strings may be added.')
    if any(not isinstance(value, str) for key, value in controls.items() if key in hints):
        raise ValueError('_comment_ hints must be quoted strings.')
    controls = {name: controls[name] for name in control_hints()}
    if type(controls['live_preview']) is not bool:
        raise ValueError('live_preview must be true or false.')
    if controls['layout'] not in ('grid', 'rings', 'spiral') or controls['wave_mode'] not in ('plane', 'radial', 'swirl'):
        raise ValueError('Unknown layout or wave_mode.')
    problems = []
    for name, (_, low, high, _) in NUMBERS.items():
        value = controls[name]
        if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
            problems.append(f'{name}={value!r}: expected a finite number from {low} to {high}')
    if problems:
        raise ValueError('; '.join(problems))
    return dict(controls)


def read_snapshot(path):
    """Bounded, stable read, safe for a worker thread; no stage access."""
    path = Path(path)
    before = path.stat()
    if before.st_size > 65536:
        raise ValueError('Control file exceeds 64 KiB.')
    with path.open('rb') as stream:
        raw = stream.read(65537)
    after = path.stat()
    if len(raw) > 65536 or (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size):
        raise ValueError('File changed during read; waiting for a complete save.')
    return raw, hashlib.sha256(raw).hexdigest()


def parse_document(raw):
    try:
        document = json.loads(raw)
    except json.JSONDecodeError as error:
        line = error.doc.splitlines()[error.lineno - 1] if error.doc.splitlines() else ''
        excerpt = line[max(0, error.colno - 45):error.colno + 70]
        raise ValueError(f'JSON syntax at line {error.lineno}, column {error.colno}: {error.msg}\nNear: {excerpt}\nCheck commas, closing quotes and line breaks inside strings.') from error
    except UnicodeDecodeError as error:
        raise ValueError('Save controls as UTF-8 JSON text.') from error
    return document, validate(document)


def read_controls(path):
    raw, digest = read_snapshot(path)
    return parse_document(raw)[1], digest


def save_controls(path, controls, expected_digest):
    """Explicit panel save; preserve prior bytes and reject a stale editor draft."""
    path = Path(path)
    before, digest = read_snapshot(path)
    if not expected_digest or digest != expected_digest:
        raise ValueError('JSON changed since this panel draft was loaded. Click Reload JSON, review the values, then Apply & Save again.')
    try:
        document, _ = parse_document(before)
    except ValueError:
        # An explicit panel save can replace malformed input; its bytes survive below.
        document = default_document()
    document['controls'] = annotated_controls(controls)
    document['$schema'] = './motion_graphics.schema.json'
    validate(document)
    output = (json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
    backup = path.parents[2] / '_pipeline_reports/motion_graphics' / ('panel_save_' + uuid.uuid4().hex)
    backup.mkdir(parents=True)
    (backup / path.name).write_bytes(before)
    (backup / 'change.json').write_text(json.dumps({'operation': 'explicit panel control save',
        'before_sha256': digest, 'after_sha256': hashlib.sha256(output).hexdigest()}, indent=2), encoding='utf-8')
    temporary = path.with_name('.motion_controls_' + uuid.uuid4().hex + '.tmp')
    try:
        temporary.write_bytes(output)
        if read_snapshot(path)[1] != digest:
            raise ValueError('JSON changed while saving. Nothing replaced; Reload JSON before retrying.')
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return document, hashlib.sha256(output).hexdigest(), backup


def evaluate(controls, seconds):
    """Return positions, wxyz orientations, scales and six prototype indices."""
    positions, orientations, scales, indices = [], [], [], []
    spacing = controls['spacing_cm']
    direction = math.radians(controls['direction_degrees'])
    temporal = math.tau * seconds * controls['speed_hz'] + math.radians(controls['phase_degrees'])
    for row in range(32):
        for column in range(32):
            index = row * 32 + column
            if controls['layout'] == 'grid':
                x, y = (column - 15.5) * spacing, (row - 15.5) * spacing
            elif controls['layout'] == 'rings':
                angle = math.tau * column / 32
                radius = (row + 2) * spacing * 0.65
                x, y = radius * math.cos(angle), radius * math.sin(angle)
            else:
                angle = index * 2.399963229728653
                radius = spacing * math.sqrt(index) * 0.6
                x, y = radius * math.cos(angle), radius * math.sin(angle)
            radius = math.hypot(x, y)
            distance = x * math.cos(direction) + y * math.sin(direction) if controls['wave_mode'] == 'plane' else radius
            phase = math.tau * distance / controls['wavelength_cm'] - temporal
            if controls['wave_mode'] == 'swirl':
                phase += 3 * math.atan2(y, x)
            f = max(0.0, 1 - radius / controls['falloff_radius_cm'])
            falloff = f * f * (3 - 2 * f)
            effect = controls['strength'] * falloff
            wave = math.sin(phase)
            noise = math.sin(index * 12.9898 + TOPOLOGY['seed'] + math.tau * seconds * controls['noise_speed_hz'])
            z = effect * (controls['amplitude_cm'] * wave + controls['noise_cm'] * noise)
            # Default elevation; extreme user amplitudes may cross the ground.
            positions.append((x, y, 700 + z))
            scale = controls['base_scale'] * (1 + effect * controls['scale_wave'] * wave)
            scales.append((scale, scale, scale * (1 + 0.2 * effect * math.cos(phase))))
            tilt = math.radians(effect * controls['rotation_degrees'] * wave) / 2
            spin = math.radians(controls['strength'] * controls['spin_degrees_per_second'] * seconds) / 2
            # qZ(spin) * qX(tilt), normalized analytically.
            orientations.append((math.cos(spin) * math.cos(tilt), math.cos(spin) * math.sin(tilt),
                                 math.sin(spin) * math.sin(tilt), math.sin(spin) * math.cos(tilt)))
            color = (row + column + math.floor(seconds * controls['color_cycle_hz'])) % 3
            indices.append(((row + column) % 2) * 3 + color)
    return positions, orientations, scales, indices


def usd_values(frame):
    from pxr import Gf, Vt
    positions, orientations, scales, indices = frame
    # Conservative bound for these 100 cm sources at Size=Normal, including tilt.
    margin = max(max(v) for v in scales) * 150
    bounds = [tuple(min(v[i] for v in positions) - margin for i in range(3)),
              tuple(max(v[i] for v in positions) + margin for i in range(3))]
    return {
        'positions': Vt.Vec3fArray([Gf.Vec3f(*v) for v in positions]),
        'orientations': Vt.QuathArray([Gf.Quath(q[0], Gf.Vec3h(*q[1:])) for q in orientations]),
        'scales': Vt.Vec3fArray([Gf.Vec3f(*v) for v in scales]),
        'protoIndices': Vt.IntArray(indices),
        'extent': Vt.Vec3fArray([Gf.Vec3f(*v) for v in bounds]),
    }
