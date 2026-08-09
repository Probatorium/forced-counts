#!/usr/bin/env python3
"""
Cotejo de la secuencia King Wen contra un artefacto independiente.

Artefacto: la transcripcion literal del apendice A de arXiv:2601.07175v3, en
artifacts/radisic-2601.07175v3-appendix-A.tsv, con su identificador completo y
sus limites declarados alli.

Este programa SOLO compara. La tabla transcrita no entra como entrada de ningun
computo de resultados de este repositorio: no la usan measure.py, ni group.py,
ni proofs.py, ni gray.py, y eso se comprueba aqui mismo.

Convencion del artefacto: entero de seis bits con el bit 0 en la linea inferior
y yang igual a uno. En las convenciones fijadas en PREREGISTRATION.md eso es
yang1 con la linea inferior como bit menos significativo.

Salida: results/corroboration.tsv

  python src/corroborate.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import measure as M                                        # noqa: E402

ART = os.path.join(ROOT, "artifacts", "radisic-2601.07175v3-appendix-A.tsv")
OUT = os.path.join(ROOT, "results", "corroboration.tsv")
ROWS = []


def emit(key, value, note=""):
    ROWS.append((key, str(value), note))


def load_artifact():
    filas = []
    with open(ART, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("kw"):
                continue
            a, b = line.split("\t")
            filas.append((int(a), int(b)))
    return filas


def main():
    art = load_artifact()
    emit("artefacto.fichero", os.path.relpath(ART, ROOT).replace("\\", "/"), "")
    emit("artefacto.identificador", "arXiv:2601.07175v3, apendice A, pagina 11", "")
    emit("artefacto.filas.transcritas", len(art), "")
    emit("artefacto.numeros.de.king.wen.consecutivos.del.1.al.64",
         int([k for k, _ in art] == list(range(1, 65))), "")
    emit("artefacto.es.una.permutacion.de.los.64.enteros",
         int(sorted(v for _, v in art) == list(range(64))),
         "comprobacion interna del artefacto, antes de compararlo con nada")

    with open(os.path.join(ROOT, "data", "sequences.json"), "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    kw = payload["sequences"]["King Wen"]
    emit("repositorio.fichero", "data/sequences.json", "")
    emit("repositorio.procedencia", payload["provenance"]["commit"],
         "kingwen-orderings-replication en la etiqueta zenodo-v3")

    # la convencion del artefacto, expresada en las de PREREGISTRATION.md
    nuestros = [M.value(p, "yang1", "bottomLSB") for p in kw]
    emit("convencion.usada", "yang1 con la linea inferior como bit menos significativo",
         "es la del artefacto, bit 0 en la linea inferior")

    difs = [(k, b, nuestros[k - 1]) for k, b in art if b != nuestros[k - 1]]
    iguales = len(art) - len(difs)
    emit("posiciones.comparadas", len(art), "")
    emit("posiciones.que.coinciden", iguales, "")
    emit("posiciones.que.difieren", len(difs), "")
    for k, a, b in difs:
        emit("DISCREPANCIA.king.wen.%d" % k, "artefacto %d, repositorio %d" % (a, b),
             "PARAR y reportar")

    # el artefacto no entra en ningun computo de resultados: se comprueba
    fuentes = ["measure.py", "group.py", "proofs.py", "gray.py"]
    usos = []
    for f in fuentes:
        texto = open(os.path.join(ROOT, "src", f), "r", encoding="utf-8").read()
        if re.search(r"artifacts|radisic|2601\.07175", texto, re.I):
            usos.append(f)
    emit("programas.de.resultados.que.tocan.el.artefacto",
         " ".join(usos) if usos else "ninguno",
         "measure.py, group.py, proofs.py y gray.py revisados")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Cotejo contra artefacto independiente. Solo comparacion.\n")
        fh.write("# clave\tvalor\tnota\n")
        for key, val, note in ROWS:
            fh.write("%s\t%s\t%s\n" % (key, val, note))

    print("escrito results/corroboration.tsv")
    for key, val, _ in ROWS:
        print("  %-58s %s" % (key, val))
    if difs:
        print()
        print("PARAR: hay %d discrepancias. No se sigue." % len(difs))
        return 1
    print()
    print("Las %d posiciones coinciden." % iguales)
    return 0


if __name__ == "__main__":
    sys.exit(main())
