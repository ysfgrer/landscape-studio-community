import unittest,tempfile,shutil,subprocess,sys,json
from pathlib import Path
APP=Path(__file__).resolve().parents[1]
class Community(unittest.TestCase):
 def run_isolated(self,code):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   for p in APP.glob('*.py'):shutil.copy2(p,root/p.name)
   for name in ('presets','web'):shutil.copytree(APP/name,root/name,ignore=shutil.ignore_patterns('generated'))
   r=subprocess.run([sys.executable,'-c',code],cwd=root,capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stdout+r.stderr)
 def test_seed_is_neutral_and_preserves_user_edits(self):
  self.run_isolated('''
import seed_projects,json
from pathlib import Path
seed_projects.ensure_projects()
from catalog import PROJECTS,rules_for,target_context
assert {x['name'] for x in PROJECTS.values()}=={'Landscape Design II','Landscape Design III','Landscape Design IV'}
for id,p in PROJECTS.items():
 assert Path(p['root']).is_relative_to(Path.cwd())
 assert p['brief'] and not p['assets']
 assert 'English' in rules_for(id)
 assert p['site'] in target_context(id)
p=Path(PROJECTS['landscape_iv']['root'])/'project.json';obj=json.loads(p.read_text());obj['brief']='My own concept';p.write_text(json.dumps(obj));seed_projects.ensure_projects();assert json.loads(p.read_text())['brief']=='My own concept'
''')
 def test_reference_job_and_board_job_use_only_local_sources(self):
  self.run_isolated('''
import server,json
from unittest.mock import patch
from PIL import Image
from pathlib import Path
server.init();server.scan();assert not server.library()['items']
u=server.APP/'data/uploads';u.mkdir();uid='a'*32;Image.new('RGB',(128,128),'white').save(u/(uid+'.png'))
with patch.object(server,'codex_bin',return_value='codex'),patch.object(server,'schedule_jobs'):
 job=server.create_job({'project_id':'landscape_iv','simple_reference':True,'references':[uid],'reference_order':[uid]})
 with server.connect() as c: row=dict(c.execute('SELECT * FROM jobs WHERE id=?',(job['id'],)).fetchone())
 prompt=(Path(row['folder'])/'brief.txt').read_text()
 assert 'Landscape Design IV' in prompt and str(Path.cwd()/'data/projects/landscape_iv') in prompt
 assert 'reference_priority' in prompt and 'main' in prompt
 board=server.create_job({'project_id':'landscape_ii','board_workflow':{'version':1,'count':2,'size':'A1','orientation':'portrait','brief':'Explore public spaces and river relationships with real evidence.'}})
 with server.connect() as c: b=dict(c.execute('SELECT * FROM jobs WHERE id=?',(board['id'],)).fetchone())
 assert b['status']=='queued'
 assert not (Path(b['folder'])/'board_reference').exists()
 assert not json.loads(b['request'])['board_reference_hierarchy']
''')
 def test_no_compulsory_private_benchmark(self):
  self.run_isolated('''
import board_workflow,board_design_protocol
from pathlib import Path
r={'board_workflow':{'version':1,'count':2,'size':'A1','orientation':'portrait','brief':'Create independent site analysis boards.'}}
prompt=board_workflow.stage_prompt(r,'evidence')
assert 'no bundled' in prompt.lower()
e={'capabilities':[],'reference_grammar':[],'selected_references':[],'sources':[],'claims':[]}
assert not board_design_protocol.issues('evidence',e,lambda _: {},Path.cwd(),{'reference_hierarchy':[]})
''')
 def test_release_contains_no_private_runtime_payload(self):
  for name in ('data','jobs','cache','board_reference','.runtime'):
   # Runtime folders may exist locally, but must be gitignored / never packaged.
   if name!='board_reference':self.assertIn(name+'/',(APP/'.gitignore').read_text())
  for path in list(APP.glob('*.py'))+list((APP/'presets').glob('*.json')):
   text=path.read_text().lower()
   for needle in ('/users/','jury01_submission','common ground','for emre','for buse','for bilge'):
    self.assertNotIn(needle,text,str(path))
if __name__=='__main__':unittest.main()
