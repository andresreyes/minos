---
version: 1.0.0
ratificada: 2026-08-13
---

# Constitución del proyecto

Los límites que ningún rol, ninguna orden de trabajo y ninguna presión de calendario
pueden cruzar. Todo lo demás en este framework —cadenas, umbrales, permisos— se
ajusta libremente. Esto no.

## Cómo leer este documento

Cada artículo tiene la misma estructura:

- **Principio** — la regla, en una frase.
- **Por qué** — el fallo concreto que evita. Sin esto, el artículo se salta en cuanto estorba.
- **Prohíbe** — lo que queda explícitamente fuera, para que no haya interpretación.
- **Gates** — qué comprueba el cumplimiento. **Un artículo sin gate es decoración.**

`scripts/verificar-constitucion.sh` comprueba esa última línea: falla si algún
artículo no nombra gates, o si nombra uno que no existe en `contratos/gates.yaml`.

---

## Artículo 1 — La evidencia manda sobre la afirmación

**Principio.** Nada avanza porque un agente diga que está bien. Avanza porque hay un
archivo que alguien puede abrir.

**Por qué.** «Las pruebas pasan» es una afirmación. Un modelo puede producirla con
total fluidez sin haber ejecutado nada, y no hay forma de distinguirlo leyendo el
texto. La única defensa es exigir el artefacto.

**Prohíbe.** Marcar un gate como aprobado con evidencia en prosa. Declarar
`no_aplica` sin justificación. Citar una ruta o una línea sin haberla abierto.

**Gates.** `G4_certificado_en_ambiente`, `G5_dictamen_emitido`, `GV_verificacion_ejecutada`

---

## Artículo 2 — Nadie certifica su propio trabajo

**Principio.** Quien produce un artefacto no es quien decide si pasa.

**Por qué.** La autoevaluación tiene el mismo punto ciego en ambos pasos: se revisa
con el razonamiento que ya se usó, así que confirma lo que ya se creía. Aplica al
agente y también a la persona.

**Prohíbe.** Que un rol corrija el trabajo de otro y lo dé por bueno. Que el
verificador reciba el razonamiento del autor. Que el mismo paso de la cadena
produzca y apruebe.

**Gates.** `GV2_sin_rechazos_bloqueantes`, `GV3_cobertura_bloqueantes`, `G3_artefactos_intactos`

---

## Artículo 3 — Lo que bloquea tiene que poder comprobarse

**Principio.** Una condición que detiene la cadena debe ser verificable por un script
o por la lectura de un archivo concreto.

**Por qué.** Un bloqueo que depende del criterio de quien lo evalúa no es un control:
es una negociación. Y las negociaciones las gana quien tiene prisa.

**Prohíbe.** Afirmaciones `bloqueante` de tipo `no_verificable`. Gates cuya
verificación sea «revisar que esté bien». Umbrales expresados en prosa.

**Gates.** `G1_alcance_acotado`, `G3_artefactos_intactos`, `G7b_hash_coincide`

---

## Artículo 4 — Producción se protege por encima de la velocidad de entrega

**Principio.** Ante un conflicto entre proteger lo que ya funciona y cumplir una
fecha, gana lo primero.

**Por qué.** El coste de un despliegue tardío es visible y acotado. El de un
despliegue que rompe algo estable es difuso, tarda en aparecer y lo paga gente que
no participó en la decisión. La asimetría no se percibe en el momento de decidir,
así que la regla tiene que estar escrita de antemano.

**Prohíbe.** Instalar sin dictamen de seguridad, sin definición de SRE o sin paquete
certificado. Instalar un artefacto cuyo hash no coincide con el certificado.
Considerar un cambio «demasiado pequeño» para exigir manual de actualización.

**Gates.** `G7_insumos_completos`, `G7b_hash_coincide`, `G7c_ventana_autorizada`, `G6b_reversibilidad_probada`

---

## Artículo 5 — El alcance no crece en silencio

**Principio.** Si el trabajo real excede la orden, se detiene y se vuelve al líder
técnico. No se amplía sobre la marcha.

**Por qué.** Cuando un rol rellena un hueco que encontró, lo que se despliega deja
de ser lo que se aprobó, y la matriz de impacto pasa a mentir sin que nadie lo note.
Es el fallo más silencioso de los cinco.

**Prohíbe.** Completar un diseño ambiguo desde la construcción. Tocar componentes
que la orden no mencionaba. Convertir un hallazgo en una corrección sin orden nueva.

**Gates.** `G1_alcance_acotado`, `G2_impacto_declarado`, `G3_artefactos_intactos`

---

## Artículo 6 — Los límites se aplican en la infraestructura, no en el texto

**Principio.** Un control que importa se hace imposible, no se pide por escrito.

**Por qué.** Un prompt puede decir «no toques producción» y el modelo puede cumplirlo
casi siempre. *Casi siempre* no es una garantía cuando el fallo es irreversible. Si
el contenedor no tiene la credencial, no hay nada que cumplir.

**Prohíbe.** Dar credenciales productivas a un entorno que no sea el del rol de
despliegue. Llevar secretos al contexto de una conversación. Confiar el aislamiento
entre roles únicamente a la redacción del prompt.

**Gates.** `G5c_secretos_ausentes`, `G7c_ventana_autorizada`

---

## Artículo 7 — Toda excepción es explícita, motivada y caduca

**Principio.** Saltarse un control es legítimo. Saltárselo en silencio no.

**Por qué.** Los frameworks que no admiten excepciones se abandonan a la primera
urgencia real. Los que las admiten sin registro acumulan deuda invisible. La salida
es la excepción con autor, fecha, motivo y vencimiento.

**Prohíbe.** Anular un gate marcado `anulable: false`. Excepciones sin fecha de
vencimiento —eso no es una excepción, es una renuncia—. Excepciones sin plan de
remediación.

**Gates.** `GC_cierre_completo`, `GC2_excepciones_con_vencimiento`

---

## Cómo se modifica esta constitución

Un artículo se agrega, cambia o retira con una decisión explícita del equipo, no en
el curso de una orden de trabajo. Al cambiarla:

1. Sube la `version` del frontmatter (MAJOR si retiras o debilitas un artículo).
2. Nombra al menos un gate existente por artículo.
3. Corre `./scripts/verificar-constitucion.sh` — falla si algún artículo queda huérfano.
4. Regenera los adaptadores: `./scripts/generar-adaptadores.sh`.

Los artículos 1, 2, 3 y 6 son el núcleo del framework: si tu equipo necesita
retirar alguno, lo que necesita probablemente es otro framework, no este con menos
artículos.
