# Landscape Studio

A local landscape-design workspace: choose a project, add visual references, create fresh drawings, review alternatives and Push toward the selected reference. Includes project galleries, drag-and-drop reference uploads, concurrent job tracking and staged board-set production.

## En kolay kurulum

Bu reponun linkini **kendi bilgisayarında çalışan Codex'e** verip şunu yaz:

> Bu repoyu bilgisayarımda bağımsız bir klasöre klonla. AGENTS.md ve SETUP_CODEX.md dosyalarını oku; gerekli bağımlılıkları kur, kendi Codex hesabımla giriş durumunu kontrol et, testleri çalıştır ve Landscape Studio'yu tarayıcımda aç. Giriş gerekiyorsa resmi tarayıcı girişini bana bırak. Örnek üretim başlatma.

Kurulumdan sonra **New production → Project → Reference → Create**. İlk referans ana görsel dili belirler; diğerleri destekleyicidir. Kendi referanslarını sürükleyip bırakabilirsin. Pafta setleri için **Boards**, sonuçlar için **My work**, devam eden işler için **Activity**.

## Included starter projects

| Project | Site | Brief |
|---|---|---|
| Landscape Design IV | Yunuseli / Nilüfer, Bursa | Neutral summary of the supplied course brief |
| Landscape Design II | Tarsus / Berdan | Generic site starter; add your syllabus |
| Landscape Design III | Küçükçekmece, Istanbul | Generic site starter; add your syllabus |

No student names, numbers, personal design goals, chat records, old productions, locked jury boards, private maps or credentials are included. No personal Pinterest archive is redistributed. Blank galleries are intentional. The presets do not establish surveyed site boundaries or an approved programme. Each student develops their own project and adds their own source materials.

## Manual quick start

Requires Python 3.10+, Git and the official Codex CLI on macOS/Linux (Windows: WSL2 Ubuntu).

```sh
codex login
python3 setup.py
.venv/bin/python launcher.py
```

Open http://127.0.0.1:8766. macOS: subsequent launches can use `Start.command`. Set `LANDSCAPE_STUDIO_PORT` if the port is occupied.

## Your own account, local execution

The app invokes the locally installed Codex CLI; each person signs in to their own account. ChatGPT sign-in uses eligible Codex subscription access and limits. API-key authentication uses separate API billing. Studio has no shared account or bundled API quota. [Official authentication documentation](https://learn.chatgpt.com/docs/auth).

This is **not a hosted ChatGPT login website**. A static deployment cannot run its Python worker or access the user's local files/CLI. No supported third-party website subscription-login integration is implemented here. Keep the server on localhost; do not expose agent execution through a public tunnel. A hosted edition would need a separate backend, authentication, per-user storage/execution isolation and an explicitly supported billing/auth design.

Image-generation and research tools available to Codex vary by installation. Login alone does not install every desktop plugin. The app checks output evidence and reports missing capabilities instead of claiming a finished result. It cannot guarantee reference-perfect or jury-ready work. [Setup and capability checks](SETUP_CODEX.md).

## Project files and privacy

Local-only folders: `data/` (projects, uploads, SQLite), `jobs/` (prompts, sources, outputs), `cache/`, `web/generated/` (previews). These are gitignored. Only educational presets and application code are distributed. Codex model requests and enabled tools may transmit selected content to their providers; “local” describes storage/execution, not an offline model. OSM map tiles, Photon search and Google Fonts make external requests from the UI.

Add a new project using **New project** or have Codex attach your documents to a starter project following SETUP_CODEX.md. Never commit personal sources or credentials.

## Development

```sh
.venv/bin/python -m unittest discover -s tests
.venv/bin/python doctor.py
```

Python HTTP server, SQLite, vanilla JavaScript, Leaflet. No Node build required. Tests use isolated temporary state and mock generation; they do not spend model credits. See [third-party notices](THIRD_PARTY_NOTICES.md).
