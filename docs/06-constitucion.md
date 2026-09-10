# La constitución del proyecto

Añadida en v1.2.0. Inspirada en el `constitution` de spec-kit (GitHub, MIT), con una
diferencia deliberada: **aquí cada artículo debe nombrar los gates que lo comprueban,
y un script lo verifica.** Un principio que nadie puede comprobar no es un límite;
es una aspiración.

## Qué separa de lo demás

El framework ya tenía tres niveles. La constitución es el cuarto, y el único que no
se ajusta al adoptar:

| Capa | Responde a | Se ajusta |
|---|---|---|
| Constitución | ¿Qué no se puede cruzar nunca? | No |
| Gates | ¿Cuánto exigimos? | Sí, cada equipo |
| Contrato del repo | ¿Cómo se opera? | Rara vez |
| Skills | ¿Cómo se hace cada paso? | Por PR al catálogo |

## Los siete artículos

1. **La evidencia manda sobre la afirmación** — nada avanza porque un agente diga
   que está bien.
2. **Nadie certifica su propio trabajo** — quien produce no decide si pasa.
3. **Lo que bloquea tiene que poder comprobarse** — un bloqueo que depende del
   criterio de quien lo evalúa es una negociación, y las gana quien tiene prisa.
4. **Producción se protege por encima de la velocidad de entrega**.
5. **El alcance no crece en silencio**.
6. **Los límites se aplican en la infraestructura, no en el texto**.
7. **Toda excepción es explícita, motivada y caduca**.

Los artículos 1, 2, 3 y 6 son el núcleo. Un equipo que necesite retirar alguno
probablemente necesita otro framework, no este con menos artículos.

## Por qué cada artículo lleva su «por qué»

Un límite sin razón se cruza en cuanto estorba, y siempre estorba en el peor momento.
Con la razón escrita, quien se plantea saltárselo tiene delante el fallo concreto que
el artículo evita, no una regla abstracta.

El artículo 4 es el ejemplo claro: el coste de un despliegue tardío es visible y
acotado; el de uno que rompe algo estable es difuso, tarda en aparecer y lo paga
gente que no participó en la decisión. Esa asimetría no se percibe en el momento de
decidir. Por eso la regla tiene que estar escrita **antes**.

## El script que la hace real

```bash
./scripts/verificar-constitucion.sh
```

Falla si un artículo no nombra gates, si nombra uno que no existe en `gates.yaml`, o
si le falta alguna de sus secciones obligatorias.

Ese script encontró un defecto real la primera vez que se ejecutó: el artículo 7
citaba `G7_cierre_completo`, un gate que la skill del líder técnico mencionaba desde
v1.0.0 pero que **nunca existió en `gates.yaml`**. Estuvo dos versiones sin que nadie
lo notara, precisamente porque nada lo comprobaba.

## Cómo se modifica

No en el curso de una orden de trabajo: es una decisión del equipo.

1. Sube la `version` del frontmatter — MAJOR si retiras o debilitas un artículo.
2. Nombra al menos un gate existente por artículo.
3. `./scripts/verificar-constitucion.sh`
4. `./scripts/generar-adaptadores.sh` — el resumen está embebido en `CLAUDE.md` y
   `AGENTS.md`, y si no regeneras, divergen.

El comando `/constitucion` guía el proceso y avisa explícitamente cuando un cambio
debilita un artículo del núcleo.
