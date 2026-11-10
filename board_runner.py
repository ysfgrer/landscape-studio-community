"""Checkpointed board orchestration on the existing local Codex worker queue."""
import json, os, signal, subprocess, time
from pathlib import Path
import board_workflow
import board_design_protocol
import project_context


def write_progress(folder, rows, current):
    dest=folder/'board_progress.json'
    tmp=dest.with_suffix('.tmp')
    tmp.write_text(json.dumps({'version':1,'stages':rows,'current_stage':current,'updated_at':time.time()},indent=2))
    tmp.replace(dest)


def run(server, job, req):
    folder=Path(job['folder']); jid=job['id']
    rows=[{**stage,'status':'pending','issues':[]} for stage in board_workflow.STAGES]
    base=(folder/'brief.txt').read_text()
    project_root=req.get('board_project_root')
    project_snapshot=project_context.write_snapshot(folder,project_root) if project_root else None
    env=os.environ.copy();env.pop('CODEX_THREAD_ID',None)
    checkpoint_path=folder/'board_checkpoints.json'
    try: checkpoints=json.loads(checkpoint_path.read_text())
    except (OSError,ValueError): checkpoints={}
    if not isinstance(checkpoints,dict): checkpoints={}
    def fingerprint(stage):
        return board_design_protocol.fingerprint(folder,req,stage,board_workflow.STAGES,board_workflow.REPORTS)
    def remember(stage):
        checkpoints[stage]=fingerprint(stage)
        tmp=checkpoint_path.with_suffix('.tmp')
        tmp.write_text(json.dumps(checkpoints,indent=2));tmp.replace(checkpoint_path)
    def notes():
        p=folder/'user_updates.txt'
        return p.read_text() if p.exists() else ''

    run_feedback=notes()
    def feedback_changed():
        context_changed=bool(project_root and project_context.changed(project_root,project_snapshot))
        if notes()==run_feedback and not context_changed:return False
        server.job_update(jid,status='needs_attention',message='Project context or feedback changed. Resume to reconcile current decisions before continuing.')
        return True

    for row in rows:
        stage=row['id']
        if feedback_changed():return
        with server.connect() as c:
            if c.execute('SELECT status FROM jobs WHERE id=?',(jid,)).fetchone()[0]=='cancelled':return
        # Revalidate durable checkpoints: an exported or self-declared pass alone is insufficient.
        issues=board_workflow.stage_issues(folder,req,stage)
        if stage=='review':
            issues.extend(board_design_protocol.review_receipt_issues(folder))
        if not issues and checkpoints.get(stage)==fingerprint(stage):
            row['status']='completed';write_progress(folder,rows,stage);continue
        if not issues: issues=['Inputs or design protocol changed; reconcile this stage and its dependencies before continuing.']
        row['status']='running';write_progress(folder,rows,stage)
        for attempt in range(1,3):
            row['attempt']=attempt
            server.job_update(jid,message=row['title']+' · '+('working' if attempt==1 else 'correcting checks'))
            updates=notes()
            prompt=base+'\n'+board_workflow.stage_prompt(req,stage)+'\nLatest user updates:\n'+updates
            prompt+='\nReconcile these existing gate issues, retaining valid fresh components: '+json.dumps(issues)
            if stage=='export':prompt+='\nThe reviewed drawing and composition files are frozen. Merge/package those exact PDFs; do not redraw or modify them during export. If a correction is needed, report it for renewed review.'
            if attempt==2:prompt+='\nCorrect this stage only. Failed checks: '+json.dumps(issues)+'. Reuse valid new components and evidence; never overwrite historical sources.'
            result=folder/f'board_{stage}_result.txt'
            cmd=[server.codex_bin(),'exec','--sandbox','workspace-write','--skip-git-repo-check','-C',str(folder),'--json','--color','never','-o',str(result),'-']
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=env,start_new_session=True)
            with server.LOCK:
                server.PROCESSES[jid]=proc
                with server.connect() as c:cancelled=c.execute('SELECT status FROM jobs WHERE id=?',(jid,)).fetchone()[0]=='cancelled'
                if cancelled:
                    os.killpg(proc.pid,signal.SIGTERM);proc.wait();server.PROCESSES.pop(jid,None);return
            try:
                proc.stdin.write(prompt);proc.stdin.close()
                with (folder/'events.jsonl').open('a') as log:
                    for line in server.process_lines(proc):
                        log.write(line);log.flush()
                        try:
                            ev=json.loads(line);msg=ev.get('item',{}).get('text')
                            if msg:server.job_update(jid,message=row['title']+'\n'+msg[-5500:])
                        except (ValueError,AttributeError):pass
                code=proc.wait()
            finally:
                if proc.poll() is None:
                    os.killpg(proc.pid,signal.SIGTERM);proc.wait()
                with server.LOCK:server.PROCESSES.pop(jid,None)
            with server.connect() as c:
                if c.execute('SELECT status FROM jobs WHERE id=?',(jid,)).fetchone()[0]=='cancelled':return
            issues=board_workflow.stage_issues(folder,req,stage)
            if notes()!=updates:
                issues.insert(0,'User feedback arrived during this stage. Reconcile the latest feedback before accepting the result.')
            if code:issues.insert(0,f'Production engine exited with code {code}.')
            row['issues']=issues;write_progress(folder,rows,stage)
            if notes()!=updates:break
            if not issues:break
        if issues:
            row['status']='needs_attention';write_progress(folder,rows,stage)
            server.scan()
            server.job_update(jid,status='needs_attention',message=row['title']+' needs attention:\n'+'\n'.join(issues)+'\n'+(result.read_text()[-3000:] if result.exists() else ''))
            return
        if feedback_changed():return
        if stage=='review':
            receipt=folder/'board_review_receipt.json'
            tmp=receipt.with_suffix('.tmp')
            tmp.write_text(json.dumps({'artifacts':board_design_protocol.reviewed_artifacts(folder),'created_at':time.time()},indent=2))
            tmp.replace(receipt)
        remember(stage)
        row['status']='completed';write_progress(folder,rows,stage)
        # New compositions become visible while later checks run. Sources/QA stay out of gallery.
        server.scan()
    with server.connect() as c:
        if c.execute('SELECT status FROM jobs WHERE id=?',(jid,)).fetchone()[0]=='cancelled':return
    if feedback_changed():return
    issues=board_workflow.delivery_issues(folder,req)
    server.scan()
    server.job_update(jid,status='needs_attention' if issues else 'completed',message='\n'.join(issues) if issues else 'Board set exported. Technical checks passed; inspect the rendered set before printing. Sources and unresolved qualifications are retained separately.')
