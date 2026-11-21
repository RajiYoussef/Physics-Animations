"""Press Run once to calculate and validate real training data. No rendering."""
from pathlib import Path
import hashlib, json, time, platform
import numpy as np
import settings
ROOT = Path(__file__).resolve().parent

def signature():
    config = {k:getattr(settings,k) for k in ('SEED','HIDDEN_UNITS','EPOCHS','LEARNING_RATE','MOMENTUM','INTERIOR_POINTS','BOUNDARY_POINTS','CHECKPOINTS')}
    config['model_sha256']=hashlib.sha256((ROOT/'model.py').read_bytes()).hexdigest()
    return config

def prepare(force=False):
    folder=ROOT/'data'; folder.mkdir(exist_ok=True)
    metadata=folder/'metadata.json'; output=folder/'training.npz'
    if not force and metadata.exists() and output.exists():
        old=json.loads(metadata.read_text())
        if old['configuration']==signature():
            print('Using verified training cache.');return output
    import model as m
    import sympy as sym
    x,y=sym.symbols('x y',real=True)
    exact=sym.sin(x)*sym.sinh(sym.pi-y)/sym.sinh(sym.pi)
    assert sym.simplify(sym.diff(exact,x,2)+sym.diff(exact,y,2))==0
    assert sym.simplify(exact.subs(y,0)-sym.sin(x))==0
    assert exact.subs(x,0)==exact.subs(x,sym.pi)==exact.subs(y,sym.pi)==0
    p=m.params_initial; velocity=m.jnp.zeros_like(p)
    # Independent analytic second derivative of this tanh network.
    px,py=.71,1.23; n=settings.HIDDEN_UNITS
    z=np.asarray(p[:n])*px+np.asarray(p[2*n:3*n])*py+np.asarray(p[n:2*n])
    analytic=np.sum(np.asarray(p[3*n:4*n])*(-2*np.tanh(z)*(1-np.tanh(z)**2))*(np.asarray(p[:n])**2+np.asarray(p[2*n:3*n])**2))
    np.testing.assert_allclose(float(m.Vxx(p,px,py)+m.Vyy(p,px,py)),analytic,rtol=1e-10,atol=1e-10)
    axis=np.linspace(0,np.pi,41); X,Y=np.meshgrid(axis,axis,indexing='xy')
    xf,yf=m.jnp.array(X.ravel()),m.jnp.array(Y.ravel())
    epochs=np.unique(np.r_[0,1,10,25,np.geomspace(50,settings.EPOCHS,settings.CHECKPOINTS).astype(int)])
    records=[]; fields=[]; residuals=[]; weights=[]; start=time.perf_counter()
    for epoch in range(settings.EPOCHS+1):
        if epoch in epochs:
            parts=np.asarray(m.components(p,m.points))
            if not np.all(np.isfinite(parts)):raise RuntimeError('Nonfinite loss; training stopped.')
            np.testing.assert_allclose(parts.sum(),float(m.loss(p,m.points)),rtol=1e-10)
            fields.append(np.asarray(m.predict(p,xf,yf)).reshape(X.shape))
            residuals.append(np.asarray(m.residual_batch(p,xf,yf)).reshape(X.shape))
            records.append(parts);weights.append(np.asarray(p))
            print(f'epoch {epoch:5d}: loss {parts.sum():.8g}',flush=True)
        if epoch<settings.EPOCHS:p,velocity=m.update(p,velocity)
    check=m.jnp.pi*m.random.uniform(m.key_check,(4096,2))
    prediction=np.asarray(m.predict(p,check[:,0],check[:,1]))
    target=np.sin(np.asarray(check[:,0]))*np.sinh(np.pi-np.asarray(check[:,1]))/np.sinh(np.pi)
    test_res=np.asarray(m.residual_batch(p,check[:,0],check[:,1]))
    edge=m.jnp.linspace(0,m.jnp.pi,257); zero=m.jnp.zeros_like(edge); far=m.jnp.full_like(edge,m.jnp.pi)
    edge_errors=np.concatenate([np.asarray(m.predict(p,edge,zero)-m.jnp.sin(edge)),np.asarray(m.predict(p,zero,edge)),np.asarray(m.predict(p,far,edge)),np.asarray(m.predict(p,edge,far))])
    metrics={'relative_L2':float(np.linalg.norm(prediction-target)/np.linalg.norm(target)),
             'sample_max_abs':float(np.max(np.abs(prediction-target))),
             'heldout_residual_rms':float(np.sqrt(np.mean(test_res**2))),
             'boundary_max_abs':float(np.max(np.abs(edge_errors))),
             'validation_interior_points':4096,'validation_edge_points':257}
    reference=np.sin(X)*np.sinh(np.pi-Y)/np.sinh(np.pi)
    np.savez_compressed(output,axis=axis,fields=fields,residuals=residuals,losses=records,
                        weights=weights,epochs=epochs,points=np.asarray(m.points),exact=reference)
    metadata.write_text(json.dumps({'configuration':signature(),'metrics':metrics,
        'seconds':time.perf_counter()-start,'jax':m.jax.__version__,'python':platform.python_version(),
        'precision':'float64','optimizer':'momentum with look-ahead gradient','device':str(m.jax.devices()),
        'checks':['symbolic PDE and four boundaries','analytic/autodiff Laplacian','loss component sum']},indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(13,4))
    axes[0].imshow(fields[-1],origin='lower',extent=[0,np.pi,0,np.pi],vmin=0,vmax=1);axes[0].set_title('Predicted V')
    im=axes[1].imshow(np.abs(fields[-1]-reference),origin='lower');fig.colorbar(im,ax=axes[1]);axes[1].set_title('Absolute error')
    axes[2].semilogy(epochs,np.sum(records,axis=1));axes[2].set_title('Measured loss');axes[2].set_xlabel('epoch')
    fig.tight_layout();fig.savefig(folder/'numerical_check.png');plt.close(fig)
    print(json.dumps(metrics,indent=2)); return output

if __name__=='__main__':prepare()
