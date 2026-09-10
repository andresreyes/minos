# Registro de cambios

## v1.7.0 — 2026-08-24

Fundamentos completos. Se habían leído solo las primeras ~3.000 palabras de cada
transcripción de origen; al leerlas enteras aparecieron cuatro temas que faltaban.

**Añadido a `FOUNDATIONS.md` (parte 4b–4e) y al PDF de fundamentos**
- **Árbol de decisión: dónde poner cada dato.** Tres preguntas en cadena — ¿aplica a
  toda interacción? ¿cambia con el tiempo? ¿debe sobrevivir a la sesión? — que
  desembocan en system prompt, archivo/skill referenciado, herramienta, memoria,
  user prompt, o «no la traigas».
- **Matriz de auditoría de contexto.** Cruza «¿cambió la respuesta?» con «¿ya lo tenía
  en contexto?» y da cuatro diagnósticos con acciones distintas: faltaba, mal ubicada,
  ruido, duplicado. El cuadrante «sí cambió y ya lo tenía» significa que la
  información estaba pero no se usaba — se acorta o se mueve, no se duplica.
- **Encadenamiento de prompts.** Un prompt gigante es la peor forma de resolver un
  problema grande: cada paso, un chat nuevo, pasando el resultado con etiquetas
  delimitadas. Es la contraparte a nivel de prompt de la cadena de handoffs.
- **Fabricar el procedimiento.** Pedir tres alternativas de razonamiento, elegir una y
  convertirla en plantilla. Acota los caminos y resuelve el problema de «qué palabras
  uso», porque la plantilla viene con las palabras del propio modelo.
- **Orden, caché y costo** en el PDF de fundamentos, con el diagrama de tres zonas.
- Noveno error común: agrandar el prompt en vez de encadenar.

**También en `CONTEXT.md`**
- La matriz de auditoría, como complemento del presupuesto de contexto.

**PDF de fundamentos:** de 7 a 12 páginas, con 4 diagramas.

## v1.6.0 — 2026-08-23

Paquete completo. Las guías pasan a nombres en inglés y quedan conectadas al framework.

**Cambiado**
- Guías del catálogo renombradas: `FOUNDATIONS.md`, `AUTHORING.md`, `CONTEXT.md`,
  `PRECISION.md`. Contenido en español; nombres estables entre equipos.
- `CLAUDE.md` y `AGENTS.md` traen una sección de fundamentos que enruta a las cuatro
  guías y extrae las **tres reglas que aplican a toda invocación de un rol**: salida
  honesta, anclaje a fuentes, y chat nuevo ante error de base.
- `prueba-humo.sh` verifica que las cuatro guías estén montadas con el submódulo.

**Añadido**
- Segundo PDF: **Fundamentos · Trabajar con agentes** (7 páginas). No depende del
  framework — sirve solo, y es el que conviene repartir primero.
- `docs/pdf/estilo.py`: paleta y componentes compartidos por los dos PDF, así que un
  cambio de estilo afecta a ambos a la vez.
- El README de la raíz describe el paquete completo y qué hace cada archivo.

## v1.5.0 — 2026-08-23

Fundamentos. Corrige una omisión: se había descartado material de prompt engineering
por «básico» tras leer solo su apertura. Contenía tres técnicas que faltaban.

**Añadido**
- Catálogo v1.5.0: **`FOUNDATIONS.md`**, documento de entrada — los tres niveles
  (prompt / contexto / sistema), cómo funciona el espacio vectorial y por qué el rol
  no es decoración, estructura de instrucción, las tres técnicas contra la invención,
  jerarquía de autoridad, y los ocho errores más comunes.
- `AUTHORING.md` §8b: **la cláusula de salida honesta**. Toda skill que consulte
  fuentes debe decir qué hacer cuando no encuentra la información. Sin esa cláusula
  el rol rellena el hueco con algo plausible — no por engañar, sino porque no le
  diste otra opción.
- `contratos/roles.yaml`: **autoconsistencia** como nivel intermedio de verificación,
  entre el anclaje y la adversarial. Varios caminos para el mismo problema; si
  divergen, hay error sin necesidad de saber la respuesta correcta. Más barata que la
  adversarial y no detecta datos inventados: se documenta el límite.

**Matiz sobre la verificación de citas**
- Una cita pedida al modelo **no siempre es literal**: puede reordenar o parafrasear.
  Un comparador de texto exacto marcaría como falsas citas sustancialmente correctas.
  El criterio fiable es «la referencia resuelve y dice lo mismo», no coincidencia
  carácter a carácter.

## v1.4.0 — 2026-08-23

Ingeniería de contexto. Corrige un defecto de posicionamiento introducido en v1.3.0.

**Corregido**
- **Las dos zonas de v1.3.0 empujaban la tarea al medio del contexto.** Optimizamos
  para caché sin considerar la atención: la misma información rinde 70–75% de
  exactitud en los extremos de la ventana y 55–60% en la mitad. Ahora son **tres
  zonas** — ancla (estable, se cachea, va primero), volumen (lo pesado, al medio) y
  filo (la tarea, siempre al final) — con la regla `nada_despues_del_filo`.

**Añadido**
- `contratos/contexto.yaml` v2 con las tres zonas y presupuesto por rol.
- `scripts/mapa-contexto.sh`: pesa cada pieza de la zona ancla y avisa cuando se
  excede el presupuesto o la lista de herramientas.
- Comando `/contexto`.
- Catálogo v1.4.0: **`CONTEXT.md`**, tercera guía — las cuatro decisiones
  (relevancia, recencia, recuperación, ranking) con su pregunta de auditoría.
- Sección 13 del PDF.

**Hallazgo del propio medidor**
- La zona ancla pesa ~1.800 palabras y el 80% es constitución + gates; el prompt del
  rol es el 8%. Se cachea una vez, así que el diseño es correcto — pero si algo hay
  que podar, es la constitución.
- La pregunta de relevancia («si quito esta línea, ¿cambia alguna respuesta?») no se
  ha corrido nunca sobre la documentación del framework. Trabajo pendiente reconocido.

## v1.3.0 — 2026-08-13

Eficiencia de tokens y medición.

**Añadido**
- `contratos/contexto.yaml`: frontera de caché declarada — prefijo estable vs. volátil.
- `scripts/resolver-referencias.sh`: comprueba sin gastar tokens que cada referencia
  resuelve y extrae el contenido citado. Una referencia rota se devuelve al autor sin
  invocar al verificador.
- `scripts/registrar-costo.sh` y `scripts/reporte-costo.sh` con `metricas/costos.csv`.
  El reporte da el % de prefijo reutilizado y la **tasa de hallazgo** de la verificación.
- Comando `/costo`.
- `docs/10-costo-y-medicion.md`.
- Catálogo v1.3.0: nueva `PRECISION.md` — cómo diseñar skills cuya salida sea
  comprobable. Destilada de cloudflare/security-audit-skill (MIT).

**Cambiado**
- `/verificar` ejecuta validación estructural y resolución de referencias ANTES de
  invocar al verificador, y lo invoca una sola vez por lote.
- El PDF corrige la estimación de costo: 3x–6x frente a un agente suelto, no 2x, y
  añade la sección 12 con caché, medición y lo que el documento no afirma.

## v1.2.0 — 2026-08-13

Constitución del proyecto y portabilidad multiplataforma.

**Añadido**
- `constitucion.md`: siete artículos con principio, razón, prohibición y los gates
  que comprueban cada uno. Concepto tomado de spec-kit (GitHub, MIT); la exigencia
  de que cada artículo nombre sus gates es propia.
- `scripts/verificar-constitucion.sh`: falla si un artículo queda huérfano o cita un
  gate inexistente. **Encontró un defecto real de v1.0.0**: `G7_cierre_completo` se
  citaba en la skill del líder técnico y nunca existió en `gates.yaml`.
- Gates `GC_cierre_completo` y `GC2_excepciones_con_vencimiento`.
- Comando `/constitucion`.
- `roles/` como fuente de verdad neutra, y `scripts/generar-adaptadores.sh` que emite
  `CLAUDE.md`, `.claude/agents/` y `AGENTS.md` desde el mismo origen.
- `AGENTS.md` para Codex, Cursor, Windsurf y Cline.
- `scripts/prueba-humo.sh`: 15 comprobaciones del andamiaje.
- `INSTALAR.md` y `docs/08-instalacion.md` (cuatro caminos de instalación).
- `docs/06-constitucion.md`, `docs/07-portabilidad.md`, `docs/09-creditos.md`.
- Guía en PDF ampliada a 22 páginas con 8 diagramas.

**Cambiado**
- La skill del líder técnico contrasta la solicitud con la constitución antes de
  emitir la orden, y exige vencimiento en toda anulación.
- `bootstrap.sh` genera adaptadores, verifica la constitución y corre la prueba de
  humo; ya no falla si se ejecuta fuera de un repo git.
- `.claude/agents/` pasa a ser **generado**. Se edita `roles/`.

## v1.1.0 — 2026-08-12

Verificación adversarial transversal. Adaptado del enfoque de auditoría de
Cloudflare (MIT), generalizado del dominio de seguridad a todo el ciclo de vida.

**Añadido**
- Rol `verificador`: octavo subagente, solo lectura, aislado del razonamiento
  del autor. Se intercala tras cada rol productor, no al final de la cadena.
- Skill `verificacion-adversarial` y referencia `_comun/references/adversarial.md`.
- Afirmaciones verificables: cada rol emite conclusiones discretas con referencia
  comprobable (`contratos/esquemas/afirmaciones.schema.json`).
- Veredictos cerrados VERIFICADO / CORREGIDO / RECHAZADO
  (`contratos/esquemas/verificacion.schema.json`).
- `scripts/validar-salida.sh`: validación estructural y semántica, sin dependencias.
- Comando `/verificar`.
- Gates `GV_verificacion_ejecutada`, `GV2_sin_rechazos_bloqueantes`,
  `GV3_cobertura_bloqueantes`.
- Parámetro `verificacion_adversarial.activa_desde_impacto` en `roles.yaml`.
- `docs/05-verificacion-adversarial.md`.

**Cambiado**
- Los seis roles productores llevan sección "Afirmaciones verificables".
- El framework pasa de verificar presencia de evidencia a verificar su contenido.
- `investigacion` queda excluida de la verificación adversarial.

## v1.0.0 — 2026-08-06

Versión inicial: siete roles, contratos de handoff, gates como dato,
catálogo de skills como submódulo, integración con Coder.
