"""Validated small creative controls and observable alternative delivery."""
from pathlib import Path
SIMILARITY={'close':'Keep a close family: same composition system and graphic language, with meaningful small variations in emphasis and arrangement.', 'balanced':'Keep one coherent visual language but offer meaningfully different compositions, hierarchy and emphasis.', 'exploratory':'Explore clearly distinct compositions and spatial storytelling; keep reference-derived drawing language, target facts and geometry consistent. Do not merely recolour duplicates.'}
DETAIL={'essential':'Show core relationships with selective context and only necessary labels. Keep useful detail readable.', 'balanced':'Include readable context, drawing detail and useful factual annotations without crowding.', 'rich':'Include richer evidence-backed context, textures and technical detail, while maintaining hierarchy and whitespace. Do not invent facts, species or dimensions to increase density.'}
def options(req):
 board_style=req.get('project_board_style',False)
 if not isinstance(board_style,bool):raise ValueError('Project board style must be on or off.')
 count=req.get('alternative_count',1)
 if isinstance(count,bool) or not isinstance(count,int) or count not in range(1,5):raise ValueError('Choose 1 to 4 alternatives.')
 similarity=req.get('alternative_similarity','balanced');detail=req.get('detail_level','balanced')
 if similarity not in SIMILARITY or detail not in DETAIL:raise ValueError('Choose valid similarity and detail settings.')
 return {'project_board_style':board_style,'alternative_count':count,'alternative_similarity':similarity,'detail_level':detail}
def brief(req):
 o=options(req);n=o['alternative_count']
 text='\nCREATIVE SETTINGS:\nDetail: '+DETAIL[o['detail_level']]+'\n'
 if n>1:text+=f'''Create exactly {n} complete alternatives in this single run, not intermediate revisions. {SIMILARITY[o['alternative_similarity']]}
Save each alternative in its own outputs/alternative_01 through outputs/alternative_{n:02d} folder. Each folder must contain its complete drawing as a high-resolution PNG and the requested PDF/editable source formats with matching base names. Do not substitute a contact sheet for complete alternatives. Keep QA/candidate renders outside these folders. Review EVERY alternative against the visual quality contract; overall passed must be false if any alternative fails. Describe the actual differences and each alternative's inspection in style_review.json observations.
'''
 if (req.get('recipe') or {}).get('category')=='Board':
  text=text.replace('Each folder must contain its complete drawing as a high-resolution PNG and the requested PDF/editable source formats with matching base names.', 'Each alternative folder must contain the board_01, board_02 and subsequent board subfolders specified in the board brief. Each board subfolder holds its complete PNG/PDF/editable source formats. Do not add duplicate composite or root previews.')
 if o['project_board_style']:text+="\nPROJECT BOARD STYLE — explicit user choice; overrides conflicting reference-palette instructions above, including the visual quality contract. Applies to EVERY alternative, including a single drawing.\nThere are two separate reference roles: ordinary visual references guide composition, spatial narrative, proportions and arrangement; files labelled TARGET PROJECT BOARD govern palette, typography, line weights, hatching, entourage and annotation style. Do not copy the boards' site contents. OPEN and inspect both groups and read this job's AGENTS.md. Explicit project rules override historical board appearance. If board evidence is missing, use documented project rules and record the limitation separately rather than inventing a style.\nBuild a coherent drawing in the selected target project's own graphic language. Translate colour by semantic role (vegetation, water, context, materials), not a global tint. Adapt assets and photographic cutouts to the board's illustration/linework language while keeping meaningful detail. Preserve selected geographic coverage and actual site geometry. Avoid pasting unrelated images around a map. Keep applicable print typography sizes and verified scales.\nIn reference_analysis.md distinguish the composition references from project-style sources and name each actual source. For style_review.json compare composition against the selected inspiration, and linework/palette/typography against TARGET PROJECT BOARD sources and project rules. Inspect every rendered alternative at full-sheet and detail scale; passing requires both coherent composition and project-style compatibility. Never let the earlier instruction to match original reference colours override this choice.\n"
 return text
def delivery_issues(folder,req):
 n=options(req)['alternative_count']
 if n==1 or (req.get('recipe') or {}).get('category')=='Board':return []
 return [f'Alternative {i:02d} needs a complete PNG and PDF in outputs/alternative_{i:02d}.' for i in range(1,n+1) if not all(any((Path(folder)/'outputs'/f'alternative_{i:02d}').glob('*'+ext)) for ext in ('.png','.pdf'))]
