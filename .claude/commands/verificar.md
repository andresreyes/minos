---
description: Verificación adversarial de las afirmaciones del último rol, optimizada en tokens.
---

Sigue este orden. Los pasos 1–3 no gastan tokens del verificador y eliminan la
mayor parte del trabajo antes de invocarlo.

1. Localiza el archivo más reciente en `evidencia/afirmaciones/`.

2. `./scripts/validar-salida.sh <archivo>` — estructura. Si es inválido, devuélvelo
   al rol autor. No verifiques un artefacto malformado.

3. `./scripts/resolver-referencias.sh <archivo>` — comprueba que cada referencia
   resuelve y **extrae el contenido citado**. Si alguna está rota, ya es CORREGIDO o
   RECHAZADO sin invocar a nadie: devuélvelo al autor. Si todas resuelven, la salida
   del script trae las líneas y archivos citados.

4. Invoca el subagente `verificador` **una sola vez**, con todas las afirmaciones
   bloqueantes juntas. Pásale la ruta del archivo y la salida del paso 3. Nada más:
   no le resumas el contexto, no le cuentes qué hizo el rol anterior, no le adelantes
   tu opinión. Ese aislamiento es lo que hace que el veredicto valga algo.

   Un llamado por lote, no uno por afirmación: el prefijo del prompt se paga una vez.

   **El archivo de afirmaciones va al final de lo que le pasas.** Nada después: ni
   recordatorios, ni formato de salida, ni repetición de las reglas. Eso empujaría
   la tarea al medio del contexto, donde la exactitud cae de 70–75% a 55–60%. Las
   reglas ya están en su prompt, que va al principio.

5. `./scripts/validar-salida.sh evidencia/verificacion/<archivo>` — valida su salida.

6. `./scripts/registrar-costo.sh <id_orden> verificador <in> <out> <cacheados>` si
   tu plataforma reporta uso de tokens.

7. Presenta el resumen: cuántas VERIFICADO, CORREGIDO y RECHAZADO.

Si hay algún RECHAZADO sobre una afirmación bloqueante, la cadena no avanza:
invoca `lider-tecnico` con el bloqueo.
