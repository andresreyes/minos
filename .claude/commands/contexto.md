---
description: Audita el presupuesto de contexto de un rol y propone qué quitar.
---

Rol: $ARGUMENTS (si está vacío, todos)

1. Ejecuta `./scripts/mapa-contexto.sh $ARGUMENTS` y presenta la tabla.

2. Para cada pieza que exceda su presupuesto en `contratos/contexto.yaml`, aplica la
   pregunta de relevancia línea por línea: **si quito esto, ¿cambia alguna
   respuesta?** Propón lo que sobra, citando qué línea y por qué no cambia nada.

3. Revisa la lista `tools:` del rol contra lo que su skill realmente usa. Las
   definiciones de herramientas ocupan contexto aunque no se invoquen.

4. Si la zona ancla creció respecto a la versión anterior, dilo. Es la señal de que
   nadie ha podado: la tendencia natural de todo framework es acumular instrucciones,
   y más instrucciones no es mejor.

No propongas quitar artículos de la constitución ni gates: eso es decisión del
equipo, no una optimización de contexto. Sí puedes señalar redacción redundante
dentro de ellos.
