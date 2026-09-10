#!/usr/bin/env bash
# Responde con datos las tres preguntas: ¿cuánto cuesta?, ¿cuánto ahorra la caché?,
# ¿la verificación encuentra algo? Sin datos, esas preguntas solo tienen opiniones.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import csv, pathlib, json, collections

f = pathlib.Path("metricas/costos.csv")
if not f.exists() or len(f.read_text().splitlines()) < 2:
    print("Sin datos todavía.")
    print("Registra cada paso con: ./scripts/registrar-costo.sh <orden> <rol> <in> <out> <cacheados>")
    raise SystemExit(0)

filas = list(csv.DictReader(f.open()))
i = lambda r, k: int(r.get(k) or 0)

ordenes = collections.defaultdict(list)
for r in filas: ordenes[r["id_orden"]].append(r)

tot_in = sum(i(r,"tokens_entrada") for r in filas)
tot_cache = sum(i(r,"tokens_cacheados") for r in filas)
tot_out = sum(i(r,"tokens_salida") for r in filas)

print(f"Órdenes: {len(ordenes)} · pasos: {len(filas)}")
print("-"*68)
print(f"Tokens entrada   {tot_in:>12,}")
print(f"  de ellos caché {tot_cache:>12,}  ({tot_cache/tot_in*100:.1f}% del prefijo reutilizado)" if tot_in else "")
print(f"Tokens salida    {tot_out:>12,}")
print(f"Media por orden  {(tot_in+tot_out)//max(len(ordenes),1):>12,} tokens")
print("-"*68)

print("Costo por rol (media de tokens por invocación)")
por_rol = collections.defaultdict(lambda: [0,0])
for r in filas:
    a = por_rol[r["rol"]]; a[0] += i(r,"tokens_entrada")+i(r,"tokens_salida"); a[1] += 1
for rol, (t, n) in sorted(por_rol.items(), key=lambda x: -x[1][0]):
    print(f"  {rol:16s} {t//n:>10,}  ×{n}")

# ¿La verificación encuentra algo? Esta es la pregunta que decide si vale la pena.
ver = pathlib.Path("evidencia/verificacion")
if ver.exists():
    c = collections.Counter(); tot = 0
    for j in ver.glob("*.json"):
        try: d = json.loads(j.read_text())
        except Exception: continue
        for v in d.get("veredictos", []):
            c[v.get("veredicto","?")] += 1; tot += 1
    print("-"*68)
    if tot:
        print(f"Rendimiento de la verificación ({tot} veredictos)")
        for k in ("VERIFICADO","CORREGIDO","RECHAZADO"):
            print(f"  {k:12s} {c[k]:>5}   {c[k]/tot*100:5.1f}%")
        hallado = c["CORREGIDO"] + c["RECHAZADO"]
        print(f"\n  Tasa de hallazgo: {hallado/tot*100:.1f}% de las afirmaciones tenía algo mal.")
        print("  Este número es el que justifica —o no— el costo de la verificación.")
        if hallado == 0:
            print("  ATENCIÓN: cero hallazgos. O el equipo es muy preciso, o el verificador")
            print("            está recibiendo contexto del autor y solo confirma.")
    else:
        print("Aún no hay veredictos registrados.")
PY
