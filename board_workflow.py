from evidence_resolution import GUIDANCE as EVIDENCE_RESOLUTION
"""Reference-backed board-set gates. Reports support review, never prove visual quality."""
import json
import board_design_protocol
from pathlib import Path

APP = Path(__file__).resolve().parent
STAGES = [
    {'id': 'evidence', 'title': 'Evidence + reference'},
    {'id': 'narrative', 'title': 'Narrative + content plan'},
    {'id': 'drawings', 'title': 'Fresh drawing production'},
    {'id': 'composition', 'title': 'Board composition'},
    {'id': 'review', 'title': 'Visual + factual review'},
    {'id': 'export', 'title': 'Verified delivery'},
]
REPORTS = {'evidence': 'board_evidence.json', 'narrative': 'board_plan.json',
           'drawings': 'board_drawings.json', 'composition': 'board_composition.json',
           'review': 'board_review.json', 'export': 'board_delivery.json'}
SIZES = {'A0': (841, 1189), 'A1': (594, 841)}

def normalize(req):
    raw = req.get('board_workflow')
    if raw is None:
        return None
    if not isinstance(raw, dict) or raw.get('version') != 1:
        raise ValueError('Choose a supported board production workflow.')
    count = raw.get('count', 5)
    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 8:
        raise ValueError('Choose 1 to 8 boards.')
    size, orientation = raw.get('size', 'A0'), raw.get('orientation', 'portrait')
    if size not in SIZES or orientation not in ('portrait', 'landscape'):
        raise ValueError('Choose A0 or A1 and a valid orientation.')
    brief = raw.get('brief', '')
    focus = raw.get('focus', '')
    if not isinstance(brief, str) or not 10 <= len(brief.strip()) <= 16000:
        raise ValueError('Describe the project and board purpose in 10–16000 characters.')
    if not isinstance(focus, str) or len(focus) > 4000:
        raise ValueError('Board priorities must be under 4000 characters.')
    if req.get('alternative_count', 1) != 1:
        raise ValueError('A board workflow produces one coordinated set per run.')
    return {'version': 1, 'count': count, 'size': size, 'orientation': orientation,
            'brief': brief.strip(), 'focus': focus.strip()}

def brief(req):
    r = normalize(req)
    if r is None:
        return ''
    hierarchy=req.get('board_reference_hierarchy',[])
    reference_rule=('Ordered visual inspirations: '+json.dumps(hierarchy,ensure_ascii=False)+'. The first selection is the primary visual inspiration and later selections supply compatible details. These roles NEVER override the current project purpose, jury feedback, evidence, programme or required content. Adapt composition and drawing types to the current argument; do not reproduce the reference layout mechanically.' if hierarchy else 'No benchmark is bundled. Develop graphic grammar from the current brief; inspect user-selected references when present. Never claim to have inspected absent reference pages.')
    return f'''
BOARD SET WORKFLOW — design protocol v2 — staged production, not one compositing prompt.
Create {r['count']} {r['size']} {r['orientation']} boards as ONE coherent narrative for the TARGET project.
Project intent: {r['brief']}
Priorities: {r['focus'] or 'Infer priorities from target evidence and the user brief.'}
{reference_rule}
CURRENT-PROJECT-FIRST OVERRIDE FOR THIS BOARD WORKFLOW: current user brief and recorded project development determine WHAT to produce and WHY. References inform HOW to communicate it. This overrides any earlier generic reference-fidelity instruction requiring the entire reference content architecture, silhouette or arrangement to be recreated.
Read board_project_context.json and its recorded current_project.json and AGENTS.md. Use current jury questions and decisions, not the historical first-jury content, to choose the next work. Distinguish decisions, hypotheses, research gaps and assistant recommendations. Never treat a suggested redesign as approved. If there is no progress record, record that gap and work from the current brief and evidence; do not invent a project history.
Inspect every selected reference and record its ordered visual role and deliberate departures in reference_analysis.md. Departures serving current project needs are expected, not fidelity failures.
Read the selected references when present. There is no bundled submission or mandatory five-page reference. Use an empty reference_pages and reference_grammar list when no references are selected; record that limitation. Otherwise inspect ALL pages and record their actual page indexes and observations.
Do not execute an old board script that writes outside this job. Read existing stage reports and continue from the current stage. Preserve successful earlier stages; if upstream correction is necessary, update the affected manifest and explicitly invalidate/rebuild its downstream dependencies. Save new drawing content only under outputs; manifests are in this job root. Sources and methods stay in outputs/supporting; QA renders in outputs/qa. No historical deliverable may be modified.
Every drawn statement is verified, observed, proposed or unknown. Never promote proposal or proximity to measured performance, official designation or safe access. Report unavailable essential evidence in blockers; do not invent it to complete the job. Fresh drawings use raw evidence, not cropped or recoloured old board illustrations. All board content is English. Use a coherent visual family inferred from the selected references or the current project brief, with clear print typography and meaningful legends. Mark uncertainty concisely and keep extended methods separate.
'''

CONTRACTS = {
'evidence': '''Inspect supplied visual references when present (all pages, sheet and detail); record their absence otherwise and target project rules/raw geometry/source notes. Inventory the reference drawing grammar, not just its subject names. Determine available project boundaries, CRS, source date, buildings, roads, vegetation, water and authentic photography. Hash or record file identity. Review current project programme and distinguish facts from hypotheses. Do not select content because an old asset happens to exist.
Write reference_analysis.md and board_evidence.json:
{"sources":[{"id":"s1","path":"/absolute/existing/source","role":"raw_geometry|factual_document|authentic_photo|visual_reference","status":"verified|observed|proposed|unknown","note":"specific provenance / date / reliability"}],"claims":[{"id":"c1","text":"substantive claim","status":"verified|observed|proposed|unknown","source_ids":["s1"]}],"blockers":[],"limitations":["remaining uncertainty"],"reference_pages":[],"reference_observations":["actual page-level and detailed observations"]}.
A source can use url instead of path for a genuinely inspected web source. Any essential missing target boundary/data belongs in blockers; ordinary optional absent analyses can be explicitly omitted with a limitation. Never manufacture complete evidence. Include actual source-render images under outputs/qa/reference and open them. This stage does not create finished boards.''',
'narrative': '''Read evidence and reference audit. Build a target-specific central argument: evidenced need → site capacity → proposed spatial response → measurable questions. A visual reference is not a fixed content recipe: adapt to requested sheet count and project. No generic climate/airport story if irrelevant. Assign each board a unique question and main takeaway. Allocate dominant/supporting modules by importance and complexity; avoid repeated giant maps, decorative empty space, oversized photos and identical boxed rows. Dense is not illegible.
Write content_plan.md (reference inventory, target counterparts, evidence/status, new creation methods, excluded old illustrations) and board_plan.json:
{"concept":"target-specific argument","boards":[{"index":1,"title":"short English title","question":"what this board answers","takeaway":"specific conclusion or proposal","modules":[{"id":"b1_m1","title":"subject","purpose":"distinct visual evidence","type":"map|diagram|section|collage|text","claim_ids":["c1"],"method":"fresh drawing method","status":"verified|observed|proposed|unknown"}]}],"logic_links":[{"problem_claim":"c1","potential_claim":"c2","strategy_claim":"c3","reason":"why this intervention follows this evidence"}],"limitations":[]}.
At least three distinct substantive modules per board; normally more compact supporting analyses as reference complexity warrants. No module quota as a substitute for a complete argument. If a masterplan is primary it receives area accordingly. Eliminate false problem labels (e.g. an existing entrance is not itself a problem). Indicate proposed routes' evidence/selection criteria; do not claim Google routing, seismic safety, ecological benefit or water sufficiency without evidence. Every module must trace to registered claims.''',
'drawings': '''Build each planned module from target evidence using native geometry/vector/text wherever feasible. Create new illustrative scenes only when relevant and supported; never repackage historical illustrations. Use real GIS coordinates and consistent transforms; compare top view and axonometry to prevent mirror/reflection. Record CRS, extent, north, scale and transformation for mapped modules. Keep context outside focal boundaries fading with distance but retain true geography; vegetation must respect buildings, roads and meaningful clearings. Simplify pixel noise, not evidence. Maintain runways/buildings only where appropriate to target scope. Existing/proposed content must be differentiated with legible strokes, hatches, semantic colours and simple swatches.
Write board_drawings.json:
{"modules":[{"id":"b1_m1","output":"outputs/components/b1_m1.svg","preview":"outputs/qa/b1_m1.png","method":"new native drawing from cited sources","source_ids":["s1"],"map_frame":{"crs":"EPSG:...","extent":[0,0,1,1],"orientation_check":"named anchors verified against top view","scale":"verified or omitted"}}],"limitations":[]}.
map_frame is required for maps and spatial diagrams, omitted for nonspatial modules. Open each preview. Native files and previews must actually exist. Retain the user-selected geometry and label non-measured proposal arrangements in source notes. Missing generation capability is a blocker, not permission to paste old art. Keep reusable components independently editable. Record originality_review.json per the fresh-production policy.''',
'composition': '''Compose every board from fresh components in one family. Derive proportions, density and visual rhythm from the selected references when present; otherwise from the brief, but make a new arrangement for this target argument. Compact comparison maps align; other modules interlock without repeated equal cards. Dominant drawing guides the page; labels, white halos, hatches and context support it. Use useful context to bridge drawings; do not cover text with basemap. Preserve separate caption/legend zones and native print typography; enlarge diagrams independently of labels. Print scale is recalculated after resizing or omitted if not verified. Never force a regional extent into a false 1:5000 crop. Check readability at native physical size.
Create outputs/board_01/board_01.pdf and board_01.png etc plus editable source for EACH requested board. Write board_composition.json:
{"boards":[{"index":1,"pdf":"outputs/board_01/board_01.pdf","preview":"outputs/board_01/board_01.png","editable":"outputs/board_01/board_01.svg","module_ids":["b1_m1"],"layout_notes":"concrete hierarchy and spacing decisions"}],"limitations":[]}.
Render entire sheets and actual-size details; do not use the source submission pages as finished backgrounds with tiny edits. New PDFs must contain target content, not reference-page images. Preserve originals.''',
'review': '''Inspect every rendered full sheet, a side-by-side family contact sheet and detailed crops at native print size. Compare with the source reference at matched sizes. Evaluate actual graphic quality, content and claim logic; successful file export is not quality. Check map registration/orientation, scope and scale, proposed versus existing distinctions, source dates, vegetation masks, continuous routes, usable legends, contrast at grayscale, text overlaps/clipping, font hierarchy, repeated information, and whether each drawing's purpose is immediately legible. Rebuild weak modules, render and recheck them; do not merely write passed=true.
Write board_review.json:
{"boards":[{"index":1,"sheet_render":"outputs/board_01/board_01.png","detail_renders":["outputs/qa/board_01_detail.png"],"observations":["specific feature and visual check outcome"],"corrections":["specific fix made"],"unresolved":[]}],"family_render":"outputs/qa/family.png","logic_review":["concrete verified chain / remaining limitation"],"blockers":[],"limitations":[]}.
At least one real detail crop per board. If unfixable material visual/factual issues persist place them in blockers, not a hidden limitations line. Document self-review honestly: it is not a professional safety audit or user approval. For source-supported claims verify actual cited text/geometry; a manifest cannot establish factual truth.''',
'export': '''Recheck all stage contracts after corrections. Export all requested single-board PDFs, previews and honest editable source; merge in narrative order into outputs/Board_Set.pdf with exactly the requested pages and physical dimensions. Create outputs/supporting/Sources_and_Methods.md, documenting every claim/source, date, proposal assumptions, missing data, scale/CRS, simplification and known limits. Keep this separate from PDF-only board deliverables.
Write board_delivery.json:
{"merged_pdf":"outputs/Board_Set.pdf","sources_methods":"outputs/supporting/Sources_and_Methods.md","boards":[{"index":1,"pdf":"outputs/board_01/board_01.pdf","preview":"outputs/board_01/board_01.png","editable":"outputs/board_01/board_01.svg"}],"limitations":[]}.
Validate each PDF after reopening: dimensions/page count and nonblank render, no truncation/corruption, correct order. Complete originality_review.json and all review requirements inherited from the main brief. Do not call a flattened bitmap editable. Do not edit runner-owned board_progress.json. Report export completion through the required delivery manifest. Report actual output files and genuine unresolved limitations.'''
}

def stage_prompt(req, stage):
    if stage not in CONTRACTS:
        raise ValueError('Unknown board workflow stage.')
    if normalize(req) is None:
        return ''
    i = next(i for i, s in enumerate(STAGES) if s['id'] == stage)
    return (brief(req) + '\nCURRENT EXECUTION STAGE: ' + stage + '\n'
            'Complete ONLY this stage; do not run later stages. Existing correct files are checkpoints, not a reason to restart. '
            'Read earlier successful manifests: ' + ', '.join(REPORTS[s['id']] for s in STAGES[:i]) + '.\n'
            'Optionally update board_activity.json with a short message and current module ID. Never edit runner-owned board_progress.json, board_checkpoints.json or board_review_receipt.json. The runner creates the receipt after successful review; if it is missing, inspect/reconcile the actual drawings and complete the stage report, not the receipt. '
            'Do not mark unresolved facts as verified. Resolve genuine blockers with evidence; reclassify an overbroad blocker only with a documented scope/claim rationale.\n' + EVIDENCE_RESOLUTION + '\n'  + CONTRACTS[stage] + '\nDESIGN REQUIREMENTS (required manifest additions):\n' + board_design_protocol.GUIDANCE[stage])


def _read(folder, name):
    p = Path(folder) / name
    if not p.is_file() or p.stat().st_size > 4_000_000:
        raise ValueError('Missing or oversized ' + name)
    obj = json.loads(p.read_text())
    if not isinstance(obj, dict):
        raise ValueError('Expected an object in ' + name)
    return obj


def _file(folder, value):
    if not isinstance(value, str) or not value:
        return None
    root = (Path(folder) / 'outputs').resolve()
    p = (Path(folder) / value).resolve()
    return p if p.is_relative_to(root) and p.is_file() and p.stat().st_size else None


def _items(report, key, issues):
    rows = report.get(key)
    if not isinstance(rows, list):
        issues.append('Report requires a '+key+' list.')
        return []
    if any(not isinstance(x, dict) for x in rows):
        issues.append(key+' entries must be objects.')
        return []
    return rows


def _pdf_issues(path, r, pages=1):
    try:
        import pymupdf
        w, h = SIZES[r['size']]
        if r['orientation'] == 'landscape': w, h = h, w
        with pymupdf.open(path) as doc:
            if len(doc) != pages:
                return ['Incorrect PDF page count: '+path.name]
            for pg in doc:
                if abs(pg.rect.width*25.4/72-w)>1 or abs(pg.rect.height*25.4/72-h)>1:
                    return ['Incorrect PDF physical dimensions: '+path.name]
                pix = pg.get_pixmap(matrix=pymupdf.Matrix(.08,.08), alpha=False)
                from PIL import Image, ImageStat
                im = Image.frombytes('RGB', [pix.width,pix.height], pix.samples)
                if max(ImageStat.Stat(im).stddev) < 1:
                    return ['PDF appears blank: '+path.name]
    except Exception as e:
        return ['Cannot validate PDF '+path.name+': '+str(e)[:120]]
    return []


def _image_issues(path):
    try:
        from PIL import Image, ImageStat
        with Image.open(path) as im:
            im.load()
            if min(im.size)<200:
                return ['Preview is too small for review: '+path.name]
            if max(ImageStat.Stat(im.convert('RGB').resize((128,128))).stddev)<1:
                return ['Preview appears blank: '+path.name]
    except Exception:
        return ['Unreadable preview: '+path.name]
    return []


def _boards(report, folder, r, issues, check_modules=False):
    rows = _items(report, 'boards', issues)
    if [x.get('index') for x in rows] != list(range(1,r['count']+1)):
        issues.append('Board indices must contain every requested board once in order.')
    plan = _read(folder,'board_plan.json') if check_modules else None
    for b in rows:
        for key in ('pdf','preview','editable'):
            p = _file(folder,b.get(key))
            if p is None:
                issues.append('Board '+str(b.get('index'))+' needs an existing '+key+' file inside outputs.')
            elif key=='pdf':
                issues.extend(_pdf_issues(p,r))
            elif key=='preview':
                issues.extend(_image_issues(p))
            elif p.suffix.lower() not in ('.svg','.psd','.psb','.ai','.indd','.idml','.qgz','.blend','.pptx'):
                issues.append('Editable source must be a native document, not a flattened preview.')
        if check_modules:
            expected=next((x for x in plan.get('boards',[]) if x.get('index')==b.get('index')), {})
            ids={x.get('id') for x in expected.get('modules',[])}
            if set(b.get('module_ids',[])) != ids:
                issues.append('Composition module coverage differs from the approved content plan.')
    return rows


def stage_issues(folder, req, stage):
    r = normalize(req)
    if r is None: return []
    if stage not in REPORTS: return ['Unknown board stage.']
    issues=[]
    try:
        report = _read(folder, REPORTS[stage])
        issues.extend(board_design_protocol.issues(stage, report, lambda name: _read(folder, name), folder, {**r, 'reference_hierarchy':req.get('board_reference_hierarchy',[])}))
        if stage in ('evidence','review') and not isinstance(report.get('blockers'),list):
            issues.append('Explicit blockers list required, empty only when no essential gap remains.')
        if stage=='evidence':
            sources=_items(report,'sources',issues); claims=_items(report,'claims',issues)
            if not sources or not claims:issues.append('Evidence needs sources and claims.')
            source_ids={x.get('id') for x in sources}
            if None in source_ids or len(source_ids)!=len(sources):issues.append('Source IDs must be unique.')
            for s in sources:
                if s.get('role') not in ('raw_geometry','factual_document','authentic_photo','visual_reference'):
                    issues.append('Source role must distinguish raw evidence from visual reference.')
                if not (isinstance(s.get('path'),str) and Path(s['path']).is_absolute() and Path(s['path']).is_file()) and not (isinstance(s.get('url'),str) and s['url'].startswith(('https://','http://'))):
                    issues.append('Source '+str(s.get('id'))+' lacks an existing path or inspected URL.')
                if s.get('status') not in ('verified','observed','proposed','unknown'):issues.append('Each source needs its factual status.')
                if not s.get('note'):issues.append('Source provenance note is required.')
            ids=[x.get('id') for x in claims]
            if None in ids or len(set(ids))!=len(ids):issues.append('Claim IDs must be unique.')
            for c in claims:
                if c.get('status') not in ('verified','observed','proposed','unknown') or not c.get('text'):issues.append('Each claim needs text and factual status.')
                refs=c.get('source_ids')
                if not isinstance(refs,list) or any(x not in source_ids for x in refs) or (c.get('status') in ('verified','observed') and not refs):issues.append('Verified/observed claims must trace to registered sources.')
            if not isinstance(report.get('reference_pages'),list) or not report.get('reference_observations'):issues.append('Record inspected reference pages (empty when none) and observations or absence.')
            if report.get('blockers'):issues.append('Essential evidence is missing: '+str(report['blockers'])[:1200])
            if not (Path(folder)/'reference_analysis.md').is_file():issues.append('Missing reference_analysis.md.')
        elif stage=='narrative':
            ev=_read(folder,'board_evidence.json');claims={x['id'] for x in ev['claims']}
            rows=_items(report,'boards',issues)
            if [x.get('index') for x in rows]!=list(range(1,r['count']+1)):issues.append('Plan must contain every requested board in order.')
            ids=[]
            if not report.get('concept'):issues.append('Missing project argument.')
            for b in rows:
                if not all(b.get(k) for k in ('title','question','takeaway')):issues.append('Each board needs title, question and takeaway.')
                mods=_items(b,'modules',issues)
                if len(mods)<3:issues.append('Each board needs at least three distinct substantive modules.')
                for m in mods:
                    ids.append(m.get('id'))
                    if not all(m.get(k) for k in ('id','title','purpose','method','status','type')):issues.append('Incomplete module plan.')
                    refs=m.get('claim_ids',[])
                    if not refs or any(x not in claims for x in refs):issues.append('Each module must trace to registered claims.')
            if None in ids or len(set(ids))!=len(ids):issues.append('Module IDs must be globally unique.')
            for link in _items(report,'logic_links',issues):
                if not link.get('reason') or any(link.get(k) not in claims for k in ('problem_claim','potential_claim','strategy_claim')):issues.append('Problem/potential/strategy links need valid claim IDs and a reason.')
            if not (Path(folder)/'content_plan.md').is_file():issues.append('Missing content_plan.md.')
        elif stage=='drawings':
            plan=_read(folder,'board_plan.json');expected={m['id']:m for b in plan['boards'] for m in b['modules']}
            rows=_items(report,'modules',issues)
            if {x.get('id') for x in rows}!=set(expected) or len(rows)!=len(expected):issues.append('Every planned module needs its own drawing record.')
            sources={x['id'] for x in _read(folder,'board_evidence.json')['sources']}
            for m in rows:
                for k in ('output','preview'):
                    p=_file(folder,m.get(k))
                    if p is None:issues.append('Module '+str(m.get('id'))+' missing '+k+'.')
                    elif k=='preview':issues.extend(_image_issues(p))
                if not m.get('method'):issues.append('Drawing creation method is missing.')
                if not isinstance(m.get('source_ids'),list) or any(x not in sources for x in m['source_ids']):issues.append('Drawing source references are invalid.')
                if expected.get(m.get('id'),{}).get('type')=='map':
                    frame=m.get('map_frame',{})
                    if not all(frame.get(k) for k in ('crs','extent','orientation_check','scale')):issues.append('Mapped module needs CRS, extent, orientation check and scale status.')
        elif stage=='composition':
            _boards(report,folder,r,issues,True)
        elif stage=='review':
            rows=_items(report,'boards',issues)
            if [x.get('index') for x in rows]!=list(range(1,r['count']+1)):issues.append('Review every board in order.')
            for b in rows:
                if not b.get('observations') or not isinstance(b['observations'],list):issues.append('Each board needs concrete visual observations.')
                details=b.get('detail_renders',[])
                if not isinstance(details,list) or not details:issues.append('Each board requires a detail render.')
                for value in [b.get('sheet_render')]+(details if isinstance(details,list) else []):
                    p=_file(folder,value)
                    if p is None:issues.append('Review render must exist inside outputs.')
                    else:issues.extend(_image_issues(p))
                if b.get('unresolved'):issues.append('Unresolved board review issues: '+str(b['unresolved'])[:400])
            p=_file(folder,report.get('family_render'))
            if p is None:issues.append('Missing board-family contact render.')
            else:issues.extend(_image_issues(p))
            if not report.get('logic_review'):issues.append('Missing substantive logic review.')
            if report.get('blockers'):issues.append('Visual/factual review is blocked: '+str(report['blockers'])[:600])
        elif stage=='export':
            issues.extend(board_design_protocol.review_receipt_issues(folder))
            from fresh_production import originality_issues
            issues.extend(originality_issues(folder, {**req, 'fresh_content_version': 1}))
            if not (Path(folder)/'content_plan.md').is_file():issues.append('Missing content_plan.md.')
            _boards(report,folder,r,issues)
            p=_file(folder,report.get('merged_pdf'))
            if p is None:issues.append('Missing merged board-set PDF.')
            else:issues.extend(_pdf_issues(p,r,r['count']))
            p=_file(folder,report.get('sources_methods'))
            if p is None or p.stat().st_size<100:issues.append('Missing substantive separate source/method notes.')
    except (ValueError,KeyError,TypeError,OSError,AttributeError) as exc:
        issues.append('Invalid '+REPORTS[stage]+': '+str(exc)[:300])
    return list(dict.fromkeys(issues))


def delivery_issues(folder, req):
    if normalize(req) is None:return []
    return [s['id']+': '+issue for s in STAGES for issue in stage_issues(folder,req,s['id'])]


def status(folder, req):
    r=normalize(req)
    if r is None:return None
    result={'stages':[dict(s,status='pending',checkpoint=(Path(folder)/REPORTS[s['id']]).is_file()) for s in STAGES],
            'count':r['count'],'current_stage':None,'stage':None,'status':'queued','message':'','module':None}
    try:
        p=_read(folder,'board_progress.json')
        current=p.get('current_stage',p.get('stage'))
        if current in REPORTS:result['current_stage']=result['stage']=current
        allowed=('pending','queued','running','needs_evidence','completed','needs_attention')
        if p.get('status') in allowed:result['status']=p['status']
        if isinstance(p.get('stages'),list):
            for row in result['stages']:
                src=next((x for x in p['stages'] if isinstance(x,dict) and x.get('id')==row['id']),{})
                if src.get('status') in allowed:row['status']=src['status']
                if isinstance(src.get('attempt'),int):row['attempt']=src['attempt']
                if isinstance(src.get('issues'),list):row['issues']=[str(x)[:500] for x in src['issues'][:15]]
        for key in ('message','module'):
            if isinstance(p.get(key),str):result[key]=p[key][:1000]
        if isinstance(p.get('updated_at'),(str,float,int)):result['updated_at']=p['updated_at']
    except (ValueError,OSError,TypeError):pass
    try:
        activity=_read(folder,'board_activity.json')
        for key in ('message','module'):
            if isinstance(activity.get(key),str):result[key]=activity[key][:1000]
    except (ValueError,OSError,TypeError):pass
    return result
