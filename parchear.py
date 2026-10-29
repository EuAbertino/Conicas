#!/usr/bin/env python3
"""Cambia el boton X de los SWF para que recargue la portada (index.html)
en vez de cargar portada1.swf dentro del propio reproductor, que Ruffle no aguanta."""
import sys, zlib, pathlib

VIEJO = b"\x83\x15\x00portada1.swf\x00_level0\x00"
NUEVO = b"\x83\x15\x00index.html?r=1\x00_self\x00"
assert len(VIEJO) == len(NUEVO)

carpeta = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
total = 0
for f in sorted(carpeta.rglob("*.swf")):
    datos = f.read_bytes()
    firma = datos[:3]
    if firma == b"CWS":
        cuerpo = datos[:8] + zlib.decompress(datos[8:])
    elif firma == b"FWS":
        cuerpo = datos
    else:
        print(f"{f}: formato no soportado ({firma!r}), lo salto")
        continue
    n = cuerpo.count(VIEJO)
    if n:
        cuerpo = cuerpo.replace(VIEJO, NUEVO)
        if firma == b"CWS":
            cuerpo = cuerpo[:8] + zlib.compress(cuerpo[8:], 9)
        f.write_bytes(cuerpo)
        total += n
        print(f"{f}: {n} boton(es) arreglado(s)")
print(f"Listo. Total: {total}")
