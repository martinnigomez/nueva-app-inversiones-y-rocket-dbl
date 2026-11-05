# Avance · Nueva App Inversiones y Rocket (Consubanco)

Reporte ejecutivo del avance de la Nueva App Inversiones: Cuenta Digital N4 y Rocket, desarrollada con Ikitech.

**Link público:** https://martinnigomez.github.io/nueva-app-inversiones-y-rocket-dbl/

El reporte se actualiza **cada jueves a las 23:59 (CDMX)** con tres fuentes:

1. **ClickUp** (espacio CSB-Ikitech): etapa de cada HU y avance de front y back.
2. **Hoja "Layout _Épicas y HU"**: alcance completo de épicas y HUs.
3. **Master Gantt de Ikitech**: el archivo `consubanco_project_gantt_roadmap.xlsx` en Google Drive, que se lee en línea con el conector de Drive. Los archivos de origen nunca se guardan en este repositorio público.

## Archivo de Ikitech en Google Drive

Ikitech debe actualizar **siempre el mismo archivo** de Drive: editándolo directamente o con **Administrar versiones › Subir nueva versión**. Si sube un archivo nuevo con otro nombre, el reporte seguirá leyendo el anterior.

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
