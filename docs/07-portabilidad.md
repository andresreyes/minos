# Portabilidad entre plataformas de agentes

El framework funciona en Claude Code, en Codex, y en cualquier agente que lea
`AGENTS.md`. No hay dos versiones que mantener: hay una fuente y un generador.

## El problema

Cada plataforma lee un archivo distinto. `AGENTS.md` se ha vuelto el estándar de
facto —está bajo la Agentic AI Foundation de la Linux Foundation y lo leen Codex,
Cursor, Windsurf y Cline— pero Claude Code sigue leyendo `CLAUDE.md`.

Mantener los dos a mano garantiza que diverjan. La primera vez que alguien cambie un
límite en uno y no en el otro, dos agentes del mismo equipo estarán operando bajo
reglas distintas sin que nadie lo sepa.

## La solución

```
FUENTE DE VERDAD              GENERADOR              ADAPTADORES
roles/*.md            ┐                        ┌─  CLAUDE.md
constitucion.md       ├─→  generar-            ├─  .claude/agents/
contratos/gates.yaml  ┤    adaptadores.sh      ├─  AGENTS.md
contratos/roles.yaml  ┘                        └─  ~/.agents/skills (enlace)
```

Los adaptadores llevan una marca de generado en la primera línea. Si alguien los
edita a mano, el siguiente `bootstrap.sh` borra el cambio — y eso es lo correcto: el
cambio pertenecía a `roles/` o a `constitucion.md`.

## Qué cambia según la plataforma

| | Claude Code | Codex / Cursor / Windsurf / Cline |
|---|---|---|
| Instrucciones | `CLAUDE.md` | `AGENTS.md` |
| Roles | Subagentes en `.claude/agents/` | Descritos en `AGENTS.md`, se adoptan uno a uno |
| Comandos | `/iniciar`, `/verificar`, `/gate`… | Se invocan los scripts directamente |
| Skills | `.claude/skills/` | Enlace en `~/.agents/skills` |
| Aislamiento del verificador | Real: subagente con herramientas de solo lectura | Parcial: exige sesión nueva |

## La diferencia que importa

En plataformas sin subagentes, el aislamiento del verificador **no se puede simular
con buena voluntad**. Si el mismo hilo produce las afirmaciones y luego las verifica,
el verificador ya vio el razonamiento del autor y va a reformularlo, no a
comprobarlo.

La instrucción en `AGENTS.md` es explícita: abrir sesión nueva para verificar. Es
menos cómodo y funciona; hacerlo en el mismo hilo produce una firma de aprobación sin
la verificación detrás, que es peor que no verificar.

## Añadir una plataforma

Edita la función generadora en `scripts/generar-adaptadores.sh` para emitir el
archivo que esa plataforma espera, reutilizando el bloque `NUCLEO`. No dupliques el
contenido: el núcleo se construye una vez y se inserta en cada adaptador.
