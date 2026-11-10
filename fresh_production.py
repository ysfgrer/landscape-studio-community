"""Content creation policy: evidence reuse is not illustration reuse."""
FRESH_POLICY = '''
FRESH PRODUCTION POLICY — latest user direction, superseding legacy asset-adaptation defaults.
For NEW productions, create a new drawing and composition for the selected reference. Project files are evidence, not a compulsory kit of finished illustrations. Never choose a subject merely because a reusable rendered asset exists. Infer subject, view type, scene count, spatial relationships and visual density from the selected reference first; then match relevant target project facts and proposed programme.
Separate sources into: (1) verified raw geometry / factual documents / authentic archival photography, (2) user-selected visual references, (3) historical finished illustrations. Reuse evidence in (1) with provenance. Learn visual grammar from (2), but redraw the target content. Do NOT paste, crop, trace, recolour, image-edit, or repackage (3) as a new production. A different title, layout or palette does not make an old drawing new. Generated old drawings are not surveyed geometry or proof of proposed design approval.
Build new native drawing geometry where evidence supports it, or generate genuinely new illustrative scenes from the reference grammar and current project brief. New proposed arrangements may be explored as proposals; do not invent surveyed geometry, existing buildings, exact species, dimensions or factual historical events. For historical collage use verified target-city archival images, not recycled project collages or fabricated historical photographs. For mapped drawings preserve the real site; for conceptual scenes distinguish proposed content from measured evidence in source notes. Lack of a scene asset is a reason to create it, not to substitute a historical finished illustration. If required generation tools or evidence are unavailable, report the unmet requirement rather than presenting an old drawing as newly created.
Before drawing, write content_plan.md: reference's actual content inventory; target counterpart for each component; evidence and proposed/verified status; how each new drawing will be made; historical illustrations deliberately excluded. Do not force a canal detail, regional map, timeline, or exploded stack into references that do not call for them.
Before delivery, write originality_review.json with mode, reused_evidence (paths and factual roles), new_components (objects with exact keys component, method, source and output; output is a relative path to an existing file under outputs), historical_illustrations_used (paths and explicit authorization, normally empty), and limitations. Inspect final renders: do they answer the chosen reference with genuinely new target content, or merely repeat an old project drawing? If the latter, rebuild the scene; cosmetic adaptation is a failed new-production requirement. This review is evidence and self-assessment, not proof of originality from a checkbox.
For PUSH: previous output is a rejected candidate. Rebuild reused historical scenes and missing reference content; do not preserve a bad scene just because it appeared in the previous attempt. Keep verified geography and facts.
For explicit REVISION or PROJECT STYLE conversion only: the user-selected parent output is the editable subject; preserve unchanged content as requested. This permits that parent, not automatic insertion of unrelated historical illustrations. A user-selected old drawing as a NEW production's reference supplies visual language, not permission to copy its finished content.
Existing asset-adaptation/source-content-preserved checks concern authorized parent edits or authentic source evidence only. Newly created scenes have no mandatory old before-image: set external_scenes_used false for fresh scenes, describe their creation and evidence in adaptation_review.limitations, and inspect the reference-to-new-drawing comparison. Do not retrieve an old scene merely to satisfy an adaptation checklist. Keep all historical files unchanged.
'''

def creation_policy(req):
 mode = 'push' if req.get('operation') == 'push' else 'project_style' if req.get('operation') == 'project_style' else 'revision' if req.get('parent_job_id') else 'new'
 return 'CURRENT CONTENT MODE: '+mode+'\n'+FRESH_POLICY

def originality_issues(folder, req):
 """Validate review provenance; this is not automated visual plagiarism detection."""
 if req.get('fresh_content_version') != 1:
  return []  # Historical jobs keep their original contract.
 import json
 from pathlib import Path
 try:
  report=json.loads((Path(folder)/'originality_review.json').read_text())
  if not isinstance(report,dict):raise ValueError('Expected an object')
  mode=creation_policy(req).splitlines()[0].split(': ')[1]
  issues=[]
  if report.get('mode')!=mode:issues.append('Originality review mode does not match this operation.')
  for key in ('reused_evidence','new_components','historical_illustrations_used','limitations'):
   if not isinstance(report.get(key),list):issues.append('Originality review requires a '+key+' list.')
  if mode in ('new','push'):
   if report.get('historical_illustrations_used'):issues.append('Rebuild historical illustrations as fresh content; cosmetic reuse is not a new production.')
   components=report.get('new_components')
   if not isinstance(components,list) or not components:issues.append('Document the newly created drawing components.')
   elif any(not isinstance(c,dict) or not all(c.get(k) for k in ('component','method','output')) for c in components):issues.append('Each new component needs component, method and output evidence.')
   else:
    for c in components:
     output=(Path(folder)/str(c['output'])).resolve()
     if not output.is_relative_to((Path(folder)/'outputs').resolve()) or not output.is_file():issues.append('New component output must exist inside this job outputs.')
  return issues
 except (ValueError,OSError,TypeError):
  return ['Missing or invalid originality_review.json; document fresh content and evidence reuse.']
