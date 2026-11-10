"""Evidence gate for reference-led outputs; not an independent aesthetic judge."""
import hashlib,json
from pathlib import Path

BRIEF='''
REFERENCE FIDELITY CONTRACT v5 — applies after category recipes.
A category or Drawing structure choice is NOT permission to discard the reference's visual content types. Exploded means spatial separation expressed in the reference's language, not automatically stacked basemaps. History plus exploded plus a detailed architectural montage requires source-backed historical/spatial episodes, architectural detail, entourage and layered narrative, not a few roads on terrain plates. Preserve reference aspect ratio and dominant spatial spine unless a user-selected sheet format requires adaptation. Balanced alternatives vary emphasis and sequencing WITHIN this visual family; changing to map-only, changing aspect ratio arbitrarily, or omitting detailed scenes is failure.
Before drawing, inspect the original reference and detailed crops. Save reference_contract.json in job root with features: a list of objects {id, observation, required, target_translation}. Inventory every visually important feature, including dominant composition, subject/detail density, built-form detail, human/botanical entourage when present, photographic/drawn episodes, chronology, contrast and secondary information. required is boolean. Mark essential visual features required=true. Project typography/arrow restrictions change the relevant mark, not the surrounding content or overall richness. Translate foreign subjects into verified target-project subjects. No invented historical evidence or illegible filler text.
Rich detail means reference-comparable richness in actual subject matter, not simply many contour vertices. Source and adapt real project or documented target-city assets for required episodes. If assets/capabilities are missing, keep the corresponding check failed; do not omit the scenes and justify success using the category setting. Native SVG output does not justify replacing detailed imagery with sparse vector maps; embedded adapted raster artwork is allowed with honest editability notes.
For EVERY delivered alternative/board, save a same-height reference/output comparison PNG and detail comparison PNG under outputs/qa. In style_review.json add fidelity_review: {outputs:[{preview, sha256, comparison, detail_comparison, features:[{id, preserved, evidence}], unresolved:[]}]}. preview is the exact delivered PNG relative path, sha256 its final hash. Each feature evidence must identify what is visibly present and where; preserved must be false for omitted essential subject matter. Include all contract feature IDs for every output. Missing essentials or unresolved fidelity issues must keep passed=false. Review the actual final export, not just a candidate. Never equate valid files or your own checkboxes with aesthetic success.
'''

def issues(folder,report):
 from production_quality import contained
 try:
  contract=json.loads((folder/'reference_contract.json').read_text())
  features=contract['features']
  if not isinstance(features,list) or not features:raise ValueError('Reference feature inventory is required.')
  ids=set();required=set()
  for f in features:
   if not f.get('id') or f['id'] in ids or not f.get('observation') or not f.get('target_translation') or not isinstance(f.get('required'),bool):raise ValueError('Invalid reference feature inventory.')
   ids.add(f['id'])
   if f['required']:required.add(f['id'])
  if not required:raise ValueError('Essential reference features must be identified.')
  rows=report['fidelity_review']['outputs'];seen=set();problems=[]
  for row in rows:
   p=contained(folder,row['preview']);seen.add(p)
   if p.suffix.lower()!='.png' or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:problems.append('Fidelity review must match the final PNG hash.')
   for key in ('comparison','detail_comparison'):
    comparison=contained(folder,row[key])
    if comparison.suffix.lower()!='.png' or not comparison.is_relative_to((folder/'outputs/qa').resolve()):raise ValueError('Fidelity comparisons must be QA PNG files.')
   checks={f['id']:f for f in row['features']}
   if set(checks)!=ids:problems.append('Review every reference feature for '+row['preview'])
   for id in required:
    f=checks.get(id,{})
    if f.get('preserved') is not True or not f.get('evidence'):problems.append('Missing reference feature '+id+' in '+row['preview'])
   if row.get('unresolved')!=[]:problems.append('Unresolved reference fidelity issues in '+row['preview'])
  # Delivered PNGs live directly under outputs, alternative_NN or board_NN;
  # QA and asset folders are never deliverable drawings.
  delivered={p.resolve() for p in (folder/'outputs').rglob('*.png') if all(part.startswith(('alternative_','board_')) for part in p.relative_to(folder/'outputs').parts[:-1])}
  if not delivered or delivered!=seen:problems.append('Fidelity review must cover every delivered alternative and board PNG exactly.')
  return problems
 except (OSError,ValueError,KeyError,TypeError) as e:return ['Invalid reference fidelity evidence: '+str(e)]
