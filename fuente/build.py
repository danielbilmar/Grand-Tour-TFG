#!/usr/bin/env python3
"""Genera las páginas HTML del sitio, en español (raíz) y en inglés (/en), a partir de los textos de /fuente.

Uso (desde la raíz del repositorio):   python3 fuente/build.py

Español                      Inglés
- fuente/capitulos/*.html    fuente/en/capitulos/*.html   → texto de cada capítulo. <!--FIG:F02-19--> marca cada figura.
- fuente/textos/*.html       fuente/en/textos/*.html      → resumen, objetivos, conclusiones y agradecimientos.
- fuente/registro.json       → registro de figuras (pie / pie_en, ref / ref_en, licencia, imagen).
- data/viajes.json           → puntos y rutas del SIG (QGIS) por caso de estudio.
- data/ejes.json             → bloques de los ejes cronológicos.
"""
import json, re, html, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(R, 'fuente')
REG = {r['id']: r for r in json.load(open(os.path.join(F, 'registro.json'), encoding='utf-8'))}
VIAJES = {v['id']: v for v in json.load(open(os.path.join(R, 'data', 'viajes.json'), encoding='utf-8'))}
AUTOR = 'Daniel Bilbao Marcos'
TUTORA = 'Beatriz Zapico Blanco'
VISTAS = {'utzon':',vista:[96,46,124,20]'}  # encuadre inicial (lon O, lat N, lon E, lat S)
RETRATOS = {'F02-24','F09-02','F09-04'}  # se muestran en la cabecera del caso
# Figuras propias que en la web se sustituyen por el mapa y el eje interactivos de cada caso
INTERACTIVAS = {'F02-25','F02-26','F03-09','F03-11','F04-24','F04-28','F05-12','F05-13','F06-10','F06-11'}

L = 'es'   # idioma activo
def t(es, en): return en if L == 'en' else es
P = ''     # prefijo de rutas hacia la raíz ('' en español, '../' en inglés)
def leer(p): return open(os.path.join(F, ('en/' if L == 'en' else '') + p), encoding='utf-8').read()
def esc(s): return html.escape(s or '', quote=True)
def pie(r): return r['pie_en'] if L == 'en' else r['pie']
def ref(r): return (r.get('ref_en') if L == 'en' else r['ref']) or ''

TIPO_EN = {'clásico':'classical','romántico':'romantic','moderno':'modern','vernáculo':'vernacular','contemporáneo':'contemporary'}
def tipo(v): return TIPO_EN[v['tipo']] if L == 'en' else v['tipo']
def viaje_tipo(v): return t('Viaje '+v['tipo'], TIPO_EN[v['tipo']].capitalize()+' journey')

def casos():
    return [
 dict(id='soane', url='soane.html', nombre='John Soane', titulo=t('El viaje clásico','The classical journey'), destino=t('Italia y Malta','Italy and Malta'), anos='1778–1780', retrato='F02-24',
      datos=[(t('753 días','753 days'),t('duración','duration')),(t('24 años','24 years'),t('edad al partir','age on departure')),(t('Italia y Malta','Italy and Malta'),t('países','countries'))]),
 dict(id='garnier', url='garnier.html', nombre='Charles Garnier', titulo=t('El viaje romántico','The romantic journey'), destino=t('España','Spain'), anos='1868', retrato=None,
      datos=[(t('≈ 4 semanas','≈ 4 weeks'),t('duración','duration')),(t('42 años','42 years'),t('edad','age')),(t('España','Spain'),t('país','country'))]),
 dict(id='lecorbusier', url='le-corbusier.html', nombre='Le Corbusier', titulo=t('El viaje moderno','The modern journey'), destino=t('Viaje de Oriente','Journey to the East'), anos='1911', retrato=None,
      datos=[(t('≈ 6 meses','≈ 6 months'),t('duración','duration')),(t('23 años','23 years'),t('edad','age')),(t('Europa central, Balcanes, Turquía, Grecia, Italia','Central Europe, Balkans, Turkey, Greece, Italy'),t('recorrido','route'))]),
 dict(id='utzon', url='utzon.html', nombre='Jørn Utzon', titulo=t('El viaje vernáculo','The vernacular journey'), destino='China', anos='1958', retrato='F09-02',
      datos=[(t('≈ 10 semanas','≈ 10 weeks'),t('duración','duration')),(t('39 años','39 years'),t('edad','age')),('China',t('país','country'))]),
 dict(id='ando', url='ando.html', nombre='Tadao Ando', titulo=t('El viaje contemporáneo','The contemporary journey'), destino=t('Europa, África y Asia','Europe, Africa and Asia'), anos='1965', retrato='F09-04',
      datos=[(t('≈ 7 meses','≈ 7 months'),t('duración','duration')),(t('23 años','23 years'),t('edad','age')),(t('Vuelta al mundo','Round the world'),t('recorrido','route'))]),
    ]

def titulo_tfg(): return t('Grand Tour. El viaje como herramienta en la formación del arquitecto','Grand Tour. Travel as a tool in the education of the architect')

def nav_def():
    C=casos()
    return [
     ('index.html',t('Inicio','Home')),('introduccion.html',t('Introducción','Introduction')),('marco-teorico.html',t('Marco teórico','Framework')),('clasificacion.html',t('Clasificación','Classification')),
     ('casos-de-estudio.html',t('Casos de estudio','Case studies'),[('casos-de-estudio.html',t('Elección y reconstrucción','Choice and reconstruction'))]+[(c['url'],c['nombre']+' · '+c['anos']) for c in C]),
     ('mapa.html',t('Mapa comparado','Comparative map')),(P+'ejes.html' if L=='en' else 'ejes.html',t('Ejes cronológicos','Timelines')),('conclusiones.html',t('Conclusiones','Conclusions')),
     ('fuentes.html',t('Fuentes','Sources'),[('fuentes.html',t('Fuentes bibliográficas','Bibliography')),('ilustraciones.html',t('Procedencia de las ilustraciones','Illustration credits'))]),
    ]
def orden(): return ['index.html','introduccion.html','marco-teorico.html','clasificacion.html','casos-de-estudio.html']+[c['url'] for c in casos()]+['mapa.html','conclusiones.html','fuentes.html','ilustraciones.html']
def nombres():
    N={'index.html':t('Inicio','Home'),'introduccion.html':t('Introducción, objetivos y metodología','Introduction, objectives and methodology'),'marco-teorico.html':t('Marco teórico','Theoretical framework'),
       'clasificacion.html':t('Propuesta de clasificación','Proposed classification'),'casos-de-estudio.html':t('Casos de estudio','Case studies'),'mapa.html':t('Mapa comparado','Comparative map'),
       'conclusiones.html':t('Conclusiones','Conclusions'),'fuentes.html':t('Fuentes bibliográficas','Bibliography'),'ilustraciones.html':t('Procedencia de las ilustraciones','Illustration credits'),
       'ejes.html':t('Ejes cronológicos','Chronological axes (timelines)')}
    N.update({c['url']:c['nombre']+'. '+c['titulo'] for c in casos()})
    return N

def nav(actual):
    out=[]
    for it in nav_def():
        url,txt=it[0],it[1]; sub=it[2] if len(it)>2 else None
        act=' class="activo"' if url==actual or (sub and any(u==actual for u,_ in sub)) else ''
        if sub:
            li=''.join(f'<li><a href="{u}"{" class=activo" if u==actual else ""}>{esc(x)}</a></li>' for u,x in sub)
            out.append(f'<li><a href="{url}"{act}>{esc(txt)}</a><ul>{li}</ul></li>')
        else: out.append(f'<li><a href="{url}"{act}>{esc(txt)}</a></li>')
    otro = ('../'+nombre_actual) if L=='en' else ('en/'+nombre_actual)
    out.append(f'<li class="idioma"><a href="{otro}" hreflang="{t("en","es")}" lang="{t("en","es")}" title="{t("Read in English","Leer en español")}">{t("EN","ES")}</a></li>')
    return '<ul>'+''.join(out)+'</ul>'

nombre_actual='index.html'
def pagina(nombre, titulo, cuerpo, scripts='', desc=''):
    global nombre_actual; nombre_actual=nombre
    O=orden(); N=nombres()
    i=O.index(nombre) if nombre in O else -1
    ant=sig=''
    if i>0: ant=f'<a href="{O[i-1]}"><span>{t("← Anterior","← Previous")}</span>{esc(N[O[i-1]])}</a>'
    if 0<=i<len(O)-1: sig=f'<a class="sig" href="{O[i+1]}"><span>{t("Siguiente →","Next →")}</span>{esc(N[O[i+1]])}</a>'
    pie_nav=f'<div class="siguiente">{ant}{sig}</div>' if (ant or sig) else ''
    tt=(titulo+' · Grand Tour') if nombre!='index.html' else titulo_tfg()
    es_url=nombre; en_url='en/'+nombre
    base='https://danielbilmar.github.io/Grand-Tour-TFG/'
    d=desc or t('Trabajo Fin de Grado de '+AUTOR+' sobre los viajes iniciáticos de John Soane, Charles Garnier, Le Corbusier, Jørn Utzon y Tadao Ando.',
                'Undergraduate thesis by '+AUTOR+' on the initiatory journeys of John Soane, Charles Garnier, Le Corbusier, Jørn Utzon and Tadao Ando.')
    return f'''<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(tt)}</title>
<meta name="description" content="{esc(d)}">
<meta name="author" content="{AUTOR}">
<meta name="gt-base" content="{P}">
<link rel="alternate" hreflang="es" href="{base}{es_url}"><link rel="alternate" hreflang="en" href="{base}{en_url}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{P}assets/estilo.css">
</head>
<body>
<header class="barra"><div class="barra-in">
<a class="marca" href="index.html">Grand <span>Tour</span></a>
<button class="hamb" type="button" aria-expanded="false">{t("Menú","Menu")}</button>
<nav class="menu" aria-label="{t("Secciones","Sections")}">{nav(nombre)}</nav>
</div></header>
<main>
{cuerpo}
{pie_nav}
</main>
<footer class="pie-sitio"><div class="envoltura">
<div><strong>{esc(titulo_tfg())}</strong><br>{t("Trabajo Fin de Grado","Undergraduate thesis (TFG)")} · {AUTOR} · {t("Grado en Fundamentos de la Arquitectura","Degree in Fundamentals of Architecture")} · ETSA {t("Universidad de Sevilla","University of Seville")} · 2026<br>{t("Tutora","Supervisor")}: {TUTORA} · {t("Grupo G","Group G")} (TFG-G)</div>
<div>{t("Mapas, ejes y diagramas: elaboración propia. Las imágenes de terceros se reproducen solo cuando son de dominio público o tienen licencia libre; el resto se enlaza a su fuente",
        "Maps, timelines and diagrams: author’s own work. Third-party images are reproduced only when they are in the public domain or openly licensed; the rest are linked to their source")} (<a href="ilustraciones.html">{t("procedencia","credits")}</a>).{t("", " This English version is a translation of the original Spanish thesis.")}</div>
</div></footer>
<script src="{P}assets/sitio.js"></script>
{scripts}
</body>
</html>
'''

def figura(fid):
    r=REG.get(fid)
    if not r or fid in INTERACTIVAS or fid in RETRATOS: return ''
    num=f'Fig. {r["num"]}.'
    p=esc(pie(r))
    if r['pub']:
        lic=t('Dominio público','Public domain') if r['lic'] in ('Dominio público','Uso académico autorizado') else (t('Elaboración propia',"Author’s own work") if r['lic']=='Propia' else r['lic'])
        return (f'<figure class="fig" id="{fid}"><a class="ampliar" href="{P}{r["img"]}" data-pie="{esc(num+" "+pie(r))}" data-ref="{esc(ref(r))}" data-lic="{esc(lic)}">'
                f'<img src="{P}{r["img"]}" width="{r["w"]}" height="{r["h"]}" loading="lazy" alt="{p}"></a>'
                f'<figcaption><b>{num}</b> {p}</figcaption></figure>')
    enlace=f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">{t("Ver en la fuente ↗","View at source ↗")}</a>' if r.get('url') else ''
    return (f'<figure class="fig fig-ext" id="{fid}"><div class="ext"><span>{t("Imagen sujeta a derechos de autor:<br>no se reproduce en la versión web.","Image subject to copyright:<br>not reproduced in the web version.")}</span>{enlace}</div>'
            f'<figcaption><b>{num}</b> {p}</figcaption></figure>')

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
    s=re.sub(r'<colgroup>.*?</colgroup>','',s,flags=re.S)
    s=s.replace(' style="width:100%;"','')
    return con_figuras(s)

def ancha(s):
    return re.sub(r'(<table>.*?</table>)',r'</div><div class="tabla-ancha">\1</div><div class="texto">',s,flags=re.S)

def cab(etq,tit,ent=''):
    return f'<header class="cap-cabecera"><div class="etq">{etq}</div><h1>{tit}</h1>{f"<p class=ent>{ent}</p>" if ent else ""}</header>'

def escribir(nombre, contenido):
    d=os.path.join(R,'en') if L=='en' else R
    os.makedirs(d,exist_ok=True)
    open(os.path.join(d,nombre),'w',encoding='utf-8').write(contenido); print('·',('en/' if L=='en' else '')+nombre)

def tarjetas():
    out=''
    for c in casos():
        v=VIAJES[c['id']]
        out+=(f'<a class="caso-card" href="{c["url"]}" style="--c:{v["color"]}"><span class="tipo">{viaje_tipo(v)}</span>'
              f'<h3>{esc(c["nombre"])}</h3><span class="dest">{esc(c["destino"])} · {c["anos"]}</span><div class="mini" data-mini="{c["id"]}"></div></a>')
    return out
def js_minis(): return f'<script src="{P}assets/mapa.js"></script><script>document.querySelectorAll("[data-mini]").forEach(e=>GT.mapa(e,{{casos:[e.dataset.mini],mini:true}}))</script>'

# ---------- INICIO
def inicio():
    N=nombres()
    indice=''.join(f'<li><a href="{(P if u=="ejes.html" else "")+u}">{esc(N[u])}</a></li>' for u in orden()[1:5]+['mapa.html','ejes.html','conclusiones.html','fuentes.html','ilustraciones.html'])
    cuerpo=f'''
<section class="portada">
<div>
<h1>Grand Tour<small>{t("El viaje como herramienta en la formación del arquitecto","Travel as a tool in the education of the architect")}</small></h1>
<div class="meta"><strong>{AUTOR}</strong><br>{t("Tutora","Supervisor")}: <strong>{TUTORA}</strong><br>{t("Trabajo Fin de Grado · Grado en Fundamentos de la Arquitectura","Undergraduate thesis (Trabajo Fin de Grado) · Degree in Fundamentals of Architecture")}<br>{t("Escuela Técnica Superior de Arquitectura · Universidad de Sevilla · 2026","School of Architecture (ETSA) · University of Seville · 2026")}<br>{t("Trabajo tutorizado dentro del grupo G (TFG-G)","Supervised within Group G (TFG-G)")}</div>
</div>
<div>
<p class="dedicatoria">{t("Dedicado a","Dedicated to")}<br><span>Antonio Marcos Estrada</span></p>
<blockquote class="epigrafe">{t("«El que lee mucho y anda mucho, ve mucho y sabe mucho».","“He who reads much and walks much, sees much and knows much.”")}<cite>Miguel de Cervantes Saavedra, <em>Don Quijote de la Mancha</em>, {t("parte II, cap. XXV.","part II, ch. XXV.")}</cite></blockquote>
</div>
</section>
<div class="envoltura"><div class="figs" style="margin:10px 0 0">{figura("F01-02")}{figura("F01-03")}</div></div>
<div class="banda"><div class="resumenes">{leer("textos/resumen.html")}</div></div>
<section class="envoltura" style="margin-top:20px">
<h2 class="sec-tit">{t("Cinco viajes, cinco formas de viajar","Five journeys, five ways of travelling")}</h2>
<p class="sec-sub">{t("Cada caso de estudio representa uno de los tipos de viaje propuestos en el trabajo. Pulsa en un arquitecto para ver su itinerario, su eje cronológico y el análisis completo.","Each case study represents one of the types of journey proposed in the thesis. Click on an architect to see the itinerary, the chronological axis and the full analysis.")}</p>
<div class="casos-grid">{tarjetas()}</div>
</section>
<section class="envoltura" style="margin-top:56px">
<h2 class="sec-tit">{t("Contenido","Contents")}</h2>
<p class="sec-sub">{t("El texto íntegro del TFG, con los mapas y ejes cronológicos en versión interactiva.","The full text of the thesis, with interactive maps and chronological axes.")}</p>
<ol class="indice">{indice}</ol>
</section>'''
    escribir('index.html',pagina('index.html',titulo_tfg(),cuerpo,js_minis()))

# ---------- INTRODUCCIÓN
def introduccion():
    s=leer('capitulos/introduccion.html')
    partes=re.split(r'<h1[^>]*>.*?</h1>',s)   # [antes, introducción, objetivos, metodología]
    intro,met=partes[1],partes[3]
    fases=re.split(r'<p>((?:Fase|Phase) \d: [^<]*)</p>',met)
    html_f='<div class="fases">'
    for k in range(1,len(fases),2):
        tit=fases[k]; cuerpo=fases[k+1]
        cuerpo=re.sub(r'<p>(Resultado|Herramientas|Outcome|Tools):\s*',r'<p><span class="lbl">\1</span>',cuerpo)
        html_f+=f'<div class="fase"><h4>{esc(tit)}</h4>{cuerpo}</div>'
    html_f+='</div>'
    cuerpo=cab(t('Capítulo 1','Chapter 1'),t('Introducción','Introduction'))+f'<div class="texto">{ajustar(intro,quitar_h=False)}{leer("textos/objetivos.html")}<h2 id="metodologia">{t("Metodología","Methodology")}</h2>{html_f}</div>'
    escribir('introduccion.html',pagina('introduccion.html',t('Introducción','Introduction'),cuerpo))

def capitulo(nombre, fuente, etq, titulo, ent=''):
    s=ajustar(leer('capitulos/'+fuente))
    cuerpo=cab(etq,titulo,ent)+'<div class="texto">'+ancha(s)+'</div>'
    escribir(nombre,pagina(nombre,titulo,cuerpo))

# ---------- CASOS
def casos_indice():
    s=ajustar(leer('capitulos/casos.html'))
    cuerpo=(cab(t('Capítulo 4','Chapter 4'),t('Casos de estudio','Case studies'),t('Elección de los casos, organización de la información en el SIG y criterios de reconstrucción de los viajes.','Choice of cases, organisation of the information in the GIS and criteria for reconstructing the journeys.'))
            +f'<section class="envoltura" style="margin-bottom:10px"><div class="casos-grid">{tarjetas()}</div></section>'
            +'<div class="texto">'+ancha(s)+'</div>')
    escribir('casos-de-estudio.html',pagina('casos-de-estudio.html',t('Casos de estudio','Case studies'),cuerpo,js_minis()))

def caso(c, n):
    v=VIAJES[c['id']]
    s=leer('capitulos/'+c['id']+'.html')
    s=ajustar(s,nivel=-1)  # h3 → h2
    s=re.sub(r'<h2([^>]*)><em>(.*?)</em></h2>',r'<h2\1>\2</h2>',s)
    if c['retrato'] and REG[c['retrato']]['pub']:
        r=REG[c['retrato']]
        ret=f'<div><a class="ampliar" href="{P}{r["img"]}" data-pie="{esc("Fig. "+r["num"]+". "+pie(r))}" data-ref="{esc(ref(r))}"><img class="retrato" src="{P}{r["img"]}" alt="{esc(pie(r))}"></a><div class="retrato-pie">Fig. {r["num"]}. {esc(pie(r))}</div></div>'
    else:
        ini=''.join(w[0] for w in c['nombre'].replace('Le ','L').split()[:2])
        ret=f'<div class="retrato vacio" style="background:linear-gradient(160deg,{v["color"]}33,{v["color"]}99)">{ini}</div>'
    datos=''.join(f'<div><b>{esc(a)}</b>{esc(b)}</div>' for a,b in c['datos'])
    np=len(v['puntos'])
    cuerpo=f'''
<header class="caso-cab" style="--c:{v['color']}">
{ret}
<div><div class="etq">{t("Caso de estudio","Case study")} {n} · {viaje_tipo(v)}</div>
<h1>{esc(c['nombre'])}<em>{esc(c['titulo'])} · {esc(c['destino'])}, {c['anos']}</em></h1>
<div class="datos">{datos}<div><b>{np}</b>{t("estancias en el SIG","stays in the GIS")}</div></div></div>
</header>
<section class="mapa-bloque" style="--c:{v['color']}">
<div><div id="mapa" class="mapa"></div></div>
<div class="itin" id="itin" style="--c:{v['color']}"><h4>{t("Itinerario","Itinerary")} · {np} {t("estancias","stays")}</h4></div>
</section>
<section class="eje-bloque">
<p class="bloque-tit">{t("Eje cronológico del viaje","Chronological axis of the journey")}</p>
<div class="eje" id="eje"></div>
<div class="eje-pie"><span>{t("Pasa el ratón por un bloque para ver lugar, fechas y duración. Filas ordenadas por latitud (norte arriba), como en el eje original. Las travesías aparecen en gris.","Hover over a bar to see the place, dates and duration. Rows are ordered by latitude (north at the top), as in the original axis. Sea and rail crossings are shown in grey.")}</span><a href="{P}ejes.html?v={v['eje']}">{t("Abrir el eje interactivo completo →","Open the full interactive timeline (Spanish) →")}</a></div>
</section>
<div class="texto">{s}</div>'''
    js=(f'<script src="{P}assets/mapa.js"></script><script src="{P}assets/eje.js"></script>'
        f'<script>GT.mapa(document.getElementById("mapa"),{{casos:["{c["id"]}"],itinerario:document.getElementById("itin"){VISTAS.get(c["id"],"")}}});'
        f'GT.eje(document.getElementById("eje"),{v["eje"]},"{v["color"]}");</script>')
    d=t(f'Reconstrucción del viaje de {c["nombre"]} ({c["destino"]}, {c["anos"]}): mapa, eje cronológico y análisis.',f'Reconstruction of {c["nombre"]}’s journey ({c["destino"]}, {c["anos"]}): map, chronological axis and analysis.')
    escribir(c['url'],pagina(c['url'],c['nombre']+'. '+c['titulo'],cuerpo,js,desc=d))

def mapa():
    ley=''.join(f'<label style="--c:{v["color"]}"><input type="checkbox" checked data-c="{v["id"]}"><i></i>{esc(v["nombre"])} · {v["anos"]}</label>' for v in VIAJES.values())
    cuerpo=cab(t('SIG del TFG','Thesis GIS'),t('Mapa comparado','Comparative map'),t('Las cinco rutas superpuestas sobre una misma proyección. Activa o desactiva cada viaje, acerca con la rueda o los botones y pasa por los puntos para ver lugar y fechas.','The five routes overlaid on a single projection. Toggle each journey on or off, zoom with the scroll wheel or the buttons and hover over the points to see place and dates.'))
    cuerpo+=f'''<section class="envoltura"><div id="mapa" class="mapa" style="aspect-ratio:16/8.5"></div><div class="leyenda">{ley}</div>
<p style="font-size:13px;color:var(--gris);max-width:80ch;margin-top:18px">{t("Superponer los itinerarios permite ver los tramos que se repiten entre casos —como el recorrido por Italia de Soane y Le Corbusier o la presencia constante de Roma y Atenas— y la progresiva ampliación geográfica del viaje desde el <em>Grand Tour</em> clásico hasta la vuelta al mundo de Ando.","Overlaying the itineraries reveals the stretches repeated across cases —such as Soane’s and Le Corbusier’s routes through Italy, or the constant presence of Rome and Athens— and the progressive geographical expansion of the journey from the classical <em>Grand Tour</em> to Ando’s journey round the world.")}</p></section>'''
    js=(f'<script src="{P}assets/mapa.js"></script><script>GT.mapa(document.getElementById("mapa"),{{}}).then(m=>{{'
        'document.querySelectorAll(".leyenda input").forEach(i=>i.addEventListener("change",()=>m.mostrar(i.dataset.c,i.checked)))})</script>')
    escribir('mapa.html',pagina('mapa.html',t('Mapa comparado','Comparative map'),cuerpo,js))

def conclusiones():
    cuerpo=cab(t('Capítulo 5','Chapter 5'),t('Conclusiones','Conclusions'),t('Conclusiones, limitaciones, futuras líneas de investigación y agradecimientos.','Conclusions, limitations, future lines of research and acknowledgements.'))+'<div class="texto">'+leer('textos/conclusiones.html')+leer('textos/agradecimientos.html')+'</div>'
    escribir('conclusiones.html',pagina('conclusiones.html',t('Conclusiones','Conclusions'),cuerpo))

def fuentes():
    s=ajustar(leer('capitulos/fuentes.html'))
    cuerpo=cab(t('Bibliografía','Bibliography'),t('Fuentes bibliográficas','Bibliography'))+'<div class="texto biblio">'+s+'</div>'
    escribir('fuentes.html',pagina('fuentes.html',t('Fuentes bibliográficas','Bibliography'),cuerpo))

LIC_EN={'Dominio público':'Public domain','Propia':'Author’s own work','Uso académico autorizado':'Authorised academic use','Derecho de cita':'Right of quotation','Pendiente de verificar':'To be verified','CC BY-SA':'CC BY-SA'}
def ilustraciones():
    li=''
    for r in REG.values():
        ok=r['pub']
        if ok: mini=f'<a class="ampliar" href="{P}{r["img"]}" data-pie="{esc("Fig. "+r["num"]+". "+pie(r))}" data-ref="{esc(ref(r))}"><img class="mini" src="{P}{r["img"]}" loading="lazy" alt=""></a>'
        elif r['id'] in INTERACTIVAS: mini=f'<div class="mini no">{t("Versión interactiva en la web","Interactive version on this site")}</div>'
        else: mini=f'<div class="mini no">{t("No reproducida","Not reproduced")}</div>'
        rf=esc(ref(r) or ('Fig. '+r['num']+'. '+pie(r)))
        rf=re.sub(r'(https?://[^\s<]+)',lambda m:f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>',rf)
        lic=r['lic'] or 'Sin verificar'
        if L=='en': lic=LIC_EN.get(lic,lic)
        li+=f'<li id="ref-{r["id"]}">{mini}<div>{rf} <span class="lic{" ok" if ok else ""}">{esc(lic)}</span></div></li>'
    aviso=t('<div class="aviso">El TFG impreso reproduce estas imágenes al amparo del derecho de cita con fines académicos. En esta versión web, de acceso público, solo se muestran las imágenes de elaboración propia, las de dominio público y las que tienen licencia libre; las demás aparecen como ficha con enlace a la fuente original.</div>',
            '<div class="aviso">The printed thesis reproduces these images under the right of quotation for academic purposes. In this publicly accessible web version, only the author’s own images, public-domain images and openly licensed images are shown; the rest appear as a card linking to the original source.</div>')
    cuerpo=cab(t('Anexo','Appendix'),t('Procedencia de las ilustraciones','Illustration credits'))+f'<div class="texto">{aviso}<ul class="ilus">{li}</ul></div>'
    escribir('ilustraciones.html',pagina('ilustraciones.html',t('Procedencia de las ilustraciones','Illustration credits'),cuerpo))

def construir():
    inicio(); introduccion()
    capitulo('marco-teorico.html','marco.html',t('Capítulo 2','Chapter 2'),t('Marco teórico','Theoretical framework'),t('Estado de la cuestión, concepto de Grand Tour, aprendizaje experiencial y definición de viaje iniciático.','State of the art, the concept of the Grand Tour, experiential learning and the definition of the initiatory journey.'))
    capitulo('clasificacion.html','clasificacion.html',t('Capítulo 3','Chapter 3'),t('Propuesta de clasificación','Proposed classification'),t('Cinco tipos de viaje arquitectónico: clásico, romántico, moderno, vernáculo y contemporáneo.','Five types of architectural journey: classical, romantic, modern, vernacular and contemporary.'))
    casos_indice()
    for n,c in enumerate(casos(),1): caso(c,n)
    mapa(); conclusiones(); fuentes(); ilustraciones()

if __name__=='__main__':
    L,P='es',''; construir()
    L,P='en','../'; construir()
