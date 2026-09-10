#!/usr/bin/env bash
# Genera los archivos que cada plataforma de agentes espera, desde una fuente
# neutra única: roles/*.md + constitucion.md + contratos/.
#
#   Claude Code  -> CLAUDE.md, .claude/agents/, .claude/commands/
#   Codex/Cursor/Windsurf/Cline -> AGENTS.md
#
# Idempotente. Correr tras cambiar roles/, la constitución o los contratos.
set -euo pipefail
cd "$(dirname "$0")/.."

AVISO="<!-- GENERADO por scripts/generar-adaptadores.sh — no editar a mano.
     Fuente: roles/*.md, constitucion.md, contratos/. -->"

python3 - "$AVISO" <<'PY'
import pathlib, re, sys, shutil

aviso = sys.argv[1]
roles = sorted(pathlib.Path("roles").glob("*.md"))
if not roles:
    print("ERROR: no hay roles/ — nada que generar", file=sys.stderr); sys.exit(1)

def frontmatter(txt):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m: return {}, txt
    meta = {}
    for linea in m.group(1).splitlines():
        if ":" in linea:
            k, v = linea.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2).strip()

datos = []
for r in roles:
    meta, cuerpo = frontmatter(r.read_text())
    datos.append((meta.get("name", r.stem), meta, cuerpo))

# ---------- Claude Code: .claude/agents/ ----------
dest = pathlib.Path(".claude/agents"); dest.mkdir(parents=True, exist_ok=True)
for r in roles:
    shutil.copyfile(r, dest / r.name)
print(f"  .claude/agents/         {len(roles)} rol(es)")

# ---------- Núcleo común de instrucciones ----------
cadena = "líder técnico → arquitecto → constructor → pruebas → seguridad → SRE → devops"

const = pathlib.Path("constitucion.md").read_text()
arts = re.findall(r"^## (Artículo \d+) — (.+?)$", const, re.M)
lineas_art = "\n".join(f"{n}. **{t}**" for n, t in
                       [(a.split()[1].rstrip("."), t) for a, t in arts])

tabla = "\n".join(
    f"| `{n}` | {m.get('description','').split('.')[0]}. |" for n, m, _ in datos)

NUCLEO = f"""## Constitución

Los límites que ningún rol puede cruzar. Texto completo en `constitucion.md`.

{lineas_art}

Un artículo sin gate que lo compruebe es decoración: `scripts/verificar-constitucion.sh`
falla si alguno queda huérfano.

## Regla primera

**No se trabaja sin rol.** Si llega una solicitud y no hay orden de trabajo vigente,
actúa como `lider-tecnico` (o invoca ese subagente si tu plataforma los soporta).
No improvises la solución, por evidente que parezca: el valor de este framework está
en la trazabilidad, y una respuesta directa la rompe.

## La cadena

```
{cadena}
```

Tras cada rol productor se intercala el verificador adversarial. Cualquier bloqueo
vuelve al líder técnico. Nadie salta pasos. Nadie corrige el trabajo de otro rol.

## Roles

| Rol | Qué hace |
|---|---|
{tabla}

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
"""

# ---------- CLAUDE.md ----------
pathlib.Path("CLAUDE.md").write_text(f"""{aviso}

# Contrato de este repositorio

Este repo define un ciclo de vida de desarrollo ejecutado por agentes con roles
separados. Léelo completo antes de actuar.

{NUCLEO}
## Organización

- `constitucion.md` — los límites. No se negocian por orden de trabajo.
- `roles/` — **fuente de verdad** de los roles. Edita aquí y regenera.
- `.claude/agents/` — roles para Claude Code (generado).
- `.claude/commands/` — `/iniciar`, `/handoff`, `/verificar`, `/gate`, `/constitucion`.
- `.claude/skills/` — submódulo con el catálogo de procedimientos.
- `contratos/` — gates, roles, esquemas. Lo único que ajusta cada equipo.
- `handoffs/` y `evidencia/` — el rastro auditable.
""")
print("  CLAUDE.md               generado")

# ---------- AGENTS.md ----------
detalle = "\n\n".join(
    f"### `{n}`\n\n{m.get('description','')}\n\nHerramientas: {m.get('tools','(según plataforma)')}\n\n{c}"
    for n, m, c in datos)

pathlib.Path("AGENTS.md").write_text(f"""{aviso}

# Instrucciones para agentes

Ciclo de vida de desarrollo con roles separados, contratos entre ellos y gates
verificables. Compatible con cualquier agente que lea `AGENTS.md` (Codex, Cursor,
Windsurf, Cline). Claude Code lee `CLAUDE.md`, generado del mismo origen.

{NUCLEO}
## Si tu plataforma no tiene subagentes

Adopta un rol a la vez, explícitamente, y **no cambies de rol dentro del mismo
mensaje**. Al terminar, escribe el handoff en `handoffs/` y anuncia qué rol sigue.
El aislamiento del verificador se conserva abriendo una sesión nueva: es la parte
del patrón que no se puede simular con buena voluntad.

## Skills

El catálogo está en `.claude/skills/` (submódulo). Formato `SKILL.md` estándar. Si
tu agente busca skills en otra ruta, `./scripts/bootstrap.sh` crea el enlace
correspondiente.

## Definición de los roles

{detalle}
""")
print("  AGENTS.md               generado")
PY

# Enlace para agentes que buscan skills en ~/.agents/skills
if [ -d ".claude/skills" ] && [ ! -e "$HOME/.agents/skills" ]; then
  mkdir -p "$HOME/.agents"
  ln -sfn "$(pwd)/.claude/skills" "$HOME/.agents/skills" 2>/dev/null || true
fi

echo "Adaptadores generados. Fuente: roles/ + constitucion.md + contratos/"
