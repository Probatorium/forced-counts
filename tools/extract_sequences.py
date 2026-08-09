#!/usr/bin/env python3
"""
Extraccion de las tres secuencias historicas desde la fuente de solo lectura.

Fuente: kingwen-orderings-replication, unicamente en la etiqueta zenodo-v3.
La extraccion se hace sobre un archivo del arbol de esa etiqueta, desplegado en
_source/zenodo-v3/ (directorio de trabajo de este repositorio, fuera de la
historia por .gitignore). El repositorio fuente no se toca.

Lo que sale de aqui es SOLO la lista de hexagramas de cada secuencia, en forma
neutral respecto de la convencion de bits: cada hexagrama es una cadena de seis
caracteres, indice 0 la linea inferior, "y" yang y "n" yin. Ninguna cifra de
resultados de la fuente se copia, y ninguna se usa como entrada del computo.

  python tools/extract_sequences.py
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_REPO = os.path.join(os.path.dirname(ROOT), "kingwen-orderings-replication", ".git")
WORKDIR = os.path.join(ROOT, "_source", "zenodo-v3")
TAG = "zenodo-v3"
OUT = os.path.join(ROOT, "data", "sequences.json")

# Convencion con la que la fuente representa un hexagrama como entero, tal y
# como su propia cabecera la documenta: lineas numeradas 1 (inferior) a 6
# (superior), yang = 1, y la linea 1 es el bit mas significativo.
SOURCE_BIT_CONVENTION = "linea 1 (inferior) como bit mas significativo, yang = 1"


def source_rev(what):
    out = subprocess.run(["git", "--git-dir=" + SRC_REPO, "rev-parse", TAG + what],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_source_module(path):
    spec = importlib.util.spec_from_file_location("zenodo_v3_verify_paper", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def to_pattern(value):
    """Entero de la fuente a patron de lineas, indice 0 la linea inferior."""
    bits = format(value, "06b")          # bits[0] es la linea 1 (inferior)
    return "".join("y" if b == "1" else "n" for b in bits)


def main():
    script = os.path.join(WORKDIR, "verify_paper.py")
    if not os.path.exists(script):
        raise SystemExit("falta " + script + ": despliega antes el archivo de la etiqueta")

    mod = load_source_module(script)
    raw = {
        "Mawangdui": list(mod.MAWANGDUI),
        "Jing Fang": list(mod.JING_FANG),
        "King Wen": list(mod.KING_WEN),
    }

    payload = {
        "provenance": {
            "source_repo": "kingwen-orderings-replication",
            "access": "solo lectura, solo en la etiqueta " + TAG,
            "tag": TAG,
            "commit": source_rev("^{commit}"),
            "tree": source_rev("^{tree}"),
            "extracted_file": "verify_paper.py",
            "extracted_file_sha256": sha256_file(script),
            "source_bit_convention": SOURCE_BIT_CONVENTION,
            "note": ("solo se extraen las tres secuencias. Ninguna cifra de "
                     "resultados de la fuente entra en este repositorio como dato."),
        },
        "encoding": {
            "hexagram": "cadena de seis caracteres, indice 0 la linea inferior",
            "y": "yang",
            "n": "yin",
        },
        "sequences": {},
    }

    for name, values in raw.items():
        if sorted(values) != list(range(64)):
            raise SystemExit("la secuencia %s no es una permutacion de los 64 hexagramas" % name)
        payload["sequences"][name] = [to_pattern(v) for v in values]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")

    print("escrito " + os.path.relpath(OUT, ROOT))
    print("commit de origen " + payload["provenance"]["commit"])
    for name in payload["sequences"]:
        print("  %-10s %d hexagramas" % (name, len(payload["sequences"][name])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
