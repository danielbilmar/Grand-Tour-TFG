#!/usr/bin/env python3
"""Genera las páginas HTML del sitio a partir de los textos de /fuente.

Uso (desde la raíz del repositorio):   python3 fuente/build.py

- fuente/capitulos/*.html  → texto de cada capítulo (procede de los .docx finales del TFG).
                              Los marcadores <!--FIG:F02-19--> indican dónde va cada figura.
- fuente/textos/*.html     → resumen, objetivos y conclusiones (texto de la versión maquetada).
- fuente/registro.json     → registro de figuras (pie, referencia, licencia, imagen).
- data/viajes.json         → puntos y rutas del SIG (QGIS) por caso de estudio.
- data/ejes.json           → bloques de los ejes cronológicos.
"""
import json, re, html, os, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(R, 'fuente')
def leer(p): return open(os.path.join(F, p), encoding='utf-8').read()
REG = {r['id']: r for r in json.load(open(os.path.join(F, 'registro.json'), encoding='utf-8'))}
VIAJES = {v['id']: v for v in json.load(open(os.path.join(R, 'data', 'viajes.json'), encoding='utf-8'))}
TITULO = 'Grand Tour. El viaje como herramienta en la formación del arquitecto'
AUTOR = 'Daniel Bilbao Marcos'
# Figuras propias que en la web se sustituyen por el mapa y el eje interactivos de cada caso
VISTAS = {'utzon':',vista:[96,46,124,20]'}  # encuadre inicial (lon O, lat N, lon E, lat S)
RETRATOS = {'F02-24','F09-02','F09-04'}  # se muestran en la cabecera del caso
INTERACTIVAS = {'F02-25','F02-26','F03-09','F03-11','F04-24','F04-28','F05-12','F05-13','F06-10','F06-11'}
CASOS = [
 dict(id='soane', url='soane.html', nombre='John Soane', titulo='El viaje clásico', destino='Italia y Malta', anos='1778–1780', retrato='F02-24',
      datos=[('753 días','duración'),('24 años','edad al partir'),('Italia y Malta','países')], vida='1753–1837'),
 dict(id='garnier', url='garnier.html', nombre='Charles Garnier', titulo='El viaje romántico', destino='España', anos='1868', retrato=None,
      datos=[('≈ 4 semanas','duración'),('42 años','edad'),('España','país')], vida='1825–1898'),
 dict(id='lecorbusier', url='le-corbusier.html', nombre='Le Corbusier', titulo='El viaje moderno', destino='Viaje de Oriente', anos='1911', retrato=None,
      datos=[('≈ 6 meses','duración'),('23 años','edad'),('Europa central, Balcanes, Turquía, Grecia, Italia','recorrido')], vida='1887–1965'),
 dict(id='utzon', url='utzon.html', nombre='Jørn Utzon', titulo='El viaje vernáculo', destino='China', anos='1958', retrato='F09-02',
      datos=[('≈ 10 semanas','duración'),('39 años','edad'),('China','país')], vida='1918–2008'),
 dict(id='ando', url='ando.html', nombre='Tadao Ando', titulo='El viaje contemporáneo', destino='Europa, África y Asia', anos='1965', retrato='F09-04',
      datos=[('≈ 7 meses','duración'),('23 años','edad'),('Vuelta al mundo','recorrido')], vida='1941'),
]
NAV = [
 ('index.html','Inicio'),('introduccion.html','Introducción'),('marco-teorico.html','Marco teórico'),('clasificacion.html','Clasificación'),
 ('casos-de-estudio.html','Casos de estudio',[('casos-de-estudio.html','Elección y reconstrucción')]+[(c['url'],c['nombre']+' · '+c['anos']) for c in CASOS]),
 ('mapa.html','Mapa comparado'),('ejes.html','Ejes cronológicos'),('conclusiones.html','Conclusiones'),
 ('fuentes.html','Fuentes',[('fuentes.html','Fuentes bibliográficas'),('ilustraciones.html','Procedencia de las ilustraciones')]),
]
ORDEN = ['index.html','introduccion.html','marco-teorico.html','clasificacion.html','casos-de-estudio.html']+[c['url'] for c in CASOS]+['mapa.html','conclusiones.html','fuentes.html','ilustraciones.html']
NOMBRES = {'index.html':'Inicio','introduccion.html':'Introducción, objetivos y metodología','marco-teorico.html':'Marco teórico','clasificacion.html':'Propuesta de clasificación','casos-de-estudio.html':'Casos de estudio','mapa.html':'Mapa comparado','conclusiones.html':'Conclusiones','fuentes.html':'Fuentes bibliográficas','ilustraciones.html':'Procedencia de las ilustraciones'}
NOMBRES['ejes.html']='Ejes cronológicos'
NOMBRES.update({c['url']:c['nombre']+'. '+c['titulo'] for c in CASOS})

def esc(s): return html.escape(s or '', quote=True)

def nav(actual):
    out=[]
    for it in NAV:
        url,txt=it[0],it[1]; sub=it[2] if len(it)>2 else None
        act=' class="activo"' if url==actual or (sub and any(u==actual for u,_ in sub)) else ''
        if sub:
            li=''.join(f'<li><a href="{u}"{" class=activo" if u==actual else ""}>{esc(t)}</a></li>' for u,t in sub)
            out.append(f'<li><a href="{url}"{act}>{esc(txt)}</a><ul>{li}</ul></li>')
        else: out.append(f'<li><a href="{url}"{act}>{esc(txt)}</a></li>')
    return '<ul>'+''.join(out)+'</ul>'

def pagina(nombre, titulo, cuerpo, scripts='', desc=''):
    i=ORDEN.index(nombre) if nombre in ORDEN else -1
    ant=sig=''
    if i>0: ant=f'<a href="{ORDEN[i-1]}"><span>← Anterior</span>{esc(NOMBRES[ORDEN[i-1]])}</a>'
    if 0<=i<len(ORDEN)-1: sig=f'<a class="sig" href="{ORDEN[i+1]}"><span>Siguiente →</span>{esc(NOMBRES[ORDEN[i+1]])}</a>'
    pie_nav=f'<div class="siguiente">{ant}{sig}</div>' if (ant or sig) else ''
    t=(titulo+' · Grand Tour') if nombre!='index.html' else TITULO
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc or 'Trabajo Fin de Grado de '+AUTOR+' sobre los viajes iniciáticos de John Soane, Charles Garnier, Le Corbusier, Jørn Utzon y Tadao Ando.')}">
<meta name="author" content="{AUTOR}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/estilo.css">
</head>
<body>
<header class="barra"><div class="barra-in">
<a class="marca" href="index.html">Grand <span>Tour</span></a>
<button class="hamb" type="button" aria-expanded="false">Menú</button>
<nav class="menu" aria-label="Secciones">{nav(nombre)}</nav>
</div></header>
<main>
{cuerpo}
{pie_nav}
</main>
<footer class="pie-sitio"><div class="envoltura">
<div><strong>{esc(TITULO)}</strong><br>Trabajo Fin de Grado · {AUTOR} · Grado en Fundamentos de la Arquitectura · ETSA Universidad de Sevilla · 2026</div>
<div>Mapas, ejes y diagramas: elaboración propia. Las imágenes de terceros se reproducen solo cuando son de dominio público o tienen licencia libre; el resto se enlaza a su fuente (<a href="ilustraciones.html">procedencia</a>).</div>
</div></footer>
<script src="assets/sitio.js"></script>
{scripts}
</body>
</html>
'''

def figura(fid):
    r=REG.get(fid)
    if not r or fid in INTERACTIVAS or fid in RETRATOS: return ''
    num=f'Fig. {r["num"]}.'
    pie=esc(r['pie'])
    if r['pub']:
        lic='Dominio público' if r['lic'] in ('Dominio público','Uso académico autorizado') else r['lic']
        return (f'<figure class="fig" id="{fid}"><a class="ampliar" href="{r["img"]}" data-pie="{esc(num+" "+r["pie"])}" data-ref="{esc(r["ref"])}" data-lic="{esc(lic)}">'
                f'<img src="{r["img"]}" width="{r["w"]}" height="{r["h"]}" loading="lazy" alt="{pie}"></a>'
                f'<figcaption><b>{num}</b> {pie}</figcaption></figure>')
    enlace=f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">Ver en la fuente ↗</a>' if r.get('url') else ''
    return (f'<figure class="fig fig-ext" id="{fid}"><div class="ext"><span>Imagen sujeta a derechos de autor:<br>no se reproduce en la versión web.</span>{enlace}</div>'
            f'<figcaption><b>{num}</b> {pie}</figcaption></figure>')

def con_figuras(s):
    def grupo(m):
        ids=re.findall(r'<!--FIG:(F\d\d-\d\d)-->',m.group(0))
        figs=[figura(i) for i in ids]; figs=[f for f in figs if f]
        if not figs: return ''
        return f'<div class="figs{" uno" if len(figs)==1 else ""}">'+''.join(figs)+'</div>'
    return re.sub(r'(?:\s*<!--FIG:F\d\d-\d\d-->)+',grupo,s)

def ajustar(s, quitar_h=True, nivel=0):
    """Limpia el HTML de pandoc: quita el título del capítulo y ajusta niveles."""
    if quitar_h: s=re.sub(r'^\s*<h[12][^>]*>.*?</h[12]>','',s,count=1,flags=re.S)
    if nivel:
        s=re.sub(r'<(/?)h([1-6])\b',lambda m:f'<{m.group(1)}h{max(1,min(int(m.group(2))+nivel,6))}',s)
    s=re.sub(r'<table>',r'<table>',s)
    s=re.sub(r'<colgroup>.*?</colgroup>','',s,flags=re.S)
    s=s.replace(' style="width:100%;"','')
    return con_figuras(s)

def ancha(s):
    return re.sub(r'(<table>.*?</table>)',r'</div><div class="tabla-ancha">\1</div><div class="texto">',s,flags=re.S)

def cab(etq,tit,ent=''):
    return f'<header class="cap-cabecera"><div class="etq">{etq}</div><h1>{tit}</h1>{f"<p class=ent>{ent}</p>" if ent else ""}</header>'

def escribir(nombre, contenido):
    open(os.path.join(R,nombre),'w',encoding='utf-8').write(contenido); print('·',nombre)

# ---------- INICIO
def inicio():
    tarjetas=''
    for c in CASOS:
        v=VIAJES[c['id']]
        tarjetas+=(f'<a class="caso-card" href="{c["url"]}" style="--c:{v["color"]}"><span class="tipo">Viaje {v["tipo"]}</span>'
                   f'<h3>{esc(c["nombre"])}</h3><span class="dest">{esc(c["destino"])} · {c["anos"]}</span><div class="mini" data-mini="{c["id"]}"></div></a>')
    indice=''.join(f'<li><a href="{u}">{esc(NOMBRES[u])}</a></li>' for u in ORDEN[1:5]+['mapa.html','ejes.html','conclusiones.html','fuentes.html','ilustraciones.html'] if u in NOMBRES or u=='ejes.html')
    indice=indice.replace('<a href="ejes.html"></a>','<a href="ejes.html">Ejes cronológicos</a>')
    f1,f2=REG['F01-02'],REG['F01-03']
    cuerpo=f'''
<section class="portada">
<div>
<h1>Grand Tour<small>El viaje como herramienta en la formación del arquitecto</small></h1>
<div class="meta"><strong>{AUTOR}</strong><br>Trabajo Fin de Grado · Grado en Fundamentos de la Arquitectura<br>Escuela Técnica Superior de Arquitectura · Universidad de Sevilla · 2026</div>
</div>
<div>
<blockquote class="epigrafe">«El que lee mucho y anda mucho, ve mucho y sabe mucho».<cite>Miguel de Cervantes Saavedra, <em>Don Quijote de la Mancha</em>, parte II, cap. XXV.</cite></blockquote>
</div>
</section>
<div class="envoltura"><div class="figs" style="margin:10px 0 0">{figura("F01-02")}{figura("F01-03")}</div></div>
<div class="banda"><div class="resumenes">{leer("textos/resumen.html")}</div></div>
<section class="envoltura" style="margin-top:20px">
<h2 class="sec-tit">Cinco viajes, cinco formas de viajar</h2>
<p class="sec-sub">Cada caso de estudio representa uno de los tipos de viaje propuestos en el trabajo. Pulsa en un arquitecto para ver su itinerario, su eje cronológico y el análisis completo.</p>
<div class="casos-grid">{tarjetas}</div>
</section>
<section class="envoltura" style="margin-top:56px">
<h2 class="sec-tit">Contenido</h2>
<p class="sec-sub">El texto íntegro del TFG, con los mapas y ejes cronológicos en versión interactiva.</p>
<ol class="indice">{indice}</ol>
</section>'''
    js='<script src="assets/mapa.js"></script><script>document.querySelectorAll("[data-mini]").forEach(e=>GT.mapa(e,{casos:[e.dataset.mini],mini:true}))</script>'
    escribir('index.html',pagina('index.html',TITULO,cuerpo,js))

# ---------- INTRODUCCIÓN
def introduccion():
    s=leer('capitulos/introduccion.html')
    intro=s.split('<h1 id="objetivos">')[0]
    met=s.split('<h1 id="metodología">')[1].split('</h1>',1)[1]
    # fases de la metodología
    fases=re.split(r'<p>(Fase \d: [^<]*)</p>',met)
    html_f='<div class="fases">'
    for k in range(1,len(fases),2):
        tit=fases[k]; cuerpo=fases[k+1]
        cuerpo=re.sub(r'<p>(Resultado|Herramientas):\s*',r'<p><span class="lbl">\1</span>',cuerpo)
        html_f+=f'<div class="fase"><h4>{esc(tit)}</h4>{cuerpo}</div>'
    html_f+='</div>'
    txt=ajustar(intro)
    cuerpo=cab('Capítulo 1','Introducción')+f'<div class="texto">{txt}{leer("textos/objetivos.html")}<h2 id="metodologia">Metodología</h2>{html_f}</div>'
    escribir('introduccion.html',pagina('introduccion.html','Introducción',cuerpo))

def capitulo(nombre, fuente, etq, titulo, ent=''):
    s=ajustar(leer('capitulos/'+fuente))
    cuerpo=cab(etq,titulo,ent)+'<div class="texto">'+ancha(s)+'</div>'
    escribir(nombre,pagina(nombre,titulo,cuerpo))

# ---------- CASOS
def casos_indice():
    s=ajustar(leer('capitulos/casos.html'))
    tarjetas=''
    for c in CASOS:
        v=VIAJES[c['id']]
        tarjetas+=(f'<a class="caso-card" href="{c["url"]}" style="--c:{v["color"]}"><span class="tipo">Viaje {v["tipo"]}</span>'
                   f'<h3>{esc(c["nombre"])}</h3><span class="dest">{esc(c["destino"])} · {c["anos"]}</span><div class="mini" data-mini="{c["id"]}"></div></a>')
    cuerpo=(cab('Capítulo 4','Casos de estudio','Elección de los casos, organización de la información en el SIG y criterios de reconstrucción de los viajes.')
            +f'<section class="envoltura" style="margin-bottom:10px"><div class="casos-grid">{tarjetas}</div></section>'
            +'<div class="texto">'+ancha(s)+'</div>')
    js='<script src="assets/mapa.js"></script><script>document.querySelectorAll("[data-mini]").forEach(e=>GT.mapa(e,{casos:[e.dataset.mini],mini:true}))</script>'
    escribir('casos-de-estudio.html',pagina('casos-de-estudio.html','Casos de estudio',cuerpo,js))

def caso(c, n):
    v=VIAJES[c['id']]
    s=leer('capitulos/'+c['id']+'.html')
    s=ajustar(s,nivel=-1)  # h3 → h2
    s=re.sub(r'<h2([^>]*)><em>(.*?)</em></h2>',r'<h2\1>\2</h2>',s)
    if c['retrato'] and REG[c['retrato']]['pub']:
        r=REG[c['retrato']]
        ret=f'<div><a class="ampliar" href="{r["img"]}" data-pie="{esc("Fig. "+r["num"]+". "+r["pie"])}" data-ref="{esc(r["ref"])}"><img class="retrato" src="{r["img"]}" alt="{esc(r["pie"])}"></a><div class="retrato-pie">Fig. {r["num"]}. {esc(r["pie"])}</div></div>'
    else:
        ini=''.join(w[0] for w in c['nombre'].replace('Le ','L').split()[:2])
        ret=f'<div class="retrato vacio" style="background:linear-gradient(160deg,{v["color"]}33,{v["color"]}99)">{ini}</div>'
    datos=''.join(f'<div><b>{esc(a)}</b>{esc(b)}</div>' for a,b in c['datos'])
    cuerpo=f'''
<header class="caso-cab" style="--c:{v['color']}">
{ret}
<div><div class="etq">Caso de estudio {n} · Viaje {v['tipo']}</div>
<h1>{esc(c['nombre'])}<em>{esc(c['titulo'])} · {esc(c['destino'])}, {c['anos']}</em></h1>
<div class="datos">{datos}<div><b>{len(v['puntos'])}</b>estancias en el SIG</div></div></div>
</header>
<section class="mapa-bloque" style="--c:{v['color']}">
<div><div id="mapa" class="mapa"></div></div>
<div class="itin" id="itin" style="--c:{v['color']}"><h4>Itinerario · {len(v['puntos'])} estancias</h4></div>
</section>
<section class="eje-bloque">
<p class="bloque-tit">Eje cronológico del viaje</p>
<div class="eje" id="eje"></div>
<div class="eje-pie"><span>Pasa el ratón por un bloque para ver lugar, fechas y duración. Filas ordenadas por latitud (norte arriba), como en el eje original. Las travesías aparecen en gris.</span><a href="ejes.html?v={v['eje']}">Abrir el eje interactivo completo →</a></div>
</section>
<div class="texto">{s}</div>'''
    js=(f'<script src="assets/mapa.js"></script><script src="assets/eje.js"></script>'
        f'<script>GT.mapa(document.getElementById("mapa"),{{casos:["{c["id"]}"],itinerario:document.getElementById("itin"){VISTAS.get(c["id"],"")}}});'
        f'GT.eje(document.getElementById("eje"),{v["eje"]},"{v["color"]}");</script>')
    escribir(c['url'],pagina(c['url'],c['nombre']+'. '+c['titulo'],cuerpo,js,desc=f'Reconstrucción del viaje de {c["nombre"]} ({c["destino"]}, {c["anos"]}): mapa, eje cronológico y análisis.'))

def mapa():
    ley=''.join(f'<label style="--c:{v["color"]}"><input type="checkbox" checked data-c="{v["id"]}"><i></i>{esc(v["nombre"])} · {v["anos"]}</label>' for v in VIAJES.values())
    cuerpo=cab('SIG del TFG','Mapa comparado','Las cinco rutas superpuestas sobre una misma proyección. Activa o desactiva cada viaje, acerca con la rueda o los botones y pasa por los puntos para ver lugar y fechas.')
    cuerpo+=f'''<section class="envoltura"><div id="mapa" class="mapa" style="aspect-ratio:16/8.5"></div><div class="leyenda">{ley}</div>
<p style="font-size:13px;color:var(--gris);max-width:80ch;margin-top:18px">Superponer los itinerarios permite ver los tramos que se repiten entre casos —como el recorrido por Italia de Soane y Le Corbusier o la presencia constante de Roma y Atenas— y la progresiva ampliación geográfica del viaje desde el <em>Grand Tour</em> clásico hasta la vuelta al mundo de Ando.</p></section>'''
    js=('<script src="assets/mapa.js"></script><script>GT.mapa(document.getElementById("mapa"),{}).then(m=>{'
        'document.querySelectorAll(".leyenda input").forEach(i=>i.addEventListener("change",()=>m.mostrar(i.dataset.c,i.checked)))})</script>')
    escribir('mapa.html',pagina('mapa.html','Mapa comparado',cuerpo,js))

def conclusiones():
    cuerpo=cab('Capítulo 5','Conclusiones','Conclusiones, limitaciones y futuras líneas de investigación.')+'<div class="texto">'+leer('textos/conclusiones.html')+'</div>'
    escribir('conclusiones.html',pagina('conclusiones.html','Conclusiones',cuerpo))

def fuentes():
    s=ajustar(leer('capitulos/fuentes.html'))
    cuerpo=cab('Bibliografía','Fuentes bibliográficas')+'<div class="texto biblio">'+s+'</div>'
    escribir('fuentes.html',pagina('fuentes.html','Fuentes bibliográficas',cuerpo))

def ilustraciones():
    li=''
    for r in REG.values():
        ok=r['pub']
        if ok: mini=f'<a class="ampliar" href="{r["img"]}" data-pie="{esc("Fig. "+r["num"]+". "+r["pie"])}" data-ref="{esc(r["ref"])}"><img class="mini" src="{r["img"]}" loading="lazy" alt=""></a>'
        elif r['id'] in INTERACTIVAS: mini='<div class="mini no">Versión interactiva en la web</div>'
        else: mini='<div class="mini no">No reproducida</div>'
        ref=esc(r['ref'] or ('Fig. '+r['num']+'. '+r['pie']))
        ref=re.sub(r'(https?://[^\s<]+)',lambda m:f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>',ref)
        lic=r['lic'] or 'Sin verificar'
        li+=f'<li id="ref-{r["id"]}">{mini}<div>{ref} <span class="lic{" ok" if ok else ""}">{esc(lic)}</span></div></li>'
    aviso=('<div class="aviso">El TFG impreso reproduce estas imágenes al amparo del derecho de cita con fines académicos. En esta versión web, '
           'de acceso público, solo se muestran las imágenes de elaboración propia, las de dominio público y las que tienen licencia libre; '
           'las demás aparecen como ficha con enlace a la fuente original.</div>')
    cuerpo=cab('Anexo','Procedencia de las ilustraciones')+f'<div class="texto">{aviso}<ul class="ilus">{li}</ul></div>'
    escribir('ilustraciones.html',pagina('ilustraciones.html','Procedencia de las ilustraciones',cuerpo))

if __name__=='__main__':
    inicio(); introduccion()
    capitulo('marco-teorico.html','marco.html','Capítulo 2','Marco teórico','Estado de la cuestión, concepto de Grand Tour, aprendizaje experiencial y definición de viaje iniciático.')
    capitulo('clasificacion.html','clasificacion.html','Capítulo 3','Propuesta de clasificación','Cinco tipos de viaje arquitectónico: clásico, romántico, moderno, vernáculo y contemporáneo.')
    casos_indice()
    for n,c in enumerate(CASOS,1): caso(c,n)
    mapa(); conclusiones(); fuentes(); ilustraciones()
