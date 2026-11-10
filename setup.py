#!/usr/bin/env python3
"""Bootstrap the app, not a setuptools package."""
import sys,subprocess,venv
from pathlib import Path
APP=Path(__file__).resolve().parent
if sys.version_info<(3,10):raise SystemExit('Python 3.10 or newer is required.')
if sys.platform=='win32':raise SystemExit('Use Ubuntu in WSL2; see SETUP_CODEX.md. Native Windows is not supported yet.')
if not (APP/'.venv/bin/python').exists():venv.EnvBuilder(with_pip=True).create(APP/'.venv')
python=APP/'.venv/bin/python'
subprocess.run([str(python),'-m','pip','install','-r',str(APP/'requirements.txt')],check=True)
subprocess.run([str(python),'-c','from seed_projects import ensure_projects; ensure_projects()'],cwd=APP,check=True)
subprocess.run([str(python),str(APP/'doctor.py')],cwd=APP,check=True)
print('Ready: .venv/bin/python launcher.py')
