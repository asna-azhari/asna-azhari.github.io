import sys,base64,json
out,bg=sys.argv[1:3]
# usage: build_viewer.py out.html background.(jpg|webp) [default=key] key:Label:file.glb [key:Label:file.glb ...]
default=next((x.split('=',1)[1] for x in sys.argv[3:] if x.startswith('default=')),None)
boards=[tuple(a.split(':',2)) for a in sys.argv[3:] if not a.startswith('default=')]
boards=[(k,n,p) for k,n,p in boards]
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
tags=''.join(f'<script id="glb-{k}" type="application/octet-stream">{b64(p)}</script>\n' for k,_,p in boards)
btns=''.join(f'<button class="bd" data-k="{k}">{n}</button>' for k,n,_ in boards)
html='''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PCB Viewer 3D</title>
<style>
:root{--bg:#14171c;--panel:#1d2128;--fg:#e6e8eb;--mut:#8b93a0;--acc:#4aa3ff}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);font:14px system-ui,sans-serif}
header{flex:none;display:flex;gap:10px;align-items:center;padding:10px 16px;background:var(--panel);border-bottom:1px solid #2c323c;flex-wrap:wrap}
h1{font-size:16px;margin:0 12px 0 0}
.spd{display:flex;align-items:center;gap:6px;color:var(--mut);font-size:13px}.spd input{width:110px;accent-color:var(--acc)}.spd span{min-width:28px;color:var(--fg)}
.sep{width:1px;height:24px;background:#3a4250;margin:0 4px}
button{background:#272d37;color:var(--fg);border:1px solid #3a4250;border-radius:6px;padding:6px 14px;cursor:pointer}
button.on{background:var(--acc);border-color:var(--acc);color:#04121f}
.info{color:var(--mut);margin-left:auto}
body{display:flex;flex-direction:column}
#s3{position:relative;flex:1;min-height:0;overflow:hidden;
 background:linear-gradient(rgba(8,12,18,.3),rgba(8,12,18,.3)),url(data:'''+('image/jpeg' if bg.lower().endswith(('.jpg','.jpeg')) else 'image/webp')+''';base64,'''+b64(bg)+''') center/cover no-repeat,#10141b}
#s3 canvas{display:block;width:100%;height:100%}
#s3.bgdark{background:radial-gradient(ellipse at 50% 35%,#3a4f6b 0%,#222d3d 45%,#10141b 100%)}
#s3.bglight{background:radial-gradient(ellipse at 50% 35%,#ffffff 0%,#dfe5ee 60%,#b9c3d1 100%)}
.tools{position:absolute;top:12px;right:12px;display:flex;flex-direction:column;gap:6px;z-index:2}
.tools button{background:rgba(29,33,40,.88);padding:6px 12px;font-size:13px;text-align:left}
#card{position:absolute;left:16px;bottom:16px;width:min(360px,calc(100% - 32px));background:rgba(20,23,28,.94);border:1px solid #3a4250;border-radius:10px;padding:12px 14px;display:none;z-index:3;font-size:13px;line-height:1.45}
#card h2{margin:0 24px 6px 0;font-size:15px}
#card .t{display:inline-block;font-size:11px;padding:1px 8px;border-radius:99px;background:#ffb020;color:#2a1a00;margin-bottom:8px}
#card table{border-collapse:collapse;margin:4px 0 8px}#card td{padding:1px 10px 1px 0;color:var(--mut)}#card td+td{color:var(--fg)}
#card p{margin:0;color:#cfd5de}
#card .x{position:absolute;top:6px;right:8px;padding:0 8px;font-size:18px;line-height:24px;background:none;border:0;color:var(--mut)}
#menu{padding:7px 10px;display:flex;align-items:center}
.curname{color:var(--acc);font-weight:600}
#side{position:absolute;top:0;left:0;bottom:0;width:230px;padding:12px;background:rgba(20,23,28,.96);border-right:1px solid #3a4250;transform:translateX(-100%);transition:transform .2s;z-index:6;overflow:auto}
#side.open{transform:none}
#side .sh{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin:2px 0 10px}
#side button{display:block;width:100%;text-align:left;margin-bottom:6px}
#msg{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;pointer-events:none;text-shadow:0 1px 4px #000}
</style></head><body>
<header><button id="menu" title="Pilih board"><svg width="18" height="14" viewBox="0 0 18 14"><path d="M0 1h18M0 7h18M0 13h18" stroke="currentColor" stroke-width="2"/></svg></button><h1>PCB Viewer</h1><span id="curname" class="curname"></span><span class="sep"></span>
<button id="bc" class="on">Komponen: ON</button><button id="br">Putar otomatis: OFF</button><label class="spd" title="Kecepatan putar">Kecepatan <input id="sp" type="range" min="0.5" max="10" step="0.5" value="2"><span id="spv">2×</span></label><button id="fit">Fit</button>
<span class="info">drag = putar, scroll = zoom, klik kanan = geser, klik bagian = deskripsi</span></header>
<div id="s3"><nav id="side"><div class="sh">Pilih board</div>'''+btns+'''</nav><div id="msg">Memuat model 3D…</div>
<div class="tools"><button id="v-top">Tampak atas</button><button id="v-bot">Tampak bawah</button><button id="v-iso">Isometrik</button><button id="bgsw">Latar: Gambar</button></div>
<div id="card"><button class="x" id="cx" title="Tutup">×</button><span class="t" id="ct"></span><h2 id="ch"></h2><table id="cd"></table><p id="cp"></p></div></div>
'''+tags+'''<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const $=id=>document.getElementById(id),s3=$('s3'),msg=$('msg');
const ren=new THREE.WebGLRenderer({antialias:true,alpha:true});ren.setPixelRatio(Math.min(devicePixelRatio,2));
ren.toneMapping=THREE.ACESFilmicToneMapping;ren.outputColorSpace=THREE.SRGBColorSpace;s3.appendChild(ren.domElement);
const scene=new THREE.Scene();scene.environment=new THREE.PMREMGenerator(ren).fromScene(new RoomEnvironment(),.04).texture;
const cam=new THREE.PerspectiveCamera(35,1,1,3000);
const ctl=new OrbitControls(cam,ren.domElement);ctl.enableDamping=true;ctl.autoRotateSpeed=2;
const dl=new THREE.DirectionalLight(0xffffff,1.6);dl.position.set(60,120,80);scene.add(dl);
scene.add(new THREE.HemisphereLight(0xffffff,0xb8c4d6,1.1));
const hl=new THREE.DirectionalLight(0xffffff,1.3);hl.position.set(0,0,1);cam.add(hl);scene.add(cam);
const loader=new GLTFLoader();loader.setMeshoptDecoder(MeshoptDecoder);
const cache={};let cur=null,compOn=true,box=null;
function rs(){ren.setSize(s3.clientWidth,s3.clientHeight);cam.aspect=s3.clientWidth/s3.clientHeight;cam.updateProjectionMatrix()}
function fit3(v){if(!box)return;v=Array.isArray(v)?v:[0,.75,.65];const c=box.getCenter(new THREE.Vector3()),s=box.getSize(new THREE.Vector3());
 const r=s.length()/2,d=r/Math.sin(THREE.MathUtils.degToRad(cam.fov/2))*.95;
 cam.position.copy(c).add(new THREE.Vector3(v[0],v[1],v[2]).normalize().multiplyScalar(d));ctl.target.copy(c);ctl.update()}
function parse(k){return new Promise((ok,no)=>{
 const bin=Uint8Array.from(atob($('glb-'+k).textContent),c=>c.charCodeAt(0)).buffer;
 loader.parse(bin,'',g=>{const m=g.scene,b=new THREE.Box3().setFromObject(m),c=b.getCenter(new THREE.Vector3());
  m.position.sub(new THREE.Vector3(c.x,0,c.z));b.translate(new THREE.Vector3(-c.x,0,-c.z));ok({m,b})},no)})}
async function select(k){
 document.querySelectorAll('.bd').forEach(b=>b.classList.toggle('on',b.dataset.k===k));
 history.replaceState(null,'','#'+k);$('curname').textContent=NAMES[k]||k;$('side').classList.remove('open');
 clearSel();if(cur)scene.remove(cache[cur].m);
 msg.style.display='flex';
 try{cache[k]??=await parse(k)}catch(e){msg.textContent='Gagal memuat 3D: '+e.message;return}
 msg.style.display='none';cur=k;scene.add(cache[k].m);box=cache[k].b;
 const c=cache[k].m.getObjectByName('components');if(c)c.visible=compOn;
 fit3()}
document.querySelectorAll('.bd').forEach(b=>b.onclick=()=>select(b.dataset.k));
$('bc').onclick=()=>{compOn=!compOn;const c=cache[cur]?.m.getObjectByName('components');if(c)c.visible=compOn;
 $('bc').classList.toggle('on',compOn);$('bc').textContent='Komponen: '+(compOn?'ON':'OFF')};
$('br').onclick=()=>{ctl.autoRotate=!ctl.autoRotate;$('br').classList.toggle('on',ctl.autoRotate);
 $('br').textContent='Putar otomatis: '+(ctl.autoRotate?'ON':'OFF')};
$('sp').oninput=e=>{const v=+e.target.value;ctl.autoRotateSpeed=v;$('spv').textContent=v+'×'};
$('fit').onclick=fit3;
const LOREM={pcb:'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',comp:'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'};
const DESC={}; // isi nanti: DESC.psu={pcb:'...',comp:'...'}
const NAMES='''+json.dumps({k:n for k,n,_ in boards})+''';
const ray=new THREE.Raycaster(),mp=new THREE.Vector2(),ufc=new WeakMap();let ov=null;
function roots(g){let r=ufc.get(g);if(r)return r;
 const ix=g.index.array,n=g.attributes.position.count,p=new Int32Array(n);for(let i=0;i<n;i++)p[i]=i;
 const f=a=>{while(p[a]!==a){p[a]=p[p[a]];a=p[a]}return a};
 for(let i=0;i<ix.length;i+=3){const ra=f(ix[i]),rb=f(ix[i+1]);if(ra!==rb)p[rb]=ra;const rc=f(ix[i+2]),r2=f(ra);if(r2!==rc)p[rc]=r2}
 for(let i=0;i<n;i++)p[i]=f(i);ufc.set(g,p);return p}
const vis=o=>{for(;o;o=o.parent)if(!o.visible)return false;return true};
function clearSel(){if(ov){ov.parent&&ov.parent.remove(ov);ov.geometry.dispose();ov=null}$('card').style.display='none'}
function pick(e){
 if(!cur)return;const r=ren.domElement.getBoundingClientRect();
 mp.set((e.clientX-r.left)/r.width*2-1,-((e.clientY-r.top)/r.height)*2+1);ray.setFromCamera(mp,cam);
 const hits=ray.intersectObject(cache[cur].m,true).filter(h=>h.object.isMesh&&h.object!==ov&&h.object.geometry.index&&vis(h.object));
 clearSel();if(!hits.length)return;
 const h=hits[0],m=h.object,g=m.geometry,rt=roots(g),ix=g.index.array,pos=g.attributes.position,root=rt[ix[h.faceIndex*3]],out=[];
 for(let i=0;i<ix.length;i+=3)if(rt[ix[i]]===root)for(let j=0;j<3;j++){const v=ix[i+j];out.push(pos.getX(v),pos.getY(v),pos.getZ(v))}
 const og=new THREE.BufferGeometry();og.setAttribute('position',new THREE.Float32BufferAttribute(out,3));
 ov=new THREE.Mesh(og,new THREE.MeshBasicMaterial({color:0xffb020,transparent:true,opacity:.8,side:THREE.DoubleSide,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-4,polygonOffsetUnits:-4}));
 ov.raycast=()=>{};m.add(ov);ov.updateWorldMatrix(true,false);
 let comp=false;for(let o=m;o;o=o.parent)if(o.name==='components')comp=true;
 const b=new THREE.Box3().setFromObject(ov),s=b.getSize(new THREE.Vector3()),c=b.getCenter(new THREE.Vector3()),t=comp?'comp':'pcb',n=v=>v.toFixed(2);
 $('ct').textContent=comp?'Komponen':'PCB';$('ch').textContent=(NAMES[cur]||cur)+(comp?' - bagian komponen':' - papan PCB');
 $('cd').innerHTML='';[['Ukuran (P × L × T)',n(s.x)+' × '+n(s.z)+' × '+n(s.y)+' mm'],['Posisi X, Y',n(c.x)+', '+n(-c.z)+' mm dari tengah board'],['Tinggi (Z)',n(b.min.y)+' s/d '+n(b.max.y)+' mm dari permukaan PCB'],['Jumlah segitiga',String(out.length/9)]].forEach(([a,v])=>{const tr=document.createElement('tr'),d1=document.createElement('td'),d2=document.createElement('td');d1.textContent=a;d2.textContent=v;tr.append(d1,d2);$('cd').append(tr)});
 $('cp').textContent=(DESC[cur]&&DESC[cur][t])||LOREM[t];$('card').style.display='block'}
let pd=null;const cv=ren.domElement;
cv.addEventListener('pointerdown',e=>{pd=e.button===0?{x:e.clientX,y:e.clientY}:null});
cv.addEventListener('pointerup',e=>{if(pd&&Math.hypot(e.clientX-pd.x,e.clientY-pd.y)<5)pick(e);pd=null});
$('menu').onclick=()=>$('side').classList.toggle('open');
cv.addEventListener('pointerdown',()=>$('side').classList.remove('open'));
$('cx').onclick=clearSel;addEventListener('keydown',e=>{if(e.key==='Escape')clearSel()});
$('v-top').onclick=()=>fit3([0,1,.02]);$('v-bot').onclick=()=>fit3([0,-1,.02]);$('v-iso').onclick=()=>fit3();
const BGS=[['Gambar',''],['Gelap','bgdark'],['Terang','bglight']];let bi=0;
$('bgsw').onclick=()=>{BGS.forEach(x=>x[1]&&s3.classList.remove(x[1]));bi=(bi+1)%BGS.length;if(BGS[bi][1])s3.classList.add(BGS[bi][1]);$('bgsw').textContent='Latar: '+BGS[bi][0]};
addEventListener('resize',rs);rs();
(function loop(){requestAnimationFrame(loop);ctl.update();ren.render(scene,cam)})();
const KEYS='''+json.dumps([k for k,_,_ in boards])+''';const DEFAULT='''+json.dumps(default if default in [k for k,_,_ in boards] else boards[0][0])+''';const h=location.hash.slice(1);select(KEYS.includes(h)?h:DEFAULT);
</script></body></html>'''
open(out,'w',encoding='utf8').write(html)
