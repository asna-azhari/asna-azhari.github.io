import sys, numpy as np
from PIL import Image
W,H=1920,1080
rng=np.random.default_rng(7)
def fbm():
    acc=np.zeros((H,W),np.float32);amp=1.0;tot=0
    for o,(gw,gh) in enumerate([(4,3),(8,5),(16,9),(32,18),(64,36),(128,72)]):
        g=rng.random((gh,gw)).astype(np.float32)
        im=Image.fromarray((g*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
        acc+=np.asarray(im,np.float32)/255*amp;tot+=amp;amp*=0.55
    return acc/tot
n=fbm()
n=(n-n.min())/(n.max()-n.min())
cloud=np.clip((n-0.48)/0.30,0,1)**1.3          # coverage + soft edges
y=np.linspace(0,1,H,dtype=np.float32)[:,None]
top=np.array([46,120,205],np.float32);bot=np.array([160,205,240],np.float32)
sky=top[None,None,:]*(1-y[...,None])+bot[None,None,:]*y[...,None]
sky=np.broadcast_to(sky,(H,W,3))
# cloud shading: brighter top, slightly grey base
shade=np.clip(1.0-0.10*(n-0.5)*2,0.9,1.0)[...,None]
col=np.array([255,255,255],np.float32)*shade
img=sky*(1-cloud[...,None])+col*cloud[...,None]
Image.fromarray(np.clip(img,0,255).astype(np.uint8)).save(sys.argv[1],'JPEG',quality=88,optimize=True)
