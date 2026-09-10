---
description: Muestra, revisa o propone cambios a la constitución del proyecto.
---

Argumento: $ARGUMENTS

**Sin argumento** — muestra los artículos y ejecuta
`./scripts/verificar-constitucion.sh`. Reporta si algún artículo quedó huérfano.

**Con una propuesta de cambio** — no la apliques directamente. Primero:

1. Di a qué artículo afecta y si lo agrega, lo modifica o lo debilita.
2. Si debilita o retira un artículo del núcleo (1, 2, 3, 6), dilo explícitamente y
   explica qué control se pierde. No lo hagas sin confirmación del usuario.
3. Propón la redacción completa: principio, por qué, prohíbe, gates.
4. Verifica que los gates citados existan en `contratos/gates.yaml`. Si no existen,
   propónlos también; un artículo sin gate es decoración.
5. Sube la `version` del frontmatter — MAJOR si retiras o debilitas.

Tras aplicar el cambio, ejecuta `./scripts/verificar-constitucion.sh` y luego
`./scripts/generar-adaptadores.sh`, porque el resumen de la constitución está
embebido en `CLAUDE.md` y `AGENTS.md`.

Un cambio de constitución no se hace en el curso de una orden de trabajo. Si estás
a mitad de una cadena, dilo y sugiere terminarla primero.
