#!/usr/bin/env python3
"""
Registro de esfuerzo, append only, para el repositorio forced-counts.

Implementa lo que EFFORT.md declara en el commit raiz:

  - sesiones con marca de inicio y de fin,
  - clasificacion de cada fichero como aparato o analisis,
  - atribucion de quien escribio y quien decidio,
  - callejones sin salida como entradas propias.

El registro vive en effort/log.jsonl, una linea JSON por evento. Es append only
por construccion y verificable: cada registro guarda el sha256 del registro
anterior, de modo que una edicion retroactiva de cualquier linea rompe la
cadena y `python tools/effort.py verify` la delata.

Uso:

  python tools/effort.py open    --actor NOMBRE [--decider NOMBRE] --note TEXTO
  python tools/effort.py close   --note TEXTO
  python tools/effort.py note    --note TEXTO [--kind KIND]
  python tools/effort.py retro   --note TEXTO --when ISO8601
  python tools/effort.py classify
  python tools/effort.py verify
  python tools/effort.py status
  python tools/effort.py export

Ninguna suborden reescribe ni borra nada. `classify` calcula el reparto de
lineas entre aparato y analisis a partir de effort/classification.tsv y anade
el resultado como un evento mas.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "effort", "log.jsonl")
CLASSES = os.path.join(ROOT, "effort", "classification.tsv")

VALID_CLASSES = ("aparato", "analisis")
VALID_ORIGINS = ("propio", "extraido")


# --- utilidades del registro ----------------------------------------------

def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_log():
    if not os.path.exists(LOG):
        return []
    with open(LOG, "r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def line_hash(record):
    """sha256 de la serializacion canonica del registro, sin su propio campo hash."""
    body = {k: v for k, v in record.items() if k != "hash"}
    blob = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def git_head():
    try:
        out = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return None


def git_dirty():
    try:
        out = subprocess.run(["git", "-C", ROOT, "status", "--porcelain"],
                             capture_output=True, text=True, check=True)
        return bool(out.stdout.strip())
    except Exception:
        return None


def append(kind, payload):
    log = read_log()
    prev = log[-1]["hash"] if log else None
    record = {
        "seq": len(log),
        "at": now_iso(),
        "kind": kind,
        "prev": prev,
        "head": git_head(),
        "dirty": git_dirty(),
    }
    record.update(payload)
    record["hash"] = line_hash(record)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    return record


def open_session(log):
    """Ultima sesion abierta y no cerrada, o None."""
    current = None
    for rec in log:
        if rec["kind"] == "session_open":
            current = rec
        elif rec["kind"] == "session_close":
            current = None
    return current


# --- clasificacion aparato / analisis --------------------------------------

def read_classification():
    rows = []
    with open(CLASSES, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, start=1):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                raise SystemExit("classification.tsv linea %d: se esperan 4 columnas" % n)
            path, klass, origin, rationale = parts[0], parts[1], parts[2], parts[3]
            if klass not in VALID_CLASSES:
                raise SystemExit("classification.tsv linea %d: clase invalida %r" % (n, klass))
            if origin not in VALID_ORIGINS:
                raise SystemExit("classification.tsv linea %d: origen invalido %r" % (n, origin))
            rows.append({"path": path, "class": klass, "origin": origin,
                         "rationale": rationale})
    return rows


def tracked_files():
    out = subprocess.run(["git", "-C", ROOT, "ls-files"],
                         capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p.strip()]


def is_binary(data):
    """Un fichero es binario si sus bytes no son texto.

    Hace falta distinguirlo porque contar los saltos de linea de un PDF y
    sumarlos a las lineas de analisis no mide esfuerzo ninguno: inflaria una
    cifra que el manuscrito imprime, con bytes que nadie ha escrito. La primera
    version de esta funcion buscaba un byte nulo, que es el criterio de costumbre
    y aqui no sirve: un PDF sin comprimir no tiene ninguno, y colaba 3421 lineas
    falsas. El criterio que decide es si el contenido se deja decodificar.
    """
    try:
        data.decode("utf-8")
        return False
    except UnicodeDecodeError:
        return True


def count_lines(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full, "rb") as fh:
        data = fh.read()
    if not data:
        return 0
    if is_binary(data):
        return None
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def classify(include_untracked=True):
    rows = read_classification()
    declared = {r["path"]: r for r in rows}
    present = set(tracked_files())
    if include_untracked:
        for r in rows:
            if os.path.exists(os.path.join(ROOT, r["path"])):
                present.add(r["path"])

    missing = sorted(p for p in present if p not in declared)
    if missing:
        raise SystemExit("sin clasificar en classification.tsv:\n  " + "\n  ".join(missing))

    per_file, totals, binarios = [], {}, []
    for path in sorted(present):
        r = declared[path]
        n = count_lines(path)
        if n is None:
            if os.path.exists(os.path.join(ROOT, path)):
                binarios.append(path)
            continue
        per_file.append({"path": path, "class": r["class"], "origin": r["origin"],
                         "lines": n})
        key = r["class"] + "/" + r["origin"]
        totals[key] = totals.get(key, 0) + n

    summary = {
        "aparato": sum(v for k, v in totals.items() if k.startswith("aparato/")),
        "analisis": sum(v for k, v in totals.items() if k.startswith("analisis/")),
        "analisis_propio": totals.get("analisis/propio", 0),
        "analisis_extraido": totals.get("analisis/extraido", 0),
        "aparato_propio": totals.get("aparato/propio", 0),
        "aparato_extraido": totals.get("aparato/extraido", 0),
        "binarios_no_contados": len(binarios),
    }
    return per_file, summary


# --- verificacion -----------------------------------------------------------

def verify():
    log = read_log()
    problems = []
    prev = None
    for i, rec in enumerate(log):
        if rec.get("seq") != i:
            problems.append("registro %d: seq %r no coincide con su posicion" % (i, rec.get("seq")))
        if rec.get("prev") != prev:
            problems.append("registro %d: prev roto" % i)
        if line_hash(rec) != rec.get("hash"):
            problems.append("registro %d: hash no coincide con el contenido" % i)
        prev = rec.get("hash")
    depth = 0
    for i, rec in enumerate(log):
        if rec["kind"] == "session_open":
            if depth:
                problems.append("registro %d: sesion abierta sobre otra sesion abierta" % i)
            depth += 1
        elif rec["kind"] == "session_close":
            if not depth:
                problems.append("registro %d: cierre sin apertura" % i)
            depth = 0
    return log, problems


# --- exportacion de recuentos ------------------------------------------------

EXPORT = os.path.join(ROOT, "results", "effort.tsv")


def export():
    """Emite results/effort.tsv con los recuentos que la seccion 9 imprime.

    Existe por una razon concreta: la seccion 9 del manuscrito hablaba de
    sesiones, de callejones sin salida y del reparto entre aparato y analisis sin
    imprimir ni una cifra, y no podia imprimirlas porque el congelador exige que
    toda cifra publicable salga de un fichero de results, y el registro de
    esfuerzo no emitia ninguno. Este subcomando cierra ese hueco.

    Todo lo que emite se deriva del propio log, y la primera fila dice si la
    cadena de hashes esta integra. Un recuento sacado de un registro roto no vale
    nada, asi que el fichero lleva esa comprobacion dentro y no al lado.
    """
    log, problems = verify()

    # CORTE, y esta decision importa. Se cuenta hasta el ultimo cierre de sesion
    # incluido, no hasta el final del log. Si se contara hasta el final, abrir
    # una sesion o anotar una decision cambiaria una cifra impresa en el
    # manuscrito, el congelador fallaria a media sesion y el texto habria que
    # refrescarlo a cada paso. Con este corte, las cifras solo se mueven cuando
    # una sesion se cierra, que es exactamente cuando toca refrescarlas.
    corte = 0
    for i, rec in enumerate(log):
        if rec["kind"] == "session_close":
            corte = i + 1
    vivos = log[:corte]

    tipos = {}
    for rec in vivos:
        tipos[rec["kind"]] = tipos.get(rec["kind"], 0) + 1

    aperturas = tipos.get("session_open", 0)
    cierres = tipos.get("session_close", 0)

    # el ultimo reparto calculado, que es el que vale
    ultima = None
    for rec in vivos:
        if rec["kind"] == "classification":
            ultima = rec
    resumen = ultima["summary"] if ultima else {}
    ficheros = len(ultima["files"]) if ultima else 0

    total = resumen.get("aparato", 0) + resumen.get("analisis", 0)
    extraido = (resumen.get("aparato_extraido", 0)
                + resumen.get("analisis_extraido", 0))

    filas = [
        ("cadena.integra", int(not problems),
         "si vale cero, ningun recuento de este fichero es de fiar"),
        ("problemas.de.la.cadena", len(problems), ""),
        ("corte", corte,
         "se cuenta hasta el ultimo cierre de sesion incluido, no hasta el "
         "final del log, para que la cifra no se mueva a media sesion"),
        ("registros", len(vivos),
         "lineas del registro append only hasta el corte"),
        ("sesiones.abiertas", aperturas, ""),
        ("sesiones.cerradas", cierres, ""),
        ("sesiones.sin.cerrar", aperturas - cierres, ""),
        ("dead_ends", tipos.get("dead_end", 0),
         "callejones sin salida registrados como entrada propia"),
        ("decisiones", tipos.get("decision", 0), ""),
        ("procedencias", tipos.get("provenance", 0), ""),
        ("notas", tipos.get("note", 0), ""),
        ("clasificaciones", tipos.get("classification", 0), ""),
        ("retroactivos", tipos.get("retroactive", 0),
         "registros reconstruidos, que no equivalen a uno tomado en vivo"),
        ("ficheros.clasificados", ficheros, ""),
        ("ficheros.binarios.no.contados",
         resumen.get("binarios_no_contados", 0),
         "sus saltos de linea no son lineas escritas y no se suman"),
        ("lineas.de.aparato", resumen.get("aparato", 0), ""),
        ("lineas.de.analisis", resumen.get("analisis", 0), ""),
        ("lineas.totales", total, ""),
        ("lineas.extraidas", extraido,
         "lineas que vienen de fuera y no se cuentan como escritas aqui"),
        ("lineas.de.analisis.propio", resumen.get("analisis_propio", 0), ""),
        ("lineas.de.aparato.propio", resumen.get("aparato_propio", 0), ""),
    ]

    os.makedirs(os.path.dirname(EXPORT), exist_ok=True)
    with open(EXPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Recuentos del registro de esfuerzo, derivados del log.\n")
        fh.write("# Emitido por: python tools/effort.py export\n")
        fh.write("# clave\tvalor\tnota\n")
        for k, v, n in filas:
            fh.write("%s\t%s\t%s\n" % (k, v, n))
        for p_ in problems:
            fh.write("PROBLEMA\t1\t%s\n" % p_)

    for k, v, _ in filas:
        print("  %-30s %s" % (k, v))
    return 1 if problems else 0


# --- ordenes -----------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="registro de esfuerzo append only")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("open")
    p.add_argument("--actor", required=True)
    p.add_argument("--decider", default=None)
    p.add_argument("--note", required=True)

    p = sub.add_parser("close")
    p.add_argument("--note", required=True)

    p = sub.add_parser("note")
    p.add_argument("--note", required=True)
    p.add_argument("--kind", default="note",
                   choices=["note", "dead_end", "decision", "provenance"])
    p.add_argument("--actor", default=None)
    p.add_argument("--decider", default=None)

    p = sub.add_parser("retro")
    p.add_argument("--note", required=True)
    p.add_argument("--when", required=True)
    p.add_argument("--actor", default=None)
    p.add_argument("--decider", default=None)

    sub.add_parser("classify")
    sub.add_parser("verify")
    sub.add_parser("status")
    sub.add_parser("export")

    args = ap.parse_args(argv)
    log = read_log()

    if args.cmd == "open":
        if open_session(log):
            raise SystemExit("ya hay una sesion abierta: cierrala antes de abrir otra")
        rec = append("session_open", {"actor": args.actor, "decider": args.decider or args.actor,
                                      "note": args.note, "live": True})
        print("sesion abierta seq=%d at=%s" % (rec["seq"], rec["at"]))

    elif args.cmd == "close":
        cur = open_session(log)
        if not cur:
            raise SystemExit("no hay sesion abierta que cerrar")
        rec = append("session_close", {"opened_seq": cur["seq"], "note": args.note,
                                       "live": True})
        print("sesion cerrada seq=%d at=%s (abierta en seq=%d)"
              % (rec["seq"], rec["at"], cur["seq"]))

    elif args.cmd == "note":
        rec = append(args.kind, {"note": args.note, "actor": args.actor,
                                 "decider": args.decider, "live": True})
        print("anotado seq=%d kind=%s" % (rec["seq"], rec["kind"]))

    elif args.cmd == "retro":
        rec = append("retroactive", {
            "note": args.note,
            "when_claimed": args.when,
            "actor": args.actor,
            "decider": args.decider,
            "live": False,
            "caveat": ("registro reconstruido: no equivale a un registro tomado en vivo, "
                       "y no se cuenta como tal"),
        })
        print("entrada retroactiva seq=%d" % rec["seq"])

    elif args.cmd == "classify":
        per_file, summary = classify()
        rec = append("classification", {"files": per_file, "summary": summary, "live": True})
        print("clasificacion seq=%d" % rec["seq"])
        for f in per_file:
            print("  %-40s %-9s %-9s %5d" % (f["path"], f["class"], f["origin"], f["lines"]))
        print("  " + json.dumps(summary, sort_keys=True))

    elif args.cmd == "verify":
        log, problems = verify()
        print("registros: %d" % len(log))
        if problems:
            for p_ in problems:
                print("PROBLEMA: " + p_)
            return 1
        print("cadena integra, append only sin roturas")
        cur = open_session(log)
        print("sesion abierta: " + ("seq=%d" % cur["seq"] if cur else "ninguna"))

    elif args.cmd == "export":
        return export()

    elif args.cmd == "status":
        cur = open_session(log)
        print("registros: %d" % len(log))
        print("sesion abierta: " + ("seq=%d desde %s" % (cur["seq"], cur["at"]) if cur else "ninguna"))
        for rec in log:
            print("  seq=%-3d %-15s %s %s" % (rec["seq"], rec["kind"], rec["at"],
                                              (rec.get("note") or "")[:70]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
