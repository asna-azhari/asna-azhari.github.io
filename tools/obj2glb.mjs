import fs from 'fs'
import {Document,NodeIO} from '@gltf-transform/core'
import {EXTMeshoptCompression,KHRMeshQuantization} from '@gltf-transform/extensions'
import {weld,quantize,reorder} from '@gltf-transform/functions'
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer'
const [,,objPath,mtlPath,outPath]=process.argv
// materials
const mats={};let cur=null
for(const l of fs.readFileSync(mtlPath,'utf8').split(/\r?\n/)){
  const p=l.trim().split(/\s+/)
  if(p[0]==='newmtl'){cur=mats[p[1]]={}}
  else if(p[0]==='Kd'&&cur)cur.kd=p.slice(1,4).map(Number)
  else if(p[0]==='Ks'&&cur)cur.ks=p.slice(1,4).map(Number)
  else if(p[0]==='d'&&cur)cur.d=Number(p[1])
}
// obj
const V=[];const groups={};let g=null
for(const l of fs.readFileSync(objPath,'utf8').split('\n')){
  const c=l.charCodeAt(0)
  if(c===118&&l.charCodeAt(1)===32){const p=l.split(' ');V.push(+p[1],+p[2],+p[3])}
  else if(c===117){g=groups[l.slice(7).trim()]??=[]}
  else if(c===102){const p=l.trim().split(/\s+/).slice(1).map(s=>parseInt(s)-1)
    for(let i=1;i<p.length-1;i++)g.push(p[0],p[i],p[i+1])}
}
const doc=new Document();const buf=doc.createBuffer();const scene=doc.createScene()
const mk=n=>{const nd=doc.createNode(n);scene.addChild(nd);const m=doc.createMesh(n);nd.setMesh(m);return m}
const meshes={board:mk('board'),components:mk('components')}
const bnames=[]
// board is mm, Z-up -> Y-up, metres not needed; keep mm
let tris=0
for(const [name,idx] of Object.entries(groups)){
  if(!idx.length)continue
  let zlo=1e9,zhi=-1e9;for(const i of idx){const z=V[i*3+2];if(z<zlo)zlo=z;if(z>zhi)zhi=z}
  const isBoard=zlo>=-1.7&&zhi<=0.02&&zlo<=0&&!(zhi-zlo<1e-9&&zlo<-1.7)
  if(isBoard)bnames.push(name)
  const m=mats[name]??{kd:[.5,.5,.5],ks:[0,0,0],d:1}
  const pos=new Float32Array(idx.length*3)
  for(let i=0;i<idx.length;i++){const v=idx[i]*3;pos[i*3]=V[v];pos[i*3+1]=V[v+2];pos[i*3+2]=-V[v+1]}
  const shiny=Math.max(...m.ks)
  const mat=doc.createMaterial(name).setBaseColorFactor([...m.kd.map(x=>Math.pow(x,2.2)),m.d??1])
    .setMetallicFactor(shiny>.2&&m.kd[0]>m.kd[2]*1.5?.85:0).setRoughnessFactor(.45).setDoubleSided(true)
  if((m.d??1)<1)mat.setAlphaMode('BLEND')
  const acc=doc.createAccessor().setType('VEC3').setArray(pos).setBuffer(buf)
  ;(isBoard?meshes.board:meshes.components).addPrimitive(doc.createPrimitive().setAttribute('POSITION',acc).setMaterial(mat))
  tris+=idx.length/3
}
console.log('board materials',bnames.join(','));console.log('materials',Object.keys(groups).length,'tris',tris)
await MeshoptEncoder.ready
await doc.transform(weld({tolerance:1e-4}),quantize({quantizePosition:16}))
doc.createExtension(EXTMeshoptCompression).setRequired(true).setEncoderOptions({method:EXTMeshoptCompression.EncoderMethod.QUANTIZE})
const io=new NodeIO().registerExtensions([EXTMeshoptCompression,KHRMeshQuantization]).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder})
await io.write(outPath,doc)
console.log('written',fs.statSync(outPath).size)
