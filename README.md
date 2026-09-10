<h1 align="center">Minos</h1>

<p align="center">
  <em>El juez que pesa cada entrega.</em><br>
  SDLC agéntico con roles separados, contratos entre ellos y gates verificables.
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-1.7.0-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="roles" src="https://img.shields.io/badge/roles-8-orange">
  <img alt="gates" src="https://img.shields.io/badge/gates%20declarados-23-lightgrey">
</p>

---

En la mitología, Minos juzga a cada alma que se le presenta. Aquí es lo mismo: un
**verificador adversarial** se intercala después de cada rol, recibe solo las
afirmaciones y el código —nunca el razonamiento del autor— y emite veredicto.

Framework estándar para desarrollar con agentes dentro de un workspace de Coder,
con roles separados, contratos entre ellos y gates verificables.

Pensado para equipos cuyo contenedor solo tiene salida a GitHub: **todo vive en el
repositorio**, no hay nada que configurar en la consola de Coder.

## Qué trae el paquete

```
minos/          este repo — roles, gates, contratos, scripts
  docs/pdf/
    Framework-SDLC-Agentico-Guia.pdf      28 pág · implantar el framework
    Fundamentos-Trabajar-con-Agentes.pdf   7 pág · fundamentos, sirve solo

minos-skills/             el catálogo (submódulo en .claude/skills)
  FOUNDATIONS.md   los fundamentos — leer primero
  AUTHORING.md     cómo se escribe una skill
  CONTEXT.md       qué información entra a la ventana
  PRECISION.md     cómo hacer que su salida sea comprobable
  <rol>/SKILL.md   los ocho procedimientos
```

Las cuatro guías del catálogo se montan con el submódulo, así que el agente las tiene
disponibles dentro del workspace. `CLAUDE.md` y `AGENTS.md` las referencian y
extraen de `FOUNDATIONS.md` las tres reglas que aplican a toda invocación de un rol:
salida honesta, anclaje a fuentes, y chat nuevo ante error de base.

## Qué resuelve

Un agente sin estructura hace las siete cosas a la vez: diseña, implementa, se
autoevalúa y despliega. Nadie puede auditar eso. Aquí cada rol tiene entrada,
salida y un gate verificable, y el trabajo pasa de uno a otro por un archivo JSON.

## Los siete roles

| Rol | Produce | No hace |
|---|---|---|
| Líder técnico | Orden de trabajo, cierre | Diseñar, implementar |
| Arquitecto | Diseño, contratos, matriz de impacto | Implementar |
| Constructor | Código, pruebas unitarias, paquete | Decidir arquitectura, desplegar |
| Pruebas | Certificación con evidencia | Corregir defectos |
| Seguridad | Dictamen y hallazgos | Corregir hallazgos |
| SRE | Objetivos, alertas, runbook, criterio de reversión | Desplegar |
| DevOps | Manual, orden cerrada, ejecución | Diseñar, corregir |
| **Verificador** | **Veredictos sobre las afirmaciones de cada rol** | **Corregir el artefacto** |

El verificador no va al final: se intercala **después de cada rol**. Recibe solo el
archivo de afirmaciones y el código, nunca el razonamiento del autor. Ver
`docs/05-verificacion-adversarial.md`.

## Instalación

```bash
git clone https://github.com/<ORG>/minos.git
cd minos
./scripts/bootstrap.sh
```

> **Nota sobre el catálogo de skills.** `minos-skills` todavía no está publicado, así
> que este repo **no** declara el submódulo: `.claude/skills/` viene con un marcador.
> Cuando el catálogo esté en GitHub, monta el submódulo con la plantilla de
> `docs/gitmodules.plantilla` y pínealo por SHA:
>
> ```bash
> git submodule add -b main https://github.com/<ORG>/minos-skills.git .claude/skills
> ```

Para integrarlo al template de Coder, ver `coder/main.tf` y `docs/03-adopcion-coder.md`.

## Uso

```
/iniciar  Necesito agregar reintentos al consumidor de eventos
```

El líder técnico acota, declara impacto y emite la orden. A partir de ahí:
`/handoff` mueve la cadena, `/verificar` lanza la verificación adversarial del
rol que acaba de terminar, y `/gate` muestra qué falta.

## Ajuste

Solo se toca `contratos/gates.yaml` y `contratos/roles.yaml`. Ver
`docs/04-personalizacion.md`. Si te encuentras editando un `SKILL.md` para cambiar
un umbral, el umbral estaba en el lugar equivocado.

## Versión

Ver `VERSION`. El catálogo de skills tiene su propio versionado y se pinea por SHA
de submódulo, así que actualizarlo es siempre un commit explícito de este repo.
