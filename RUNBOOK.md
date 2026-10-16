# Runbook: actualización semanal del reporte

Este documento es la guía que sigue Claude cada jueves a las 23:59 (hora de la Ciudad de México) para actualizar el reporte. También sirve para hacerlo a mano.

- **Link público:** https://mnieto-consubanco.github.io/nueva-app-inversiones-y-rocket/
- **Responsable (PO):** Martín Nieto
- **Repositorio:** `mnieto-consubanco/nueva-app-inversiones-y-rocket`

## Fuentes

| Fuente | Dónde está | Qué aporta |
|---|---|---|
| ClickUp | Espacio **CSB-Ikitech** (id `90146380570`) | Etapa de cada HU, avance front/back por subtareas, entregas recientes, quién trabaja en qué |
| Hoja de épicas "Layout _Épicas y HU" | Google Sheets, id en `data/reporte.json` → `meta.hoja_epicas_id` | HUs del alcance que aún no existen en ClickUp (backlog) y nombres de épicas |
| Master Gantt de Ikitech | Google Drive, archivo `consubanco_project_gantt_roadmap.xlsx` (fileId `1f0aMSS-JAf1Lst2H9VL68gUPf8-7KKgQ`). Ikitech lo actualiza en el mismo archivo. Nunca lo copies al repositorio público | Avance real por proyecto y componente, roadmap de 21 semanas, sprints, hitos, habilitadores del banco y alertas |

Listas de producto en ClickUp (las únicas que cuentan como HUs):

| Lista | id | Épica en el reporte |
|---|---|---|
| 00_Linamiento de experiencia | 901417906899 | Experiencia |
| 01_OnBoarding | 901418117579 | Onboarding |
| 02_Cimentación Arquitectónica… | 901418751676 | Cimentación técnica (solo HU-T01 a T05; los Spikes no son HUs) |
| 03 Inicio de Sesión | 901421672935 | Inicio de sesión |
| Apertura de cuenta Digital N4 | 901418305319 | Cuenta Digital N4 |
| Apertura cuenta Rocket | 901417906259 | Rocket |
| Cuenta Rocket en App | 901421926946 | Manejo cuenta Rocket |
| Cuenta Rocket en Consola | 901421928782 | Consola Rocket |

Las listas de casos de prueba, sprints y Greenfield no son HUs y no se cuentan.

## Archivos que se actualizan

- `data/hus.json`: una entrada por HU con `epica, codigo, nombre, etapa, devs, nota, link, f, b, avance, fs, bs`.
- `data/reporte.json`: todo el contenido del reporte (fechas de corte, plan de Ikitech, alertas, entregado, equipo, sprint actual).
- **No** se edita el diseño (`src/template.html`) salvo que algo se vea roto.

## Paso 1. ClickUp → `data/hus.json`

1. Lee las tareas principales de las listas de producto con `clickup_filter_tasks` (`include_closed: true`, `subtasks: false`).
2. **Etapa de cada HU:**
   - `complete` → **Completada**
   - `en progreso` → **En progreso**
   - `to do` con la etiqueta `refinadas` → **Refinada, por iniciar**
   - `to do` sin esa etiqueta → **Por refinar**
   - HU que está en la hoja de épicas y no existe en ClickUp → **En backlog**
3. **Avance front/back** (solo para HUs en progreso). Usa el operador `task.get_many` con la consulta `tasks[*].data.{id:id,n:name,subs:subtask_ids}`. Después vuelve a llamarlo con los ids de las subtareas y la consulta `tasks[*].data.{id:id,n:name,s:status.status,p:direct_parent}`.
   - Las subtareas que se llaman Front/Frontend/front (incluidas "Frontend n4" y "Frontend rocket") son **front**. Las que se llaman Back/Backend/BackEnd son **back**.
   - Si la HU no tiene subtareas con esos nombres, clasifícalas por su contenido. Pantallas, maquetación y ajustes visuales son front. Endpoints, integraciones, tablas, SDK y llamados a servicios son back.
   - `f` = subtareas de front en `complete` ÷ total de subtareas de front. `b` = lo mismo con back. Si no hay subtareas de back, `b = 0`.
   - `avance = round(50*f + 50*b)`. Las completadas valen 100 (`f=b=1`) y las demás etapas valen 0.
   - `fs` y `bs`: "Listo" si vale 1; "En curso" si es mayor que 0 o si alguna subtarea está `en progreso`; "Pendiente" en otro caso. Para las HUs que no están en progreso deja `fs` y `bs` vacíos, excepto las completadas, que llevan "Listo".
4. **Códigos y nombres.** El código de ClickUp manda. Si una HU nueva de ClickUp choca con un código de la hoja, la de la hoja queda con código `—`. Escribe los nombres en español claro y sin jerga, como los que ya existen.
5. **Equipo (`devs`):** usa los asignados de las subtareas (Dev01–Dev05).
6. **Nota:** máximo una frase positiva y concreta, por ejemplo "Front terminado el 14 oct".

## Paso 2. Hoja de épicas

Lee la hoja (id en `meta.hoja_epicas_id`) con el conector de Google Sheets. Agrega las HUs nuevas del alcance que no existan en ClickUp, con etapa **En backlog**. **Nunca** menciones en el reporte diferencias entre la hoja y ClickUp.

## Paso 3. Master Gantt de Ikitech → `data/reporte.json`

Lee el archivo con el conector de **Google Drive**:

1. `get_file_metadata` con el fileId `1f0aMSS-JAf1Lst2H9VL68gUPf8-7KKgQ`. Si `modifiedTime` (convertido a hora de la CDMX) no es posterior a `meta.corte_ikitech`, conserva el plan como está y solo revisa los textos que dependen de la fecha.
2. Si es más nuevo, `download_file_content` devuelve el `.xlsx` en base64 (campo `content`). Decodifícalo a un archivo **fuera** del repositorio (por ejemplo `/tmp/ikitech/gantt.xlsx`) y ábrelo con openpyxl para leer valores y colores de celda. `read_file_content` sirve para una lectura rápida del texto, pero no trae los colores del gantt.
3. Compara contra el corte anterior y aplica solo lo que cambió.

- **Pestaña "Executive Dashboard 360":**
  - Semana y sprint activo → `meta.roadmap.semana_actual` y `meta.sprint`.
  - Avance real de N4 y Rocket → `proyectos[*][2]`.
  - Alertas críticas → `alertas`, redactadas en tono positivo (ver Paso 5).
  - Proyección por sprint (Sprint 0 a 6) → `sprints`, en lenguaje claro.
- **Pestaña "Gantt Project Control":**
  - Cada fila 1.x / 2.x se vuelve un componente de `proyectos` y de `gantt_master`, con su peso, avance y estado.
  - Las filas 3.x van a `deps` y al grupo "Habilitadores del banco" del gantt.
  - Colores de celda de las semanas W1–W21 (columnas H a AB) → tipo de segmento:
    - `D9D9D9` = `prep`
    - `366092` = `done`
    - `FFC000` = `cur`
    - `C00000` = `dep`
    - `E6B8B7` = `risk`
    - `95B3D7` = `proj`
    - `FFD966` = `ms` (ventana de hito)
    - `C6EFCE` = `ok`
  - Los índices de semana empiezan en 0 (W1 = 0).
- `meta.corte_ikitech` = la fecha de `modifiedTime` del archivo en Drive (hora de la CDMX).
- Revisa `hitos_plan` y `rail.hitos` contra el archivo.

Si encuentras inconsistencias dentro del archivo de Ikitech (totales que no cuadran con los pesos, dos fechas para un mismo hito), **no** las pongas en el reporte. Repórtalas a Martín en el resumen final.

## Paso 4. Entregado y equipo

- Busca las tareas y subtareas cerradas desde el corte anterior con `clickup_filter_tasks` (`subtasks: true`, `date_closed_from` = corte anterior). Agrúpalas por día y frente, y agrega entradas a `entregado` con el formato `[fecha ISO, "rango legible", frente, texto]`. Frentes válidos: Onboarding, N4, N4 servicios, N4 y Rocket, Rocket, Calidad, Experiencia, Sprint, App, Arquitectura, Servicios, Base.
- Actualiza `equipo` (Entregado / En curso por Dev) con base en los asignados y estados recientes.
- No borres entregas anteriores.

## Paso 5. Textos y tono (obligatorio)

- Tono positivo y políticamente correcto. En lugar de "bloqueado", "pausado" o "impedimento" usa "Requiere atención", "Con dependencia del banco" o "Siguiente paso".
- Sin jerga técnica. Por ejemplo, "bureau" se dice "revisión del teléfono en listas de riesgo" y "OTP" se dice "código SMS".
- No menciones comparativas entre la hoja de épicas y ClickUp. No agregues una sección de acuerdos.
- Sí deja explícito el impacto en fechas que Ikitech estime, por ejemplo "estima un ajuste de 1 a 1.5 sprints".
- Actualiza `meta.corte_clickup` con la fecha de la corrida y `hero.contexto` con el sprint y la semana actuales.
- Si cambió el sprint, arma `sprint_actual` con la fila de `sprints` correspondiente:
  - Título y fechas del sprint.
  - Alcance de N4 y de Rocket.
  - Grupos del gantt con las HUs en progreso de N4, Rocket, Calidad, Habilitadores y Definición.
  - Cierre del sprint y sus hitos.

## Paso 6. Construir, verificar y publicar

```bash
python3 src/build.py
```

1. Verifica en Playwright `index.html`: sin errores de consola, que las 6 pestañas rendericen y que el PDF tenga 15 páginas o menos.
2. Haz commit con el mensaje `Actualización semanal (corte AAAA-MM-DD)` y push a `main`. GitHub Pages publica en 1 o 2 minutos.

## Paso 7. Resumen para Martín

Envía un mensaje breve con:

- Las cifras principales: avance de N4 y Rocket según Ikitech, avance por HU y días para el fin de desarrollo.
- Qué cambió en la semana: HUs nuevas, completadas y entregas.
- Las alertas nuevas.
- Las inconsistencias que encontraste en las fuentes.
- Si falta algo, por ejemplo si no llegó un archivo nuevo de Ikitech.
