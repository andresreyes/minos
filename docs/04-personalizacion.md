# Personalización

## Lo que se ajusta

**`contratos/gates.yaml`** — umbrales del equipo. Es el archivo esperado a cambiar:

- `G4b_cobertura_minima.umbral` — porcentaje de cobertura exigido.
- `G5b_sin_hallazgos_sobre_umbral.severidad_maxima` — severidad tolerada.
- `activo_si` de cada gate — a partir de qué nivel de impacto se exige.
- `anulable` — qué puede saltarse el líder técnico con motivo.

**`contratos/roles.yaml`** — qué cadena atiende cada tipo de trabajo. Aquí se acorta
la cadena para correcciones, o se agrega un tipo propio del equipo.

**`.claude/settings.json`** — permisos por herramienta según el ambiente.

## Lo que no se toca

Los `SKILL.md` del catálogo. Si necesitas cambiar uno, casi siempre es una de dos
cosas:

1. **Querías cambiar un umbral** → va en `gates.yaml`. El catálogo ya lo contempla.
2. **Tu equipo tiene un paso que otros no** → propón el cambio al catálogo como PR,
   o agrega una skill local en `.claude/skills-locales/` y referéncíala desde el
   subagente. No edites el submódulo: el próximo `git submodule update` borra tu cambio.

## Cómo agregar un rol

1. Skill nueva en el catálogo, siguiendo el formato de las siete existentes.
2. Subagente en `.claude/agents/` que cargue esa skill y declare sus herramientas.
3. Gates en `gates.yaml` con `rol:` apuntando al nombre del subagente.
4. Insertar el rol en la cadena correspondiente en `roles.yaml`.
5. Actualizar el diagrama en `docs/02-roles-y-gates.md`.

Si el rol nuevo no tiene al menos un gate verificable, probablemente no es un rol:
es una etapa de otro rol.

## Cómo agregar un gate

Un gate necesita las cuatro cosas o no es un gate:

- **Nombre** estable, referenciado desde el `SKILL.md` del rol.
- **Verificación** — cómo se comprueba: presencia de archivo, comparación de hash,
  umbral numérico, o `manual`.
- **Evidencia** — qué archivo lo demuestra.
- **Condición de aborto** — qué pasa si falla.

Un gate `manual` es legítimo, pero cada uno que agregues es un punto donde el
framework confía en una afirmación. Manténlos en minoría.

## Versionado

El framework y el catálogo se versionan por separado. Al subir el pin del catálogo,
haz un commit dedicado con la diferencia de procedimientos en el mensaje: es el
registro de cuándo cambió la forma de trabajar del equipo.
