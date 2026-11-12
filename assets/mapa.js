/* Mapas de itinerarios — proyección Robinson (ESRI:54030), sin dependencias externas.
   Uso: GT.mapa(elemento, {casos:['soane'], itinerario: elementoLista, mini:false}) */
(function(){
'use strict';
const T=[[1,0],[.9986,.062],[.9954,.124],[.99,.186],[.9822,.248],[.973,.31],[.96,.372],[.9427,.434],[.9216,.4958],[.8962,.5571],[.8679,.6176],[.835,.6769],[.7986,.7346],[.7597,.7903],[.7186,.8435],[.6732,.8936],[.6213,.9394],[.5722,.9761],[.5322,1]];
function rob(lon,lat){
  const a=Math.min(Math.abs(lat),90)/5,i=Math.min(Math.floor(a),17),f=a-i;
  const X=T[i][0]+(T[i+1][0]-T[i][0])*f, Y=T[i][1]+(T[i+1][1]-T[i][1])*f;
  return [0.8487*X*lon*Math.PI/180*100, -1.3523*Y*(lat<0?-1:1)*100];
}
const cache={};
function json(u){return cache[u]||(cache[u]=fetch(u).then(r=>{if(!r.ok)throw new Error(u);return r.json()}))}
const BASE=(document.querySelector('meta[name=gt-base]')||{}).content||'';
const NS='http://www.w3.org/2000/svg';
function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
const EN=document.documentElement.lang==='en';
function tx(es,en){return EN?en:es}
// Nombres de lugar en inglés (solo los que cambian)
const LUG={'Atenas':'Athens','Belgrado':'Belgrade','Benarés':'Varanasi','Bolonia':'Bologna','Bolonia - Ferrara':'Bologna - Ferrara','Bolonia - Florencia':'Bologna - Florence','Bolonia - Parma - Milán':'Bologna - Parma - Milan','Brescia - Verona - Mantua- Vicenza':'Brescia - Verona - Mantua - Vicenza','Bucarest':'Bucharest','Burdeos':'Bordeaux','Bayona':'Bayonne','Cantón (Guangzhou)':'Canton (Guangzhou)','Chengdú':'Chengdu','Ciudad del Cabo':'Cape Town','Copenhague':'Copenhagen','Costa de Marfil':'Ivory Coast','Cádiz':'Cadiz','Delfos':'Delphi','Desierto de Gobi':'Gobi Desert','Dresde':'Dresden','Estambul':'Istanbul','Florencia':'Florence','Génova':'Genoa','Islas Salónicas':'Thessaloniki (islands)','Lagunas Pontinas (Desaparecidas)':'Pontine Marshes (drained)','Lucerna':'Lucerne','Marsella':'Marseille','Milán':'Milan','Monte Athos':'Mount Athos','Monte Song':'Mount Song','Moscú':'Moscow','Najodka':'Nakhodka','Nankín':'Nanjing','Nápoles':'Naples','Padua':'Padua','París':'Paris','Pekín':'Beijing','Perpiñán':'Perpignan','Pompeya':'Pompeii','Praga':'Prague','Roma':'Rome','Salónica':'Thessaloniki','San Petersburgo':'St Petersburg','Sevilla':'Seville','Sicilia':'Sicily','Sidney':'Sydney','Sídney':'Sydney','Singapur':'Singapore','Tarascón':'Tarascon','Travesía':'Crossing','Venecia':'Venice','Viena':'Vienna','Vladivostok (Transiberiano)':'Vladivostok (Trans-Siberian)','Salerno - Paestum':'Salerno - Paestum','Danubio':'Danube','Yangtsé':'Yangtze','Transiberiano':'Trans-Siberian'};
function nombre(n){if(!EN)return n;if(LUG[n])return LUG[n];let m=/^Viaje de (.*)$/.exec(n);if(m)return m[1].replace('Ganier','Garnier')+'’s journey';m=/^Vida de (.*)$/.exec(n);if(m)return 'Life of '+m[1];return n}
const MES=EN?['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']:['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
function fecha(s){if(!s)return '';const m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(s);if(!m)return s;return (+m[3])+' '+MES[+m[2]-1]+' '+m[1]}
function rango(p){if(!p.ini&&!p.fin)return '';if(p.ini&&p.fin&&p.ini!==p.fin)return fecha(p.ini)+' – '+fecha(p.fin);return fecha(p.ini||p.fin)}
function pathFrom(rings){let d='';for(const r of rings){let first=true,prev=null;for(const [lo,la] of r){const [x,y]=rob(lo,la);if(prev&&Math.abs(lo-prev)>180){first=true}d+=(first?'M':'L')+x.toFixed(1)+' '+y.toFixed(1);first=false;prev=lo}}return d}

GT_mapa.fechaRango=rango;
function GT_mapa(cont,opt){
  opt=opt||{};
  return Promise.all([json(BASE+'data/mundo.json'),json(BASE+'data/viajes.json')]).then(([mundo,viajes])=>{
    const casos=viajes.filter(v=>!opt.casos||opt.casos.includes(v.id));
    cont.innerHTML='';cont.classList.add('mapa');
    const svg=el('svg',{role:'img','aria-label':tx('Mapa de itinerario','Itinerary map')},cont);
    const gT=el('g',{},svg), gR=el('g',{},svg), gP=el('g',{},svg);
    let d='';for(const r of mundo)d+=pathFrom([r]);
    el('path',{d,class:'tierra'},gT);
    // límites
    let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
    const capas={};
    for(const v of casos){
      const g=el('g',{'data-caso':v.id},gR);const gp=el('g',{'data-caso':v.id},gP);capas[v.id]=[g,gp];
      for(const x of (v.extras||[])){ // ríos y ferrocarriles de referencia (SIG del TFG)
        const pd=pathFrom(x.lineas);
        if(x.tipo==='rio')el('path',{d:pd,class:'rio'},g);
        else{el('path',{d:pd,class:'tren',stroke:v.color},g);el('path',{d:pd,class:'tren-int'},g)}
      }
      for(const ln of v.ruta){const pd=pathFrom([ln]);el('path',{d:pd,class:'ruta',stroke:v.color},g)}
      for(const p of v.puntos){const [x,y]=rob(p.c[0],p.c[1]);x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y)}
    }
    if(opt.vista){const a=rob(opt.vista[0],opt.vista[1]),b=rob(opt.vista[2],opt.vista[3]);x0=a[0];y0=a[1];x1=b[0];y1=b[1]}
    const W=x1-x0,H=y1-y0,pad=Math.max(W,H)*(opt.mini?.1:.07)+1;
    let vb=[x0-pad,y0-pad,W+2*pad,H+2*pad];
    const ar=cont.clientWidth/(cont.clientHeight||1)||1.6;
    if(vb[2]/vb[3]<ar){const nw=vb[3]*ar;vb[0]-=(nw-vb[2])/2;vb[2]=nw}else{const nh=vb[2]/ar;vb[1]-=(nh-vb[3])/2;vb[3]=nh}
    const vb0=vb.slice();
    const tip=document.createElement('div');tip.className='tip';cont.appendChild(tip);
    const pts=[];
    function escala(){return vb[2]/(cont.clientWidth||800)}
    function dibujaPuntos(){
      gP.innerHTML='';pts.length=0;
      const s=escala();
      const vistos={};
      for(const v of casos){
        const gp=el('g',{'data-caso':v.id},gP);capas[v.id][1]=gp;if(capas[v.id].oculto)gp.style.display='none';
        if(!opt.mini)for(const x of (v.extras||[])){
          let L=x.lineas.reduce((a,b)=>b.length>a.length?b:a,[]);if(!L.length)continue;
          const q=L[Math.floor(L.length*(x.tipo==='rio'?.42:.5))],[ex,ey]=rob(q[0],q[1]);
          const t=el('text',{x:ex,y:ey-6*s,'font-size':11*s,'stroke-width':3*s,class:'etq-'+x.tipo,'text-anchor':'middle'},gp);t.textContent=nombre(x.nombre);
        }
        v.puntos.forEach((p,i)=>{
          const [x,y]=rob(p.c[0],p.c[1]);
          const g=el('g',{class:'pt',transform:`translate(${x},${y})`},gp);
          el('circle',{r:(opt.mini?2.6:4.2)*s,fill:v.color},g);
          const k=v.id+'|'+p.lugar;
          if(!opt.mini&&!vistos[k]){vistos[k]=1;const t=el('text',{x:6*s,y:3.6*s,'font-size':10.5*s,'stroke-width':3*s},g);t.textContent=nombre(p.lugar)}
          g.addEventListener('mouseenter',()=>muestra(v,p,x,y));g.addEventListener('mouseleave',()=>tip.classList.remove('ver'));
          g.addEventListener('click',()=>{selecciona(v.id,i,false);muestra(v,p,x,y)});
          pts.push({v,i,g,x,y});
        });
      }
    }
    function aplica(){svg.setAttribute('viewBox',vb.join(' '));dibujaPuntos()}
    function muestra(v,p,x,y){
      const r=svg.getBoundingClientRect(),cr=cont.getBoundingClientRect();
      const px=(x-vb[0])/vb[2]*r.width+(r.left-cr.left),py=(y-vb[1])/vb[3]*r.height+(r.top-cr.top);
      tip.innerHTML='<b>'+p.n+'. '+nombre(p.lugar)+'</b>'+(rango(p)||'<i>'+tx('sin fecha documentada','no documented date')+'</i>')+(casos.length>1?'<br><span style="opacity:.7">'+v.nombre+'</span>':'');
      tip.style.left=px+'px';tip.style.top=py+'px';tip.classList.add('ver');
    }
    function selecciona(id,i,centrar){
      pts.forEach(o=>o.g.classList.toggle('sel',o.v.id===id&&o.i===i));
      if(opt.itinerario){opt.itinerario.querySelectorAll('li').forEach((li,k)=>li.classList.toggle('sel',k===i));
        const li=opt.itinerario.querySelectorAll('li')[i];if(li&&!centrar)li.scrollIntoView({block:'nearest',behavior:'smooth'})}
      if(centrar){const o=pts.find(o=>o.v.id===id&&o.i===i);if(o){muestra(o.v,o.v.puntos[i],o.x,o.y)}}
    }
    // zoom y desplazamiento
    function zoom(f,cx,cy){
      if(cx===undefined){cx=vb[0]+vb[2]/2;cy=vb[1]+vb[3]/2}
      const nw=vb[2]*f;if(nw<8||nw>4200)return;
      vb=[cx-(cx-vb[0])*f,cy-(cy-vb[1])*f,nw,vb[3]*f];aplica();
    }
    if(!opt.mini){
      svg.addEventListener('wheel',e=>{e.preventDefault();const r=svg.getBoundingClientRect();
        const cx=vb[0]+(e.clientX-r.left)/r.width*vb[2],cy=vb[1]+(e.clientY-r.top)/r.height*vb[3];zoom(e.deltaY>0?1.15:1/1.15,cx,cy);tip.classList.remove('ver')},{passive:false});
      let arr=null;const toques=new Map();let dist0=0;
      svg.addEventListener('pointerdown',e=>{toques.set(e.pointerId,e);if(toques.size===1)arr={x:e.clientX,y:e.clientY,vb:vb.slice()};else if(toques.size===2){const [a,b]=[...toques.values()];dist0=Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);arr=null}});
      window.addEventListener('pointermove',e=>{if(!toques.has(e.pointerId))return;toques.set(e.pointerId,e);const r=svg.getBoundingClientRect();
        if(toques.size===2){const [a,b]=[...toques.values()];const d2=Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);if(dist0){zoom(dist0/d2);dist0=d2}return}
        if(!arr)return;const dx=(e.clientX-arr.x)/r.width*arr.vb[2],dy=(e.clientY-arr.y)/r.height*arr.vb[3];
        if(Math.abs(e.clientX-arr.x)+Math.abs(e.clientY-arr.y)>3){vb=[arr.vb[0]-dx,arr.vb[1]-dy,arr.vb[2],arr.vb[3]];svg.setAttribute('viewBox',vb.join(' '));tip.classList.remove('ver')}});
      window.addEventListener('pointerup',e=>{toques.delete(e.pointerId);if(toques.size===0&&arr){arr=null;aplica()}});
      const c=document.createElement('div');c.className='ctrl';
      c.innerHTML='<button type="button" aria-label="'+tx('Acercar','Zoom in')+'">+</button><button type="button" aria-label="'+tx('Alejar','Zoom out')+'">−</button><button type="button" aria-label="'+tx('Encuadre inicial','Reset view')+'" style="font-size:12px">⤢</button>';
      const [bm,bn,br]=c.querySelectorAll('button');bm.onclick=()=>zoom(1/1.4);bn.onclick=()=>zoom(1.4);br.onclick=()=>{vb=vb0.slice();aplica()};
      cont.appendChild(c);
      const n=document.createElement('div');n.className='nota';n.textContent=tx('Proyección Robinson · Elaboración propia a partir del SIG del TFG','Robinson projection · Author’s own work from the thesis GIS');cont.appendChild(n);
    }
    aplica();
    // itinerario
    if(opt.itinerario&&casos.length===1){
      const v=casos[0];const ol=document.createElement('ol');
      v.puntos.forEach((p,i)=>{const li=document.createElement('li');const r=rango(p);
        li.innerHTML='<span class="num">'+p.n+'</span><span><span class="lug">'+nombre(p.lugar)+'</span><br><span class="fe'+(r?'':' sin')+'">'+(r||tx('sin fecha documentada','no documented date'))+'</span>'+(p.doc?' · <a href="'+p.doc+'" target="_blank" rel="noopener">'+tx('documento','document')+' ↗</a>':'')+'</span>';
        li.addEventListener('click',e=>{if(e.target.tagName==='A')return;selecciona(v.id,i,true)});ol.appendChild(li)});
      opt.itinerario.appendChild(ol);
    }
    return {
      mostrar(id,on){const c=capas[id];if(!c)return;c.oculto=!on;c[0].style.display=on?'':'none';if(c[1])c[1].style.display=on?'':'none'}
    };
  }).catch(err=>{cont.innerHTML='<p style="padding:20px;font-size:13px">'+tx('No se pudo cargar el mapa','The map could not be loaded')+' ('+err.message+').</p>'});
}
window.GT=window.GT||{};window.GT.mapa=GT_mapa;window.GT.json=json;window.GT.base=BASE;window.GT.nombre=nombre;window.GT.tx=tx;window.GT.EN=EN;
})();
