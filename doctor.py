#!/usr/bin/env python3
"""Read-only setup checks. Never reads or prints credential contents."""
import importlib.util,subprocess,shutil,sys
from pathlib import Path
issues=[]
for module in ('pymupdf','PIL'):
 if importlib.util.find_spec(module) is None:issues.append('Missing dependency: '+module)
codex=shutil.which('codex')
if not codex:issues.append('Install Codex CLI and ensure codex is on PATH.')
else:
 try:
  r=subprocess.run([codex,'login','status'],capture_output=True,timeout=15)
  if r.returncode:issues.append('Codex is not signed in. Run codex login and complete the browser sign-in yourself.')
 except (OSError,subprocess.TimeoutExpired):issues.append('Could not check Codex login status.')
if sys.platform=='win32':issues.append('Run inside WSL2 Ubuntu, not native Windows.')
for issue in issues:print('ACTION:',issue)
print('Setup needs attention.' if issues else 'Ready: dependencies and local Codex sign-in found. Generation capabilities depend on your Codex tools and sources.')
sys.exit(bool(issues))
