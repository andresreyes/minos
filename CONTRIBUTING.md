# Cómo contribuir

## Al catálogo de skills (`minos-skills`)

Un cambio de procedimiento afecta a todos los equipos que lo pineen. Por eso:

1. Abre un issue describiendo **el problema real** que motivó el cambio, no la
   solución. Un procedimiento sin problema documentado envejece mal: nadie sabe
   después si sigue haciendo falta.
2. El PR cambia un solo `SKILL.md` salvo que el contrato de handoff cambie.
3. Si tu cambio agrega un paso, di explícitamente qué gate lo verifica. Un paso
   sin gate es una sugerencia.
4. Si tu cambio necesita un umbral, **no lo pongas en el SKILL.md**: agrégalo a
   `gates.yaml` de referencia y documéntalo en `docs/04-personalizacion.md`.
5. Versiona: MAJOR si cambia el contrato de handoff, MINOR si agregas rol o paso,
   PATCH para redacción.

## Al framework (`minos`)

Cada equipo mantiene el suyo. Los cambios que valgan para todos suben al repo
plantilla vía PR, con la misma regla: problema primero, solución después.

## Revisión

Un PR al catálogo necesita revisión de alguien de un equipo distinto al del autor.
Es la única forma de que el catálogo no se convierta en la costumbre de un solo equipo.
