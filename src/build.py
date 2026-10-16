#!/usr/bin/env python3
"""Genera el reporte de avance de la Nueva App Inversiones y Rocket.

Entradas:
  data/hus.json        HUs con etapa y avance front/back (ClickUp + hoja de épicas)
  data/reporte.json    Contenido del plan de Ikitech y textos del reporte
  src/template.html    Diseño (look and feel Grupo Consupago)
  src/fonts.css        Fuentes Merriweather y Source Sans 3 incrustadas
  src/assets/*.png     Logo y favicon de Consubanco (tomados de la guía de marca)

Salidas:
  index.html                          Página publicada en GitHub Pages
  descargas/Avance_App_Inversiones.pdf PDF descargable (A4 horizontal)
  build/artifact.html                 Versión sin botón de PDF (para compartir como archivo)

Uso:  python3 src/build.py            (genera HTML y PDF)
      python3 src/build.py --sin-pdf  (solo HTML)
"""
import base64, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def b64(name):
    return base64.b64encode((SRC / "assets" / name).read_bytes()).decode()


def render(pdf_button: bool, robots: bool) -> str:
    tpl = (SRC / "template.html").read_text(encoding="utf-8")
    hus = json.loads((ROOT / "data" / "hus.json").read_text(encoding="utf-8"))
    rep = json.loads((ROOT / "data" / "reporte.json").read_text(encoding="utf-8"))
    btn = ('<a class="btn btn--ghost" href="descargas/Avance_App_Inversiones.pdf" download>Descargar PDF</a>\n    '
           if pdf_button else "")
    body = (tpl.replace("__FONTS__", (SRC / "fonts.css").read_text(encoding="utf-8"))
               .replace("__FAV64__", b64("favicon_64.png"))
               .replace("__FAV180__", b64("favicon_180.png"))
               .replace("__LOGO__", b64("logo_header.png"))
               .replace("__PDFBTN__", btn)
               .replace("__HUS__", json.dumps(hus, ensure_ascii=False))
               .replace("__R__", json.dumps(rep, ensure_ascii=False)))
    i = body.index("<header class=\"masthead\">")
    meta = ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<meta name="theme-color" content="#1B355D">\n')
    if robots:
        meta += '<meta name="robots" content="noindex, nofollow">\n'
    return ("<!doctype html>\n<html lang=\"es-MX\">\n<head>\n" + meta + body[:i] +
            "</head>\n<body>\n" + body[i:] + "\n</body>\n</html>\n")


def main():
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "descargas").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(render(True, True), encoding="utf-8")
    (ROOT / "build" / "artifact.html").write_text(render(False, False), encoding="utf-8")
    print("HTML generado: index.html y build/artifact.html")
    if "--sin-pdf" in sys.argv:
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto((ROOT / "build" / "artifact.html").as_uri())
        pg.wait_for_timeout(1500)
        pg.pdf(path=str(ROOT / "descargas" / "Avance_App_Inversiones.pdf"), format="A4", landscape=True,
               print_background=True, scale=0.8, prefer_css_page_size=True)
        b.close()
    print("PDF generado: descargas/Avance_App_Inversiones.pdf")


if __name__ == "__main__":
    main()
