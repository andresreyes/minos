#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el PDF explicativo del framework SDLC agéntico."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, PageBreak,
                                KeepTogether, NextPageTemplate)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

from estilo import *  # noqa: F401,F403

# --- Plantilla de página -----------------------------------------------------
TITULO = "Framework SDLC Agéntico"

def marco(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRISCL); canvas.setLineWidth(0.5)
    canvas.line(22*mm, 275*mm, 188*mm, 275*mm)
    canvas.setFont("DJ", 7.6); canvas.setFillColor(GRIS)
    canvas.drawString(22*mm, 278*mm, TITULO)
    canvas.drawRightString(188*mm, 278*mm, "v1.4.0  ·  Guía de adopción, instalación y personalización")
    canvas.line(22*mm, 17*mm, 188*mm, 17*mm)
    canvas.drawString(22*mm, 12*mm, "Documento reutilizable — sin datos de organización")
    canvas.setFont("DJB", 8.4); canvas.setFillColor(AZUL)
    canvas.drawRightString(188*mm, 12*mm, str(doc.page - 1))
    canvas.restoreState()


def portada_fondo(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(AZUL)
    canvas.rect(0, 246*mm, 210*mm, 51*mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#F0F4F8"))
    canvas.rect(0, 0, 210*mm, 26*mm, stroke=0, fill=1)
    canvas.restoreState()


doc = BaseDocTemplate("framework.pdf", pagesize=A4,
                      leftMargin=22*mm, rightMargin=22*mm,
                      topMargin=26*mm, bottomMargin=22*mm,
                      title="Framework SDLC Agentico - Guia de adopcion",
                      author="Guia de adopcion y personalizacion")

fr = Frame(22*mm, 20*mm, 166*mm, 250*mm, id='n',
           leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
frp = Frame(22*mm, 30*mm, 166*mm, 210*mm, id='p',
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id='portada', frames=[frp], onPage=portada_fondo),
    PageTemplate(id='normal', frames=[fr], onPage=marco),
])

E = []
IMG = "img"

# ============================ PORTADA ========================================
E += [Spacer(1, 13*mm),
      P("Framework SDLC Agéntico", 'portada_t'),
      Spacer(1, 6*mm),
      P("Un estándar reutilizable para que cualquier equipo de desarrollo<br/>"
        "trabaje con agentes de forma auditable", 'portada_s'),
      Spacer(1, 20*mm)]

resumen = Table([[[
    P("<b>Qué es</b>", 'h3'),
    P("Un ciclo de vida de desarrollo ejecutado por agentes con <b>roles separados</b>, "
      "contratos entre ellos y <b>gates verificables por script</b>. Todo vive en un "
      "repositorio Git: no hay nada que configurar en una consola, ni servicio que "
      "mantener. Un equipo lo adopta clonando y ajustando dos archivos.", 'p'),
    P("<b>Documento compañero</b>", 'h3'),
    P("<i>Fundamentos · Trabajar con agentes</i> cubre los fundamentos que sostienen "
      "este framework y que sirven aunque no lo adoptes: los tres niveles, la "
      "estructura de una instrucción y las técnicas contra la respuesta inventada. "
      "Empieza por ahí si es tu primer contacto con el tema.", 'p'),
    P("<b>Por qué se puede reutilizar</b>", 'h3'),
    P("Los <i>procedimientos</i> viven en un catálogo compartido; los <i>umbrales</i> "
      "viven en cada equipo. Esa separación es lo que permite que cinco equipos con "
      "exigencias muy distintas usen exactamente las mismas instrucciones y solo "
      "cambien los números.", 'p'),
]]], colWidths=[152*mm])
resumen.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 0.6, GRISCL),
    ('LINEBEFORE', (0,0), (0,-1), 3, AZUL),
    ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
]))
E += [resumen, NextPageTemplate('normal'), PageBreak()]

# ============================ 1. EL PROBLEMA =================================
E += [P("1 · El problema que resuelve", 'h1'),
      P("Un agente sin estructura hace las siete cosas a la vez: interpreta la "
        "solicitud, diseña, implementa, se autoevalúa, declara que está seguro y "
        "despliega. El resultado se lee bien y nadie puede auditarlo. No porque el "
        "agente sea malo, sino porque <b>no hay ningún punto de la cadena donde algo "
        "pueda ser rechazado</b>.", 'p'),
      P("Los tres fallos concretos que aparecen sin estructura:", 'p'),
      LI("<b>Autoevaluación.</b> Quien produce el artefacto lo revisa con el mismo "
         "razonamiento que ya usó, así que confirma lo que ya creía."),
      LI("<b>Alcance que crece solo.</b> Al implementar aparece un hueco de diseño, "
         "el agente lo rellena, y lo que se despliega ya no es lo que se aprobó."),
      LI("<b>Evidencia declarativa.</b> «Las pruebas pasan» es una afirmación, no una "
         "evidencia. Sin un archivo que alguien pueda abrir, no hay nada que auditar."),
      Spacer(1, 5),
      P("Este framework responde a los tres con una idea simple: <b>separar la "
        "autoridad</b>. Cada rol tiene entrada, salida y una condición verificable "
        "para pasar el trabajo al siguiente. Nadie certifica su propio trabajo.", 'p')]

E += [PageBreak(), P("2 · La cadena", 'h1')]
E += FIG(f"{IMG}/g1.png", 112,
         "Figura 1 — Cadena de roles. Siete roles secuenciales más un verificador "
         "adversarial que se intercala después de cada rol productor. Cualquier "
         "bloqueo vuelve al líder técnico, nunca al rol anterior.")

E += [TABLA([
    ["Rol", "Produce", "No hace"],
    ["Líder técnico", "Orden de trabajo con alcance acotado e impacto declarado; cierre", "Diseñar, implementar"],
    ["Arquitecto", "Diseño, contratos, matriz de impacto", "Implementar"],
    ["Constructor", "Código, pruebas unitarias, inventario de artefactos", "Decidir arquitectura, desplegar"],
    ["Pruebas", "Certificación con evidencia de ejecución", "Corregir defectos"],
    ["Seguridad", "Dictamen y hallazgos con criterio de cierre", "Corregir hallazgos"],
    ["SRE", "Objetivos, alertas, runbook, criterio de reversión", "Desplegar"],
    ["DevOps", "Manual de actualización, orden cerrada, ejecución", "Diseñar, corregir"],
    ["Verificador", "Veredictos sobre las afirmaciones de cada rol", "Corregir el artefacto"],
], [30*mm, 76*mm, 60*mm])]

E += [Spacer(1, 8),
      CALLOUT("Por qué el líder técnico y el arquitecto están separados",
              "Es la separación que más se cuestiona al adoptar el framework. La razón: si el mismo "
              "rol asigna trabajo y produce el diseño, no hay quién desempate cuando el diseño resulta "
              "ser más grande que la orden. Uno decide <b>qué entra</b>, el otro decide <b>cómo se hace</b>. "
              "En equipos pequeños puede ser la misma persona alternando roles — pero no el mismo paso "
              "de la cadena.", AZUL)]

E += [PageBreak()]

# ============================ 3. ARQUITECTURA ================================
E += [P("3 · Las tres capas y por qué se separan", 'h1'),
      P("Aquí está la decisión que hace el framework reutilizable. Tres cosas que "
        "suelen ir mezcladas en un mismo archivo se separan porque cambian a ritmos "
        "distintos y tienen dueños distintos.", 'p')]
E += FIG(f"{IMG}/g2.png", 158,
         "Figura 2 — Separación de capas. El procedimiento es común a todos los "
         "equipos; los umbrales, el enrutamiento y los permisos son de cada uno.")

E += [TABLA([
    ["Capa", "Qué contiene", "Ejemplo", "Dueño"],
    ["Rol", "Identidad, permisos, herramientas", ".claude/agents/sre.md", "Plataforma"],
    ["Skill", "El procedimiento: qué consume, qué produce", "sre/SKILL.md", "Comunidad de práctica"],
    ["Gate", "El umbral que decide si el trabajo pasa", "gates.yaml", "Cada equipo"],
], [22*mm, 62*mm, 44*mm, 38*mm], mono_cols=(2,))]

E += [Spacer(1, 10),
      P("La regla que sostiene todo", 'h2'),
      P("<b>Ningún número vive dentro de una instrucción.</b> La skill de pruebas dice "
        "«la cobertura mínima la fija el equipo en gates.yaml; no la negocies aquí». "
        "El número está en un archivo YAML que un script lee.", 'p'),
      P("Esto tiene una consecuencia que va más allá de la limpieza: un agente puede "
        "ignorar una instrucción escrita en un prompt — les pasa a todos, en algún "
        "porcentaje de las veces. Lo que no puede hacer es que un script de "
        "verificación devuelva cero cuando el archivo de evidencia no existe. "
        "<b>Mover el control del prompt al dato es mover el control de la persuasión "
        "a la aritmética.</b>", 'p')]


E += [PageBreak(), P("4 · La constitución del proyecto", 'h1'),
      P("Encima de las tres capas anteriores hay una cuarta que <b>no se ajusta al "
        "adoptar el framework</b>: los límites que ningún rol, ninguna orden de "
        "trabajo y ninguna presión de calendario pueden cruzar.", 'p')]
E += FIG(f"{IMG}/g6.png", 148,
         "Figura 3 — Las cuatro capas por grado de negociabilidad. Solo la segunda "
         "se toca de forma rutinaria.")

E += [P("Los siete artículos", 'h2'),
      TABLA([
        ["#", "Artículo", "Lo que prohíbe, en concreto"],
        ["1", "La evidencia manda sobre la afirmación",
         "Aprobar un gate con evidencia en prosa; citar una línea sin abrirla"],
        ["2", "Nadie certifica su propio trabajo",
         "Que el verificador reciba el razonamiento del autor"],
        ["3", "Lo que bloquea tiene que poder comprobarse",
         "Afirmaciones bloqueantes de tipo no_verificable"],
        ["4", "Producción se protege sobre la velocidad de entrega",
         "Instalar sin dictamen, sin definición SRE o con hash distinto"],
        ["5", "El alcance no crece en silencio",
         "Completar un diseño ambiguo desde la construcción"],
        ["6", "Los límites van en la infraestructura, no en el texto",
         "Confiar el aislamiento entre roles a la redacción del prompt"],
        ["7", "Toda excepción es explícita, motivada y caduca",
         "Excepciones sin fecha de vencimiento"],
      ], [7*mm, 62*mm, 97*mm]),
      Spacer(1, 8),
      P("Cada artículo tiene cuatro partes: <b>principio</b>, <b>por qué</b> (el fallo "
        "concreto que evita), <b>prohíbe</b> (para que no haya interpretación) y "
        "<b>gates</b> (qué comprueba el cumplimiento).", 'p'),
      P("Un artículo sin gate es decoración", 'h2'),
      P("Es la diferencia deliberada frente a otros enfoques de «constitución de "
        "proyecto». Aquí un script lo comprueba:", 'p'),
      CODE(["./scripts/verificar-constitucion.sh"]),
      P("Falla si un artículo no nombra gates, si nombra uno inexistente, o si le "
        "falta alguna sección obligatoria.", 'p'),
      Spacer(1, 4),
      CALLOUT("Lo que encontró la primera vez que se ejecutó",
              "El artículo 7 citaba un gate llamado <font face='DJM' size='8.6'>G7_cierre_completo</font>. "
              "La skill del líder técnico lo mencionaba desde la primera versión del framework — pero "
              "<b>nunca existió en gates.yaml</b>. Estuvo dos versiones sin que nadie lo notara, "
              "precisamente porque nada lo comprobaba. Ese es el argumento entero de la sección, en un "
              "caso real.", AZUL),
      Spacer(1, 6),
      P("Por qué cada artículo lleva su razón escrita", 'h2'),
      P("Un límite sin razón se cruza en cuanto estorba, y siempre estorba en el peor "
        "momento. El artículo 4 es el ejemplo: el coste de un despliegue tardío es "
        "visible y acotado; el de uno que rompe algo estable es difuso, tarda en "
        "aparecer y lo paga gente que no participó en la decisión. Esa asimetría no se "
        "percibe al decidir. Por eso la regla tiene que estar escrita <b>antes</b>.", 'p'),
      Spacer(1, 4),
      P("Los artículos 1, 2, 3 y 6 son el núcleo. Un equipo que necesite retirar alguno "
        "probablemente necesita otro framework, no este con menos artículos. El comando "
        "<font face='DJM' size='8.6'>/constitucion</font> avisa explícitamente cuando un "
        "cambio propuesto debilita uno de ellos.", 'p')]

E += [PageBreak(), P("5 · Por qué sirve para reusar", 'h1')]
E += FIG(f"{IMG}/g3.png", 128,
         "Figura 3 — Un catálogo, muchos equipos. Las mismas instrucciones, "
         "distintos umbrales. El pin por SHA del submódulo significa que ningún "
         "equipo recibe un cambio de procedimiento sin un commit propio.")

E += [P("Tres equipos con perfiles de riesgo distintos —uno de pagos, uno de "
        "herramientas internas, uno de datos— comparten los ocho procedimientos "
        "sin discutirlos. Lo que negocian es su <font face='DJM' size='8.6'>gates.yaml</font>: "
        "el de pagos exige cobertura alta y tolera solo hallazgos bajos; el de "
        "herramientas internas es más laxo. Mismas instrucciones, distinta exigencia.", 'p'),
      P("La alternativa —copiar las skills al repo de cada equipo— se descarta porque "
        "las copias divergen en semanas y después nadie sabe cuál es la buena. Con el "
        "submódulo, la actualización es explícita: un commit que dice «subimos el "
        "catálogo de v1.1.0 a v1.2.0», y ahí queda registrado cuándo cambió la forma "
        "de trabajar del equipo.", 'p')]

E += [PageBreak()]

# ============================ 5. ADVERSARIAL =================================
E += [P("6 · Verificación adversarial", 'h1'),
      P("Es el mecanismo que más precisión aporta, y no es un control de seguridad: "
        "es un control de <b>exactitud</b>. Un agente que produce un artefacto y luego "
        "lo revisa tiene el mismo punto ciego en ambos pasos.", 'p'),
      P("El obstáculo a resolver primero: <b>no se puede verificar prosa</b>. Un "
        "revisor enfrentado a párrafos solo puede opinar. Por eso cada rol emite, "
        "además de su artefacto, un archivo de <b>afirmaciones</b>: conclusiones "
        "discretas, cada una con dónde comprobarla.", 'p')]

E += FIG(f"{IMG}/g4.png", 162,
         "Figura 4 — Ciclo de verificación. El verificador recibe las afirmaciones y "
         "el código. Nunca el razonamiento del autor.")

E += [CODE([
    '{ "id": "AF-01",',
    '  "tipo": "codigo",',
    '  "referencia": "src/consumidor/reintentos.py:47",',
    '  "texto": "El backoff exponencial tiene tope de 30 segundos",',
    '  "criticidad": "bloqueante" }',
])]

E += [P("El verificador abre ese archivo, y encuentra que la línea 52 aplica jitter "
        "hasta 1.5x. Veredicto: <font face='DJM' size='8.6'>CORREGIDO — máximo "
        "efectivo 45 s</font>. Es el tipo de imprecisión que un agente autoevaluándose "
        "nunca encuentra, porque ya «sabe» lo que escribió.", 'p'),
      P("Los tres invariantes", 'h2'),
      LI("<b>Autor y verificador son agentes distintos</b>, y el verificador no ve el "
         "razonamiento del autor. Solo las afirmaciones y el código."),
      LI("<b>La carga de la prueba se invierte.</b> La instrucción no es «revisa si "
         "está bien», es «desmiente esto; si no puedes, confírmalo con la evidencia "
         "que te lo impidió»."),
      LI("<b>El veredicto es cerrado</b>: VERIFICADO, CORREGIDO o RECHAZADO. "
         "«Parece correcto pero» no sirve para decidir."),
      Spacer(1, 6),
      CALLOUT("El aislamiento no es negociable",
              "El verificador es el mismo modelo con el mismo entrenamiento. Si le entregas el "
              "razonamiento del autor, no verifica: lo reformula. El framework gana una firma de "
              "aprobación sin ganar precisión, lo cual es <b>peor que no verificar</b> — produce "
              "confianza infundada en algo que nadie comprobó. Por eso el subagente verificador "
              "tiene solo herramientas de lectura y su prompt le prohíbe leer los handoffs.", ROJO)]

E += [Spacer(1, 8),
      P("Lo que este mecanismo NO resuelve", 'h2'),
      P("Verificador y autor comparten modelo. El aislamiento de contexto mitiga el "
        "sesgo compartido; no lo elimina. Si ambos recuerdan mal la misma API, los dos "
        "se equivocan igual. Un lote donde todo sale VERIFICADO no significa que esté "
        "todo bien: significa que las referencias resuelven y dicen lo que se afirmó. "
        "Eso es bastante más de lo que había antes, y bastante menos que una garantía. "
        "<b>El gate no sustituye la revisión humana: la enfoca.</b>", 'p')]

E += [PageBreak()]

# ============================ 6. CÓMO SE MODIFICA ============================
E += [P("7 · Cómo se modifica el framework", 'h1'),
      P("Esta sección es la que hay que leer para adoptarlo. La pregunta siempre es la "
        "misma: <b>¿qué archivo toco para conseguir este cambio?</b>", 'p')]

E += FIG(f"{IMG}/g5.png", 118,
         "Figura 5 — Mapa de personalización. Verde: cambios rutinarios en tu propio "
         "repo. Ámbar: cambio estructural. Rojo: afecta a todos los equipos y va por PR.")

E += [P("7.1 · Los cambios rutinarios", 'h2'),
      P("Cinco cosas cubren el 90% de lo que un equipo necesita ajustar, y todas "
        "están en su propio repo.", 'p'),
      TABLA([
        ["Quiero...", "Toco", "Qué cambio ahí"],
        ["Exigir más o menos cobertura",
         "contratos/gates.yaml",
         "G4b_cobertura_minima → umbral"],
        ["Tolerar hallazgos de otra severidad",
         "contratos/gates.yaml",
         "G5b → severidad_maxima"],
        ["Que un gate solo aplique a cambios grandes",
         "contratos/gates.yaml",
         "activo_si: ninguno | indirecto | directo"],
        ["Permitir saltarse un gate con motivo",
         "contratos/gates.yaml",
         "anulable: true"],
        ["Acortar la cadena para correcciones",
         "contratos/roles.yaml",
         "tipos.correccion.cadena"],
        ["Subir o bajar el rigor global",
         "contratos/roles.yaml",
         "verificacion_adversarial.activa_desde_impacto"],
        ["Restringir qué puede ejecutar un agente",
         ".claude/settings.json",
         "permissions.deny / permissions.ask"],
        ["Cambiar el prompt de un rol",
         ".claude/agents/&lt;rol&gt;.md",
         "cuerpo del archivo (ver 7.2)"],
      ], [52*mm, 44*mm, 70*mm], mono_cols=(1,2))]

E += [Spacer(1, 8),
      P("La perilla principal", 'h3'),
      P("Si solo se toca una cosa, que sea esta:", 'p'),
      CODE([
        "# contratos/roles.yaml",
        "verificacion_adversarial:",
        "  activa_desde_impacto: indirecto   # ninguno | indirecto | directo",
      ]),
      P("En <font face='DJM' size='8.6'>ninguno</font> se verifica todo y el ciclo cuesta "
        "aproximadamente el doble. En <font face='DJM' size='8.6'>directo</font> solo se "
        "verifica lo que toca producción. Es el control de rigor contra velocidad, y "
        "conviene empezar en <font face='DJM' size='8.6'>indirecto</font> y moverlo con "
        "datos, no con intuición.", 'p')]

E += [PageBreak(), P("7.2 · Dónde viven los prompts", 'h1'),
      P("Un rol se comporta según tres textos que el agente lee en momentos distintos. "
        "Saber cuál toca cambiar evita el error más común al adoptar el framework: "
        "engordar el prompt con instrucciones que pertenecen a otro sitio.", 'p'),
      TABLA([
        ["Nivel", "Archivo", "Cuándo se lee", "Qué contiene"],
        ["Contrato del repo", "CLAUDE.md",
         "Siempre, en toda sesión",
         "Las reglas que valen para todos los roles: no trabajar sin orden, no dar "
         "contexto al verificador, no poner credenciales en un prompt"],
        ["Prompt del rol", ".claude/agents/&lt;rol&gt;.md",
         "Al invocar ese subagente",
         "Identidad en una frase, herramientas permitidas, la frontera con los roles "
         "vecinos, y la orden de cargar su skill"],
        ["Procedimiento", "&lt;rol&gt;/SKILL.md",
         "Cuando el rol carga la skill",
         "Entrada, salida, pasos, reglas, gates. El grueso del contenido"],
      ], [30*mm, 40*mm, 34*mm, 62*mm], mono_cols=(1,)),
      Spacer(1, 9),
      P("Por qué los prompts son tan cortos", 'h2'),
      P("Los ocho prompts del framework suman 118 líneas entre todos: entre 12 y 23 "
        "cada uno. No es minimalismo por gusto. Un prompt de rol responde solo tres "
        "preguntas —quién eres, qué NO haces, qué skill cargas— y todo lo demás vive "
        "en la skill, donde puede compartirse entre equipos y versionarse aparte.", 'p'),
      P("El prompt completo del rol SRE, íntegro:", 'p'),
      CODE([
        "---",
        "name: sre",
        "description: Define objetivos de servicio, alertas, runbook y criterio",
        "  de reversión antes del despliegue. Invócalo tras un dictamen favorable.",
        "tools: Read, Grep, Glob, Write, Bash, Skill",
        "---",
        "",
        "Eres el rol SRE. Carga la skill `sre` y síguela.",
        "",
        "Respondes: cuando esto falle en producción, ¿cómo nos enteramos y qué",
        "hacemos?",
        "",
        "Cada alerta apunta a un runbook. El criterio de reversión es numérico,",
        "con ventana. La reversibilidad se prueba en un ambiente no productivo",
        "y se registra: un procedimiento escrito sin ejecutar no es evidencia.",
        "",
        "Los umbrales que fijes se escriben en `contratos/gates.yaml`.",
      ]),
      P("La línea <font face='DJM' size='8.6'>tools:</font> no es decorativa: define "
        "qué herramientas tiene el subagente. El verificador, por ejemplo, no lleva "
        "<font face='DJM' size='8.6'>Write</font> sobre el código — solo lectura y su "
        "carpeta de veredictos. Esa línea es un control real, no una sugerencia.", 'p')]

E += [Spacer(1, 6),
      P("Qué SÍ va en un prompt de rol", 'h2'),
      LI("La identidad y la frontera: «no diseñas, no despliegas»."),
      LI("Las herramientas permitidas, en <font face='DJM' size='8.6'>tools:</font>."),
      LI("Las dos o tres reglas cuya violación rompería el rol entero — por ejemplo, "
         "que el verificador no lea los handoffs."),
      LI("La orden de cargar la skill."),
      Spacer(1, 5),
      P("Qué NO va en un prompt de rol", 'h2'),
      LI("<b>El procedimiento.</b> Va en la skill, que se comparte entre equipos. Un "
         "paso metido en el prompt se pierde para los demás equipos y para el "
         "versionado del catálogo."),
      LI("<b>Umbrales.</b> Van en <font face='DJM' size='8.6'>gates.yaml</font>. "
         "Sigue siendo la regla número uno, y en un prompt es más tentador que nunca."),
      LI("<b>Contexto del proyecto.</b> Va en "
         "<font face='DJM' size='8.6'>CLAUDE.md</font>; si está en cada prompt, hay "
         "ocho copias que se desincronizan."),
      Spacer(1, 6),
      CALLOUT("La prueba antes de tocar un prompt",
              "Si lo que quieres agregar valdría para el mismo rol en otro equipo, va en la "
              "<b>skill</b>. Si es un número, va en <b>gates.yaml</b>. Si vale para todos los roles, "
              "va en <b>CLAUDE.md</b>. Solo lo que queda después de esos tres descartes pertenece "
              "al prompt del rol — y suele ser muy poco.", AZUL)]

E += [PageBreak(), P("7.3 · Agregar un rol", 'h2'),
      P("Cinco pasos. Si el rol nuevo no tiene al menos un gate verificable, "
        "probablemente no es un rol: es una etapa de otro rol.", 'p'),
      LI("<b>Skill</b> en el catálogo, siguiendo <font face='DJM' size='8.6'>AUTHORING.md</font>."),
      LI("<b>Subagente</b> en <font face='DJM' size='8.6'>.claude/agents/</font> que cargue "
         "esa skill y declare sus herramientas."),
      LI("<b>Gates</b> en <font face='DJM' size='8.6'>gates.yaml</font>, con "
         "<font face='DJM' size='8.6'>rol:</font> apuntando al nombre del subagente."),
      LI("<b>Insertar</b> el rol en la cadena correspondiente en "
         "<font face='DJM' size='8.6'>roles.yaml</font>."),
      LI("<b>Actualizar</b> el diagrama de la documentación."),
      Spacer(1, 6),
      P("7.4 · Agregar un gate", 'h2'),
      P("Un gate necesita las cuatro cosas o no es un gate:", 'p'),
      TABLA([
        ["Elemento", "Qué es"],
        ["Nombre", "Estable, referenciado desde el SKILL.md del rol"],
        ["Verificación", "presencia_archivo · comparacion_hash · umbral_numerico · manual"],
        ["Evidencia", "Qué archivo lo demuestra"],
        ["Condición de aborto", "Qué pasa si falla"],
      ], [36*mm, 130*mm]),
      Spacer(1, 5),
      P("Un gate <font face='DJM' size='8.6'>manual</font> es legítimo, pero cada uno "
        "es un punto donde el framework confía en una afirmación en vez de comprobarla. "
        "Manténlos en minoría.", 'p')]

E += [Spacer(1, 6),
      P("7.5 · Lo que NO se toca", 'h2'),
      P("Los <font face='DJM' size='8.6'>SKILL.md</font> del catálogo compartido. Si "
        "aparece la necesidad de editar uno, casi siempre es una de dos cosas:", 'p'),
      LI("<b>Querías cambiar un umbral.</b> Va en "
         "<font face='DJM' size='8.6'>gates.yaml</font>; el catálogo ya lo contempla."),
      LI("<b>Tu equipo tiene un paso que otros no.</b> Proponlo al catálogo como PR, o "
         "agrega una skill local en <font face='DJM' size='8.6'>.claude/skills-locales/</font> "
         "y referénciala desde el subagente."),
      Spacer(1, 4),
      CALLOUT("No edites el submódulo directamente",
              "Un cambio hecho dentro de <font face='DJM' size='8.6'>.claude/skills/</font> "
              "desaparece en el próximo <font face='DJM' size='8.6'>git submodule update</font>, "
              "normalmente sin aviso y en el peor momento. Si el cambio vale para todos, va por PR "
              "al catálogo; si es solo tuyo, va en una skill local.", ROJO)]

# ============================ 8. PORTABILIDAD ================================
E += [PageBreak(), P("8 · Portabilidad entre plataformas", 'h1'),
      P("El mismo repositorio funciona en Claude Code, en Codex y en cualquier agente "
        "que lea <font face='DJM' size='8.6'>AGENTS.md</font>. No hay dos versiones "
        "que mantener: hay una fuente y un generador.", 'p'),
      P("El problema es que cada plataforma lee un archivo distinto. "
        "<font face='DJM' size='8.6'>AGENTS.md</font> se ha vuelto el estándar de "
        "facto —está bajo la Agentic AI Foundation de la Linux Foundation y lo leen "
        "Codex, Cursor, Windsurf y Cline— pero Claude Code sigue leyendo "
        "<font face='DJM' size='8.6'>CLAUDE.md</font>. Mantener ambos a mano garantiza "
        "que diverjan, y el día que alguien cambie un límite en uno y no en el otro, "
        "dos agentes del mismo equipo estarán operando bajo reglas distintas sin que "
        "nadie lo sepa.", 'p')]
E += FIG(f"{IMG}/g7.png", 162,
         "Figura 6 — Una fuente, varios adaptadores. Los archivos generados llevan "
         "marca de generado en la primera línea; editarlos a mano es un cambio que "
         "el siguiente bootstrap borra.")

E += [TABLA([
        ["", "Claude Code", "Codex · Cursor · Windsurf · Cline"],
        ["Instrucciones", "CLAUDE.md", "AGENTS.md"],
        ["Roles", "Subagentes en .claude/agents/", "Descritos en AGENTS.md, se adoptan uno a uno"],
        ["Comandos", "/iniciar · /verificar · /gate", "Se invocan los scripts directamente"],
        ["Skills", ".claude/skills/", "Enlace en ~/.agents/skills"],
        ["Aislamiento del verificador", "Real: subagente de solo lectura",
         "Parcial: exige abrir sesión nueva"],
      ], [40*mm, 55*mm, 71*mm]),
      Spacer(1, 9),
      CALLOUT("La diferencia que importa de verdad",
              "En plataformas sin subagentes, el aislamiento del verificador <b>no se puede simular "
              "con buena voluntad</b>. Si el mismo hilo produce las afirmaciones y luego las verifica, "
              "el verificador ya vio el razonamiento del autor y va a reformularlo, no a comprobarlo. "
              "Por eso <font face='DJM' size='8.6'>AGENTS.md</font> instruye abrir una sesión nueva "
              "para verificar: es menos cómodo y funciona.", ROJO)]


E += [PageBreak(), P("9 · Instalación paso a paso", 'h1'),
      P("Requisitos: <font face='DJM' size='8.6'>git</font>, "
        "<font face='DJM' size='8.6'>python3</font> (3.8+) y "
        "<font face='DJM' size='8.6'>bash</font>. Sin Node, sin Docker, sin servicios "
        "que levantar, sin paquetes que instalar. Diez minutos la primera vez, dos las "
        "siguientes.", 'p'),
      P("9.0 · Publicar los dos repos (una sola vez)", 'h2'),
      CODE([
        "# 1. El catálogo — compartido entre todos los equipos",
        "cd agentic-sdlc-skills",
        "git init && git add -A && git commit -m 'Catálogo v1.2.0'",
        "git tag v1.2.0",
        "git remote add origin <URL-DEL-CATALOGO>",
        "git push -u origin main --tags",
        "",
        "# 2. El framework — cada equipo tendrá el suyo",
        "cd ../agentic-sdlc-framework",
        "git init && git add -A && git commit -m 'Framework v1.2.0'",
        "git submodule add <URL-DEL-CATALOGO> .claude/skills",
        "cd .claude/skills && git checkout v1.2.0 && cd ../..",
        "git add .gitmodules .claude/skills && git commit -m 'Pin v1.2.0'",
        "git remote add origin <URL-DEL-FRAMEWORK> && git push -u origin main",
      ]),
      P("Nada depende de un proveedor Git concreto: si no usas GitHub, cambia la URL.", 'p')]

E += [Spacer(1, 6), P("9.1 · Camino A — Coder", 'h2'),
      P("El caso del equipo destinatario: contenedor con salida solo al servidor Git.", 'p'),
      CODE([
        "# En el main.tf del template, copiar el bloque de coder/main.tf y ajustar:",
        "variable \"framework_repo\" { default = \"<URL-DEL-FRAMEWORK>\" }",
        "variable \"framework_ref\"  { default = \"v1.2.0\" }   # pinear, nunca main",
        "",
        "coder templates push <nombre-del-template>",
      ]),
      P("Al arrancar el workspace, el script clona con submódulos y corre "
        "<font face='DJM' size='8.6'>bootstrap.sh</font> solo. No hay paso manual. "
        "Comprobar con <font face='DJM' size='8.6'>./scripts/prueba-humo.sh</font>.", 'p'),
      Spacer(1, 4),
      CALLOUT("Antes de llevarlo a producción",
              "Crea un template <b>aparte</b> para el rol de despliegue, con las credenciales "
              "productivas y una allowlist de red más estrecha. El template general no debe tenerlas "
              "nunca — es el artículo 6 de la constitución aplicado a la infraestructura.", AZUL)]

E += [PageBreak(), P("9.2 · Camino B — Claude Code", 'h2'),
      CODE([
        "git clone --recurse-submodules <URL-DEL-FRAMEWORK>",
        "cd agentic-sdlc-framework",
        "./scripts/bootstrap.sh",
        "claude",
      ]),
      P("Claude Code lee <font face='DJM' size='8.6'>CLAUDE.md</font> al arrancar y "
        "descubre solo los subagentes y los comandos. Comprueba con "
        "<font face='DJM' size='8.6'>/constitucion</font>: debe listar los siete "
        "artículos y confirmar que todos tienen gate.", 'p'),
      P("Si ya lo habías clonado sin submódulos: "
        "<font face='DJM' size='8.6'>git submodule update --init --recursive</font>.", 'p'),
      Spacer(1, 5),
      P("9.3 · Camino C — Codex", 'h2'),
      CODE([
        "git clone --recurse-submodules <URL-DEL-FRAMEWORK>",
        "cd agentic-sdlc-framework && ./scripts/bootstrap.sh",
        "",
        "# si tu Codex busca skills en otra ruta:",
        "mkdir -p ~/.agents && ln -sfn \"$(pwd)/.claude/skills\" ~/.agents/skills",
        "",
        "codex",
      ]),
      P("Codex lee <font face='DJM' size='8.6'>AGENTS.md</font>, generado de la misma "
        "fuente que <font face='DJM' size='8.6'>CLAUDE.md</font>. Como no tiene "
        "subagentes, los roles se adoptan uno a uno:", 'p'),
      CODE([
        "Actúa como lider-tecnico según AGENTS.md.",
        "Solicitud: agregar reintentos con backoff al consumidor de eventos.",
      ]),
      P("Los comandos slash no existen aquí; se invocan los scripts directamente "
        "(<font face='DJM' size='8.6'>./scripts/verificar-gates.sh</font>, "
        "<font face='DJM' size='8.6'>./scripts/validar-salida.sh</font>).", 'p'),
      Spacer(1, 4),
      CALLOUT("La única parte que no se puede improvisar",
              "Para verificar, <b>abre una sesión nueva</b>. Si verificas en el mismo hilo, el "
              "verificador ya vio el razonamiento del autor y va a reformularlo en vez de "
              "comprobarlo. Es incómodo y es lo que hace que el veredicto valga algo.", ROJO),
      Spacer(1, 5),
      P("9.4 · Camino D — Cursor, Windsurf, Cline", 'h2'),
      P("Clonar y correr <font face='DJM' size='8.6'>bootstrap.sh</font> igual que en B. "
        "Los tres auto-descubren <font face='DJM' size='8.6'>AGENTS.md</font> en la raíz "
        "y lo cargan en su motor de reglas: no hay configuración adicional. A partir de "
        "ahí, igual que Codex — roles uno a uno y sesión nueva para verificar.", 'p')]

E += [PageBreak(), P("9.5 · Paso final, común a todos", 'h2'),
      CODE([
        "$EDITOR contratos/gates.yaml    # los dos umbrales marcados AJUSTAR",
        "$EDITOR contratos/roles.yaml    # activa_desde_impacto",
        "",
        "./scripts/verificar-constitucion.sh",
        "./scripts/prueba-humo.sh        # -> 15 correcto(s), 0 fallo(s)",
        "",
        "git add -A && git commit -m 'Umbrales del equipo'",
      ]),
      Spacer(1, 5),
      P("Solución de problemas", 'h2'),
      TABLA([
        ["Síntoma", "Causa", "Salida"],
        ["catálogo de skills no montado", "Clonado sin --recurse-submodules",
         "git submodule update --init --recursive"],
        ["CONSTITUCIÓN NO EXIGIBLE", "Un artículo cita un gate inexistente",
         "Agregar el gate o corregir la cita"],
        ["el submódulo NO está en el SHA pinneado", "Alguien lo movió a mano",
         "git submodule update --init"],
        ["El agente ignora los roles", "Editaste CLAUDE.md o AGENTS.md a mano",
         "Editar roles/ y regenerar adaptadores"],
        ["bloqueante no_verificable rechazada", "Afirmación sin referencia comprobable",
         "Añadir ruta:linea o bajar a informativa"],
      ], [50*mm, 56*mm, 60*mm])]

E += [PageBreak(), P("10 · Adopción organizativa", 'h1'),
      P("Requisitos: un contenedor con un agente CLI que lea "
        "<font face='DJM' size='8.6'>.claude/</font>, "
        "<font face='DJM' size='8.6'>git</font>, "
        "<font face='DJM' size='8.6'>python3</font> y salida de red hacia el "
        "servidor Git. Nada más — sin servicios, sin registro de paquetes, sin "
        "dependencias que instalar.", 'p'),
      TABLA([
        ["#", "Paso", "Resultado"],
        ["1", "Publicar los dos repos: catálogo y framework",
         "El catálogo se comparte; el framework se forkea por equipo"],
        ["2", "Enganchar el submódulo y pinearlo a un tag",
         "El equipo controla cuándo cambia su procedimiento"],
        ["3", "Ajustar gates.yaml y roles.yaml",
         "Los umbrales pasan a ser los del equipo"],
        ["4", "Separar el entorno con credenciales productivas",
         "Solo el rol de despliegue las tiene"],
        ["5", "Correr ./scripts/prueba-humo.sh",
         "15 comprobaciones: contratos, constitución, validadores, adaptadores"],
        ["6", "Correr una orden de punta a punta en un cambio real y pequeño",
         "El equipo ve la cadena completa antes de confiar en ella"],
      ], [8*mm, 76*mm, 82*mm]),
      Spacer(1, 8),
      CALLOUT("El aislamiento va en la infraestructura, no en el prompt",
              "El rol de despliegue debe correr en un entorno distinto, con las credenciales "
              "productivas y una allowlist de red más estrecha. Un prompt puede decir «no toques "
              "producción» y el modelo puede cumplirlo casi siempre. <b>Casi siempre no es una "
              "garantía.</b> Si el contenedor no tiene la credencial, no hay nada que cumplir.", AZUL)]

E += [Spacer(1, 8),
      P("Primera corrida", 'h2'),
      CODE([
        "git clone --recurse-submodules <repo-del-framework>",
        "cd agentic-sdlc-framework && ./scripts/bootstrap.sh",
        "",
        "/iniciar   Agregar reintentos al consumidor de eventos",
        "/verificar            # verificación adversarial del rol que terminó",
        "/gate                 # qué falta para que la cadena avance",
        "/constitucion         # los límites, y si siguen siendo exigibles",
      ]),
      P("Elige para la primera corrida un cambio real pero pequeño, con impacto "
        "declarado <font face='DJM' size='8.6'>indirecto</font>. Un cambio grande hace "
        "que el equipo culpe al framework de la fricción propia del cambio; uno "
        "trivial no activa suficientes gates como para que se vea el valor.", 'p')]

E += [PageBreak()]

# ============================ 8. LÍMITES =====================================

E += [P("11 · Fuentes y créditos", 'h1'),
      P("Este framework no se inventó de cero. Se ensambló a partir de trabajo público "
        "de otros, y esta sección dice qué se tomó de dónde, bajo qué licencia, y —tan "
        "importante como lo anterior— qué se evaluó y se descartó, con la razón. Eso "
        "último evita que el siguiente equipo repita la evaluación.", 'p')]
E += FIG(f"{IMG}/g8.png", 130,
         "Figura 7 — De cada fuente, lo que se tomó. En rojo, lo evaluado y descartado.")

E += [P("Lo que se adoptó", 'h2'),
      TABLA([
        ["Fuente", "Licencia", "Qué se tomó"],
        ["Formato Agent Skills", "Formato abierto",
         "La estructura del catálogo. Es la razón de que no quede atado a una plataforma."],
        ["cloudflare/security-audit-skill", "MIT",
         "El rol adversarial separado, la evidencia validada por esquema, y los criterios "
         "de severidad con impacto obligatorio."],
        ["github/spec-kit", "MIT",
         "El concepto de constitución del proyecto."],
        ["AGENTS.md (Linux Foundation)", "Convención abierta",
         "El formato como destino de generación multiplataforma."],
        ["Coder", "Producto comercial",
         "El modelo de template declarativo, y el argumento de que los controles de "
         "seguridad no viven en el prompt — que es el artículo 6."],
      ], [42*mm, 26*mm, 98*mm]),
      Spacer(1, 8),
      P("Dónde nos separamos de las fuentes", 'h2'),
      P("<b>Frente a Cloudflare.</b> Su patrón adversarial funciona porque cada hallazgo "
        "de seguridad trae <font face='DJM' size='8.6'>file:line</font>. Generalizarlo a "
        "todos los roles obligó a inventar el archivo de <b>afirmaciones</b>, porque no "
        "se puede verificar prosa. Ese fue el trabajo propio.", 'p'),
      P("<b>Frente a spec-kit.</b> Allí la constitución son principios en prosa. Aquí "
        "cada artículo debe nombrar los gates que lo comprueban y un script lo verifica. "
        "Además, spec-kit es <i>horizontal</i> —las fases de construir una feature— y "
        "esto es <i>vertical</i> —quién tiene autoridad sobre qué—. No son alternativas: "
        "spec-kit puede vivir <b>dentro</b> de los roles de arquitecto y constructor.", 'p')]

E += [Spacer(1, 6), P("Lo que se evaluó y se descartó", 'h2'),
      P("<font face='DJM' size='8.6'>betta-tech/agentic-patterns-typescript</font> — "
        "ejemplos de patrones agénticos (pipeline, router, reflexión, "
        "orquestador-trabajadores) en TypeScript.", 'p'),
      LI("<b>Capa equivocada.</b> Construye agentes <i>en código</i>, llamando a una API "
         "desde Node. Este framework no ejecuta agentes: los ejecuta el CLI del "
         "workspace. Adoptarlo significaría un servicio que mantener."),
      LI("<b>Red.</b> Necesita instalar paquetes; el contenedor destino solo alcanza el "
         "servidor Git."),
      LI("<b>Sin licencia declarada</b> en el repositorio, lo que por sí solo impide "
         "adoptarlo en un entorno corporativo."),
      Spacer(1, 4),
      P("Sí aportó una idea: su patrón <i>router</i> es conceptualmente el mismo que el "
        "líder técnico —clasificar primero, activar un único especialista después, "
        "derivar a humano con baja confianza—. Eso reforzó la regla de bloqueo hacia el "
        "líder técnico. Ideas de diseño, no código.", 'p')]

E += [Spacer(1, 8), P("Lo que es original de este framework", 'h2'),
      LI("La separación en <b>siete roles</b> con contratos de handoff y frontera explícita."),
      LI("Los <b>gates como dato</b>, con <font face='DJM' size='8.6'>activo_si</font> y "
         "<font face='DJM' size='8.6'>anulable</font>."),
      LI("El archivo de <b>afirmaciones verificables</b>, que hace posible generalizar la "
         "verificación adversarial fuera del dominio de seguridad."),
      LI("La regla de que <b>cada artículo de la constitución nombre sus gates</b>, con "
         "script que lo comprueba."),
      LI("La <b>capa de portabilidad</b>: fuente neutra más generador de adaptadores."),
      LI("El estándar de autoría de skills."),
      Spacer(1, 6),
      P("Ninguna de las fuentes MIT se redistribuye aquí: se tomaron patrones e ideas, "
        "reescritos. Si en el futuro se incorpora código de alguna de ellas, hay que "
        "incluir su aviso de copyright.", 'p')]


E += [PageBreak(), P("12 · Costo, caché y medición", 'h1'),
      P("Una orden completa son siete invocaciones de rol más las pasadas del "
        "verificador: <b>alrededor de trece llamadas donde antes había una</b>. Cada "
        "una vuelve a pagar el contexto fijo. Frente a un agente suelto haciendo la "
        "misma tarea, la relación realista está entre 3x y 6x, no en el doble.", 'p'),
      P("Eso es corregible sin tocar la arquitectura, y la palanca es grande.", 'p'),
      P("12.1 · La frontera de caché", 'h2'),
      P("El proveedor reutiliza el cómputo del prefijo idéntico de una petición. La "
        "medición pública de referencia sobre más de 500 sesiones agénticas: cachear "
        "reduce el costo de API entre <b>41% y 80%</b> y mejora el time-to-first-token "
        "entre 13% y 31%. El matiz importa: cachear solo el contexto estable rinde más "
        "que cachear todo, que puede incluso aumentar la latencia.", 'p')]
E += FIG(f"{IMG}/g9.png", 108,
         "Figura 8 — Frontera de caché. Estable arriba, volátil abajo. El framework "
         "ya tenía esta separación por otras razones; declararla la vuelve accionable.")

E += [P("La separación no hubo que inventarla: constitución, gates, prompt de rol y "
        "skill son estables por diseño; handoffs, evidencia y código son volátiles. "
        "Está declarada en <font face='DJM' size='8.6'>contratos/contexto.yaml</font>, "
        "con dos consecuencias operativas: hay un mínimo de tokens por debajo del cual "
        "la caché no compensa, y una ventana de reutilización — <b>partir una orden en "
        "varios días paga el prefijo cada vez</b>.", 'p'),
      Spacer(1, 6),
      P("12.2 · Mover del agente al script", 'h2'),
      P("Este es el ahorro propio del framework, y es del 100% en lo que cubre, no del "
        "80%. Antes de invocar al verificador, "
        "<font face='DJM' size='8.6'>resolver-referencias.sh</font> comprueba sin gastar "
        "un token que cada referencia resuelve —el archivo existe, la línea está en "
        "rango, el ejecutable está disponible— y <b>extrae el contenido citado</b>.", 'p'),
      P("Dos efectos. Una referencia rota ya es CORREGIDO o RECHAZADO sin invocar a "
        "nadie. Y cuando todas resuelven, el verificador recibe las líneas ya "
        "extraídas: le queda el juicio, no la búsqueda.", 'p'),
      Spacer(1, 4),
      CALLOUT("La regla general",
              "Toda comprobación que un script pueda hacer es una que el agente no debe hacer. "
              "Los cuatro gates marcados <font face='DJM' size='8.6'>manual</font> que quedan son "
              "la lista de trabajo pendiente en esta dirección: cada uno es un agente haciendo "
              "aritmética que sale gratis en bash.", VERDE)]

E += [PageBreak(), P("12.3 · Medir en vez de opinar", 'h2'),
      P("La pregunta «¿es eficiente?» no tiene respuesta hoy en ningún equipo que no "
        "instrumente. Es exactamente el vacío que motivó a la Linux Foundation a "
        "anunciar la Tokenomics Foundation en junio de 2026, en alianza con la FinOps "
        "Foundation: no existía un lugar neutral para definir cómo se mide la eficiencia "
        "de tokens, y el trabajo incluye extender la especificación FOCUS de FinOps al "
        "gasto basado en tokens.", 'p'),
      P("Mientras esos estándares maduran, el framework registra lo mínimo indispensable:", 'p'),
      CODE([
        "./scripts/registrar-costo.sh <orden> <rol> <in> <out> <cacheados>",
        "./scripts/reporte-costo.sh      #  o  /costo",
      ]),
      P("El reporte da dos números que hay que leer juntos:", 'p'),
      TABLA([
        ["Número", "Qué significa", "Qué hacer si sale mal"],
        ["% de prefijo reutilizado",
         "Cuánto está funcionando la caché",
         "Por debajo del 50%, hay contenido volátil colado en el prefijo estable"],
        ["Tasa de hallazgo de la verificación",
         "Qué proporción de afirmaciones resultó tener algo mal",
         "Si es cero tras varias órdenes, lo más probable es que el verificador esté "
         "recibiendo contexto del autor y solo confirme"],
      ], [40*mm, 52*mm, 74*mm]),
      Spacer(1, 8),
      CALLOUT("Lo que este documento NO afirma",
              "No hay medición propia de que el framework mejore la precisión. El argumento es de "
              "diseño —separar quien afirma de quien comprueba— y hay una anécdota a favor: el "
              "verificador de la constitución encontró un gate roto que llevaba dos versiones sin "
              "detectarse. <b>Una anécdota no es una tasa.</b> La tasa de hallazgo del reporte es "
              "precisamente el número que convierte esa creencia en dato, y hay que dejar correr "
              "diez órdenes reales antes de defender nada.", ROJO),
      Spacer(1, 8),
      P("12.4 · Dónde no usarlo", 'h2'),
      P("Un cambio trivial, un prototipo, una exploración. Para eso existe "
        "<font face='DJM' size='8.6'>activa_desde_impacto</font>. Un equipo que lo deje "
        "en <font face='DJM' size='8.6'>ninguno</font> y lo aplique a todo va a odiarlo "
        "en dos semanas, con razón.", 'p'),
      P("Y la comparación justa no es «framework contra agente suelto», sino «framework "
        "contra agente suelto <b>más</b> el tiempo humano de revisar lo que produjo». Si "
        "hoy nadie revisa nada, el framework es puro costo añadido. Si alguien revisa, "
        "ahí empieza a pagarse.", 'p')]


E += [PageBreak(), P("13 · Ingeniería de contexto", 'h1'),
      P("El eje que faltaba. Las guías anteriores cubren cómo se <i>estructura</i> una "
        "skill y qué <i>sale</i> de ella. Esta cubre qué <b>entra</b> antes de que "
        "corra — porque una skill impecable con el contexto equivocado produce una "
        "respuesta impecable y equivocada, que es peor que una mala: nadie la revisa.", 'p'),
      P("El cambio de pregunta: la ingeniería de prompt pregunta <i>¿cómo lo escribo?</i> "
        "y si falla, reformulas. La ingeniería de contexto pregunta <i>¿qué necesita "
        "saber el modelo ahora?</i> y si falla, revisas de dónde salió la información. "
        "Uno es redacción; el otro, arquitectura.", 'p')]
E += FIG(f"{IMG}/g11.png", 130,
         "Figura 9 — Las cuatro decisiones y su pregunta de auditoría. Aplicar solo "
         "una arregla la cuarta parte del problema.")

E += [P("13.1 · La tensión que había que resolver", 'h2'),
      P("Dos optimizaciones que tirábamos en direcciones opuestas sin darnos cuenta:", 'p'),
      LI("<b>La caché</b> exige que lo estable vaya <b>primero</b>: el proveedor "
         "reutiliza el cómputo del prefijo idéntico."),
      LI("<b>La atención</b> exige que lo importante vaya al principio <b>o al final</b>. "
         "La misma información rinde 70–75% de exactitud en los extremos y 55–60% en la "
         "mitad — quince a veinte puntos solo por la posición."),
      Spacer(1, 4),
      P("Puestas juntas mal, el prefijo estable empuja la tarea real hacia la mitad —la "
        "peor posición— y se gana en costo lo que se pierde en exactitud. La versión "
        "anterior de este framework tenía exactamente ese defecto.", 'p')]
E += FIG(f"{IMG}/g10.png", 150,
         "Figura 10 — Tres zonas en vez de dos. El ancla ocupa el inicio (cacheada y "
         "bien posicionada), la tarea el final, y el volumen de baja señal el medio, "
         "donde menos daño hace.")

E += [CALLOUT("La regla que hace que funcione",
              "Nunca escribas nada después de la zona filo. Ni un recordatorio, ni un «responde en "
              "formato X», ni una repetición de las reglas. Cualquier coletilla empuja la tarea al "
              "medio y la degrada. Si una restricción es crítica y hay que repetirla, va en la zona "
              "ancla —donde ya está cacheada y bien posicionada—, no como cierre.", VERDE)]

E += [PageBreak(), P("13.2 · Presupuesto de contexto", 'h2'),
      P("Lo que no se mide, crece. El mapa por rol:", 'p'),
      CODE(["./scripts/mapa-contexto.sh <rol>      #  o  /contexto"]),
      P("La primera corrida sobre este mismo framework dio un resultado útil: la zona "
        "ancla pesa unas 1.800 palabras, de las cuales <b>el 80% es constitución más "
        "gates</b> y el prompt del rol apenas el 8%. La parte compartida se cachea una "
        "vez, así que el diseño es correcto — pero deja claro que si algo hay que podar, "
        "es la constitución, no los prompts.", 'p'),
      TABLA([
        ["Señal", "Qué significa"],
        ["El historial supera el 60%", "Nadie lo administra; falta recencia"],
        ["Más de 20 herramientas declaradas", "Un benchmark citado: falló con 46, funcionó con 19"],
        ["La zona ancla crece versión tras versión", "Nadie ha corrido la pregunta de relevancia"],
        ["Documentos precargados «por si acaso»", "Candidatos a recuperación bajo demanda"],
      ], [62*mm, 104*mm]),
      Spacer(1, 8),
      P("Un detalle que sorprende: <b>las definiciones de herramientas ocupan contexto "
        "aunque no se usen.</b> Un rol con cuarenta declaradas y seis en uso paga las "
        "cuarenta en cada mensaje.", 'p'),
      Spacer(1, 6),
      P("13.3 · La crítica que esto le hace al framework", 'h2'),
      P("La pregunta de relevancia —<i>si quito esta línea, ¿cambia alguna respuesta?</i>— "
        "no se ha corrido nunca sobre este documento ni sobre la constitución. La "
        "tendencia natural de todo framework es acumular instrucciones, y la evidencia "
        "apunta en contra: Anthropic recortó más del 80% del system prompt de su "
        "herramienta de código para los modelos Claude 5, y el benchmark de herramientas "
        "muestra que quitar capacidades puede mejorar el resultado.", 'p'),
      P("Es trabajo pendiente reconocido, no una sugerencia.", 'p'),
      Spacer(1, 6),
      CALLOUT("Procedencia de las cifras de esta sección",
              "Provienen de material formativo sobre ingeniería de contexto y <b>no han sido "
              "verificadas de forma independiente</b> por este framework. Trátalas como órdenes de "
              "magnitud que orientan una decisión de diseño, no como constantes. El diseño de tres "
              "zonas se sostiene aunque las cifras difieran, porque la dirección del efecto —los "
              "extremos rinden más que el medio— está bien establecida.", AZUL)]

E += [P("14 · Límites conocidos", 'h1'),
      P("Un framework que solo enumera sus virtudes es difícil de adoptar bien, porque "
        "el equipo descubre los límites en producción en vez de en la evaluación. "
        "Estos son los que se conocen.", 'p'),
      P("<b>Es secuencial a propósito.</b> No hay ejecución en paralelo. El valor está "
        "en la trazabilidad, no en la velocidad. Un equipo que necesite throughput por "
        "encima de auditabilidad debería mirar otra cosa.", 'p'),
      P("<b>Verificador y autor comparten modelo.</b> Ya tratado en la sección 5. El "
        "aislamiento de contexto mitiga el sesgo compartido; no lo elimina.", 'p'),
      P("<b>Los gates manuales son un acto de fe.</b> Cuatro de los gates de referencia "
        "se marcan <font face='DJM' size='8.6'>manual</font>: el framework confía en "
        "que el agente los evaluó. Convertirlos en verificables por script es la vía "
        "de mejora más rentable que queda abierta.", 'p'),
      P("<b>No impide trabajar por fuera.</b> Cualquiera puede hacer el cambio sin pasar "
        "por la cadena. Lo que impide es que ese trabajo pase por certificado.", 'p'),
      P("<b>Cuesta más.</b> Entre 3x y 6x frente a un agente suelto, antes de aplicar "
        "caché. Ver la sección 12 para las mitigaciones y para cómo medirlo en tu "
        "propio equipo en vez de creerse esta cifra.", 'p'),
      P("<b>La precisión no está medida.</b> El argumento a favor es de diseño, no "
        "empírico. Es el límite más importante de esta lista.", 'p')]

E += [Spacer(1, 10),
      P("15 · Resumen de una página", 'h1'),
      TABLA([
        ["Pregunta", "Respuesta"],
        ["¿Qué hace reutilizable el framework?",
         "Los procedimientos son compartidos; los umbrales son de cada equipo. "
         "Ningún número vive dentro de una instrucción."],
        ["¿Qué toca un equipo al adoptarlo?",
         "gates.yaml y roles.yaml. Casi siempre nada más."],
        ["¿Qué no debe tocar nunca?",
         "Los SKILL.md del catálogo compartido, ni el submódulo directamente."],
        ["¿Qué hace que los gates funcionen?",
         "Que son datos leídos por un script, no instrucciones en un prompt."],
        ["¿Qué aporta el verificador adversarial?",
         "Precisión. Separa quien afirma de quien comprueba, e invierte la carga "
         "de la prueba."],
        ["¿Cuánto cuesta de más?",
         "3x–6x frente a un agente suelto, antes de caché. Con la frontera de caché "
         "declarada, entre 41% y 80% de eso se recupera."],
        ["¿Dónde va cada cosa en la ventana?",
         "Tres zonas: ancla (estable, se cachea), volumen (al medio), filo (la tarea, "
         "siempre al final). Nada después del filo."],
        ["¿Cuál es la única perilla que hay que entender?",
         "verificacion_adversarial.activa_desde_impacto — rigor contra velocidad."],
        ["¿Qué NO se ajusta nunca?",
         "La constitución. Siete artículos, cada uno con los gates que lo comprueban."],
        ["¿Funciona fuera de Claude Code?",
         "Sí. Una fuente neutra genera CLAUDE.md y AGENTS.md; el segundo lo leen "
         "Codex, Cursor, Windsurf y Cline."],
        ["¿Sustituye la revisión humana?",
         "No. La enfoca: muestra qué falta y qué no se pudo comprobar."],
      ], [56*mm, 110*mm])]

doc.build(E)
print("PDF generado")
