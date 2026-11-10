"""Portable catalog: only this installation's project directories are indexed."""
import re, unicodedata
from pathlib import Path
from project_registry import projects as saved_projects
from seed_projects import ensure_projects
ensure_projects()
PROJECTS=saved_projects()
def norm(s):
 return ''.join(c for c in unicodedata.normalize('NFKD',str(s).lower().replace('ı','i')) if not unicodedata.combining(c))
def canonical(project,path):
 p=Path(path);s=norm(p.stem);full=norm(path)
 version=max([int(x) for x in re.findall(r'(?:^|[_/ -])v(\d+)(?=[_/ .-]|$)',full)] or [1])
 final=bool(re.search(r'(?:^|[_ -])(final|son)(?:[_ .-]|$)',s))
 s=re.sub(r'(?:^|[_ -])v\d+(?=[_ -]|$)','_',s).strip('_ -')
 s=re.sub(r'(?i)(?:[_ -](?:preview|onizleme|transparent|seffaf|editable|duzenlenebilir|katmanli|vektor|vector|high_resolution|yuksek_cozunurluk|\d+dpi|final|son|beyaz|white|print|screen))+$','',s).strip('_ -')
 s=re.sub(r'[_ -]+','_',s)
 return s,version,int(final)

def is_current(project,family,rows):
 return not re.search(r'(method|source|check|preview)',family)
def rules_for(project):
 return (Path(PROJECTS[project]['root'])/'AGENTS.md').read_text()
def target_context(project):
 root=Path(PROJECTS[project]['root'])
 return (root/'project.json').read_text()+'\nRead the project brief and source documents in '+str(root)
