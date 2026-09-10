---
description: Verifica el estado de los gates de la orden de trabajo vigente.
---

Ejecuta `./scripts/verificar-gates.sh` y presenta el resultado como tabla:
gate, estado, evidencia.

Para cada gate `pendiente`, di qué rol lo cierra. Para cada `rechazado`, muestra
la evidencia. No propongas anular un gate: eso es decisión del líder técnico y
solo aplica a gates con `anulable: true`.
