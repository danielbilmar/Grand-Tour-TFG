/* Menú móvil y visor de figuras */
(function(){
'use strict';
const b=document.querySelector('.hamb'),m=document.querySelector('nav.menu');
if(b&&m)b.addEventListener('click',()=>{const a=m.classList.toggle('abierto');b.setAttribute('aria-expanded',a)});
const v=document.createElement('div');v.className='visor';v.setAttribute('role','dialog');v.setAttribute('aria-modal','true');
v.innerHTML='<button type="button">Cerrar ✕</button><img alt=""><div class="pie"></div>';
document.body.appendChild(v);
const img=v.querySelector('img'),pie=v.querySelector('.pie');
function cerrar(){v.classList.remove('ver');img.src=''}
v.addEventListener('click',e=>{if(e.target!==img)cerrar()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')cerrar()});
document.addEventListener('click',e=>{
  const a=e.target.closest('a.ampliar');if(!a)return;e.preventDefault();
  img.src=a.getAttribute('href');img.alt=a.dataset.pie||'';
  pie.innerHTML=(a.dataset.ref||a.dataset.pie||'')+(a.dataset.lic?'<br><span class="lic">'+a.dataset.lic+'</span>':'');
  v.classList.add('ver');
});
})();
