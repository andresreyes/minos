# Fuentes, frameworks y créditos

Este framework no se inventó de cero. Se ensambló a partir de trabajo público de
otros, y esta página dice qué se tomó de dónde, bajo qué licencia, y —tan importante
como lo anterior— **qué se evaluó y se descartó, con la razón**.

## Lo que se adoptó

### Formato Agent Skills (`SKILL.md`)

**Qué es.** El formato abierto de skills: carpeta con `SKILL.md` de frontmatter YAML
(`name`, `description`) más `references/`, `scripts/`, `assets/` opcionales.

**Qué tomamos.** El formato completo del catálogo. Es la razón de que el catálogo no
quede atado a una plataforma: lo leen Claude Code y Codex.

**Dónde se ve.** Todo `minos-skills/`, y `AUTHORING.md` como guía de autoría.

---

### `cloudflare/security-audit-skill` — MIT

**Qué es.** Una skill de auditoría de seguridad de Cloudflare, agent-neutral por
diseño: su propio `SKILL.md` aclara que «Task tool» significa el mecanismo de
subagentes de la plataforma que sea.

**Qué tomamos, y es lo más valioso del framework:**

1. **El rol adversarial separado.** Un agente cuyo único trabajo es desmentir cada
   hallazgo, y otro que verifica que las líneas citadas existan. Nosotros lo
   generalizamos: de dominio de seguridad a **todos los roles**, porque el problema
   que resuelve no es de seguridad sino de precisión.
2. **Evidencia validada por máquina.** Esquema JSON con `additionalProperties: false`
   y un validador sin dependencias que sale con código 1. De ahí salió
   `scripts/validar-salida.sh`.
3. **Severidad con impacto obligatorio.** Su regla —si no puedes describir el daño
   concreto, la severidad es menor de lo que crees— más la lista de antipatrones.

**Qué no tomamos.** Sus companion files de dominios específicos (memory safety,
cliente web), y su orquestación en paralelo, que choca con nuestra cadena secuencial.

**Nuestra aportación encima.** El obstáculo que ellos no tenían que resolver: su
patrón funciona porque cada hallazgo trae `file:line`. Para generalizarlo hubo que
inventar el archivo de **afirmaciones** —conclusiones discretas con referencia
comprobable— porque *no se puede verificar prosa*.

---

### `github/spec-kit` — MIT

**Qué es.** Desarrollo dirigido por especificación, de GitHub. Muy activo. Su flujo
es `constitution` → `specify` → `clarify` → `plan` → `tasks` → `analyze` →
`implement`.

**Qué tomamos.** El concepto de **constitución del proyecto**: principios que todos
los comandos leen en tiempo de ejecución, por encima de cualquier tarea concreta.

**Nuestra diferencia deliberada.** En spec-kit la constitución son principios en
prosa. Aquí **cada artículo debe nombrar los gates que lo comprueban**, y
`verificar-constitucion.sh` falla si alguno queda huérfano. Un principio que nadie
puede comprobar no es un límite; es una aspiración.

**Qué no tomamos.** El flujo de fases. Spec-kit es *horizontal* —las etapas de
construir una feature— y este framework es *vertical* —quién tiene autoridad sobre
qué—. Son ejes perpendiculares, no alternativas: spec-kit puede vivir **dentro** de
los roles de arquitecto y constructor.

**Lo que sí les falta y aquí está.** Separación de autoridad, gates como dato
verificable, y verificación adversarial: su comando `analyze` es autochequeo del
mismo agente, justo el punto ciego que atacamos.

---

### `AGENTS.md` — Agentic AI Foundation (Linux Foundation)

**Qué es.** La convención de instrucciones para agentes que donó OpenAI a la
fundación, junto con MCP de Anthropic. Estándar de facto: lo leen Codex, Cursor,
Windsurf y Cline.

**Qué tomamos.** El formato como destino de generación. Claude Code sigue leyendo
`CLAUDE.md`, así que generamos ambos desde una fuente única —ver
`docs/07-portabilidad.md`.

---

### Coder

**Qué es.** La plataforma de workspaces de desarrollo remoto sobre la que corre el
equipo destinatario.

**Qué tomamos.** El modelo de template como infraestructura declarativa, y su
argumento de que los controles de seguridad no deben vivir en el prompt del agente.
Ese argumento es el artículo 6 de nuestra constitución.

---

## Lo que se evaluó y se descartó

Incluirlo tiene tanto valor como lo anterior: evita que el siguiente equipo repita
la evaluación.

### `betta-tech/agentic-patterns-typescript`

**Qué es.** Ejemplos pedagógicos de patrones agénticos en TypeScript: pipeline,
router, reflexión, orquestador-trabajadores.

**Por qué se descartó.**

- **Capa equivocada.** Construye agentes *en código*, llamando a una API desde Node.
  Nuestro framework no ejecuta agentes: los ejecuta el CLI del workspace. Adoptarlo
  significaría un servicio Node que mantener.
- **Runtime incompatible** con el agente que ya corre en el contenedor.
- **Red.** Necesita instalar paquetes; el contenedor destino solo alcanza el
  servidor Git.
- **Sin licencia declarada** en el repositorio, lo que por sí solo impide adoptarlo
  en un entorno corporativo.

**Qué sí aportó.** Su patrón *router* es conceptualmente el mismo que nuestro líder
técnico: clasificar primero, activar un único especialista después, y derivar a
humano cuando la confianza es baja. Ese último detalle reforzó nuestra regla de
bloqueo hacia el líder técnico. Ideas de diseño, no código.

---

## Tabla de licencias

| Fuente | Licencia | Qué se usó |
|---|---|---|
| Formato Agent Skills | Formato abierto | Estructura del catálogo |
| `cloudflare/security-audit-skill` | MIT | Patrón adversarial, evidencia validada, criterios de severidad |
| `github/spec-kit` | MIT | Concepto de constitución |
| `AGENTS.md` (AAIF / Linux Foundation) | Convención abierta | Destino de generación multiplataforma |
| Coder | Producto comercial | Modelo de template; argumento del artículo 6 |
| `betta-tech/agentic-patterns-typescript` | Sin licencia declarada | **Nada.** Solo ideas de diseño |

Ninguna de las fuentes MIT se redistribuye en este framework: se tomaron patrones e
ideas, reescritos. Si en el futuro se incorpora código de alguna de ellas, hay que
incluir su aviso de copyright.

## Lo que es original de aquí

Para que quede claro qué no viene de fuera:

- La separación en **siete roles** con contratos de handoff y frontera explícita.
- Los **gates como dato** en `gates.yaml`, con `activo_si` y `anulable`.
- El archivo de **afirmaciones verificables** que hace posible generalizar la
  verificación adversarial fuera del dominio de seguridad.
- La regla de que **cada artículo de la constitución nombre sus gates**, con script
  que lo comprueba.
- La **capa de portabilidad**: fuente neutra en `roles/` + generador de adaptadores.
- El `AUTHORING.md` de autoría de skills.
