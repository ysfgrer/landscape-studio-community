"""Category-specific intent and board contents, validated before creating a job."""
import json
from pathlib import Path
CONFIG=json.loads((Path(__file__).parent/'web/production-recipes.json').read_text())
SECTIONS={s['id']:s for s in CONFIG['sections']}
def normalize(req):
 recipe=req.get('recipe')
 if recipe is None:return None
 if not isinstance(recipe,dict):raise ValueError('Invalid category settings.')
 kind=recipe.get('category')
 if kind not in (*CONFIG['questions'],'Board'):raise ValueError('Choose a production category.')
 expected='Reference-led drawing' if kind=='Reference' else kind
 if req.get('kind')!=expected:raise ValueError('Category settings do not match the production type.')
 if kind=='Board':
  mode=recipe.get('mode','custom')
  if mode not in ('custom','reference'):raise ValueError('Choose a valid board content mode.')
  boards=recipe.get('boards');size=recipe.get('size','A0');orientation=recipe.get('orientation','portrait')
  if size not in ('A0','A1') or orientation not in ('portrait','landscape'):raise ValueError('Choose a valid board format.')
  if not isinstance(boards,list) or not 1<=len(boards)<=3:raise ValueError('Choose 1 to 3 boards.')
  if mode=='reference':
   refs=req.get('reference_order') or list(dict.fromkeys(req.get('references',[])+req.get('sources',[])))
   if len(refs)<len(boards):raise ValueError('Add one reference board for each requested board.')
  for board in boards:
   if not isinstance(board,list) or not (0 if mode=='reference' else 1)<=len(board)<=len(SECTIONS) or len(set(board))!=len(board) or any(s not in SECTIONS for s in board):raise ValueError('Choose distinct valid content topics for each board.')
  return {'category':kind,'mode':mode,'boards':boards,'size':size,'orientation':orientation}
 answers=recipe.get('answers',{})
 if not isinstance(answers,dict):raise ValueError('Invalid category answers.')
 clean={}
 for q in CONFIG['questions'][kind]:
  value=answers.get(q['id'],q['default']);allowed={c[0] for c in q['choices']}
  if q.get('multiple'):
   if not isinstance(value,list) or not 1<=len(value)<=len(allowed) or any(v not in allowed for v in value) or len(set(value))!=len(value):raise ValueError('Choose valid topics for '+q['label'])
  elif value not in allowed:raise ValueError('Choose a valid answer for '+q['label'])
  clean[q['id']]=value
 return {'category':kind,'answers':clean}
def apply(req):
 recipe=normalize(req)
 if recipe is None:return req
 req={**req,'recipe':recipe}
 if recipe.get('mode')=='reference':req['detail_level']='rich'
 if recipe['category']=='Collage':
  req['geographic_scope']='custom';req['scope_details']='Narrative coverage: '+recipe['answers']['place']+'. This is a narrative collage, not a bounded site map. Use the target project city and its documented historical or landscape context; no local study-boundary clipping is requested.'
 return req
def brief(req):
 r=req.get('recipe')
 if not r:return ''
 text='\nCATEGORY-SPECIFIC DRAWING BRIEF — selected subject and structure. Interpret these WITH the selected reference, never as permission to replace its composition, detailed scenes or visual richness with a generic template.\n'
 if r['category']=='Board':
  text+=f"Create a coordinated set of {len(r['boards'])} {r['size']} {r['orientation']} presentation boards per alternative. Each selected section is a content module, not necessarily a cross-section drawing. Preserve the chosen module order as the compositional sequence; use a dominant drawing and integrated supporting modules, not equal boxes or pasted isolated panels. Allocate area to drawing complexity. Do not add decorative divider rules or explanatory filler. Keep project typography at native print sizes. The chosen geographic scope governs the main project drawing; location plates and regional/historical context modules explicitly permit the broader extents needed to fulfil those selected modules.\n"
  if r.get('mode')=='reference':
   from reference_board import brief as reference_board_brief
   return reference_board_brief(req)
  for i,board in enumerate(r['boards'],1):
   text+=f'BOARD {i:02d} — exactly these {len(board)} modules, in this order:\n'
   for order,key in enumerate(board,1):
    section=SECTIONS[key];text+=f"{order}. {section['label']}: {section['prompt']}\n"
   text+=f'Save the complete board PNG, PDF and editable SVG where feasible with matching names under '+('outputs/alternative_XX/' if req.get('alternative_count',1)>1 else 'outputs/')+f'board_{i:02d}/. XX is the alternative number starting at 01. Every alternative must include every requested board. No standalone root previews that duplicate a board in the gallery.\n'
  text+='Record a board_content_review.json in the job root with boards listing index, rendered file and each selected section id with a substantive evidence-backed observation. Inspect every board at sheet and detail scale; missing modules must not pass. Keep research limitations in source/method notes.\n'
 else:
  for q in CONFIG['questions'][r['category']]:
   values=r['answers'][q['id']];values=values if isinstance(values,list) else [values]
   for v in values:
    c=next(c for c in q['choices'] if c[0]==v);text+=q['label']+' — '+c[1]+': '+c[3]+'\n'
  if r['category']=='Collage':text+='Historical period controls apply to documentary content; if Future vision is selected, historic material may appear only as explicitly historic context. Source captions, dates and historical assets must be verified; no invented archival evidence. The selected city follows the target project, never the inspiration image.\n'
 return text

def board_delivery_issues(folder,req):
 r=(req.get('recipe') or {})
 if r.get('category')!='Board':return []
 from reference_board import coverage_issues
 issues=coverage_issues(Path(folder),req);n=req.get('alternative_count',1)
 for a in range(1,n+1):
  root=Path(folder)/'outputs'
  if n>1:root=root/f'alternative_{a:02d}'
  for i in range(1,len(r['boards'])+1):
   dest=root/f'board_{i:02d}'
   if not all(any(dest.glob('*'+ext)) for ext in ('.png','.pdf')):issues.append(f'Alternative {a}, board {i}: complete PNG and PDF required.')
 return issues
