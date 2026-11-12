/* Banner de entrada: parallax y luz que siguen al ratón; recuerda la visita en la sesión */
(function(){
'use strict';
const s=document.getElementById('intro');if(!s)return;
const reducido=matchMedia('(prefers-reduced-motion: reduce)').matches;
const destino=document.getElementById('inicio');
try{ if(sessionStorage.getItem('gt-intro')&&destino&&!location.hash){ window.scrollTo(0,destino.offsetTop-53); } }catch(e){}
function visto(){try{sessionStorage.setItem('gt-intro','1')}catch(e){}}
s.querySelector('.intro-entrar').addEventListener('click',e=>{e.preventDefault();visto();window.scrollTo({top:destino.offsetTop-53,behavior:reducido?'auto':'smooth'})});
window.addEventListener('scroll',()=>{if(window.scrollY>s.offsetHeight*.5)visto()},{passive:true});
if(reducido)return;
let raf=0,px=.5,py=.5;
s.addEventListener('pointermove',e=>{
  const r=s.getBoundingClientRect();px=(e.clientX-r.left)/r.width;py=(e.clientY-r.top)/r.height;
  if(!raf)raf=requestAnimationFrame(()=>{raf=0;
    s.style.setProperty('--mx',(px*100)+'%');s.style.setProperty('--my',(py*100)+'%');
    s.style.setProperty('--ix',((.5-px)*36)+'px');s.style.setProperty('--iy',((.5-py)*26)+'px');
    s.style.setProperty('--tx',((px-.5)*14)+'px');s.style.setProperty('--ty',((py-.5)*10)+'px');
  });
});
s.addEventListener('pointerleave',()=>{['--ix','--iy','--tx','--ty'].forEach(v=>s.style.setProperty(v,'0px'));s.style.setProperty('--mx','70%');s.style.setProperty('--my','45%')});
})();
