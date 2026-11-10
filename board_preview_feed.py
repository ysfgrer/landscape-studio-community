"""Read-only production snapshots for the UI; never changes job/checkpoint files."""
import argparse,fcntl,json,os,sqlite3,time
from pathlib import Path
APP=Path(__file__).resolve().parent

def read(p):
 try:return json.loads(p.read_text())
 except (OSError,ValueError):return {}
def publish(folder,dest):
 import sys
 sys.path.insert(0,str(APP/'.runtime'))
 import pymupdf
 from PIL import Image
 evidence=read(folder/'board_evidence.json');plan=read(folder/'board_plan.json');progress=read(folder/'board_progress.json')
 boards=plan.get('boards',[]);modules={m['id']:m for b in boards for m in b.get('modules',[]) if m.get('id')}
 dest.mkdir(parents=True,exist_ok=True);previews=[]
 available=list((folder/'outputs/components').glob('*'))+list((folder/'outputs').glob('board_*/*'))
 rank={'.svg':1,'.pdf':2,'.jpg':3,'.png':4};groups={}
 for item in sorted(available,key=lambda p:rank.get(p.suffix.lower(),0)):
  if item.is_file() and item.suffix.lower() in rank:groups[str(item.with_suffix(''))]=item
 candidates=list(groups.values())
 for source in sorted(candidates):
  if not source.resolve().is_relative_to((folder/'outputs').resolve()):continue
  try:
   stamp=source.stat().st_mtime_ns
   import hashlib
   key=hashlib.sha256(str(source.relative_to(folder)).encode()).hexdigest()[:16]
   target=dest/(key+'.jpg');meta=dest/(key+'.stamp')
   if not target.exists() or not meta.exists() or meta.read_text()!=str(stamp):
    temp=target.with_suffix('.tmp')
    if source.suffix.lower() in {'.svg','.pdf'}:
     with pymupdf.open(source) as d:
      page=d[0];scale=min(1500/page.rect.width,1500/page.rect.height);pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    else:
     with Image.open(source) as src:im=src.convert('RGB');im.thumbnail((1500,1500))
    im.save(temp,format='JPEG',quality=90);temp.replace(target);meta.write_text(str(stamp))
   module=modules.get(source.stem,{})
   previews.append({'id':source.stem,'title':module.get('title',source.stem),'kind':'Drawing draft' if source.parent.name=='components' else 'Sheet draft','url':'/generated/board-previews/'+folder.name+'/'+target.name+'?v='+str(stamp),'purpose':module.get('purpose','')})
  except Exception:continue # A producer may still be writing; retry next tick.
 data={'updated':time.time(),'stages':progress.get('stages',[]),'findings':{'claims':[{k:c.get(k) for k in ('id','text','status')} for c in evidence.get('claims',[])], 'limitations':evidence.get('limitations',[]),'blockers':evidence.get('blockers',[]),'source_count':len(evidence.get('sources',[]))},'plan':{'concept':plan.get('concept',''),'boards':[{'index':b.get('index'),'title':b.get('title'),'question':b.get('question'),'takeaway':b.get('takeaway'),'modules':[{'id':m.get('id'),'title':m.get('title'),'purpose':m.get('purpose'),'status':m.get('status')} for m in b.get('modules',[])]} for b in boards]},'previews':previews}
 tmp=dest/'index.tmp';tmp.write_text(json.dumps(data,ensure_ascii=False));tmp.replace(dest/'index.json')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--watch',action='store_true');parser.add_argument('--parent',type=int);args=parser.parse_args()
 lock=(APP/'data/board-preview-feed.lock').open('w')
 for attempt in range(10):
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
  except BlockingIOError:
   if not args.watch or attempt==9:return
   time.sleep(1)
 while True:
  if args.parent:
   try:os.kill(args.parent,0)
   except ProcessLookupError:return
  try:
   with sqlite3.connect('file:'+str(APP/'data/studio.sqlite3')+'?mode=ro',uri=True) as c:rows=c.execute('SELECT id,folder,request FROM jobs').fetchall()
   for jid,path,request in rows:
    try:
     if json.loads(request or '{}').get('board_workflow') and Path(path).resolve().parent==(APP/'jobs').resolve():publish(Path(path),APP/'web/generated/board-previews'/jid)
    except Exception:continue
  except sqlite3.Error:pass
  if not args.watch:return
  time.sleep(6)
if __name__=='__main__':main()
