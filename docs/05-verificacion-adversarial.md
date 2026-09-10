# Verificación adversarial

Añadido en v1.1.0. Es la evolución más importante del framework hasta ahora, y no
es un control de seguridad: es un mecanismo de **precisión**.

## De dónde sale

Del enfoque de auditoría de seguridad de Cloudflare (MIT), generalizado del dominio
de seguridad a todo el ciclo de vida. Su hallazgo central: un agente que produce un
artefacto y luego lo revisa tiene el mismo punto ciego en ambos pasos. Se
autoevalúa con el razonamiento que ya usó, así que confirma lo que ya creía.

Eso pasa igual en un diseño, una certificación de pruebas o un runbook. El texto se
lee bien y los detalles pueden estar mal: una ruta que no existe, una línea que dice
otra cosa, un umbral que nadie midió.

## El cambio de fondo: no se puede verificar prosa

Este es el punto que hace posible todo lo demás. Un verificador enfrentado a
párrafos solo puede opinar. Enfrentado a una afirmación con referencia comprobable,
puede abrir el archivo y mirar.

Por eso cada rol ahora emite dos cosas: su artefacto de siempre, y un archivo de
**afirmaciones** — conclusiones discretas, cada una con dónde comprobarla:

```json
{
  "id": "AF-03",
  "tipo": "codigo",
  "referencia": "src/consumidor/reintentos.py:47",
  "texto": "El backoff exponencial tiene tope de 30 segundos",
  "criticidad": "bloqueante"
}
```

El framework pasa así de verificar **presencia** ("existe un archivo de evidencia")
a verificar **contenido** ("lo que ese archivo afirma es cierto").

## Los tres invariantes

**Autor y verificador son agentes distintos**, y el verificador no ve el
razonamiento del autor. Solo el archivo de afirmaciones y el código.

**La carga de la prueba se invierte.** La instrucción no es "revisa si está bien",
es "desmiente esto; si no puedes, confírmalo con la evidencia que te lo impidió".

**El veredicto es cerrado**: VERIFICADO, CORREGIDO o RECHAZADO. Nada intermedio.
"Parece correcto pero" no sirve para decidir.

## Por qué el aislamiento no es negociable

El verificador es el mismo modelo con el mismo entrenamiento. Si le entregas el
razonamiento del autor, no verifica: lo reformula. El framework gana una firma de
aprobación sin ganar precisión, que es **peor que no verificar** — produce confianza
infundada en un resultado que nadie comprobó.

De ahí que el subagente `verificador` tenga solo herramientas de lectura y su prompt
prohíba explícitamente leer `handoffs/`. Y de ahí la regla en `CLAUDE.md`: al
invocarlo, se le pasa la ruta del archivo y nada más.

## Costo

Verificar todo cuesta el doble. La regla de proporción:

- Toda afirmación `bloqueante` se verifica, sin excepción (gate `GV3`).
- Las `informativas` van por muestra; si aparece un error en la muestra, se
  verifica el resto.
- El tipo de trabajo `investigacion` no lleva verificación: no hay artefacto
  desplegable que proteger.
- La verificación se activa desde impacto `indirecto`. Un cambio de impacto
  `ninguno` no la lleva.

Ese último parámetro está en `contratos/roles.yaml` bajo `verificacion_adversarial`.
Un equipo que quiera más rigor lo baja a `ninguno`; uno con presión de entrega lo
sube a `directo`. Es la perilla principal del framework.

## El riesgo que queda abierto

El verificador comparte modelo con el autor. El aislamiento de contexto mitiga el
problema; no lo elimina. Si ambos comparten un sesgo del entrenamiento —una
convención mal aprendida, una API que ambos recuerdan mal— los dos se equivocarán
igual.

Por eso `GV2_sin_rechazos_bloqueantes` no sustituye la revisión humana: la enfoca.
Un lote donde todo sale VERIFICADO no significa que esté todo bien; significa que
las referencias resuelven y dicen lo que se afirmó. Eso es bastante más de lo que
había antes, y bastante menos que una garantía.
