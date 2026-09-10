# Arquitectura del framework

## Decisión 1 — Roles y procedimientos van separados

Un **rol** es un actor: identidad, permisos, herramientas. Vive en
`.claude/agents/` como subagente.

Un **procedimiento** es el "cómo": qué consume, qué produce, qué verifica. Vive en
`.claude/skills/` como `SKILL.md`, en el catálogo compartido.

Se separan porque cambian a ritmos distintos y pertenecen a dueños distintos. Los
permisos son del equipo de plataforma; los procedimientos son de la comunidad de
práctica que mantiene el catálogo. Si estuvieran en el mismo archivo, cada mejora
de procedimiento exigiría revisar permisos y viceversa.

## Decisión 2 — El catálogo es submódulo, no copia

`.claude/skills` es un submódulo Git apuntando al repo del catálogo. Consecuencias:

- El pin es por SHA. Ningún equipo recibe un cambio de procedimiento sin un commit
  explícito en su propio repo.
- Solo se necesita acceso a GitHub. Sin registro de paquetes, sin descargas HTTP,
  sin servicio que mantener.
- La ruta coincide con la que Claude Code ya usa para skills de proyecto, así que
  no hace falta script de sincronización ni symlinks.

Alternativa descartada: copiar las skills al repo de cada equipo. Se descartó porque
las copias divergen en semanas y nadie sabe cuál es la buena.

## Decisión 3 — Los umbrales no viven en los prompts

`contratos/gates.yaml` es dato, no texto de prompt. Un agente puede ignorar una
instrucción de prompt; no puede hacer que `verificar-gates.sh` devuelva cero.

Esto también es lo que hace el catálogo compartible: dos equipos con exigencias
muy distintas usan los mismos `SKILL.md` y distinto `gates.yaml`.

## Decisión 4 — Todo pasa por archivo

Cada transición entre roles produce un JSON en `handoffs/`. El estado del trabajo
no vive en la conversación: vive en el repo, versionado, y sobrevive al cierre
del workspace, al cambio de modelo y al cambio de persona.

## Lo que este framework NO hace

- No orquesta agentes en paralelo. La cadena es secuencial a propósito: el valor
  está en la trazabilidad, no en la velocidad.
- No sustituye la revisión humana. Los gates hacen visible lo que falta; quién
  autoriza sigue siendo una persona.
- No impide que alguien haga el trabajo por fuera. Impide que ese trabajo pase
  por certificado.
