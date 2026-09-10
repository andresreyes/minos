# Ingeniería de contexto

Ver también `CONTEXT.md` en el catálogo de skills, que es la guía de autoría.
Este documento cubre la parte del framework.

## Las tres zonas

```
ZONA 1 · ANCLA     constitución · gates · prompt del rol · SKILL.md
ZONA 2 · VOLUMEN   historial · documentos recuperados · salidas largas
ZONA 3 · FILO      handoff · afirmaciones · solicitud — SIEMPRE al final
```

Declarado en `contratos/contexto.yaml`.

## Por qué tres y no dos

v1.3.0 tenía dos: estable y volátil. Optimizaba la caché y **rompía la atención**.

- La caché exige lo estable **primero**.
- La atención exige lo importante al principio **o al final**: 70–75% de exactitud en
  los extremos, 55–60% en la mitad.

Con dos zonas, el prefijo estable empujaba la tarea al medio. Se ganaba en costo lo
que se perdía en exactitud, y nadie lo habría notado sin medirlo.

**La regla que lo cierra:** nada después de la zona filo. Si una restricción es
crítica y hay que repetirla, va en la zona ancla.

## Medir

```bash
./scripts/mapa-contexto.sh <rol>    # o /contexto
```

| Señal | Qué significa |
|---|---|
| Historial > 60% | Falta administrar la recencia |
| Más de 20 herramientas | Las definiciones ocupan contexto aunque no se usen |
| La zona ancla crece cada versión | Nadie ha corrido la pregunta de relevancia |

## Trabajo pendiente reconocido

La pregunta *si quito esta línea, ¿cambia alguna respuesta?* no se ha aplicado nunca
a la constitución ni a los documentos generados. La tendencia natural de todo
framework es acumular instrucciones, y la evidencia apunta en contra.
