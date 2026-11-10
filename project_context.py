"""Snapshot current project intent separately from historical visual references."""
import hashlib
import json
from pathlib import Path


def snapshot(root):
    root=Path(root)
    files={}
    for relative in ('AGENTS.md','project_context/current_project.json'):
        path=root/relative
        if path.is_file():
            content=path.read_text()
            files[relative]={'path':str(path.resolve()),'sha256':hashlib.sha256(content.encode()).hexdigest(),'content':content}
    return {'project_root':str(root.resolve()),'files':files,
            'scope':'Recorded project instructions and current progress; not automatic synchronization of every chat.'}


def write_snapshot(folder, root):
    value=snapshot(root)
    path=Path(folder)/'board_project_context.json'
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2));tmp.replace(path)
    return value


def changed(root, value):
    return snapshot(root)!=value
