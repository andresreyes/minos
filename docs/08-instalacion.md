# Instalación paso a paso

Cuatro caminos según la plataforma. Todos parten de lo mismo y terminan en la misma
comprobación. Tiempo estimado: 10 minutos el primero, 2 minutos los siguientes.

## Requisitos

- `git`, `python3` (3.8+), `bash`
- Acceso de red al servidor Git donde publiques los dos repos

Nada más. Sin Node, sin Docker, sin servicios que levantar, sin paquetes que instalar.

---

## Paso 0 — Publicar los dos repos (una sola vez, por el que instala)

```bash
# 1. El catálogo de skills — compartido entre todos los equipos
cd minos-skills
git init && git add -A && git commit -m "Catálogo v1.2.0"
git tag v1.2.0
git remote add origin https://github.com/andresreyes/minos-skills.git
git push -u origin main --tags

# 2. El framework — cada equipo tendrá el suyo
cd ../minos
git init && git add -A && git commit -m "Framework v1.2.0"
git submodule add https://github.com/andresreyes/minos-skills.git .claude/skills
cd .claude/skills && git checkout v1.2.0 && cd ../..
git add .gitmodules .claude/skills && git commit -m "Pin catálogo v1.2.0"
git tag v1.2.0
git remote add origin https://github.com/andresreyes/minos.git
git push -u origin main --tags
```

Reemplaza `andresreyes` por tu organización. Si tu servidor Git no es GitHub, cambia la
URL: nada del framework depende de GitHub en particular.

---

## Camino A — Coder (workspace)

Es el caso del equipo destinatario: contenedor con salida solo al servidor Git.

**A.1 — Añadir el bloque al template**

Copia `coder/main.tf` dentro del `main.tf` del template del equipo y ajusta dos
variables:

```hcl
variable "framework_repo" {
  default = "https://github.com/andresreyes/minos.git"
}
variable "framework_ref" {
  default = "v1.2.0"      # pinea a un tag; nunca a main
}
```

**A.2 — Publicar el template**

```bash
coder templates push <nombre-del-template>
```

**A.3 — Crear el workspace**

Al arrancar, el `coder_script` clona con submódulos y corre `bootstrap.sh` solo.
No hay paso manual.

**A.4 — Comprobar**

```bash
cd ~/minos && ./scripts/prueba-humo.sh
```

Debe terminar en `15 correcto(s), 0 fallo(s)`.

> **Antes de producción:** crea un template **aparte** para el rol de despliegue, con
> las credenciales productivas y una allowlist de red más estrecha. El template
> general no debe tenerlas nunca (artículo 6 de la constitución).

---

## Camino B — Claude Code

**B.1 — Clonar con submódulos**

```bash
git clone --recurse-submodules https://github.com/andresreyes/minos.git
cd minos
```

Si ya lo clonaste sin `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

**B.2 — Preparar**

```bash
./scripts/bootstrap.sh
```

Genera adaptadores, verifica la constitución y corre la prueba de humo.

**B.3 — Abrir y comprobar**

```bash
claude
```

Claude Code lee `CLAUDE.md` al arrancar y descubre solo los subagentes de
`.claude/agents/` y los comandos de `.claude/commands/`. Comprueba con:

```
/constitucion
```

Debe listar los siete artículos y confirmar que todos tienen gate.

**B.4 — Primera orden**

```
/iniciar Agregar reintentos con backoff al consumidor de eventos
```

---

## Camino C — Codex CLI

**C.1 y C.2** — idénticos a B.1 y B.2.

**C.3 — Enlazar el catálogo de skills**

`bootstrap.sh` ya lo intenta. Si tu Codex busca skills en otra ruta:

```bash
mkdir -p ~/.agents
ln -sfn "$(pwd)/.claude/skills" ~/.agents/skills
```

**C.4 — Abrir**

```bash
codex
```

Codex lee `AGENTS.md` de la raíz, que el generador produjo desde la misma fuente que
`CLAUDE.md`. Contiene la constitución, la cadena y la definición completa de los
ocho roles.

**C.5 — Trabajar sin subagentes**

Codex no tiene subagentes, así que los roles se adoptan uno a uno:

```
Actúa como lider-tecnico según AGENTS.md.
Solicitud: agregar reintentos con backoff al consumidor de eventos.
```

Al terminar cada rol, escribe su handoff y anuncia el siguiente. Los comandos slash
no existen aquí; se invocan los scripts:

```bash
./scripts/verificar-gates.sh
./scripts/validar-salida.sh evidencia/afirmaciones/<archivo>.json
```

> **Importante:** para la verificación adversarial, **abre una sesión nueva**. Si
> verificas en el mismo hilo, el verificador ya vio el razonamiento del autor y va a
> reformularlo en vez de comprobarlo. Es la única parte del patrón que no se puede
> sustituir con buena voluntad.

---

## Camino D — Cursor, Windsurf, Cline

**D.1 y D.2** — idénticos a B.1 y B.2.

**D.3 — Abrir la carpeta**

Los tres auto-descubren `AGENTS.md` en la raíz del repo y lo cargan en su motor de
reglas. No hay configuración adicional.

**D.4** — Igual que C.5: roles uno a uno, scripts en vez de comandos slash, sesión
nueva para verificar.

---

## Paso final — Común a todos

**1. Ajustar los umbrales del equipo**

```bash
$EDITOR contratos/gates.yaml
```

Dos valores marcados `AJUSTAR`: `G4b_cobertura_minima.umbral` y
`G5b_sin_hallazgos_sobre_umbral.severidad_maxima`.

**2. Ajustar el rigor**

```yaml
# contratos/roles.yaml
verificacion_adversarial:
  activa_desde_impacto: indirecto   # ninguno = todo | directo = solo producción
```

**3. Comprobar que sigue coherente**

```bash
./scripts/verificar-constitucion.sh
./scripts/prueba-humo.sh
```

**4. Confirmar**

```bash
git add -A && git commit -m "Umbrales del equipo"
```

---

## Solución de problemas

| Síntoma | Causa | Salida |
|---|---|---|
| `catálogo de skills no montado` | Clonado sin `--recurse-submodules` | `git submodule update --init --recursive` |
| `CONSTITUCIÓN NO EXIGIBLE` | Un artículo cita un gate que no existe | Agrega el gate a `gates.yaml` o corrige la cita |
| `el submódulo NO está en el SHA pinneado` | Alguien movió el catálogo a mano | `git submodule update --init` |
| El agente ignora los roles | Editaste `CLAUDE.md`/`AGENTS.md` y se regeneraron | Edita `roles/` o `constitucion.md`, luego `./scripts/generar-adaptadores.sh` |
| `No hay handoffs` | Aún no se emitió una orden | `/iniciar <solicitud>` |
| `bloqueante no_verificable` rechazada | Afirmación sin referencia comprobable | Añade `ruta:linea` o baja a `informativa` |

## Desinstalar

```bash
rm -rf minos
```

No hay estado fuera de la carpeta, salvo el enlace opcional `~/.agents/skills`.
