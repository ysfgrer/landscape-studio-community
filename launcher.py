#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,time,urllib.request,json,os,webbrowser
APP=Path(__file__).resolve().parent
PORT=int(os.environ.get('LANDSCAPE_STUDIO_PORT','8766'))
URL=f'http://127.0.0.1:{PORT}'
def running():
 try:
  with urllib.request.urlopen(URL+'/api/status',timeout=1) as r:
   data=json.load(r)
   if data.get('app')!='landscape-studio-community' or Path(data['project']).resolve()!=APP:raise RuntimeError('Port belongs to another application. Set LANDSCAPE_STUDIO_PORT to a free port.')
   return True
 except (OSError,ValueError):return False
if not running():
 (APP/'data').mkdir(exist_ok=True)
 with (APP/'data/server.log').open('a') as log:
  subprocess.Popen([sys.executable,str(APP/'server.py')],cwd=APP,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
 for _ in range(50):
  if running():break
  time.sleep(.2)
if running():
 print(URL)
 if '--no-open' not in sys.argv:webbrowser.open(URL)
else:
 print('Could not start Studio. See data/server.log.',file=sys.stderr);sys.exit(1)
