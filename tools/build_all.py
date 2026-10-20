"""Bangun ulang 'PCB Viewer 3D.html' dari boards.json (urutan = urutan menu; yang pertama jadi default).
Pakai:  python -I tools/build_all.py
"""
import json, os, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(root, 'boards.json'), encoding='utf8'))
args = [sys.executable, '-I', os.path.join(root, 'tools', 'build_viewer.py'),
        os.path.join(root, cfg['output']), os.path.join(root, cfg['background'])]
args += ['default=' + cfg.get('default', cfg['boards'][0]['key'])]
args += [f"{b['key']}:{b['label']}:{os.path.join(root, b['glb'])}" for b in cfg['boards']]
subprocess.run(args, check=True)
print('OK ->', os.path.join(root, cfg['output']))
