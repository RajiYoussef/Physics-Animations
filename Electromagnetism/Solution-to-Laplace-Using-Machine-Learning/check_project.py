"""Optional numerical/source validation; not needed for normal rendering."""
from pathlib import Path
import ast,json
import numpy as np
from plot_data import potential_grid
ROOT=Path(__file__).resolve().parent

def check():
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
    data=np.load(ROOT/'data/training.npz')
    assert len(data['weights'][0])==401
    assert data['epochs'][0]==0 and data['epochs'][-1]==10000
    assert np.isfinite(data['losses']).all()
    assert np.sum(data['losses'][-1])<np.sum(data['losses'][0])
    for k in [0,len(data['epochs'])//2,-1]:
        X,Y,V=potential_grid(data['weights'][k])
        np.testing.assert_allclose(V,data['fields'][k],atol=1e-12)
    np.testing.assert_allclose(data['exact'][0],np.sin(data['axis']),atol=1e-12)
    np.testing.assert_allclose(data['exact'][-1],0,atol=1e-12)
    script=json.loads((ROOT/'narration.json').read_text(encoding='utf-8'))
    assert len(script)==9
    for i,scene in enumerate(script,1):
        text=(ROOT/'narration'/f'scene_{i:02d}.txt').read_text(encoding='utf-8')
        for block in scene['blocks']:assert block['text'] in text
    for filename in ['model.py','plot_data.py']:
        text=(ROOT/filename).read_text()
        for part in text.split('# snippet:')[1:]:
            name,body=part.split('\n',1);code=body.split('# end:'+name)[0]
            ast.parse(code)
    print('PASS: Python syntax, checkpoint consistency, independent NumPy evaluation, boundary benchmark, narration consistency, executable snippets.')
    print(json.dumps(json.loads((ROOT/'data/metadata.json').read_text())['metrics'],indent=2))

if __name__=='__main__':check()
