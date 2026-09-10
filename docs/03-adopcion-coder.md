# Adopción en Coder

Contexto asumido: workspaces de Coder con un agente CLI dentro del contenedor
(Claude Code u otro que lea `.claude/`), y salida de red **solo hacia GitHub**.
Sin Coder Agents en el control plane.

## Paso 1 — Publicar los dos repos

| Repo | Contenido | Quién lo mantiene |
|---|---|---|
| `minos-skills` | Catálogo de procedimientos | Comunidad de práctica |
| `minos` | Roles, gates, contratos, scripts | Cada equipo (fork o plantilla) |

Ambos en la misma organización de GitHub, para que la credencial que ya tiene el
contenedor sirva para los dos.

## Paso 2 — Enganchar el submódulo

En el repo del framework, apuntar `.gitmodules` al catálogo real y fijarlo:

```bash
git submodule add https://github.com/<ORG>/minos-skills.git .claude/skills
cd .claude/skills && git checkout v1.0.0 && cd -
git add .gitmodules .claude/skills && git commit -m "Pin catálogo v1.0.0"
```

## Paso 3 — Integrar al template

Copiar el bloque de `coder/main.tf` al template del equipo. El `coder_script` clona
con `--recurse-submodules` en cada arranque y corre `bootstrap.sh`, que es idempotente.

**Pinea `framework_ref` a un tag.** Un template apuntando a `main` significa que el
framework de un equipo cambia sin que el equipo lo decida.

## Paso 4 — Separar el template de despliegue

No le des credenciales productivas al template general. Crea uno aparte para el rol
devops, con esas credenciales y una allowlist de red más estrecha.

La razón: el aislamiento entre roles debe venir de la infraestructura. Un prompt
puede decir "no toques producción" y el modelo puede cumplirlo casi siempre —
casi siempre no es una garantía. Si el contenedor no tiene la credencial, no hay
nada que cumplir.

## Paso 5 — Primera corrida

```
/iniciar Agregar reintentos con backoff al consumidor de eventos
```

Verifica con `/gate` que aparezcan pendientes los gates del arquitecto. Si aparecen
también los de devops, el impacto quedó declarado como `directo`; revisa si era
correcto.

## Si más adelante habilitan Coder Agents

Coder 2.36 agregó invocación de skills del workspace desde el menú `/` y el control
plane permite administrar prompts de sistema y servidores MCP centralmente. Nada de
eso invalida este diseño: las skills seguirían viniendo del repo. Lo que cambiaría es
que parte de `settings.json` podría migrar a política del control plane, que se
aplica del lado servidor y el usuario no puede sobrescribir. Migra en ese momento,
no antes.
