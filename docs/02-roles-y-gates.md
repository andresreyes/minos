# Roles y gates

## La cadena

```
líder técnico ──> arquitecto ──> constructor ──> pruebas ──> seguridad ──> SRE ──> devops
      ^                │              │             │            │          │        │
      │                ▼              ▼             ▼            ▼          ▼        ▼
      │           [verificador adversarial: desmiente las afirmaciones del rol]
      │                │              │             │            │          │        │
      └────────────────┴──────────────┴─────────────┴────────────┴──────────┴────────┘
                  cualquier bloqueo o RECHAZADO vuelve al líder técnico
```

## Por qué líder técnico y arquitecto están separados

Es la separación que más se cuestiona al adoptar el framework. La razón: si el
mismo rol asigna trabajo y produce el diseño, no hay quién desempate cuando el
diseño resulta ser demasiado grande para la orden. El líder técnico decide **qué
entra**; el arquitecto decide **cómo se hace**. Un rol acota, el otro profundiza.

En equipos pequeños puede ser la misma persona alternando roles — pero no el mismo
paso de la cadena.

## Tabla de gates por rol

| Gate | Rol | Anulable | Activo si |
|---|---|---|---|
| G1_alcance_acotado | líder técnico | no | siempre |
| G2_impacto_declarado | arquitecto | no | siempre |
| G2b_contrato_versionado | arquitecto | sí | indirecto+ |
| G3_artefactos_intactos | constructor | no | siempre |
| G3b_pruebas_unitarias | constructor | sí | siempre |
| G4_certificado_en_ambiente | pruebas | no | siempre |
| G4b_cobertura_minima | pruebas | sí | siempre |
| G4c_regresion_ejecutada | pruebas | sí | indirecto+ |
| G5_dictamen_emitido | seguridad | no | siempre |
| G5b_sin_hallazgos_sobre_umbral | seguridad | no | siempre |
| G5c_secretos_ausentes | seguridad | no | siempre |
| G6_observabilidad_definida | SRE | no | directo |
| G6b_reversibilidad_probada | SRE | no | directo |
| G6c_retencion_declarada | SRE | sí | directo |
| G7_insumos_completos | devops | no | directo |
| G7b_hash_coincide | devops | no | directo |
| G7c_ventana_autorizada | devops | no | directo |
| G7d_verificacion_posterior | devops | no | directo |
| GV_verificacion_ejecutada | verificador | no | indirecto+ |
| GV2_sin_rechazos_bloqueantes | verificador | no | indirecto+ |
| GV3_cobertura_bloqueantes | verificador | no | indirecto+ |

## Los tres gates que más se subestiman

**G3_artefactos_intactos** — el constructor demuestra con hashes que lo que la matriz
de impacto declaró intocado sigue intocado. Es el gate que atrapa el cambio pequeño
que arrastró algo estable.

**G6b_reversibilidad_probada** — exige haber *ejecutado* la reversión, no haberla
escrito. Un rollback documentado y nunca probado falla justo cuando se necesita.

**G7b_hash_coincide** — el artefacto que se instala es byte a byte el que se certificó.
Sin esto, toda la cadena anterior certifica algo que nadie desplegó.
