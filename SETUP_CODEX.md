# Codex: install this for me

Complete the following on the user's machine. They should not need to understand terminals. Report the final URL and any actual blocker.

1. Clone this repository into a standalone writable directory (not inside an existing studio project). Do not clone another person's private project data. Read this AGENTS.md.
2. Check OS. Use macOS/Linux; on Windows use WSL2 Ubuntu and keep the repository inside its Linux home. Native Windows is not supported. Check Python >=3.10 with venv/pip and Git. Install missing prerequisites with the user's normal package manager where authorized; Ubuntu may need python3-venv. Never alter system Python packages.
3. Find `codex` on PATH. If missing, consult https://learn.chatgpt.com/docs/codex/cli and install the official Codex CLI for this OS. Do not assume the desktop app's private binary is portable.
4. Run `codex login status` without displaying credentials. If login is required, run `codex login` and let the user complete the browser login with THEIR account. Do not request passwords, copy auth.json, reuse someone else's session, or add API keys to the repository. Check status again. Local ChatGPT sign-in uses the account's eligible Codex entitlement/limits; an API-key session is billed separately.
5. Run `python3 setup.py`. This creates .venv, installs requirements, seeds three independent local projects once, and checks local sign-in. Resolve an actual installation failure and retry; do not report ready on a failed doctor.
6. Run `.venv/bin/python -m unittest discover -s tests`. Run `.venv/bin/python doctor.py`. No model call is needed for these tests.
7. Run `.venv/bin/python launcher.py`. Default URL http://127.0.0.1:8766. If occupied, set LANDSCAPE_STUDIO_PORT to a free port in this process environment; never stop another application's server. Verify /api/status identifies landscape-studio-community, /api/library has three course projects, and the page opens. On WSL, open the printed localhost URL in the Windows browser if browser launching is unavailable.
8. Explain the short flow: New production → project → upload/select reference(s) → Create. References and My work initially contain no other student's materials. New project accepts the user's syllabus/brief/boards and a study frame. For a preset, add the user's own documents to data/projects/<project_id>/documents, raw data to sources, existing boards to boards; update project.json asset inventory and BRIEF.md with their permission. Restart only an idle server to refresh manually added catalog files, or use the app's rescan endpoint with its local session token.
9. Check available Codex drawing/image-generation and research tools before the first real job. CLI sign-in does not guarantee every desktop image tool/plugin is available to codex exec. Native diagram generation can use Python/SVG/PDF. Photographic collage requires authentic imagery; AI raster generation requires a tool available in the user's Codex execution environment. If missing, explain the limitation and help configure supported tools; do not invent outputs or silently activate a paid API fallback. Do not promise that all reference types work merely because setup passed.
10. Leave the app running and provide the Start.command shortcut on macOS or `.venv/bin/python launcher.py` on Linux/WSL. Do not auto-launch a production; the user's Create action authorizes it.

## Updating and backup

Stop only this app when no jobs run, then git pull and rerun setup.py. Runtime files are ignored and seeded presets never overwrite an existing project.json. Back up data/, jobs/ and any external user sources privately. To move an existing installation to another path, have Codex migrate the local project root/asset paths and database paths; a fresh clone is portable but runtime absolute paths are not a migration format.

## Troubleshooting

- No engine: ensure `codex` is on the same PATH as the server and login status succeeds.
- Missing data: presets are briefs, not surveyed maps. Supply your own site geometry or let Codex research available sources with provenance.
- Missing Pillow/PyMuPDF: use the .venv Python, not the system Python.
- Jobs need review: open stage evidence and fix the named source/tool issue; do not bypass integrity checks.
- Server logs: data/server.log (local only). Do not upload logs without inspecting them for private data.
