# Costo, caché y medición

## El punto de partida

Una orden completa son siete invocaciones de rol más las pasadas del verificador:
**alrededor de trece llamadas donde antes había una**, cada una repagando el contexto
fijo. Frente a un agente suelto, la relación realista está entre **3x y 6x**.

## Mitigación 1 — Frontera de caché

Declarada en `contratos/contexto.yaml`. La medición pública de referencia sobre 500+
sesiones agénticas: cachear el contexto estable reduce el costo entre 41% y 80% y
mejora el time-to-first-token entre 13% y 31%. Cachear *todo* rinde menos y puede
aumentar la latencia.

- **Estable** (se cachea): constitución, gates, roles.yaml, prompt del rol, SKILL.md
- **Volátil** (nunca en el prefijo): handoffs, evidencia, código leído, la solicitud

Dos consecuencias operativas: hay un mínimo de tokens por debajo del cual la caché no
compensa, y una ventana de reutilización — **partir una orden en varios días paga el
prefijo cada vez**.

## Mitigación 2 — Del agente al script

```bash
./scripts/resolver-referencias.sh evidencia/afirmaciones/<archivo>.json
```

Comprueba sin gastar un token que cada referencia resuelve, y extrae el contenido
citado. Efectos:

- Una referencia rota es CORREGIDO o RECHAZADO **sin invocar a nadie**.
- Cuando todas resuelven, el verificador recibe las líneas ya extraídas: le queda el
  juicio, no la búsqueda.

Ahorro del 100% en lo que cubre, no del 80%. Los cuatro gates `manual` restantes son
la lista de trabajo pendiente en esta dirección.

## Mitigación 3 — Un llamado por lote

El verificador se invoca **una vez** con todas las afirmaciones bloqueantes juntas.
El prefijo se paga una sola vez. Está en el comando `/verificar`.

## Medición

```bash
./scripts/registrar-costo.sh <orden> <rol> <in> <out> <cacheados>
./scripts/reporte-costo.sh      # o /costo
```

Dos números que se leen juntos:

| Número | Qué hacer si sale mal |
|---|---|
| % de prefijo reutilizado | Por debajo del 50%, hay contenido volátil en el prefijo estable |
| Tasa de hallazgo de la verificación | Si es cero tras varias órdenes, probablemente el verificador recibe contexto del autor y solo confirma |

El contexto: la Linux Foundation anunció en junio de 2026 la Tokenomics Foundation,
en alianza con FinOps, precisamente porque no existía forma neutral de medir
eficiencia de tokens; su trabajo incluye extender la especificación FOCUS al gasto por
tokens. Cuando esos estándares maduren, conviene alinear `metricas/costos.csv` con
ellos.

## Lo que no se afirma

**No hay medición propia de que el framework mejore la precisión.** El argumento es de
diseño. La única evidencia a favor es una anécdota: el verificador de la constitución
encontró un gate roto que llevaba dos versiones sin detectarse. Una anécdota no es una
tasa.

La tasa de hallazgo del reporte es el número que convierte esa creencia en dato. Deja
correr diez órdenes reales antes de defender nada ante el equipo.

## Dónde no usarlo

Cambio trivial, prototipo, exploración. Para eso está `activa_desde_impacto`. Un
equipo que lo deje en `ninguno` y lo aplique a todo va a odiarlo en dos semanas.

La comparación justa no es «framework contra agente suelto», sino «framework contra
agente suelto **más** el tiempo humano de revisar lo que produjo».
