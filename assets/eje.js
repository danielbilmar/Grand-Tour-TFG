/* Ejes cronológico-geográficos (solo lectura), generados a partir de los datos del eje interactivo.
   Uso: GT.eje(elemento, indiceDelViaje, colorDelCaso) */
(function(){
'use strict';
const NS='http://www.w3.org/2000/svg';
function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
const EN=document.documentElement.lang==='en';
const MES=EN?['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']:['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
function parse(s){const m=/^(\d{1,2})\/(\d{1,2})\/(-?\d{1,4})$/.exec(s||'');if(!m)return null;const d=new Date(0);d.setUTCFullYear(+m[3],+m[2]-1,+m[1]);d.setUTCHours(0,0,0,0);return d.getTime()}
function fmt(t){const d=new Date(t);return d.getUTCDate()+' '+MES[d.getUTCMonth()]+' '+d.getUTCFullYear()}
const DIA=864e5;
function GT_eje(cont,idx,color){
  return GT.json(GT.base+'data/ejes.json').then(ejes=>{
    const e=ejes[idx];if(!e){cont.textContent=EN?'Timeline not available':'Eje no disponible';return}
    const bl=e.bloques.map(b=>({...b,s:parse(b.a),e:parse(b.b)})).filter(b=>b.s!=null&&b.e!=null);
    // Orden de filas: el del eje original (por latitud, norte arriba); los nombres no incluidos van al final
    const filas=(e.filas||[]).slice();for(const b of bl){if(!filas.includes(b.n))filas.push(b.n)}
    let t0=Math.min(...bl.map(b=>b.s)),t1=Math.max(...bl.map(b=>b.e))+DIA;
    const span=(t1-t0)/DIA, largo=span>3650;
    const lab=150, alto=filas.length>14?17:22, top=26;
    const ancho=Math.max(cont.clientWidth-24,720);
    const px=Math.max((ancho-lab)/span, largo?0:0);
    const W=lab+span*px+10,H=top+filas.length*alto+8;
    cont.innerHTML='';
    const svg=el('svg',{width:W,height:H,viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':(EN?'Timeline: ':'Eje cronológico: ')+e.nombre},cont);
    filas.forEach((f,i)=>{if(i%2===0)el('rect',{x:0,y:top+i*alto,width:W,height:alto,fill:'#f6f4ef'},svg);const fn=GT.nombre(f);const t=el('text',{x:4,y:top+i*alto+alto/2+3.5},svg);t.textContent=fn.length>24?fn.slice(0,23)+'…':fn;const ti=el('title',{},t);ti.textContent=fn});
    // marcas temporales
    const d0=new Date(t0);
    if(largo){
      const y0=d0.getUTCFullYear(),y1=new Date(t1).getUTCFullYear();const paso=y1-y0>200?25:10;
      for(let y=Math.ceil(y0/paso)*paso;y<=y1;y+=paso){const d=new Date(0);d.setUTCFullYear(y,0,1);const x=lab+(d.getTime()-t0)/DIA*px;
        el('line',{x1:x,x2:x,y1:top-4,y2:H,stroke:'#e4e0d8'},svg);const t=el('text',{x:x+3,y:14,class:'ano'},svg);t.textContent=y}
    }else{
      const d=new Date(Date.UTC(d0.getUTCFullYear(),d0.getUTCMonth(),1));
      if(d.getTime()<t0)d.setUTCMonth(d.getUTCMonth()+1);
      const meses=span/30, salto=meses>18?3:1;
      while(d.getTime()<=t1){const x=lab+(d.getTime()-t0)/DIA*px;const ene=d.getUTCMonth()===0;
        if(d.getUTCMonth()%salto===0||ene){el('line',{x1:x,x2:x,y1:top-4,y2:H,stroke:ene?'#b9b2a6':'#ece8e1'},svg);
          const t=el('text',{x:x+3,y:14,class:ene?'ano':'mes'},svg);t.textContent=ene?d.getUTCFullYear():MES[d.getUTCMonth()]}
        d.setUTCMonth(d.getUTCMonth()+1)}
    }
    for(const b of bl){
      const i=filas.indexOf(b.n),x=lab+(b.s-t0)/DIA*px,w=Math.max((b.e-b.s+DIA)/DIA*px,3);
      const trav=/traves|tren|barco|viaje en/i.test(b.n);
      const r=el('rect',{class:'b',x,y:top+i*alto+4,width:w,height:alto-8,rx:1.5,fill:trav?'#9c968c':(idx===5?(b.c||color):color),opacity:trav?.7:1},svg);
      const ti=el('title',{},r);const dias=Math.round((b.e-b.s)/DIA)+1;
      ti.textContent=GT.nombre(b.n)+' · '+fmt(b.s)+' → '+fmt(b.e)+(largo?'':' ('+dias+(EN?' day':' día')+(dias>1?'s':'')+')')+(b.nota?' · '+b.nota:'');
    }
  });
}
window.GT=window.GT||{};window.GT.eje=GT_eje;
})();
