# Simple Macro (Windows)

A tiny GUI to build a repeating macro with two step types:
- Click center of screen
- Wait for N seconds

## Run
```bash
python -m pip install -r requirements.txt
python app.py
```

## Build .exe
```bat
build.bat
```

## Build .exe on GitHub (from macOS)
1. Push to the `main` branch.
2. Open the repo on GitHub and go to Actions → `build-windows-exe`.
3. Run the workflow or wait for it to run on push.
4. Download the `SimpleMacro-windows` artifact (contains `SimpleMacro.exe`).

## Use
1. Add steps (Click Center / Wait).
2. Click "Run Forever".
3. Click "Stop" to end the loop.

Notes:
- Keep the window visible to stop the macro.
- PyAutoGUI may ask for accessibility permissions on first run.
