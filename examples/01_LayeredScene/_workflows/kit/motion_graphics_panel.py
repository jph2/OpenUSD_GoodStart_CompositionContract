"""Native Kit controls; values and file operations belong to the shared model/controller."""
import omni.ui as ui


class MotionControlsPanel:
    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        self.path = None
        self.base_digest = None
        self.dirty = False
        self.loading = False
        self.busy = False
        self.listeners = []
        self.values = {}
        self.combos = {}
        self.window = None
        hints = model.control_hints()
        try:
            self.build(hints)
        except Exception:
            self.destroy()
            raise

    def build(self, hints):
        controller, model = self.controller, self.model
        self.window = ui.Window('Motion Graphics Controls', width=620, height=860, visible=True)
        with self.window.frame:
            with ui.VStack(spacing=8):
                ui.Label('1. Change controls   2. Apply & Save JSON   3. Play', height=24)
                self.path_label = ui.Label('Waiting for SceneROOT_MotionGraphics.usda', height=40, word_wrap=True)
                self.runtime_status = ui.Label('CONNECTING — waiting for the current USD stage...', height=56, word_wrap=True)
                self.probe_status = ui.Label('Playback read-back: waiting for Play.', height=42, word_wrap=True)
                self.status = ui.Label('Starting controller...', height=64, word_wrap=True)
                self.draft_status = ui.Label('No file loaded.', height=0, word_wrap=True)
                with ui.HStack(height=30, spacing=6):
                    self.save_button = ui.Button('Apply & Save JSON', clicked_fn=self.save, enabled=False)
                    self.reload_button = ui.Button('Reload JSON', clicked_fn=controller.reload_from_panel, enabled=False)
                    self.preset_button = ui.Button('Visible wave preset', clicked_fn=self.preset, enabled=False)
                self.playback = ui.HStack(height=28, spacing=6)
                with self.playback:
                    ui.Button('Play', clicked_fn=controller.play)
                    ui.Button('Pause', clicked_fn=controller.pause)
                    ui.Button('Reconnect', clicked_fn=controller.reconnect,
                              tooltip='Reload saved controls and recreate this controller\'s preview. Discards unsaved panel edits.')
                ui.Label('Writes only the DATA JSON. USD animation is not baked by this panel.', height=20)
                self.edit_area = ui.ScrollingFrame(horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF)
                with self.edit_area:
                    with ui.VStack(spacing=10, height=0):
                        with ui.HStack(height=24, spacing=8):
                            ui.Label('Live preview', width=160)
                            value = ui.SimpleBoolModel(True)
                            ui.CheckBox(model=value, width=24)
                            self.track('live_preview', value)
                        ui.Label(hints['live_preview'], height=0, word_wrap=True)
                        for name, choices in model.CHOICES.items():
                            with ui.HStack(height=26, spacing=8):
                                ui.Label(name.replace('_', ' ').title(), width=160)
                                combo = ui.ComboBox(0, *choices)
                                self.combos[name] = combo
                                self.track(name, combo.model.get_item_value_model())
                            ui.Label(hints[name], height=0, word_wrap=True)
                        for name, (default, low, high, help_text) in model.NUMBERS.items():
                            ui.Separator(height=2)
                            ui.Label(f'{name}  |  range {low} to {high}', height=22)
                            value = ui.SimpleFloatModel(default)
                            value.set_min(float(low))
                            value.set_max(float(high))
                            ui.FloatSlider(model=value, min=float(low), max=float(high),
                                           step=0.01, format='%.3f', height=26, tooltip=hints[name])
                            self.track(name, value)
                            ui.Label(help_text, height=0, word_wrap=True)
                ui.Label('Close hides this panel; live control continues. Rerun the bootstrap to reopen.', height=30, word_wrap=True)
        self.window.focus()

    def track(self, name, value):
        self.values[name] = value
        token = value.add_value_changed_fn(self.changed)
        self.listeners.append((value, token))

    def changed(self, *_):
        if not self.loading:
            self.dirty = True
            self.draft_status.text = 'DRAFT ONLY — click Apply & Save JSON to change the scene.'

    def set_busy(self, busy):
        self.busy = busy
        self.edit_area.enabled = bool(self.path) and not busy
        self.save_button.enabled = bool(self.path and self.base_digest) and not busy
        self.reload_button.enabled = bool(self.path) and not busy
        self.preset_button.enabled = bool(self.path) and not busy

    def bind(self, path):
        self.path = path
        self.base_digest = None
        self.dirty = False
        self.path_label.text = str(path) if path else 'Open SceneROOT_MotionGraphics.usda to enable these controls.'
        self.draft_status.text = 'Reading JSON...' if path else 'No motion control file attached.'
        self.set_busy(False)

    def fill(self, controls):
        self.loading = True
        try:
            for name, value in controls.items():
                self.values[name].set_value(self.model.CHOICES[name].index(value) if name in self.model.CHOICES else value)
        finally:
            self.loading = False

    def accepted(self, controls, digest, force=False):
        if self.dirty and not force:
            self.draft_status.text = 'JSON accepted, but panel has an unapplied draft. Reload JSON to replace the draft.'
            return
        self.fill(controls)
        self.base_digest = digest
        self.dirty = False
        self.draft_status.text = 'Panel matches accepted JSON.'
        self.set_busy(self.busy)

    def rejected(self, message, digest=None, force=False):
        self.set_status('NOT APPLIED — keeping last valid motion, or the saved clip.\n' + message, error=True)
        # Keep the usable values displayed. Explicit Save can repair this revision,
        # with original bytes backed up. An existing draft keeps its old revision.
        if (not self.dirty or force) and digest:
            self.base_digest = digest
            self.draft_status.text = 'File is invalid. Adjust the displayed values or choose a preset, then Apply & Save to repair it (backup kept).'
        self.set_busy(self.busy)

    def set_status(self, text, error=False):
        self.status.text = text
        self.status.style = {'color': 0xFF8D8DFF if error else 0xFFBFE6B7}

    def set_runtime(self, text, error=False):
        self.runtime_status.text = text
        self.runtime_status.style = {'color': 0xFF8D8DFF if error else 0xFFBFE6B7}

    def set_probe(self, text, error=False):
        self.probe_status.text = text
        self.probe_status.style = {'color': 0xFF8D8DFF if error else 0xFFBFE6B7}

    def preset(self):
        controls = self.model.validate(self.model.default_document())
        controls.update(layout='rings', wave_mode='plane', amplitude_cm=600.0,
                        wavelength_cm=1800.0, speed_hz=0.5, base_scale=1.0,
                        scale_wave=0.8, rotation_degrees=60.0, falloff_radius_cm=12000.0)
        self.fill(controls)
        self.changed()

    def save(self):
        controls = {name: value.as_float for name, value in self.values.items() if name in self.model.NUMBERS}
        controls['live_preview'] = self.values['live_preview'].as_bool
        for name, choices in self.model.CHOICES.items():
            controls[name] = choices[self.values[name].as_int]
        self.controller.save_from_panel(controls, self.base_digest)

    def destroy(self):
        for value, token in self.listeners:
            value.remove_value_changed_fn(token)
        self.listeners.clear()
        if self.window is not None:
            self.window.destroy()
            self.window = None
        self.values.clear()
        self.combos.clear()
        self.controller = None
