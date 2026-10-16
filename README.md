# Avance · Nueva App Inversiones y Rocket (Consubanco)

Reporte ejecutivo del avance de la Nueva App Inversiones: Cuenta Digital N4 y Rocket, desarrollada con Ikitech.

**Link público:** https://mnieto-consubanco.github.io/nueva-app-inversiones-y-rocket/

El reporte se actualiza **cada jueves a las 23:59 (CDMX)** con tres fuentes:

1. **ClickUp** (espacio CSB-Ikitech): etapa de cada HU y avance de front y back.
2. **Hoja "Layout _Épicas y HU"**: alcance completo de épicas y HUs.
3. **Master Gantt de Ikitech**: el archivo `.xlsx` más reciente del repositorio **privado** `mnieto-consubanco/fuentes-avance-inversiones` (carpeta `ikitech/`). Los archivos de origen nunca se guardan en este repositorio público.

## Cómo subir el archivo semanal de Ikitech

1. Entra al repositorio **privado** `mnieto-consubanco/fuentes-avance-inversiones`, carpeta `ikitech/`.
2. Usa **Add file › Upload files** y arrastra el `.xlsx`.
3. Renómbralo con la fecha al inicio, por ejemplo `2026-10-22_consubanco_project_gantt_roadmap.xlsx`.
4. Da clic en **Commit changes**. Súbelo antes del jueves a las 23:59.

## Estructura

```
index.html              Página publicada (se genera, no editar a mano)
descargas/              PDF descargable del reporte
data/hus.json           HUs con etapa y avance front/back
data/reporte.json       Plan de Ikitech, textos, entregado y equipo
src/template.html       Diseño (look and feel Grupo Consupago)
src/build.py            Genera index.html y el PDF
src/assets/             Logo y favicon (guía de uso del logotipo de Consubanco)
RUNBOOK.md              Procedimiento detallado de la actualización semanal
```

Para regenerar el reporte a mano, corre `python3 src/build.py`. Requiere Playwright para el PDF.
