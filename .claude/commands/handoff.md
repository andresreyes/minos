---
description: Avanza la cadena al siguiente rol leyendo el último handoff.
---

1. Lee el handoff más reciente en `handoffs/`.
2. Verifica que sus gates estén resueltos con `./scripts/verificar-gates.sh`.
3. Si hay `bloqueos` no vacíos, invoca `lider-tecnico`, no el rol de destino.
4. Si está limpio, invoca el subagente indicado en `rol_destino`.

Nunca inventes el siguiente rol: sale del handoff, no de tu criterio.
