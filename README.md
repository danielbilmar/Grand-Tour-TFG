# Grand Tour. El viaje como herramienta en la formación del arquitecto

Web del Trabajo Fin de Grado de **Daniel Bilbao Marcos** (Grado en Fundamentos de la Arquitectura, ETSA Universidad de Sevilla, 2026).

Publicada con GitHub Pages: https://danielbilmar.github.io/Grand-Tour-TFG/

## Qué contiene

| Página | Contenido |
|---|---|
| `index.html` | Portada, resumen / abstract y acceso a los cinco casos |
| `introduccion.html` | Introducción, objetivos y metodología |
| `marco-teorico.html` | Marco teórico |
| `clasificacion.html` | Propuesta de clasificación de los viajes y tabla resumen |
| `casos-de-estudio.html` | Elección de casos y reconstrucción en el SIG |
| `soane.html`, `garnier.html`, `le-corbusier.html`, `utzon.html`, `ando.html` | Cada caso: mapa interactivo, itinerario, eje cronológico, texto y figuras |
| `mapa.html` | Las cinco rutas superpuestas |
| `ejes.html` | Ejes cronológicos interactivos (solo lectura). `ejes.html?v=0` … `?v=5` abre un viaje concreto |
| `conclusiones.html` | Conclusiones, limitaciones y futuras líneas |
| `fuentes.html`, `ilustraciones.html` | Bibliografía y procedencia de las ilustraciones |

## Cómo está hecho

Web estática sin dependencias (HTML, CSS y JavaScript). Las páginas se generan con un script de Python a partir de los textos de `fuente/`:

```
python3 fuente/build.py
```

- `fuente/capitulos/` — texto de cada capítulo (desde los .docx finales). Los marcadores `<!--FIG:F02-19-->` indican dónde va cada figura.
- `fuente/textos/` — resumen, objetivos y conclusiones (versión maquetada final).
- `fuente/registro.json` — registro de figuras: pie, referencia Chicago, licencia e imagen.
- `data/viajes.json` — puntos y rutas exportados del SIG (QGIS, `261104_QGIS Grand Tour Final.gpkg`).
- `data/ejes.json` — bloques de los ejes cronológicos.
- `data/mundo.json` — cartografía base (Natural Earth, simplificada).
- `assets/` — estilos, mapas (proyección Robinson) y ejes.

Para cambiar un texto, edita el archivo de `fuente/` y vuelve a ejecutar `build.py`.

## Imágenes

En la web solo se reproducen las imágenes de elaboración propia, de dominio público o con licencia libre. Las demás figuras del TFG aparecen como ficha con su pie y un enlace a la fuente original.
