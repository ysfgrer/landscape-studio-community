"""Design contracts supplement technical gates; declarations are not visual proof."""
import hashlib
import json
from pathlib import Path

REVISION = 4
GUIDANCE = {
'evidence': '''Additional required evidence fields:
selected_references: [{path, priority:main|supporting, observed_content, adopted_grammar, conflicts, resolution}], matching the supplied board_reference_hierarchy in order; empty when none selected. All visual references, including the jury set, are communication benchmarks subordinate to current project needs. Main/supporting indicates visual inspiration priority only.
capabilities: [{task, tool, available: boolean, fallback, essential: boolean}]. Inspect actual available tools; do not claim a renderer/research source exists without checking.
reference_grammar: [{page, dominant_drawing, supporting_drawings, relationships, density_observation, transferable_rule, avoid_copying}]; one record for each inspected reference page; empty when no references are selected. Describe sizes/relationships seen, not invented font measurements.
Each claim additionally requires locator (page/feature/date or user instruction), spatial_scope and limitation. Visual references may support style, never a verified geographic or social claim. Resolve conflicting source dates/boundaries explicitly. Missing optional data changes the content plan; do not fill it with invented analysis.''',
'narrative': '''Additional required board_plan fields:
project_evolution: {context_source, current_stage, retained_decision_ids:[], priority_responses:[{priority_id, module_ids:[], disposition:addressed|deferred|out_of_scope, reason}], new_contribution, historical_repetition_avoided:[], proposals_requiring_user_decision:[]}. Read the current project snapshot and cover each recorded jury priority explicitly, including justified deferrals for this request. Do not claim a research question is solved merely because a diagram was drawn. New contribution must explain what advances beyond previous project work. Match present needs first; the reference supplies richness and communication techniques, never programme or mandatory layout.
argument: {need_claim_ids:[], site_capacity_claim_ids:[], response_claim_ids:[], central_question, design_intent, unresolved_questions:[]}.
creative_routes: at least two genuinely different set-level approaches [{id, narrative, spatial_emphasis, tradeoff, selected:boolean, selection_reason}]. Select exactly one based on target evidence and reference quality, not a cosmetic colour variation.
Each module additionally requires drawing_brief: {message, viewer_question, visual_answer, evidence_to_show, view, spatial:boolean, anchors:[], layers:[], detail_requirements:[], annotation_plan, legend_plan, print_width_mm, print_height_mm, priority:dominant|supporting|detail, dependencies:[], acceptance_checks:[], omitted_content:[]}.
Specify actual geometry/features to show, where evidence ends and proposal begins, intended comparison, and readable printed detail. At least two substantive detail requirements and two observable acceptance checks per module. A textual module can specify typography and factual relationships instead of spatial detail. Dependencies refer to module IDs and must be acyclic.
Each board additionally requires composition_intent: {dominant_module, reading_relationships, reference_connection, density_budget, repetition_to_avoid}. Density budget explains space allocation to distinct information and avoids both giant repeated maps and illegible miniature drawings. Do not impose an invented universal percent-filled quota.
For every PPS chain add location, mechanism, alternative_considered, and validation_needed. Explain why HERE, why this action and why this scale. An entrance is an asset unless an evidenced constraint is identified. Building density alone establishes neither structural vulnerability nor safe gathering provision. Routes must have destinations, actual street geometry, selection criteria and unresolved crossings. Water proposals need source/path/storage/overflow relationships without invented flows. Do not import airport programme to other projects.''',
'drawings': '''Work module by module from drawing_brief; save each preview as it is completed and update board_activity.json with module and message. Do not postpone all visual inspection until composition. Compare each spatial drawing to at least three non-collinear named geographic anchors where available; preserve handedness, distances and relative positions across every view. If fewer anchors exist explain the limitation.
Each drawing record additionally requires brief_response: {message_delivered, details_built:[], checks:[{criterion, observation}], remaining_limits:[]} and spatial:boolean matching the plan.
Spatial modules require map_frame including crs, extent, orientation_check, scale plus anchors:[{name, source_position, drawing_position}], transform_description. Coordinates/positions must come from the actual transform, not illustrative numbers. Sources requiring a new interpretation remain proposed.
Use the same physical map frame for comparisons. Depth comes from restrained shadows/line hierarchy, not shearing geography or fabricating buildings. Make proposed routes visible over context, vary semantic hatches rather than near-identical red fills, and make legends reproduce actual marks. Keep native geometry, labels and composition separately editable where supported. Record unavailable assets as limitations/blockers, never recycle rejected scenes.''',
'composition': '''Before final placement make two small layout studies PER board using the actual modules, not empty rectangles. Save under outputs/qa/layouts; compare matched-size reference and both studies. Select by hierarchy, meaning, density and print legibility, not by symmetry alone.
Each composition board record additionally requires layout_candidates:[{preview, rationale, selected:boolean}] (at least two; exactly one selected), placements:[{module_id, x_mm,y_mm,width_mm,height_mm,legend_zone,annotation_zone}], print_review:{smallest_text_pt, scale_adjustments:[], crowding_fixes:[], hierarchy_observation}.
All placements are within the physical sheet; map scale is recalculated after resizing. Overlapping context is allowed, overlapping essential labels/legends is not. Text zones and motif carry a consistent family while compositions differ. No filler narratives, useless repeated location maps, decorative humans or repetitive exploded stacks. Every module must earn its area through a distinct message. Use source-specific imagery only where it adds evidence.''',
'review': '''Run a sceptical design critique, not a pass-formality. Each board additionally requires rubric:[{criterion, evidence, verdict:pass|revise|blocked, module_ids:[]}], covering argument, geographic_integrity, visual_hierarchy, print_legibility, reference_translation, distinct_information, factual_honesty. Evidence identifies actual rendered features/crops. A score alone is insufficient.
Write revision_log:[{issue, severity:critical|major|minor, affected_modules:[], action, before_render, after_render, resolution}] at root of report, empty only if genuinely no correction needed. Every correction requires actual before/after images. Rebuild bad drawing content rather than mask it with captions. Reinspect all dependent modules after a geography, palette or programme change.
Include at least two useful detail crops per board (dense map/legend and typography/diagram), not the same sheet renamed. Include grayscale family comparison in grayscale_render. If any rubric verdict is revise/blocked, keep blockers nonempty until corrected. Do not remove warnings merely to pass. Revalidate earlier manifests when changes affect them. Include a concise jury_questions array [{question, answer, claim_ids, remaining_uncertainty}] challenging the central design rationale. Do not claim self-review equals user approval.''',
'export': '''Include delivery_summary:{completed:[], unresolved:[], omitted:[], editable_limitations:[]} in board_delivery.json. Report meaningful missing content, exact native editability and unverified claims honestly. Reopen final exported PDFs, not just intermediate SVG previews. Confirm reference assets did not become target content. Retain iteration evidence outside the clean delivery folder. All downstream PDFs must reflect the final reviewed module versions.'''
}


def issues(stage, report, read, folder, config):
    out=[]
    def require(obj, keys, label):
        for key in keys:
            if key not in obj or obj[key] is None or obj[key] == '': out.append(label+' requires '+key+'.')
    def candidates(rows, label):
        if not isinstance(rows,list) or len(rows)<2 or sum(x.get('selected') is True for x in rows if isinstance(x,dict))!=1:
            out.append(label+' needs two alternatives and exactly one selection.')
    if stage=='evidence':
        require(report,['capabilities','reference_grammar'],'Evidence')
        if not isinstance(report.get('reference_grammar'),list):out.append('Reference grammar must be a list (empty without references).')
        if config.get('reference_hierarchy') and not report.get('reference_grammar'):out.append('Inspect the selected visual references.')
        selected=report.get('selected_references',[])
        expected=config.get('reference_hierarchy',[])
        if not isinstance(selected,list) or [(r.get('path'),r.get('priority')) for r in selected] != [(r.get('path'),r.get('priority')) for r in expected]:out.append('Selected reference order and main/supporting roles must match the request.')
        for r in selected:require(r,['observed_content','adopted_grammar','conflicts','resolution'],'Selected reference')
        refs={s['id'] for s in report.get('sources',[]) if s.get('role')=='visual_reference'}
        for c in report.get('claims',[]):
            require(c,['locator','spatial_scope','limitation'],'Claim '+str(c.get('id')))
            if c.get('status') in ('verified','observed') and set(c.get('source_ids',[]))<=refs:out.append('Factual claim cannot rely solely on visual-reference sources.')
        for cap in report.get('capabilities',[]):
            if cap.get('essential') and not cap.get('available') and not cap.get('fallback'):out.append('Essential production capability unavailable: '+str(cap.get('task')))
    elif stage=='narrative':
        evolution=report.get('project_evolution',{})
        require(evolution,['context_source','current_stage','retained_decision_ids','priority_responses','new_contribution','historical_repetition_avoided','proposals_requiring_user_decision'],'Project evolution')
        snapshot_path=Path(folder)/'board_project_context.json'
        if snapshot_path.is_file():
            snapshot=json.loads(snapshot_path.read_text())
            current=snapshot.get('files',{}).get('project_context/current_project.json',{})
            if current:
                progress=json.loads(current['content'])
                expected={p['id'] for p in progress.get('jury_priorities',[])}
                responses=evolution.get('priority_responses',[])
                if {p.get('priority_id') for p in responses}!=expected:out.append('Plan must address or explicitly defer each current jury priority.')
                module_ids={m['id'] for b in report.get('boards',[]) for m in b.get('modules',[])}
                for response in responses:
                    if response.get('disposition') not in ('addressed','deferred','out_of_scope') or not response.get('reason'):out.append('Jury priority needs a disposition and reason.')
                    linked=response.get('module_ids',[])
                    if any(m not in module_ids for m in linked) or (response.get('disposition')=='addressed' and not linked):out.append('Addressed jury priorities must link to planned modules.')
        require(report,['argument','creative_routes'],'Plan');candidates(report.get('creative_routes'),'Narrative')
        argument=report.get('argument',{})
        require(argument,['central_question','design_intent','need_claim_ids','site_capacity_claim_ids','response_claim_ids','unresolved_questions'],'Argument')
        claims={c['id'] for c in read('board_evidence.json')['claims']}
        for key in ('need_claim_ids','site_capacity_claim_ids','response_claim_ids'):
            if not argument.get(key) or any(c not in claims for c in argument.get(key,[])):out.append('Argument '+key+' must trace to evidence.')
        modules={m['id']:m for b in report.get('boards',[]) for m in b.get('modules',[])}
        graph={}
        for b in report.get('boards',[]):
            ci=b.get('composition_intent',{});require(ci,['dominant_module','reading_relationships','reference_connection','density_budget','repetition_to_avoid'],'Composition intent')
            if ci.get('dominant_module') not in {m['id'] for m in b['modules']}:out.append('Dominant module must belong to its board.')
            for m in b['modules']:
                d=m.get('drawing_brief',{});require(d,['message','viewer_question','visual_answer','evidence_to_show','view','spatial','anchors','layers','detail_requirements','annotation_plan','legend_plan','print_width_mm','print_height_mm','priority','dependencies','acceptance_checks','omitted_content'],m['id'])
                for key in ('detail_requirements','acceptance_checks'):
                    if len(d.get(key,[]))<2:out.append(m['id']+' needs substantive '+key+'.')
                for key in ('print_width_mm','print_height_mm'):
                    if not isinstance(d.get(key),(int,float)) or isinstance(d.get(key),bool) or d.get(key,0)<=0:out.append(m['id']+' needs positive '+key+'.')
                graph[m['id']]=d.get('dependencies',[])
                if any(x not in modules for x in graph[m['id']]):out.append('Unknown module dependency.')
        visiting=set();done=set()
        def visit(n):
            if n in visiting:raise ValueError('Cyclic module dependencies.')
            if n in done:return
            visiting.add(n)
            for dep in graph.get(n,[]):visit(dep)
            visiting.remove(n);done.add(n)
        for n in graph:visit(n)
        for link in report.get('logic_links',[]):require(link,['location','mechanism','alternative_considered','validation_needed'],'PPS reasoning')
    elif stage=='drawings':
        plan={m['id']:m for b in read('board_plan.json')['boards'] for m in b['modules']}
        for m in report.get('modules',[]):
            response=m.get('brief_response',{});require(response,['message_delivered','details_built','checks','remaining_limits'],'Drawing '+str(m.get('id')))
            d=plan.get(m.get('id'),{}).get('drawing_brief',{})
            if m.get('spatial')!=d.get('spatial'):out.append('Drawing spatial classification must match plan.')
            if len(response.get('checks',[]))<2:out.append('Drawing needs observed acceptance checks.')
            if d.get('spatial'):
                frame=m.get('map_frame',{});require(frame,['crs','extent','orientation_check','scale','anchors','transform_description'],'Spatial frame')
                if len(frame.get('anchors',[]))<3 and not response.get('remaining_limits'):out.append('Fewer than three anchors needs explicit limitation.')
    elif stage=='composition':
        for b in report.get('boards',[]):
            candidates(b.get('layout_candidates'),'Board layout')
            require(b,['placements','print_review'],'Composed board')
            expected=set(b.get('module_ids',[]));placed=[p.get('module_id') for p in b.get('placements',[])]
            if set(placed)!=expected or len(placed)!=len(expected):out.append('Every module needs exactly one placement.')
            dims=(841,1189) if config['size']=='A0' else (594,841)
            if config['orientation']=='landscape':dims=dims[::-1]
            for p in b.get('placements',[]):
                require(p,['x_mm','y_mm','width_mm','height_mm','legend_zone','annotation_zone'],'Placement')
                x,y,w,h=(p.get(k) for k in ('x_mm','y_mm','width_mm','height_mm'))
                if not all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in (x,y,w,h)):out.append('Placement dimensions must be numeric.');continue
                if min(x,y)<0 or min(w,h)<=0 or x+w>dims[0] or y+h>dims[1]:out.append('Module placement exceeds sheet bounds.')
            for c in b.get('layout_candidates',[]):
                if not output_file(folder,c.get('preview')):out.append('Layout study preview missing.')
    elif stage=='review':
        require(report,['revision_log','grayscale_render','jury_questions'],'Review')
        if not output_file(folder,report.get('grayscale_render')):out.append('Missing grayscale review render.')
        criteria={'argument','geographic_integrity','visual_hierarchy','print_legibility','reference_translation','distinct_information','factual_honesty'}
        for b in report.get('boards',[]):
            rubric=b.get('rubric',[])
            if {r.get('criterion') for r in rubric}!=criteria:out.append('Incomplete design critique rubric.')
            for r in rubric:
                if r.get('verdict')!='pass' or not r.get('evidence'):out.append('Unresolved or unsubstantiated design critique: '+str(r.get('criterion')))
            if len(set(b.get('detail_renders',[])))<2:out.append('Two distinct print-detail crops required per board.')
        for revision in report.get('revision_log',[]):
            require(revision,['issue','severity','affected_modules','action','resolution'],'Revision')
            for key in ('before_render','after_render'):
                if not output_file(folder,revision.get(key)):out.append('Revision evidence missing '+key+'.')
        if not report.get('jury_questions'):out.append('Missing jury rationale challenge.')
    elif stage=='export':
        require(report.get('delivery_summary',{}),['completed','unresolved','omitted','editable_limitations'],'Delivery summary')
        composed=read('board_composition.json').get('boards',[])
        keys=('index','pdf','preview','editable')
        if [tuple(b.get(k) for k in keys) for b in report.get('boards',[])] != [tuple(b.get(k) for k in keys) for b in composed]:
            out.append('Delivery must reference the exact reviewed composition files in order.')
    return out


def output_file(folder, value):
    if not isinstance(value,str):return None
    p=(Path(folder)/value).resolve();root=(Path(folder)/'outputs').resolve()
    return p if p.is_relative_to(root) and p.is_file() and p.stat().st_size else None


def fingerprint(folder, req, stage, stages, reports):
    """Hash prior manifests and referenced outputs; stale checkpoints never silently skip."""
    folder=Path(folder)
    h=hashlib.sha256(json.dumps({'protocol':REVISION,'request':req},sort_keys=True,default=str).encode())
    def add(path):
        path=Path(path);h.update(str(path).encode())
        if path.is_file():
            with path.open('rb') as f:
                for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    add(folder/'user_updates.txt');add(folder/'brief.txt');add(folder/'board_project_context.json')
    for s in stages:
        name=reports[s['id']];p=folder/name;add(p)
        if p.is_file():
            try:
                obj=json.loads(p.read_text())
                def walk(v):
                    if isinstance(v,dict):
                        for item in v.values():walk(item)
                    elif isinstance(v,list):
                        for item in v:walk(item)
                    elif isinstance(v,str):
                        if v.startswith('outputs/'):
                            target=output_file(folder,v)
                            if target:add(target)
                        elif s['id']=='evidence' and Path(v).is_absolute() and Path(v).is_file():add(v)
                walk(obj)
            except (ValueError,OSError):pass
        if s['id']==stage:break
    return h.hexdigest()


def reviewed_artifacts(folder):
    """Content identity of drawings and composed sheets, independent of model declarations."""
    folder=Path(folder); result={}
    def digest(path):
        h=hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
        return h.hexdigest()
    for name, collection, fields in (
        ('board_drawings.json','modules',('output','preview')),
        ('board_composition.json','boards',('pdf','preview','editable')),
    ):
        path=folder/name
        report=json.loads(path.read_text())
        result[name]=digest(path)
        for row in report[collection]:
            for field in fields:
                value=row.get(field);target=output_file(folder,value)
                if target is None:raise ValueError('Missing reviewed artifact: '+str(value))
                result[value]=digest(target)
    return result


def review_receipt_issues(folder):
    try:
        folder=Path(folder)
        receipt=json.loads((folder/'board_review_receipt.json').read_text())
        if receipt.get('artifacts')!=reviewed_artifacts(folder):
            return ['Drawings or composed sheets changed after visual review. Review the final versions again before delivery.']
    except (OSError,ValueError,KeyError,TypeError):
        return ['Missing or invalid runner-owned visual review receipt.']
    return []
