# Landscape Studio — community installation

If the user asks to install/open this app, carry out SETUP_CODEX.md fully. Do not stop after listing commands. This repository is a self-contained, local-first application. Do not inherit course/person-specific conventions from another directory. Install into a standalone folder outside another student's project.

- Never copy credentials, other chat histories, local paths or private source materials into Git. Never read or print auth.json contents. Each person signs in to their own Codex CLI using the official browser flow.
- Bind the server to 127.0.0.1 only. Do not publish this executable local agent as a public server or tunnel it.
- Presets contain neutral educational briefs, not approved designs or surveyed basemaps. data/projects contains the user's writable copies. Never overwrite their edits on update.
- New visual content must use the current user's evidence and selected references. Preserve original files. Prior finished illustrations are not default subjects or raw site evidence.
- The app is Python + vanilla JS; no frontend build. Run .venv/bin/python -m unittest discover -s tests before changing execution workflows. Use a separate port and an isolated copy for smoke tests. Do not start a paid generation merely to test setup.
- macOS and Linux supported; Windows uses WSL2 Ubuntu. Native Windows is not supported because the workers use POSIX process handling and file locks.
- Generated outputs, uploads, database, previews and logs are private runtime files, never repository assets.
