"""Full reference-board adaptation: content inventory and delivery coverage."""
import json

def brief(req):
 r=req['recipe'];n=len(r['boards'])
 text='''
REFERENCE BOARD MODE — recreate the selected reference board's entire content architecture and arrangement for the TARGET PROJECT. This replaces manual module selection and generic section recipes. Create BOARD_COUNT complete SELECTED_SIZE SELECTED_ORIENTATION boards per alternative. References in selection order supply Board 1, Board 2, etc.; additional references support style only. Do not blend the primary boards or omit small drawings. No eight-module limit. Reference content coverage and rich detail override generic essential/balanced simplification. The selected scope governs the main design; regional location and historical modules use their appropriate broader target-project extents.
“Same content” means the same information TYPES and analytical questions, using the target project's own supported facts. Never transplant the source city's names, statistics, dates, conclusions, boundaries, species or proposal. A land-use diagram is a sub-drawing within a larger analytical group, not necessarily a whole section. Preserve this hierarchy.
BEFORE DRAWING: open every primary reference at full resolution and inspect overlapping crops covering the whole board, including margins, small legends and bottom details. Inventory all visible groups AND their children: titles; location hierarchy; historical timelines; base maps; land-use, figure-ground, mobility, height, ecology and climate analyses; concept sequences; masterplans; exploded views; sections; construction details; perspectives/collages; charts; legends; scale/north cues; photographs and their relationships. This list is illustrative, not a template to add unrequested material. Record the actual reference, not a generic checklist. Unreadable source text is not permission to invent facts: infer only the visible diagram type; record uncertainty separately.
Save reference_board_inventory.json before composition: {boards:[{index,reference_id,groups:[{id,label,bounds:[x,y,width,height],children:[{id,label,bounds:[x,y,width,height],target_content,sources,source_status}]}]}]}. Bounds are normalized 0–1 relative to the whole reference sheet. Every group includes its actual sub-drawings (use a single child for a standalone drawing). Unique child IDs within each board. reference_id is the actual selected reference ID. target_content describes the project-specific equivalent, sources identify evidence, source_status is verified, proposal, or missing. Do not silently delete an essential element due to missing data.
RESEARCH AND TRANSLATION: build a source plan for every child. Use project files first, then reliable documentary/spatial sources when available. Match time periods, geographic level, analytical function and design intent; use the target city's real history. Location content must reproduce the reference's actual representation (e.g. nested axonometric country/region/city/site maps), not default to flat thumbnails. Analytical categories must use target data, not decorative random charts. Distinguish measured existing conditions from design proposals. Source limitations go in methods, not invented board filler.
COMPOSITION: preserve relative placement, area proportions, dominant spine, nested grouping, alignments, image-to-text balance, overlap, visual transitions, detail density and drawing hierarchy. Recreate the board as a coordinated whole, not an equal-card grid or a menu of isolated sections. Adapt the whole composition proportionally to the explicitly selected sheet format; never stretch geography or typography. Keep useful drawings large enough to read. Do not simplify a dense reference into a few diagrams or stretch a small subset across the sheet. Every alternative retains the COMPLETE same inventory and placement logic; alternatives are refinements within this layout family.
DRAWING: recreate each child in the reference's drawing language with comparable substantive detail. Preserve real target geometry. Adapt scene assets before assembling; no unchanged stock render stickers. Embedded adapted raster artwork is allowed; describe editability honestly. Apply mandatory project text/leader/marker rules locally, without deleting related drawings. Project-board-style mode, if enabled, changes palette and linework while preserving this reference's content architecture and layout. Actual source text is replaced with concise accurate English target information, not copied, garbled or padded.
REVIEW: render complete sheets at showroom height and inspect each child at native detail scale. Compare reference/output side by side and by corresponding crops. Inventory all children again from the rendered result: every source child must have a visible counterpart in the same relative location. Save board_content_review.json: {boards:[{index,alternative,preview,children:[{id,rendered,evidence}]}]}. preview is the delivered PNG relative path. evidence identifies the actual target content and its position; rendered=false for missing or placeholder content. Missing required data/drawings must remain unresolved, never marked successful merely because the file exists. Maintain the v5 reference fidelity review too. Preserve all intermediate QA under outputs/qa and all sources separately.
'''
 text=text.replace('BOARD_COUNT',str(n)).replace('SELECTED_SIZE',r['size']).replace('SELECTED_ORIENTATION',r['orientation'])
 for i in range(1,n+1):
  root=('outputs/alternative_XX/' if req.get('alternative_count',1)>1 else 'outputs/')+f'board_{i:02d}/'
  text+=f'Board {i}: save its complete PNG, PDF and editable source (where feasible) with matching base names under {root}. XX starts at 01. No duplicate root composite previews.\n'
 return text

def coverage_issues(folder,req):
 if (req.get('recipe') or {}).get('mode')!='reference':return []
 try:
  from production_quality import contained
  refs=req.get('reference_order') or list(dict.fromkeys(req.get('references',[])+req.get('sources',[])))
  inventory=json.loads((folder/'reference_board_inventory.json').read_text())['boards']
  count=len(req['recipe']['boards']);expected={};problems=[]
  for board in inventory:
   i=board['index']
   if not isinstance(i,int) or i not in range(1,count+1) or i in expected or board['reference_id']!=refs[i-1]:raise ValueError('Inventory must match the selected primary boards.')
   children=[c for g in board['groups'] for c in g['children']]
   ids={c['id'] for c in children}
   if not ids or len(ids)!=len(children):raise ValueError('Inventory needs unique content IDs.')
   for c in children:
    if not c.get('target_content') or not c.get('sources') or c.get('source_status') not in ('verified','proposal'):problems.append(f'Board {i}: unresolved source for '+c['id'])
   expected[i]=ids
  if set(expected)!=set(range(1,count+1)):raise ValueError('Inventory missing a board.')
  rows=json.loads((folder/'board_content_review.json').read_text())['boards'];seen=set()
  for row in rows:
   pair=(row['alternative'],row['index'])
   if pair in seen:raise ValueError('Duplicate board review.')
   seen.add(pair);p=contained(folder,row['preview'])
   base=folder/'outputs'
   if req.get('alternative_count',1)>1:base=base/f'alternative_{pair[0]:02d}'
   if p.parent!=(base/f'board_{pair[1]:02d}').resolve() or p.suffix.lower()!='.png':raise ValueError('Board review points to the wrong output.')
   checks={c['id']:c for c in row['children']}
   if set(checks)!=expected[pair[1]] or any(c.get('rendered') is not True or not c.get('evidence') for c in checks.values()):problems.append(f'Alternative {pair[0]}, board {pair[1]}: missing reference content.')
  if seen!={(a,i) for a in range(1,req.get('alternative_count',1)+1) for i in expected}:problems.append('Review every reference board in every alternative.')
  return problems
 except (OSError,ValueError,KeyError,TypeError,IndexError) as e:return ['Invalid reference-board coverage evidence: '+str(e)]
