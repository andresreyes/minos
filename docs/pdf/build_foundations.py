#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF de fundamentos — compañero de framework.pdf, mismo estilo."""

from estilo import *  # noqa: F401,F403

TITULO = "Fundamentos · Trabajar con agentes"


def marco(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRISCL); canvas.setLineWidth(0.5)
    canvas.line(22*mm, 275*mm, 188*mm, 275*mm)
    canvas.setFont("DJ", 7.6); canvas.setFillColor(GRIS)
    canvas.drawString(22*mm, 278*mm, TITULO)
    canvas.drawRightString(188*mm, 278*mm, "Compañero de la Guía del Framework SDLC Agéntico")
    canvas.line(22*mm, 17*mm, 188*mm, 17*mm)
    canvas.drawString(22*mm, 12*mm, "Documento reutilizable — sin datos de organización")
    canvas.setFont("DJB", 8.4); canvas.setFillColor(AZUL)
    canvas.drawRightString(188*mm, 12*mm, str(doc.page - 1))
    canvas.restoreState()


def portada_fondo(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(VERDE)
    canvas.rect(0, 246*mm, 210*mm, 51*mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#F0F4F8"))
    canvas.rect(0, 0, 210*mm, 26*mm, stroke=0, fill=1)
    canvas.restoreState()


doc = BaseDocTemplate("fundamentos.pdf", pagesize=A4,
                      leftMargin=22*mm, rightMargin=22*mm,
                      topMargin=26*mm, bottomMargin=22*mm,
                      title="Fundamentos - Trabajar con agentes",
                      author="Guia de fundamentos")

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

# ---------------- PORTADA ----------------
E += [Spacer(1, 13*mm),
      P("Fundamentos", 'portada_t'),
      Spacer(1, 5*mm),
      P("Trabajar con agentes: prompt, contexto y sistema", 'portada_s'),
      Spacer(1, 20*mm)]

res = Table([[[
    P("<b>Para quién</b>", 'h3'),
    P("Cualquiera que trabaje con agentes, use o no el framework. Es el documento de "
      "entrada: los fundamentos que sostienen todo lo demás, sin depender de ninguna "
      "herramienta concreta.", 'p'),
    P("<b>Qué resuelve</b>", 'h3'),
    P("La confusión entre tres oficios distintos —redactar el prompt, decidir el "
      "contexto, diseñar el sistema— que hace que la gente intente arreglar con "
      "redacción un problema de arquitectura. Y da las tres técnicas concretas contra "
      "la respuesta inventada.", 'p'),
]]], colWidths=[152*mm])
res.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 0.6, GRISCL),
    ('LINEBEFORE', (0,0), (0,-1), 3, VERDE),
    ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12),
]))
E += [res, NextPageTemplate('normal'), PageBreak()]

# ---------------- 1 ----------------
E += [P("1 · Los tres niveles", 'h1'),
      P("Hay tres oficios distintos que se confunden todo el tiempo. Confundirlos hace "
        "que la gente reformule veinte veces algo que fallaba por falta de información.", 'p'),
      TABLA([
        ["Nivel", "Pregunta", "Si falla"],
        ["Prompt", "¿Cómo lo escribo?", "Reformulas"],
        ["Contexto", "¿Qué necesita saber ahora?", "Revisas de dónde salió la información"],
        ["Sistema", "¿Quién decide y con qué evidencia?", "Revisas quién tenía autoridad para aprobarlo"],
      ], [26*mm, 62*mm, 78*mm]),
      Spacer(1, 8),
      P("Los tres hacen falta. Un prompt impecable con el contexto equivocado produce "
        "una respuesta impecable y equivocada — y esa no la revisa nadie, porque se ve "
        "bien.", 'p')]

E += [Spacer(1, 6), P("2 · Cómo funciona por dentro", 'h1'),
      P("Lo mínimo que hay que entender para que el resto tenga sentido.", 'p'),
      P("Las palabras tienen ubicación", 'h2'),
      P("Un modelo asigna a cada palabra una posición en un espacio de muchas "
        "dimensiones, donde la cercanía representa cercanía de significado. "
        "<i>Rey</i> está cerca de <i>reina</i>; <i>hospital</i>, de <i>médico</i>. "
        "Tanto que la aritmética funciona: <font face='DJM' size='8.6'>rey − hombre + "
        "mujer</font> cae donde está <i>reina</i>.", 'p'),
      P("<b>Por qué importa:</b> cada palabra que escribes mueve la atención hacia una "
        "región de ese espacio. No estás dando instrucciones a un programa; estás "
        "eligiendo desde qué zona del conocimiento va a responder.", 'p'),
      P("De ahí una recomendación poco obvia: <b>escribe en tu lengua nativa</b>. En un "
        "idioma que no dominas se pierden sutilezas y matices culturales que sí sabes "
        "usar en el propio — y esas sutilezas son exactamente lo que mueve la atención.", 'p'),
      Spacer(1, 4),
      P("El rol no es decoración", 'h2'),
      P("Asignar un rol es el mecanismo más barato para mover la atención a la región "
        "correcta. No es maquillaje de tono: cambia de qué zona del espacio sale la "
        "respuesta.", 'p'),
      CALLOUT("La práctica que casi nadie hace",
              "Antes de asignar un rol, pregúntale al modelo <b>qué entiende él por ese rol</b>. "
              "Muchas veces crees que necesitas un «community manager» y resulta que lo que hace "
              "falta es un guionista. Lo descubres preguntando, no suponiendo.", AZUL),
      Spacer(1, 6),
      P("Delegar, no ordenar", 'h2'),
      P("El encuadre más útil: trata al modelo como alguien competente que acaba de "
        "entrar y no conoce tu contexto. Cuando delegamos mal a una persona, es fácil "
        "culparla y no revisar cómo delegamos. Con un modelo pasa igual, con la "
        "diferencia de que <b>nunca te va a decir «no entendí»</b>.", 'p')]

# ---------------- 3 ----------------
E += [PageBreak(), P("3 · Estructura de una instrucción", 'h1'),
      P("Cuatro piezas. No es una regla de oro, sino una lista de preguntas para saber "
        "qué le falta a lo que escribiste.", 'p'),
      TABLA([
        ["Pieza", "Qué responde", "Error típico"],
        ["Rol", "¿Desde qué conocimiento respondes?", "Elegirlo por intuición sin preguntar qué entiende el modelo"],
        ["Enfoque", "¿Qué tiene que hacer?", "Decorar la instrucción. No hace falta pedir el favor"],
        ["Contexto", "¿Qué información necesita?", "Suponer que ya lo sabe"],
        ["Límites", "¿Qué forma tiene el resultado?", "Decir «corto» sin decir cuánto"],
      ], [22*mm, 62*mm, 82*mm]),
      Spacer(1, 8),
      P("Sobre los límites: <b>«corto» no significa nada.</b> En un libro, ochenta "
        "páginas es corto. Cuantifica —caracteres, oraciones, viñetas— y añade "
        "adjetivos que orienten: accionable, conciso, pragmático.", 'p'),
      Spacer(1, 6),
      P("Destilar el prompt", 'h2'),
      P("Cuando el problema es nuevo, iterar en conversación está bien. Lo que casi "
        "nadie hace es el paso final. Una vez llegaste al resultado que querías:", 'p'),
      CODE(["¿Cuál hubiera sido el prompt que debí darte al inicio",
            "para llegar a este resultado?"]),
      P("El modelo devuelve la instrucción destilada. Eso convierte una conversación de "
        "diez turnos en un prompt reutilizable — y es la forma más barata de fabricar "
        "la primera versión de una skill.", 'p')]

# ---------------- 4 ----------------
E += [Spacer(1, 6), P("4 · Las cuatro decisiones de contexto", 'h1'),
      TABLA([
        ["Decisión", "Gobierna", "Pregunta de auditoría"],
        ["Relevancia", "Qué entra", "Si quito esta línea, ¿cambia alguna respuesta?"],
        ["Recencia", "Qué sale", "Lo viejo, ¿se muere o solo se acumula?"],
        ["Recuperación", "Cuándo entra", "¿Siempre, o solo cuando lo pidan?"],
        ["Ranking", "Dónde se coloca", "Lo importante, ¿está donde más se ve?"],
      ], [30*mm, 34*mm, 102*mm]),
      Spacer(1, 8),
      P("Dos consecuencias que sorprenden:", 'p'),
      LI("<b>Más no es mejor.</b> En un benchmark de llamadas a funciones, un modelo "
         "falló con 46 herramientas y funcionó con 19. Quitar capacidades lo mejoró."),
      LI("<b>Las definiciones de herramientas ocupan contexto aunque no se usen.</b> "
         "Cuarenta declaradas y seis en uso: pagas las cuarenta en cada mensaje."),
      Spacer(1, 5),
      P("Y el orden importa: la misma información rinde 70–75% de exactitud al inicio o "
        "al final de la ventana, y 55–60% en la mitad. De ahí las tres zonas — "
        "<b>ancla</b> (estable, se cachea) → <b>volumen</b> (lo pesado, al medio) → "
        "<b>filo</b> (la tarea, siempre al final). Nada después del filo.", 'p')]


# ---------------- 4b · árbol ----------------
E += [PageBreak(), P("5 · Dónde poner cada dato", 'h1'),
      P("Tres preguntas en cadena resuelven casi todas las decisiones de ubicación. "
        "Cabe en una tarjeta.", 'p')]
E += FIG(f"{IMG}/g12.png", 150,
         "Figura 1 — Árbol de decisión. Las tres preguntas son, en orden, relevancia "
         "(¿aplica siempre?), recencia (¿cambia?) y recuperación (¿la necesito ahora?).")

E += [P("Dos ramas merecen atención porque son las que más se hacen mal:", 'p'),
      LI("<b>«Sí, pero es larga» → archivo referenciado, no system prompt.</b> La "
         "tentación es pegar el manual entero arriba. Eso lo mete en cada llamada "
         "aunque casi nunca haga falta, y lo empuja al medio de la ventana, donde peor "
         "rinde."),
      LI("<b>«Cambia y no la necesito ahora» → no la traigas.</b> No es «tráela por si "
         "acaso». Un dato que cambia y no se usa hoy solo puede hacer una cosa: estar "
         "desactualizado cuando alguien lo lea.")]

# ---------------- 4c · auditoría ----------------
E += [Spacer(1, 8), P("6 · Auditar qué está sobrando", 'h1'),
      P("El árbol dice dónde poner las cosas. Esta matriz dice <b>qué quitar de lo que "
        "ya pusiste</b>. Corre la tarea varias veces, anota qué información trajiste y "
        "responde dos preguntas: ¿cambió la respuesta? y ¿ya lo tenía en contexto?", 'p')]
E += FIG(f"{IMG}/g14.png", 152,
         "Figura 2 — Cuatro diagnósticos, cuatro acciones distintas. La misma tabla "
         "sirve para decidir qué subir y qué borrar.")

E += [CALLOUT("El cuadrante que más enseña",
              "«Sí cambió <b>y</b> ya lo tenía» no significa que faltara: significa que donde estaba "
              "<b>no la estaba usando</b> — enterrada en un bloque largo o en la mitad de la ventana. "
              "Meterla dos veces no es la solución. Acortarla o reubicarla, sí.", AMBAR),
      Spacer(1, 6),
      P("Córrela en <b>sesiones limpias</b>, una por variante. En la misma sesión, lo "
        "que trajiste antes contamina lo siguiente y la tabla miente.", 'p')]

# ---------------- 4d · encadenar ----------------
E += [PageBreak(), P("7 · Encadenar en vez de agrandar", 'h1'),
      P("La reacción natural ante una tarea compleja es escribir un prompt más largo y "
        "meterlo todo en una conversación. Pero la ventana crece, y con ella crecen los "
        "errores, las invenciones y las instrucciones olvidadas. <b>Un prompt gigante "
        "es la peor forma de resolver un problema grande.</b>", 'p'),
      P("Nadie construye un coche de una sola vez. Hay una estación que monta el "
        "chasis, otra el motor, otra lo eléctrico. Cada una sabe exactamente qué tiene "
        "que resolver y recibe el trabajo de la anterior. Con los prompts funciona "
        "igual: <b>cada paso es un prompt en un chat nuevo</b>.", 'p')]
E += FIG(f"{IMG}/g13.png", 155,
         "Figura 3 — Cada estación arranca con la ventana limpia y una sola tarea. Lo "
         "que arrastra no es el documento entero, sino el resultado destilado.")

E += [P("Pasar el resultado con etiquetas", 'h2'),
      CODE(["A partir de los siguientes hallazgos, escribe un resumen de",
            "100 palabras enfocado en las soluciones más viables.",
            "",
            "<hallazgos>",
            "... la salida del paso anterior ...",
            "</hallazgos>"]),
      P("Sin las etiquetas, el modelo no distingue tu instrucción del material, y a "
        "veces responde sobre el material en lugar de hacer lo que le pediste.", 'p'),
      Spacer(1, 5),
      P("La ventaja que no es obvia", 'h2'),
      P("<b>Cada paso es un prompt que puedes iterar por separado</b> hasta dejarlo "
        "bien. Una vez afinado, la cadena entera produce la misma calidad cada vez. Con "
        "un prompt gigante no puedes hacer eso: si el resultado sale mal, no sabes qué "
        "parte falló.", 'p')]

E += [Spacer(1, 8), P("8 · Fabricar el procedimiento", 'h1'),
      P("Cómo conseguir el paso a paso de una tarea sin inventártelo. Tres movimientos.", 'p'),
      CODE(["1.  ¿Qué harías paso a paso para resolver este tipo de",
            "    problemas? Dame tres alternativas.",
            "",
            "2.  [eliges la que mejor resuelve tu caso]",
            "",
            "3.  Usando esta plantilla, resuelve el problema que te daré.",
            "    <plantilla> ... </plantilla>",
            "    <problema> ... </problema>"]),
      P("Dos efectos, y el segundo importa más de lo que parece:", 'p'),
      LI("<b>Acota el razonamiento.</b> Al darle el paso a paso, limitas los caminos "
         "que puede tomar. Más rápido y más consistente entre ejecuciones."),
      LI("<b>Resuelve el problema de «qué palabras uso».</b> La plantilla viene "
         "formulada con las palabras del propio modelo para razonar sobre ese tipo de "
         "problema — mejores que las que tú adivinarías desde fuera."),
      Spacer(1, 5),
      P("Combinado con la destilación del prompt, es la forma más barata de fabricar la "
        "primera versión de una skill: el modelo te da el procedimiento <b>y</b> la "
        "instrucción que lo invoca. Tú decides cuál de las alternativas es correcta, "
        "que es la parte que no se delega.", 'p')]

# ---------------- 4e · caché ----------------
E += [PageBreak(), P("9 · Orden, caché y costo", 'h1'),
      P("Dos optimizaciones que tiran en direcciones opuestas si no las ves juntas:", 'p'),
      LI("<b>La caché</b> exige que el contenido estable vaya <b>primero</b>: el "
         "proveedor reutiliza el cómputo del prefijo idéntico entre llamadas. Hay "
         "medición de reducciones de costo de API entre 41% y 80%, y de mejora del "
         "time-to-first-token entre 13% y 31%."),
      LI("<b>La atención</b> exige que lo importante vaya al principio <b>o al final</b>: "
         "70–75% de exactitud en los extremos, 55–60% en la mitad."),
      Spacer(1, 4),
      P("Puestas juntas mal, el prefijo estable empuja la tarea real hacia la mitad —la "
        "peor posición— y se gana en costo lo que se pierde en exactitud.", 'p')]
E += FIG(f"{IMG}/g10.png", 150,
         "Figura 4 — Tres zonas lo resuelven. El ancla ocupa el inicio (cacheada y bien "
         "posicionada), la tarea el final, y el volumen de baja señal el medio, donde "
         "menos daño hace.")

E += [CALLOUT("La regla de cierre",
              "Nunca escribas nada después de la tarea. Ni un recordatorio, ni un «responde en "
              "formato X», ni una repetición de las reglas. Cualquier coletilla la empuja al medio. "
              "Si una restricción es crítica y hay que repetirla, va arriba —donde ya está cacheada "
              "y bien posicionada—, no como cierre.", VERDE),
      Spacer(1, 6),
      P("Un matiz que ahorra dinero: cachear <b>solo</b> el contexto estable rinde más "
        "que cachear todo el contexto, que paradójicamente puede aumentar la latencia. "
        "Y hay una ventana de reutilización: <b>partir una tarea en varios días paga el "
        "prefijo cada vez</b>.", 'p')]

# ---------------- 5 ----------------
E += [PageBreak(), P("10 · Contra la invención", 'h1'),
      P("Tres técnicas, de la más barata a la más cara. Elige por lo que cuesta el "
        "error, no por costumbre.", 'p'),
      P("10.1 · Anclaje a fuentes", 'h2'),
      P("Dos partes, y la segunda es la que casi todo el mundo olvida:", 'p'),
      CODE(["Responde ÚNICAMENTE con base en <nombre exacto del documento>.",
            "Si la información no se encuentra en él, responde que no",
            "está disponible."]),
      P("<b>Nombra el documento</b>, no digas «los adjuntos»: con varias fuentes se "
        "enfoca en una y te deja fuera el resto sin avisar.", 'p'),
      P("La segunda cláusula es la decisiva: <b>darle una salida honesta</b>. Un modelo "
        "al que le falta información y no tiene forma legítima de decirlo rellena el "
        "hueco con algo plausible. No por engañar — porque no le diste otra opción.", 'p'),
      Spacer(1, 5),
      P("10.2 · Citas textuales verificables", 'h2'),
      P("Pide la cita entre comillas y luego <b>búscala en el documento original</b>.", 'p'),
      CALLOUT("El matiz que rara vez se documenta",
              "La cita <b>no siempre es literal</b>: a veces reordena o parafrasea sin avisar. Busca "
              "fragmentos de tres o cuatro palabras, no la frase completa, y si no aparece, pide la "
              "página. Consecuencia para cualquier verificación automatizada: un comparador de texto "
              "exacto marcaría como falsas citas sustancialmente correctas. El criterio fiable es "
              "«la referencia resuelve y dice lo mismo», no coincidencia carácter a carácter.", AMBAR),
      Spacer(1, 6),
      P("10.3 · Autoconsistencia", 'h2'),
      CODE(["Resuelve esto de tres formas distintas y compara los resultados."]),
      P("Si los tres coinciden, sube la confianza. <b>Si divergen, encontraste un error "
        "sin necesidad de saber cuál era la respuesta correcta.</b> Esa es la propiedad "
        "valiosa: la divergencia es señal, y detectarla no exige un verificador.", 'p'),
      P("Sirve donde el error es de razonamiento o cálculo. <b>No sirve donde el error "
        "es un dato inventado</b>: los tres caminos parten del mismo dato falso y "
        "coinciden felizmente.", 'p'),
      Spacer(1, 5),
      TABLA([
        ["Riesgo del error", "Técnica"],
        ["Bajo", "Anclaje"],
        ["Medio, y el error sería de razonamiento", "Anclaje + autoconsistencia"],
        ["Alto, o el error sería un dato falso", "Anclaje + verificación adversarial"],
      ], [78*mm, 88*mm]),
      Spacer(1, 6),
      P("La regla de fondo, y vale para las tres: <b>no creas ciegamente lo que dice el "
        "modelo; crea mecanismos para validarlo.</b> Y prefiere el mecanismo más barato "
        "que detecte el error que te importa.", 'p')]

# ---------------- 6 ----------------
E += [PageBreak(), P("11 · Autoridad y jerarquía", 'h1'),
      P("Cuando dos instrucciones se contradicen hay un orden entrenado de privilegio:", 'p'),
      TABLA([
        ["Nivel", "Origen", "Privilegio"],
        ["1", "Mensaje de sistema", "Máximo"],
        ["2", "Mensaje del usuario", "Alto"],
        ["3", "Instrucciones dentro de imágenes o audio", "Medio"],
        ["4", "Texto que viene de herramientas: búsquedas, documentos, salidas de código", "El más bajo"],
      ], [14*mm, 116*mm, 36*mm]),
      Spacer(1, 8),
      P("El nivel 4 es una defensa: si un documento trae escondido un <i>ignora tus "
        "instrucciones anteriores</i>, debe ser ignorado.", 'p'),
      P("Dos matices que evitan usarlo mal:", 'p'),
      LI("<b>Solo aplica cuando hay conflicto.</b> Si están alineadas, obedece la de "
         "menor privilegio sin problema."),
      LI("<b>No es una garantía absoluta.</b> Es una tendencia entrenada, no un "
         "control. Para lo que de verdad no puede fallar, el límite va en la "
         "infraestructura: si el proceso no tiene la credencial, no hay instrucción "
         "que evadir."),
      Spacer(1, 8),
      P("12 · Elegir el modelo", 'h1'),
      P("Un modelo rápido y uno de razonamiento no se diferencian en «cuál es más "
        "listo», sino en <b>cuánto espacio se dan para pensar antes de responder</b>.", 'p'),
      LI("<b>Rápido</b> — respuesta directa, tareas acotadas, alto volumen."),
      LI("<b>Razonamiento</b> — varios pasos, restricciones que interactúan, cálculo."),
      Spacer(1, 4),
      P("Con modelos actuales, la instrucción <i>piensa paso a paso</i> ya no cambia "
        "mucho: razonan por defecto. Sigue sirviendo cuando quieres <b>ver</b> el "
        "razonamiento para auditarlo, que es distinto de que lo haga.", 'p')]

# ---------------- 8 ----------------
E += [PageBreak(), P("13 · La disciplina que sostiene todo", 'h1'),
      P("Sesión limpia para comparar", 'h2'),
      P("Si quieres saber si un cambio mejoró algo, corre las dos versiones en sesiones "
        "limpias. En la misma sesión, lo anterior contamina lo siguiente y la "
        "comparación no vale.", 'p'),
      P("Lo corregido no se borra, se acumula", 'h2'),
      P("Cuando corriges al modelo a mitad de conversación, el dato equivocado <b>sigue "
        "en el contexto</b> junto al correcto. Hay medición de que un error temprano en "
        "una conversación de varios turnos degrada el desempeño cerca de un 39%.", 'p'),
      CALLOUT("Consecuencia práctica",
              "Ante un error de base, <b>abre chat nuevo</b>. No sigas corrigiendo encima. Es la "
              "razón de que en un sistema por roles un bloqueo vuelva al principio en lugar de "
              "seguir discutiendo en el mismo hilo.", VERDE),
      Spacer(1, 6),
      P("Auditar antes de suponer", 'h2'),
      P("Antes de rediseñar un asistente que heredaste, pregúntale qué tiene:", 'p'),
      CODE(["¿Qué información tienes disponible sobre mí en este momento?",
            "Enlístala por origen: instrucciones del sistema, memoria de",
            "sesiones anteriores, este chat, archivos que subí, herramientas.",
            "Si no tienes acceso a alguna de esas fuentes, dilo explícitamente."]),
      P("Lo interesante no es lo que dice que tiene: <b>es lo que dice que no tiene.</b> "
        "Ahí están los huecos que nadie te avisó.", 'p'),
      P("Cuando encuentres uno, escríbelo con esta forma — obliga a nombrar el supuesto, "
        "que es la parte que normalmente queda tácita:", 'p'),
      CODE(["«Yo asumía que sabía ____, y resulta que no está en ningún",
            " lado del contexto.»"])]

# ---------------- 9 ----------------
E += [PageBreak(), P("14 · Los nueve errores más comunes", 'h1'),
      TABLA([
        ["#", "Error", "Qué hacer"],
        ["1", "Culpar al modelo por una delegación mala",
         "Si a una persona nueva le hubiera faltado ese dato, al modelo también"],
        ["2", "Confundir problema de contexto con problema de redacción",
         "Antes de reformular otra vez, pregunta qué información falta"],
        ["3", "Pedir «corto», «profesional», «bien»",
         "Adjetivos sin unidad. Cuantifica"],
        ["4", "Acumular instrucciones",
         "Hay recortes documentados de más del 80% de un prompt de sistema que mejoraron el resultado"],
        ["5", "Corregir encima cuando el error es de base",
         "Chat nuevo"],
        ["6", "Creer la cita sin buscarla — o descartarla porque no coincide letra a letra",
         "Busca fragmentos cortos; pide la página"],
        ["7", "No darle salida honesta",
         "Sin un «di que no está disponible», inventa"],
        ["8", "Comparar en la misma sesión",
         "Contamina y no te enteras"],
        ["9", "Agrandar el prompt en vez de encadenar",
         "Divide el problema en estaciones, cada una un chat nuevo"],
      ], [7*mm, 76*mm, 83*mm])]

E += [Spacer(1, 10), P("15 · Dónde seguir", 'h1'),
      TABLA([
        ["Documento", "Cuándo leerlo"],
        ["FOUNDATIONS.md", "Este documento, en el catálogo de skills"],
        ["AUTHORING.md", "Al escribir una skill nueva: anatomía y formato"],
        ["CONTEXT.md", "Al decidir qué información entra a la ventana"],
        ["PRECISION.md", "Al diseñar una skill cuya salida deba ser comprobable"],
        ["Guía del Framework (PDF)", "Al implantar el ciclo de vida por roles en un equipo"],
      ], [44*mm, 122*mm]),
      Spacer(1, 10),
      CALLOUT("Procedencia de las cifras",
              "Los datos citados —46 frente a 19 herramientas, caída del 39% por error temprano, "
              "70–75% frente a 55–60% según posición, recorte de más del 80% de un prompt de "
              "sistema— provienen de material formativo y <b>no han sido verificados de forma "
              "independiente</b>. Trátalos como órdenes de magnitud que orientan una decisión, no "
              "como constantes. Las prácticas se sostienen aunque las cifras exactas difieran.", AZUL)]

doc.build(E)
print("fundamentos.pdf generado")
