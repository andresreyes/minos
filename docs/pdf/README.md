# Documentos en PDF

Dos documentos, mismo estilo, público distinto.

| Archivo | Público | Contenido |
|---|---|---|
| `Framework-SDLC-Agentico-Guia.pdf` | Quien implanta el framework en un equipo | 28 páginas, 11 diagramas: roles, gates, constitución, portabilidad, instalación, costo |
| `Fundamentos-Trabajar-con-Agentes.pdf` | Cualquiera que trabaje con agentes | 12 páginas, 4 diagramas: los tres niveles, árbol de decisión, matriz de auditoría, encadenamiento, caché y orden, técnicas contra la invención |

El de fundamentos **no depende del framework**: sirve solo. Es el que conviene
repartir primero.

## Regenerarlos

```bash
cd docs/pdf/img && for f in *.dot; do dot -Tpng -Gdpi=200 "$f" -o "${f%.dot}.png"; done
cd .. && python3 build.py && python3 build_foundations.py
```

Requiere `graphviz` y `reportlab`. Los estilos compartidos están en `estilo.py`, así
que un cambio de paleta o tipografía afecta a los dos a la vez. Los diagramas son
fuente Graphviz editable (`img/*.dot`), no imágenes opacas.
