<!-- GENERADO por scripts/generar-adaptadores.sh — no editar a mano.
     Fuente: roles/*.md, constitucion.md, contratos/. -->

# Contrato de este repositorio

Este repo define un ciclo de vida de desarrollo ejecutado por agentes con roles
separados. Léelo completo antes de actuar.

## Constitución

Los límites que ningún rol puede cruzar. Texto completo en `constitucion.md`.

1. **La evidencia manda sobre la afirmación**
2. **Nadie certifica su propio trabajo**
3. **Lo que bloquea tiene que poder comprobarse**
4. **Producción se protege por encima de la velocidad de entrega**
5. **El alcance no crece en silencio**
6. **Los límites se aplican en la infraestructura, no en el texto**
7. **Toda excepción es explícita, motivada y caduca**

Un artículo sin gate que lo compruebe es decoración: `scripts/verificar-constitucion.sh`
falla si alguno queda huérfano.

## Regla primera

**No se trabaja sin rol.** Si llega una solicitud y no hay orden de trabajo vigente,
actúa como `lider-tecnico` (o invoca ese subagente si tu plataforma los soporta).
No improvises la solución, por evidente que parezca: el valor de este framework está
en la trazabilidad, y una respuesta directa la rompe.

## La cadena

```
líder técnico → arquitecto → constructor → pruebas → seguridad → SRE → devops
```

Tras cada rol productor se intercala el verificador adversarial. Cualquier bloqueo
vuelve al líder técnico. Nadie salta pasos. Nadie corrige el trabajo de otro rol.

## Roles

| Rol | Qué hace |
|---|---|
| `arquitecto` | Produce diseño de solución, contratos y matriz de impacto a partir de una orden de trabajo. |
| `constructor` | Implementa el código a partir de un diseño aprobado y produce el inventario de artefactos. |
| `devops` | Prepara y ejecuta el despliegue. |
| `lider-tecnico` | Enrutador del ciclo de vida. |
| `pruebas` | Certifica o rechaza un paquete construido, con evidencia de ejecución. |
| `seguridad` | Emite dictamen de seguridad sobre un paquete certificado. |
| `sre` | Define objetivos de servicio, alertas, runbook y criterio de reversión antes del despliegue. |
| `verificador` | Verifica adversarialmente las afirmaciones de cualquier rol antes de que la cadena avance. |

## Fundamentos

Antes de escribir o modificar cualquier skill, el catálogo en `.claude/skills/` trae
cuatro guías. La primera es de lectura obligada; las otras se consultan según la tarea:

| Guía | Cuándo |
|---|---|
| `FOUNDATIONS.md` | Siempre. Los tres niveles, la estructura de una instrucción, las técnicas contra la invención |
| `AUTHORING.md` | Al escribir una skill nueva |
| `CONTEXT.md` | Al decidir qué información entra a la ventana |
| `PRECISION.md` | Al diseñar una skill cuya salida deba ser comprobable |

Tres reglas de `FOUNDATIONS.md` aplican a **toda** invocación de un rol, sin excepción:

1. **Salida honesta.** Si te falta información para cumplir, dilo y emite bloqueo.
   No lo supongas. Un rol sin forma legítima de decir «me falta X» rellena el hueco
   con algo plausible.
2. **Anclaje.** Responde con base en las fuentes que te dieron, nombradas. Si algo no
   está en ellas, decláralo en vez de completarlo.
3. **Chat nuevo ante error de base.** Corregir encima no borra el dato equivocado:
   convive con el correcto en el mismo contexto. Por eso un bloqueo vuelve al líder
   técnico en lugar de seguir discutiendo en el mismo hilo.

## Orden del contexto — tres zonas

Lo que entra en la ventana se organiza así, y el orden no es cosmético:

```
ZONA 1 · ANCLA     constitución · gates · prompt del rol · SKILL.md
ZONA 2 · VOLUMEN   historial · documentos recuperados · salidas largas
ZONA 3 · FILO      el handoff, las afirmaciones, la solicitud — SIEMPRE al final
```

La zona ancla es estable, así que se cachea y ocupa la mejor posición. La tarea va
al final, que es la otra buena posición. Lo voluminoso y de baja señal queda en el
medio, que es donde menos daño hace: la misma información rinde 70–75% de exactitud
al inicio o al final, y 55–60% en la mitad.

**Nunca escribas nada después de la zona filo.** Ni un recordatorio, ni un "responde
en formato X", ni una repetición de las reglas. Cualquier coletilla empuja la tarea
al medio y la degrada. Si una restricción es crítica y hay que repetirla, va en la
zona ancla, no como cierre.

Detalle: **las definiciones de herramientas ocupan contexto aunque no se usen.** Si
un rol declara cuarenta y usa seis, paga las cuarenta en cada mensaje. Mide con
`./scripts/mapa-contexto.sh <rol>`.

## Verificación adversarial

Cada rol productor emite, además de su artefacto, **afirmaciones verificables** en
`evidencia/afirmaciones/`: conclusiones discretas con una referencia comprobable
(`ruta:linea`, un comando, un archivo). Después, el verificador intenta desmentirlas.

**Al invocar al verificador, pásale solo la ruta del archivo de afirmaciones.** No le
resumas el contexto ni le cuentes qué hizo el rol anterior. Si conoce el razonamiento
del autor, lo repite en lugar de verificarlo, y el veredicto deja de valer.

## Comandos de verificación

```bash
./scripts/verificar-gates.sh          # estado de la orden vigente
./scripts/validar-salida.sh <archivo> # valida afirmaciones o veredictos
./scripts/verificar-constitucion.sh   # la constitución sigue siendo exigible
./scripts/prueba-humo.sh              # todo el andamiaje responde
./scripts/mapa-contexto.sh <rol>      # presupuesto de contexto del rol
```

## Lo que nunca se hace

- Escribir umbrales en un prompt o en un `SKILL.md`. Van en `contratos/gates.yaml`.
- Marcar un gate aprobado sin evidencia en archivo.
- Dejar que un rol modifique artefactos de un rol anterior.
- Poner credenciales productivas en un prompt.
- Darle contexto al verificador más allá del archivo de afirmaciones.
- Marcar `bloqueante` una afirmación sin referencia comprobable.

## Organización

- `constitucion.md` — los límites. No se negocian por orden de trabajo.
- `roles/` — **fuente de verdad** de los roles. Edita aquí y regenera.
- `.claude/agents/` — roles para Claude Code (generado).
- `.claude/commands/` — `/iniciar`, `/handoff`, `/verificar`, `/gate`, `/constitucion`.
- `.claude/skills/` — submódulo con el catálogo de procedimientos.
- `contratos/` — gates, roles, esquemas. Lo único que ajusta cada equipo.
- `handoffs/` y `evidencia/` — el rastro auditable.
