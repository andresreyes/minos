---
description: Reporte de tokens por orden y rendimiento real de la verificación.
---

Ejecuta `./scripts/reporte-costo.sh` y presenta el resultado.

Presta atención a dos números y coméntalos:

- **Porcentaje de prefijo reutilizado.** Por debajo del 50%, la caché no está
  funcionando: probablemente hay contenido volátil colado en el prefijo estable.
  Revisa `contratos/contexto.yaml`.
- **Tasa de hallazgo de la verificación.** Es el número que justifica —o no— su
  costo. Si es cero tras varias órdenes, no celebres: lo más probable es que el
  verificador esté recibiendo contexto del autor y solo esté confirmando.

No inventes cifras de costo en moneda: el reporte da tokens, y el precio por token
depende del proveedor y del plan.
