# Instalación rápida

Versión de una pantalla. Detalle por plataforma en `docs/08-instalacion.md`.

## Requisitos

`git`, `python3` (3.8+), `bash`. Nada más.

## Tres comandos

```bash
git clone --recurse-submodules <URL-DEL-FRAMEWORK>
cd minos
./scripts/bootstrap.sh
```

`bootstrap.sh` resuelve el catálogo de skills, genera los adaptadores de plataforma,
verifica la constitución y corre 15 comprobaciones. Debe terminar en
`15 correcto(s), 0 fallo(s)`.

## Según tu agente

| Agente | Qué hacer |
|---|---|
| **Claude Code** | `claude` — lee `CLAUDE.md` y descubre roles y comandos solo |
| **Codex** | `codex` — lee `AGENTS.md`; adopta los roles uno a uno |
| **Cursor · Windsurf · Cline** | Abre la carpeta — auto-descubren `AGENTS.md` |
| **Coder** | Ya está: el template lo hizo al arrancar el workspace |

## Ajusta dos cosas

```bash
$EDITOR contratos/gates.yaml    # umbrales marcados AJUSTAR
$EDITOR contratos/roles.yaml    # verificacion_adversarial.activa_desde_impacto
```

## Primera orden

```
/iniciar Agregar reintentos con backoff al consumidor de eventos
```

En agentes sin comandos slash:

```
Actúa como lider-tecnico según AGENTS.md. Solicitud: <la tuya>
```

## Si algo falla

```bash
./scripts/prueba-humo.sh    # dice qué falta, en una línea por comprobación
```

Tabla de síntomas y soluciones en `docs/08-instalacion.md`.
