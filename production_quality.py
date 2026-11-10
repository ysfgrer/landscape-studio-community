"""Reference-led production brief and verifiable review evidence."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageOps

QUALITY_BRIEF='''
VISUAL QUALITY CONTRACT v4 — do the design critique yourself before delivery.
Priority: latest user brief and chosen scope > compatible earlier decisions > original visual reference > defaults. Earlier criticism is a defect to fix, not a style requirement to preserve. Write a short resolved brief before drawing; explicitly discard superseded instructions (e.g. excessive faintness or empty space). The original reference remains the style target; rejected prior outputs are geometry sources, not approved appearance.
Produce a useful finished drawing with deliberate contrast and density. Pale must remain visible. White space should articulate the subject, not erase it. At regional scale, adapt stroke weights and context coverage to the page rather than shrinking a local drawing. Preserve geographic truth and the selected extent. Do not fill empty areas with invented geometry, unsupported annotations or decoration.
Inspect the reference at the SAME displayed page height as the proposed output. Infer its visible hierarchy, not just its nominal colours. For linework maps: primary water should read first; urban structure should read second as connected streets/blocks; terrain should read as coherent landform, with stronger index contours if useful. Use actual road/building data for selective corridor context. Avoid tiny isolated ghost patches or barely visible hairlines. Respect monochrome when requested: neutral grey RGB values, black and white, without olive/red tint.
ASSET LINE-LANGUAGE ADAPTATION — BEFORE COMPOSITION:
The reference is the drawing-language target, not merely the placement template. First identify contour character, relative stroke hierarchy, hatching/stipple density, silhouette edge treatment, shadow versus paper, botanical detail and image-to-map contrast at final print/display size. Record this in line_language_profile.md in job root. Preserve project text/leader rules; apply the visual style to the actual drawing content.
For new productions, generate fresh scenes; do not search the project archive for finished illustrations to fill the page. The following adaptation instructions apply ONLY to explicitly authorized parent edits or authentic factual imagery, not to historical project illustrations. Inventory every authorized external local scene you propose to use. Existing detailed rendered axonometrics often conflict with loose architectural pen sketches. Do not embed them unchanged merely because they belong to this project. For each mismatched scene, adapt it BEFORE composing the board; preserve the source file. Keep structural geometry, viewpoint, planting arrangement, railings, material identity and any supplied human entourage. Do not invent dimensions, species, buildings or a survey.
If the source is genuinely editable vector/code-native geometry, restyle its actual strokes, fills and hatch densities natively; do not substitute generic vector icons. For raster illustrations use the built-in image-generation/editing tool (image_gen) with TWO explicit image roles: the existing scene as edit target and the selected reference as style reference. Read the imagegen skill and inspect both inputs first. Ask for high-fidelity content preservation, reference-matched architectural linework, controlled fine contours, selective hatching and open paper rather than volumetric tonal rendering. Request true transparency for placement into a common paper field. Save tool outputs inside outputs/adapted_assets. Keep generated paths and a concise prompt/method record. Never use Python edge extraction, opacity reduction, thresholding, tracing filters, or generic redraw stand-ins as a substitute for raster style transfer. Do not use a paid API/CLI fallback unless separately authorized; if the built-in image tool is unavailable and no genuine native source exists, report the capability limitation and fail the adaptation check instead of pasting the original again.
Produce only the small number of local scenes required for the composition; adapt them consistently. Compare source, restyled scene and reference at the intended displayed scale before accepting. A lighter copy of the same shaded cutout is not sufficient. Check construction details and human/plant silhouettes against source; reject hallucinated changes. Keep qualified uncertainty in methods, not on-board filler.
The assembled map/context must use a compatible line hierarchy too: local scenes cannot read as dark rendered stickers against faint vector hairlines. Match visual contrast and texture where fields meet while retaining main water hierarchy and legible topography. Place the ADAPTED assets, not the original sources, in the final PDF/SVG/PNG. Do not call a tool-produced illustration fully vector-editable. This pipeline is a drawing-language conversion, not permission to warp the regional geography.
COMPOSITION BEFORE ASSEMBLY:
Infer the reference's spatial grammar: what is the main continuous drawing, how local scenes emerge from it, where ground lines or textures continue, how overlaps and transitions work, and where genuine pauses occur. Do not reduce this to a list of assets or copy the reference's rough compass placement. A large map centered between isolated images on the margins is a failed transfer when the reference is integrated.
Before rendering, write composition_plan.md in the job root with the main visual spine, 2–4 meaningful local episodes, source-supported relationships to map features, hierarchy, transitions and planned white space. Make a small rough layout first. Compose map and local views together; do not finish the map first and then distribute image cutouts into leftover corners. Create only the new local views needed for the reference narrative; reuse a finished local view only for an explicitly requested parent edit; do not maximize the count of available assets. Avoid equal-sized exhibits, rigid margin slots, disconnected inset boxes, floating labels and repeated headers that make a catalog of parts.
For integrated map-and-sketch references, create genuine graphic continuity using shared ground/context strokes, controlled overlap at a local scene's base, selective reveal of map linework behind a scene, and coherent tonal/line-weight treatment. Let at least some local episodes engage the map's drawing field instead of all sitting outside it. Keep primary water/terrain geometry readable and unaltered. Prefer clear contact/transition between drawing fields over connector-only integration. Adding leaders between unchanged floating rectangles does not solve composition. Do not add decorative lines, arrowheads, or invented continuous terrain/roads to force connections. Preserve true geography; local axonometric/section views are distinct-scale drawings and must not masquerade as georeferenced footprints. Use existing transparent/vector/cropped source assets where available. Rectangular opaque image backgrounds must not visibly interrupt the shared paper field; never crop away substantive drawing content merely to conceal this problem.
Place exact anchors only when source evidence establishes them. For generic/typological existing details, compose them as associated views without false coordinate claims; document their relationship and any uncertainty separately. Do not invent spatial evidence. Source constraints may limit fidelity; report that honestly rather than claiming a generic collage is integrated.
Before final export, render at least TWO materially different COMPOSITION candidates in outputs/qa/candidates. Change the map/view relationship, scale of episodes or overlap/transition strategy; recolouring identical placements alone is not a composition candidate. Evaluate topology of the page before refining contrast. Then review candidates at 720px full-page height and 480px showroom height, and inspect details at high resolution. Choose internally; do not ask the user to art-direct these routine decisions. Preserve the previous readability checks.
Self-critique: identify actual weaknesses in the first candidate, correct them and render again. No automatic 'all passed' without specific evidence. Check that required content remains identifiable at 480px: the main subject, meaningful context and terrain where relevant must all survive. Text still follows native project point sizes; do not enlarge labels to compensate for weak drawing. The reference's own limitations are not a reason to make the result unusable.
Record style_review.json in job root with passed, checks (composition,visual_hierarchy,context_density,linework_palette,target_geometry,render_inspected,screen_legibility,empty_space_balance,integrated_composition,spatial_associations,graphic_continuity,line_language_coherence,asset_adaptation,source_content_preserved), reference_observations, output_observations, deviations, plus review_version:4, final_preview (relative path to the delivered PNG under outputs), final_preview_sha256 (actual SHA256), candidates (at least two distinct PNG paths under outputs/qa/candidates), issues_fixed (specific problems and their changes), screen_review (480px and 720px observations, stating which secondary elements are visible). Do not claim a good screen review just because the export opens or a high-resolution crop looks detailed.
For v3 also provide composition_review: an object with strategy, candidate_layouts (at least two objects with exact keys candidate and description; candidate is a reviewed PNG path and description explains its materially different layout), associations (list of source-backed scene/map relationships, or an explicit explanation if the reference has no local scenes), continuity (specific visible contacts/overlaps/transitions), and remaining_limitations. Test the failure case explicitly: if images could be swapped among corners without changing meaning, the page is still a pasted gallery. Fix the layout before claiming integrated_composition true. For a reference that intentionally separates panels, preserve its grammar and explain why the integration test is not applicable; do not force arbitrary overlaps.
For v4 include adaptation_review with profile (actual reference stroke/hatch/tonal observations), external_scenes_used (boolean), assets (list), map_scene_coherence (specific observations) and limitations (list). For each external scene include exact keys before (a source-copy PNG saved under outputs/qa/source_assets), after (accepted adapted PNG or native SVG inside outputs/adapted_assets), method (image_gen or native_vector), changes (observed style changes), preserved (source-content invariants verified), used_in_final (true only after checking the actual final composition). Save a source–adapted–reference comparison under outputs/qa and name it as adaptation_review.comparison. If the reference calls for local scenes, create fresh ones from evidence; do not omit them or fetch old illustrations to satisfy this checklist. For fresh scenes and map-only references set external_scenes_used false, and record creation methods and evidence in limitations. A before-image is required only for an authorized external scene adaptation.
The server checks the final PNG hash, distinct candidate evidence, required review fields and produces its own 480/720px previews with pixel-density measurements. These measurements are diagnostics, not a universal aesthetic score. If the review fails, the Studio automatically requests one corrective pass; unresolved failure stays needs_attention. Never reduce the chosen scope to solve density problems.
'''

def contained(folder,value):
 p=(folder/str(value)).resolve()
 if not p.is_relative_to((folder/'outputs').resolve()) or not p.is_file():raise ValueError('Review evidence must be an existing output file.')
 return p

def review_issues(folder,version=1):
 try:
  r=json.loads((folder/'style_review.json').read_text());checks=r['checks']
  required={'composition','visual_hierarchy','context_density','linework_palette','target_geometry','render_inspected'}
  if version>=2:required|={'screen_legibility','empty_space_balance'}
  if version>=3:required|={'integrated_composition','spatial_associations','graphic_continuity'}
  if version>=4:required|={'line_language_coherence','asset_adaptation','source_content_preserved'}
  problems=[]
  if r.get('passed') is not True:problems.append('Visual self-review did not pass.')
  problems.extend('Review failed or missing: '+k for k in sorted(required) if checks.get(k) is not True)
  if not r.get('reference_observations') or not r.get('output_observations'):problems.append('Missing visual observations.')
  if version>=2:
   if r.get('review_version')!=version:problems.append(f'Review version {version} is required.')
   final=contained(folder,r['final_preview'])
   if final.suffix.lower()!='.png':problems.append('Final preview must be PNG.')
   if hashlib.sha256(final.read_bytes()).hexdigest()!=r.get('final_preview_sha256'):problems.append('Final image changed after review; inspect the actual final export again.')
   hashes=set()
   for value in r.get('candidates',[]):
    p=contained(folder,value)
    if not p.is_relative_to((folder/'outputs/qa/candidates').resolve()):raise ValueError('Candidates belong in outputs/qa/candidates.')
    with Image.open(p) as im:hashes.add(hashlib.sha256(im.convert('RGB').tobytes()).hexdigest())
   if len(hashes)<2:problems.append('Two visually distinct candidate images are required.')
   if not r.get('issues_fixed') or not r.get('screen_review'):problems.append('Document corrected issues and actual 480px/720px observations.')
   if version>=3:
    composition=r.get('composition_review',{})
    if not isinstance(composition,dict):raise ValueError('Composition review must be an object.')
    for key in ('strategy','associations','continuity'):
     if not composition.get(key):problems.append('Missing composition evidence: '+key)
    layouts=composition.get('candidate_layouts',[])
    if not isinstance(layouts,list) or len(layouts)<2:problems.append('Compare at least two composition layouts.')
    else:
     descriptions=set();paths=set()
     for layout in layouts:
      if not isinstance(layout,dict):raise ValueError('Each layout needs candidate and description.')
      candidate=layout.get('candidate');description=str(layout.get('description','')).strip()
      if candidate not in r.get('candidates',[]):problems.append('Layout evidence must name a reviewed candidate.')
      if description:descriptions.add(description)
      paths.add(str(candidate))
     if len(descriptions)<2 or len(paths)<2:problems.append('Composition layouts need distinct candidates and descriptions.')
    if 'remaining_limitations' not in composition:problems.append('State remaining composition limitations, or an empty list.')
   if version>=4:
    adaptation=r.get('adaptation_review',{})
    if not isinstance(adaptation,dict):raise ValueError('Adaptation review must be an object.')
    for key in ('profile','map_scene_coherence'):
     if not adaptation.get(key):problems.append('Missing line-language evidence: '+key)
    if not isinstance(adaptation.get('limitations'),list):problems.append('Record adaptation limitations as a list.')
    if not isinstance(adaptation.get('external_scenes_used'),bool):problems.append('Declare whether external scenes were used.')
    if adaptation.get('external_scenes_used'):
     assets=adaptation.get('assets',[])
     if not isinstance(assets,list) or not assets:problems.append('External scenes require before/after adaptation evidence.')
     for asset in assets:
      if not isinstance(asset,dict):raise ValueError('Invalid asset evidence.')
      before=contained(folder,asset['before']);after=contained(folder,asset['after'])
      if not before.is_relative_to((folder/'outputs/qa/source_assets').resolve()):problems.append('Source copies must stay under outputs/qa/source_assets.')
      if not after.is_relative_to((folder/'outputs/adapted_assets').resolve()):problems.append('Adapted assets must stay under outputs/adapted_assets.')
      if hashlib.sha256(before.read_bytes()).digest()==hashlib.sha256(after.read_bytes()).digest():problems.append('Unchanged source asset cannot pass adaptation.')
      if asset.get('method') not in {'image_gen','native_vector'}:problems.append('Use genuine image editing or native vector restyling.')
      if not asset.get('changes') or not asset.get('preserved') or asset.get('used_in_final') is not True:problems.append('Verify style changes, content preservation and final use.')
     contained(folder,adaptation['comparison'])
    elif not adaptation.get('limitations'):problems.append('Explain why no external scenes are needed.')
   if version>=5:
    from reference_fidelity import issues as fidelity_issues
    problems.extend(fidelity_issues(folder,r))
   audit(folder,final)
  return problems
 except (OSError,ValueError,KeyError,TypeError) as e:return ['Incomplete or invalid visual review: '+str(e)]

def audit(folder,final):
 dest=folder/'outputs/qa';dest.mkdir(parents=True,exist_ok=True)
 metrics={}
 with Image.open(final) as src:
  im=ImageOps.exif_transpose(src).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
  for h in (480,720):
   small=bg.convert('RGB').resize((max(1,round(im.width*h/im.height)),h),Image.Resampling.LANCZOS)
   small.save(dest/f'server_screen_{h}.png');hist=small.convert('L').histogram();n=sum(hist)
   metrics[str(h)]={'dark_fraction':sum(hist[:100])/n,'visible_midtone_fraction':sum(hist[100:235])/n,'very_faint_fraction':sum(hist[235:252])/n,'white_fraction':sum(hist[252:])/n}
 (folder/'quality_metrics.json').write_text(json.dumps({'final_sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'screens':metrics,'note':'Diagnostic only; actual geography and reference density differ.'},indent=2))
 return metrics

from reference_fidelity import BRIEF as FIDELITY_BRIEF
QUALITY_BRIEF += FIDELITY_BRIEF
