// Estúdio 3D da NOCTÉA (three.js r160). Exporta build(renderer) → {scene, cam, set(state)}.
import * as THREE from './lib/three.module.min.js';
import {RoomEnvironment} from './lib/RoomEnvironment.js';
const V2=(a,b)=>new THREE.Vector2(a,b);

function canvasTex(w,h,draw){const cv=document.createElement('canvas');cv.width=w;cv.height=h;draw(cv.getContext('2d'),w,h);const t=new THREE.CanvasTexture(cv);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t;}
function labelTex(name,sub,ml){return canvasTex(2048,1024,(g,w,h)=>{g.clearRect(0,0,w,h);const cx=w*.5;g.fillStyle='rgba(238,231,215,.95)';g.textAlign='center';g.textBaseline='middle';
  g.font='300 150px Corm';g.letterSpacing='46px';g.fillText(name,cx+23,h*.40);g.fillRect(cx-70,h*.53,140,3);
  g.font='400 46px Jost';g.letterSpacing='20px';g.fillText(sub,cx+10,h*.62);g.font='300 40px Jost';g.letterSpacing='14px';g.globalAlpha=.7;g.fillText(ml,cx+7,h*.74);
  g.globalAlpha=1;g.beginPath();const sx=cx,sy=h*.2,s=26;for(let i=0;i<8;i++){const r=i%2?s*.18:s,a=i*Math.PI/4-Math.PI/2;g.lineTo(sx+Math.cos(a)*r,sy+Math.sin(a)*r);}g.closePath();g.fill();});}

export function build(r){
  r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=1.05;r.outputColorSpace=THREE.SRGBColorSpace;r.shadowMap.enabled=false;
  const sc=new THREE.Scene();sc.background=new THREE.Color('#010604');
  const pm=new THREE.PMREMGenerator(r);sc.environment=pm.fromScene(new RoomEnvironment(),.035).texture;
  const cam=new THREE.PerspectiveCamera(28,1080/1920,.05,200);

  // ---- fundo: parede com luz esmeralda (softbox atrás) ----
  const bgMat=new THREE.ShaderMaterial({uniforms:{uC:{value:new THREE.Vector2(.5,.52)},uI:{value:1},uT:{value:0},uW:{value:.35}},depthWrite:false,
    vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:`varying vec2 vUv;uniform vec2 uC;uniform float uI,uT,uW;
      float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
      void main(){vec2 d=(vUv-uC)*vec2(1.,1.6);float r=length(d);
        vec3 base=vec3(.002,.01,.007);vec3 em=vec3(.02,.2,.12);vec3 hot=vec3(.25,.6,.42);
        float g=exp(-r*r/(uW*uW))*uI;float core=exp(-r*r/(uW*uW*.12))*uI*.6;
        float bands=.5+.5*sin(vUv.x*40.+uT*.6);float caust=pow(bands,8.)*.08*g;
        float beam=exp(-pow((vUv.x-vUv.y*.55-.18+sin(uT*.15)*.05)*9.,2.))*.05*uI;
        vec3 c=base+em*g+hot*core+vec3(.3,.8,.6)*caust+vec3(.5,.9,.7)*beam;c+= (h(vUv*900.+uT)-.5)*.012;
        gl_FragColor=vec4(c,1.);}`});
  const bg=new THREE.Mesh(new THREE.PlaneGeometry(60,60),bgMat);bg.position.set(0,6,-14);sc.add(bg);
  const bgM=new THREE.Mesh(new THREE.PlaneGeometry(60,60),bgMat);bgM.position.set(0,-6,-14);bgM.scale.y=-1;sc.add(bgM);

  // ---- piso espelhado (reflexo falso: produtos espelhados + piso semitransparente) ----
  const floorMat=new THREE.MeshPhysicalMaterial({color:'#010604',roughness:.3,metalness:.0,clearcoat:1,clearcoatRoughness:.1,transparent:true,opacity:.9});
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(80,80),floorMat);floor.rotation.x=-Math.PI/2;floor.renderOrder=2;sc.add(floor);

  // ---- materiais ----
  const glass=new THREE.MeshPhysicalMaterial({color:'#4fbf8f',transmission:1,thickness:1.4,roughness:.04,ior:1.52,attenuationColor:new THREE.Color('#12704a'),attenuationDistance:3.2,clearcoat:1,clearcoatRoughness:.03,envMapIntensity:1.6,specularIntensity:1});
  const liquid=new THREE.MeshPhysicalMaterial({color:'#7fe0b3',transmission:.9,thickness:1.0,roughness:.1,ior:1.36,attenuationColor:new THREE.Color('#0a4a30'),attenuationDistance:1.2});
  const gold=new THREE.MeshStandardMaterial({color:'#e3cc95',metalness:1,roughness:.18,envMapIntensity:2.2});
  const rubber=new THREE.MeshPhysicalMaterial({color:'#060807',roughness:.55,clearcoat:.4,clearcoatRoughness:.5,envMapIntensity:1.2});
  const matte=new THREE.MeshPhysicalMaterial({color:'#050706',roughness:.42,clearcoat:.6,clearcoatRoughness:.3,envMapIntensity:1.3});
  const jarMat=new THREE.MeshPhysicalMaterial({color:'#0b3a27',roughness:.12,clearcoat:1,clearcoatRoughness:.04,envMapIntensity:1.6,sheen:.3,sheenColor:new THREE.Color('#3fa77a')});
  const swirl=canvasTex(1024,1024,(g,w,h)=>{g.fillStyle='#efeadc';g.fillRect(0,0,w,h);g.translate(w/2,h/2);
    for(let i=0;i<70;i++){const r0=10+i*7;g.strokeStyle=i%2?'rgba(255,255,255,.55)':'rgba(170,165,150,.35)';g.lineWidth=3+(i%3);g.beginPath();for(let a=0;a<Math.PI*2.02;a+=.05){const r=r0+Math.sin(a*3+i*.4)*6+a*9;g.lineTo(Math.cos(a+i*.15)*r,Math.sin(a+i*.15)*r);}g.stroke();}
    const rg=g.createRadialGradient(0,0,0,0,0,w*.5);rg.addColorStop(0,'rgba(255,255,255,.35)');rg.addColorStop(1,'rgba(0,0,0,.12)');g.fillStyle=rg;g.fillRect(-w/2,-h/2,w,h);});
  const cream=new THREE.MeshPhysicalMaterial({map:swirl,color:'#b9b3a4',roughness:.55,sheen:.4,sheenColor:new THREE.Color('#ffffff'),clearcoat:.25,clearcoatRoughness:.4,envMapIntensity:.6});

  // ---- sérum conta-gotas ----
  function serum(name,sub,ml,scale=1){const g=new THREE.Group();
    const prof=[V2(0,0),V2(.86,0),V2(.95,.05),V2(1,.16),V2(1,2.25),V2(.97,2.42),V2(.86,2.56),V2(.62,2.66),V2(.38,2.72),V2(.36,2.95),V2(0,2.95)];
    const body=new THREE.Mesh(new THREE.LatheGeometry(prof,128),glass);g.add(body);
    const lp=[V2(0,.12),V2(.88,.12),V2(.88,1.7),V2(0,1.7)];const liq=new THREE.Mesh(new THREE.LatheGeometry(lp,64),liquid);g.add(liq);
    const lab=new THREE.Mesh(new THREE.CylinderGeometry(1.006,1.006,1.25,128,1,true,-Math.PI*.42,Math.PI*.84),new THREE.MeshStandardMaterial({map:labelTex(name,sub,ml),transparent:true,roughness:.6,metalness:0,depthWrite:false}));
    lab.position.y=1.2;g.add(lab);
    // conta-gotas (grupo que pode subir)
    const dr=new THREE.Group();dr.name='dropper';
    const col=new THREE.Mesh(new THREE.LatheGeometry([V2(0,0),V2(.47,0),V2(.5,.04),V2(.5,.52),V2(.47,.56),V2(0,.56)],96),gold);col.position.y=2.86;dr.add(col);
    const ring=new THREE.Mesh(new THREE.TorusGeometry(.5,.025,16,96),gold);ring.rotation.x=Math.PI/2;ring.position.y=3.3;dr.add(ring);
    for(const yy of [2.98,3.04,3.1,3.16]){const gr=new THREE.Mesh(new THREE.TorusGeometry(.502,.006,8,96),new THREE.MeshStandardMaterial({color:'#6d5a32',metalness:1,roughness:.35}));gr.rotation.x=Math.PI/2;gr.position.y=yy;dr.add(gr);}
    const bulb=new THREE.Mesh(new THREE.LatheGeometry([V2(0,0),V2(.34,0),V2(.36,.15),V2(.33,.6),V2(.3,.95),V2(.2,1.12),V2(0,1.17)],96),rubber);bulb.position.y=3.42;dr.add(bulb);
    const tube=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,2.2,32,1,true),new THREE.MeshPhysicalMaterial({color:'#bfe9d4',transmission:1,thickness:.1,roughness:.02,ior:1.5}));tube.position.y=1.8;dr.add(tube);
    g.add(dr);g.scale.setScalar(scale);return g;}
  // ---- pote ----
  function jar(scale=1){const g=new THREE.Group();
    const body=new THREE.Mesh(new THREE.LatheGeometry([V2(0,0),V2(1.45,0),V2(1.55,.08),V2(1.6,.2),V2(1.6,1.15),V2(1.5,1.22),V2(0,1.22)],128),jarMat);g.add(body);
    const jl=new THREE.Mesh(new THREE.CylinderGeometry(1.605,1.605,.62,128,1,true,-Math.PI*.4,Math.PI*.8),new THREE.MeshStandardMaterial({map:labelTex('NOCTÉA','CRÈME ÉTOILE','50 ML'),transparent:true,roughness:.6,depthWrite:false}));jl.position.y=.6;g.add(jl);
    const cr=new THREE.Mesh(new THREE.CylinderGeometry(1.4,1.4,.1,96),cream);cr.position.y=1.2;g.add(cr);
    const lid=new THREE.Group();lid.name='lid';
    const l1=new THREE.Mesh(new THREE.LatheGeometry([V2(0,0),V2(1.62,0),V2(1.64,.06),V2(1.64,.72),V2(1.58,.8),V2(0,.8)],128),matte);lid.add(l1);
    const lr=new THREE.Mesh(new THREE.CylinderGeometry(1.645,1.645,.09,128,1,true),gold);lr.position.y=.06;lid.add(lr);
    lid.position.y=1.22;g.add(lid);g.scale.setScalar(scale);return g;}
  // ---- frasco alto (essência) ----
  function tall(scale=1){const g=new THREE.Group();
    const body=new THREE.Mesh(new THREE.LatheGeometry([V2(0,0),V2(.62,0),V2(.66,.08),V2(.66,3.2),V2(.5,3.42),V2(.26,3.5),V2(.25,3.7),V2(0,3.7)],96),glass);g.add(body);
    const cap=new THREE.Mesh(new THREE.CylinderGeometry(.34,.34,1.05,64),matte);cap.position.y=4.2;g.add(cap);
    const cr=new THREE.Mesh(new THREE.CylinderGeometry(.345,.345,.06,64,1,true),gold);cr.position.y=3.72;g.add(cr);
    const lab=new THREE.Mesh(new THREE.CylinderGeometry(.665,.665,1.4,96,1,true,-Math.PI*.45,Math.PI*.9),new THREE.MeshStandardMaterial({map:labelTex('NOCTÉA','ESSÊNCIA','100 ML'),transparent:true,roughness:.6,depthWrite:false}));lab.position.y=1.7;g.add(lab);
    g.scale.setScalar(scale);return g;}
  // ---- pódios ----
  function podium(rad,h){const m=new THREE.Mesh(new THREE.CylinderGeometry(rad,rad,h,128),new THREE.MeshPhysicalMaterial({color:'#03120b',roughness:.18,clearcoat:1,clearcoatRoughness:.06,envMapIntensity:1.4}));m.position.y=h/2;
    const e=new THREE.Mesh(new THREE.TorusGeometry(rad,.012,8,160),gold);e.rotation.x=Math.PI/2;e.position.y=h;const g=new THREE.Group();g.add(m,e);return g;}

  const radTex=(c0,c1)=>canvasTex(256,256,(g,w,h)=>{const r=g.createRadialGradient(w/2,h/2,0,w/2,h/2,w/2);r.addColorStop(0,c0);r.addColorStop(1,c1);g.fillStyle=r;g.fillRect(0,0,w,h);});
  const shTex=radTex('rgba(0,0,0,.95)','rgba(0,0,0,0)'),poolTex=radTex('rgba(120,255,190,.9)','rgba(40,160,110,0)');
  function grounded(obj,rad,pool=true){const g=new THREE.Group();g.add(obj);
    const sh=new THREE.Mesh(new THREE.PlaneGeometry(rad*2.6,rad*2.6),new THREE.MeshBasicMaterial({map:shTex,transparent:true,depthWrite:false}));sh.rotation.x=-Math.PI/2;sh.position.y=.004;sh.renderOrder=3;g.add(sh);
    if(pool){const pl=new THREE.Mesh(new THREE.PlaneGeometry(rad*2.2,rad*4.2),new THREE.MeshBasicMaterial({map:poolTex,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,opacity:.28,toneMapped:false}));pl.rotation.x=-Math.PI/2;pl.position.set(0,.006,rad*1.7);pl.renderOrder=4;g.add(pl);}
    return g;}
  const S=serum('NOCTÉA','SÉRUM NOTURNO','30 ML'),J=jar(),E=tall(),P1=podium(1.7,.5),P2=podium(1.25,1.1),P3=podium(1.35,.25);
  const hero=new THREE.Group();hero.add(grounded(S,1.0));sc.add(hero);
  const line=new THREE.Group();line.add(P1,P2,P3);sc.add(line);
  const J2=jar(.62),E2=tall(.62),S2=serum('NOCTÉA','SÉRUM NOTURNO','30 ML',.78);line.add(J2,E2,S2);[[J2,1.0],[E2,.45],[S2,.8]].forEach(([o,r])=>{const sh=new THREE.Mesh(new THREE.PlaneGeometry(r*2.6,r*2.6),new THREE.MeshBasicMaterial({map:shTex,transparent:true,depthWrite:false}));sh.rotation.x=-Math.PI/2;sh.renderOrder=3;sh.position.copy(o.position);sh.position.y+=.004;line.add(sh);});
  P1.position.set(0,0,0);S2.position.set(0,.5,0);P2.position.set(-2.4,0,-.8);E2.position.set(-2.4,1.1,-.8);P3.position.set(2.35,0,-.5);J2.position.set(2.35,.25,-.5);
  const jarG=new THREE.Group();jarG.add(grounded(J,1.6));sc.add(jarG);
  // reflexos: cópias espelhadas
  function mirror(src){const m=src.clone(true);m.scale.y*=-1;sc.add(m);return m;}
  const heroM=mirror(hero),lineM=mirror(line),jarM=mirror(jarG);
  // ---- luzes ----
  const key=new THREE.SpotLight('#fff6e6',90,0,.42,.7,1.4);key.position.set(5,8,6);sc.add(key);sc.add(key.target);
  const rimL=new THREE.SpotLight('#8ff0c4',140,0,.5,.6,1.2);rimL.position.set(-6,5,-5);sc.add(rimL);sc.add(rimL.target);
  const rimR=new THREE.SpotLight('#d9fbe9',80,0,.5,.6,1.2);rimR.position.set(6,3,-6);sc.add(rimR);sc.add(rimR.target);
  const fill=new THREE.HemisphereLight('#1b4d38','#000000',.6);sc.add(fill);
  // gota
  const drop=new THREE.Mesh(new THREE.SphereGeometry(.12,48,32),new THREE.MeshPhysicalMaterial({color:'#ffffff',transmission:.92,thickness:.35,roughness:0,ior:1.33,clearcoat:1,envMapIntensity:4,specularIntensity:1}));drop.scale.set(.7,.95,.7);sc.add(drop);
  const ripple=new THREE.Mesh(new THREE.RingGeometry(.96,1,128),new THREE.MeshBasicMaterial({color:'#cfeedd',transparent:true,opacity:0,side:THREE.DoubleSide}));ripple.rotation.x=-Math.PI/2;ripple.position.y=.005;sc.add(ripple);

  // texto atrás do produto (plano com textura de canvas, desenhado por quadro)
  const backCv=document.createElement('canvas');backCv.width=2048;backCv.height=1024;const backTex=new THREE.CanvasTexture(backCv);backTex.colorSpace=THREE.SRGBColorSpace;
  const back=new THREE.Mesh(new THREE.PlaneGeometry(16,8),new THREE.MeshBasicMaterial({map:backTex,transparent:true,depthWrite:false,toneMapped:false}));back.position.set(0,2.4,-3.2);sc.add(back);
  const groups={hero,line,jarG};const mir={hero:heroM,line:lineM,jarG:jarM};
  function syncMirror(){for(const k in groups){const a=groups[k],m=mir[k];m.visible=a.visible;m.position.set(a.position.x,-a.position.y,a.position.z);m.rotation.set(-a.rotation.x,a.rotation.y,-a.rotation.z);
      m.traverse(o=>{});const srcDr=a.getObjectByName('dropper'),dstDr=m.getObjectByName('dropper');if(srcDr&&dstDr)dstDr.position.copy(srcDr.position);
      const sl=a.getObjectByName('lid'),dl=m.getObjectByName('lid');if(sl&&dl){dl.position.copy(sl.position);dl.rotation.copy(sl.rotation);}}}
  // estado por quadro
  function set(st){
    hero.visible=!!st.hero;line.visible=!!st.line;jarG.visible=!!st.jar;
    if(st.hero){hero.position.set(...(st.hero.pos||[0,0,0]));hero.rotation.set(st.hero.rx||0,st.hero.ry||0,st.hero.rz||0);S.getObjectByName('dropper').position.y=st.hero.dropper||0;}
    if(st.line){line.rotation.y=st.line.ry||0;}
    if(st.jar){jarG.position.set(...(st.jar.pos||[0,0,0]));jarG.rotation.set(0,st.jar.ry||0,0);const l=J.getObjectByName('lid');l.position.y=1.22+(st.jar.lid||0);l.rotation.z=(st.jar.lidr||0);}
    drop.visible=!!st.drop;if(st.drop){drop.position.set(...st.drop);}
    ripple.material.opacity=st.ripple?st.ripple[1]:0;if(st.ripple){ripple.scale.setScalar(st.ripple[0]);ripple.position.x=st.ripple[2]||0;ripple.position.z=st.ripple[3]||0;}
    cam.fov=st.fov||28;cam.position.set(...st.cam);cam.lookAt(new THREE.Vector3(...st.look));if(st.roll)cam.rotateZ(st.roll);cam.updateProjectionMatrix();
    bgMat.uniforms.uI.value=st.bgI??1;bgMat.uniforms.uT.value=st.t||0;bgMat.uniforms.uW.value=st.bgW??.35;if(st.bgC)bgMat.uniforms.uC.value.set(...st.bgC);
    key.intensity=st.key??90;rimL.intensity=st.rim??140;rimR.intensity=(st.rim??140)*.6;key.target.position.set(...st.look);rimL.target.position.set(...st.look);rimR.target.position.set(...st.look);
    back.visible=!!st.back;if(st.back){back.position.set(...(st.back.pos||[0,2.4,-3.2]));back.scale.setScalar(st.back.s||1);}
    floor.visible=st.floor!==false;syncMirror();
  }
  return {scene:sc,cam,set,backCv,backTex};
}
