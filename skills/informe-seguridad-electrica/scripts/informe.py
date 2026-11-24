#!/usr/bin/env python3
"""Genera el informe de un ensayo de seguridad eléctrica (IEC 62353) en Markdown.

    python3 informe.py ensayo.json > informe.md

El veredicto lo calcula este script con los límites de iec62353.py, nunca el modelo de IA.
Formato de ensayo.json: ver ../ejemplo.json
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from iec62353 import evaluar  # noqa: E402

MEDIDAS = ("resistencia_tierra_ohm", "fuga_equipo_uA", "fuga_parte_aplicable_uA", "aislamiento_Mohm")


def informe(d):
    eq = d.get("equipo", {})
    m = d.get("mediciones", {})
    r = evaluar(eq.get("clase", ""), eq.get("parte_aplicable", "ninguna"), d.get("metodo", "directo"),
                **{k: m[k] for k in MEDIDAS if k in m})

    def fmt(x):
        return f"{x:g}".replace(".", ",")

    L = [
        "# Informe de ensayo de seguridad eléctrica",
        "",
        f"**Veredicto: {r['veredicto']}**",
        "",
        "## Equipo",
        "",
        "| Campo | Valor |", "|---|---|",
        f"| Equipo | {eq.get('nombre', '—')} |",
        f"| Marca / modelo | {eq.get('marca', '—')} / {eq.get('modelo', '—')} |",
        f"| N.º de serie | {eq.get('serie', '—')} |",
        f"| Inventario | {eq.get('inventario', '—')} |",
        f"| Ubicación | {eq.get('ubicacion', '—')} |",
        f"| Clase de protección | {r['equipo']['clase']} |",
        f"| Parte aplicable | {r['equipo']['parte_aplicable']} |",
        "",
        "## Ensayo",
        "",
        f"- Tipo: {d.get('motivo', 'ensayo recurrente')}",
        f"- Método de fuga: {r['equipo']['metodo']}",
        f"- Analizador: {d.get('analizador', '—')}",
        f"- Fecha: {d.get('fecha', date.today().isoformat())}",
        f"- Técnico: {d.get('tecnico', '—')}",
        "",
        "## Resultados",
        "",
        "| Ensayo | Medido | Límite | Resultado |", "|---|---:|---:|---|",
    ]
    for e in r["ensayos"]:
        marca = "✅" if e["resultado"] == "APTO" else "❌"
        L.append(f"| {e['ensayo']} | {fmt(e['medido'])} {e['unidad']} | ≤ {fmt(e['limite'])} {e['unidad']} "
                 f"| {marca} {e['resultado']} |")
    if "aislamiento_Mohm" in m:
        L.append(f"| Resistencia de aislamiento (informativa) | {fmt(m['aislamiento_Mohm'])} MΩ | — | ℹ️ |")
    if r["avisos"]:
        L += ["", "## Avisos", ""] + [f"- {a}" for a in r["avisos"]]
    if d.get("observaciones"):
        L += ["", "## Observaciones", "", d["observaciones"]]
    L += ["", "---", "",
          f"_{r['referencia']} Este informe debe revisarlo y firmarlo el técnico responsable._",
          "", "Firma del técnico: ____________________"]
    return "\n".join(L) + "\n", r


def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 informe.py ensayo.json")
    texto, r = informe(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    sys.stdout.write(texto)
    sys.exit(0 if r["veredicto"] == "APTO" else 2)


if __name__ == "__main__":
    main()
