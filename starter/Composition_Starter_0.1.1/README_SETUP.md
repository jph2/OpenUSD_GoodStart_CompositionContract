# Create a Composition Contracts project

**Version 0.1.1.** Choose one of these three ways to copy the preset to your project location. All produce the same scene files and folder structure.

## 1. Extract manually — no scripts

Use **Extract All** on `Composition_Starter.zip` and choose a fresh project folder. You can then copy the entire extracted structure wherever you want. Preserve relative paths and open scenes only after extraction; do not work inside the ZIP.

## 2. Run PowerShell setup

Keep `Create_Composition_Project.ps1` beside the ZIP. From that folder, run:

```powershell
.\Create_Composition_Project.ps1 -Destination "E:\Projects\MyWorkcell"
```

This creates the destination folders and extracts the preset. Without `-Destination`, it extracts beside the script. Existing destination files with matching names stop setup before extraction.

## 3. Run batch setup

Keep the BAT, PS1 and ZIP together. Copy this setup folder to your intended location and double-click `Create_Composition_Project.bat` to extract beside it. Alternatively, choose a destination from a terminal:

```bat
Create_Composition_Project.bat -Destination "E:\Projects\MyWorkcell"
```

The batch file calls the same PowerShell setup script. It uses `-ExecutionPolicy Bypass` for that process only; it does not change the saved Windows execution policy.

## What setup changes

Setup writes project folders and files at the destination. It does not launch Kit or install applications, solvers or connectors. Script setup requires Windows PowerShell; no Python, network access or administrator rights are needed. Inspect the scripts before running them if desired. If extraction is interrupted, partial new files may remain. Use a fresh folder; setup does not migrate existing projects. For manual extraction, avoid merging into an existing project or accepting overwrite prompts.

## After setup

Read **README.md inside the extracted project** for scenes, authoring and diagrams. Open `SceneROOT_STARTER.usda` directly in an installed compatible Kit application, or run `Open_In_Kit.ps1 -Scene STARTER` for Opinion authoring and layer protection. That launcher starts Kit; the setup scripts only extract files.

There are two entry documents: this `README_SETUP.md` beside the ZIP, and the project's `README.md` inside it. No separate `START_HERE.md` is needed.
