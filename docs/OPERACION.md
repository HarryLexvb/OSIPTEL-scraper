# Operación y recuperación

> Publicación en GitHub: esta distribución conserva el código auditado, con usuario y contraseña vacíos en `config.py` y `ProxyConfig`. Las referencias a credenciales embebidas describen la copia local auditada; la externalización sigue pendiente. Se conserva el archivo MIT `LICENSE` ya existente en el repositorio de destino. No se publican CSV operativos, resultados, ZIP ni cachés.

Estado revisado: 16/11/2026. [Volver al Índice](../README.md).

## Entorno e instalación

Trabaje desde la carpeta interior del repositorio. Las rutas de entrada, salida e instalador se resuelven respecto del directorio de trabajo. Dependencias declaradas: Camoufox, aiofiles, aiohttp, pandas, openpyxl y psutil; sus rangos están en [requirements.txt](../requirements.txt). No hay lockfile ni garantía de reproducir exactamente un entorno anterior.

La instalación manual está en el README. Como alternativa, `start.bat` verifica Python y, si no lo encuentra, intenta descargar e instalar Python 3.12.10 para todos los usuarios, refrescar PATH, crear/activar venv, instalar dependencias, descargar Camoufox y crear rucs. Esa versión es la fijada en el script, no una afirmación sobre la versión más reciente de Python.

Ejecute el BAT desde su propia carpeta. No cambia de directorio por sí mismo. Puede requerir privilegios para instalar Python. Su refresco de PATH tiene problemas de expansión de variables en bloques y un fallo de descarga de Camoufox no impide que anuncie instalación completa. Verifique el resultado de cada etapa. No se ejecutó el instalador durante la revisión documental.

## Entrada admitida por el flujo habitual

Use CSV separado por comas, con cabecera y RUC en primera columna:

```csv
RUC
20100047218
20100130204
```

`AutoScraper.initialize` busca una columna cuyo nombre contenga ruc; el lector central toma siempre la primera; la limpieza usa otra heurística. Una única columna `RUC` evita esa discrepancia. Ambos lectores asumen cabecera: un archivo sin ella pierde la primera fila como dato. El lector central conserva caracteres numéricos y acepta longitud 11; no comprueba el dígito verificador ni deduplica. El preconteo automático exige once caracteres numéricos tras strip y puede diferir de la normalización posterior.

El lector central reconoce xlsx/xls, pero `run_auto.py` llama read_csv antes de alcanzarlo: no anuncie Excel como entrada funcional del lanzador. El motor de xls no está declarado en dependencias. `osiptel_main.py` puede ejecutarse directamente para su menú interno, pero usa otros defaults y no carga config.py; no es un reemplazo equivalente.

## Ejecución

Con la instalación lista, use una copia de trabajo del CSV y una carpeta nueva para una corrida nueva:

```powershell
.\venv\Scripts\python.exe run_auto.py 'rucs/mi_copia.csv' --output 'osiptel_output/corrida_001'
```

El menú aparece incluso antes de procesar argumentos como `--help`. Selección 1: detección inicial; selección 2: workers manuales de 1 a 50. Aun en modo manual se realiza la detección inicial de recursos/red. No existe --workers ni --no-cleanup ni --no-resume en la CLI.

| Argumento | Default | Efecto real |
|---|---|---|
| input_file | Obligatorio | Archivo comprobado mediante exists; lectura posterior CSV |
| --output / -o | osiptel_output | Directorio de resultados y progreso |
| --bandwidth / -b | 10000 | Valor nominal de presupuesto y reportes; **no corta tráfico** |

`AutoScraper` crea `<entrada>.backup` si no existe; no lo refresca en corridas posteriores. El backup está junto a la entrada, no en rucs/backups. No sustituye copias por corrida.

## Salidas y contratos

| Ruta relativa al output | Contenido / comportamiento |
|---|---|
| resultados.csv | Solo resultados SUCCESS, anexados; 301 columnas: RUC + 100 grupos Modalidad_i, Numero_Telefonico_i, Empresa_Operadora_i |
| progress.json | processed_rucs, failed_rucs, statistics y last_save; temporal .tmp seguido de os.replace |
| failed_rucs.csv | RUC, Error_Type, Error_Message, Attempts; generado al cierre si hay fallidos, con mensajes recortados |
| statistics.json | Resumen del orquestador al cierre |
| scraper.log | Log detallado anexado |
| save/<entrada>_1000_parteN.csv | Hasta 1000 resultados exitosos por lote; último lote puede ser menor; mismo esquema de 301 columnas |
| save/<entrada>_timing_report.json | summary y batches de los lotes del escritor actual |
| performance_report.json | timing, rucs, speed, bandwidth, workers, errors, retry_count, finish_reason del lanzador |

El 1000 cuenta resultados exitosos enviados al escritor, no todas las consultas. Un éxito sin líneas produce una fila con solo RUC. RUCResult.to_dict no serializa el detalle de PhoneLine: progress.json no permite reconstruir números perdidos. Las estadísticas pueden contar más de 100 líneas aunque la exportación descarte las adicionales. No hay archivo de errores actualizado por consulta.

## Reanudación e interrupciones

Reutilizar el mismo CSV de trabajo y el mismo --output carga progress.json y omite los RUC de processed_rucs, incluidos fallidos. Resultados CSV se anexan. Sin embargo, índices de lote y tiempos empiezan de cero: los parciales anteriores pueden sobrescribirse. Antes de reanudar, preserve una copia del output y del CSV; no trate los parciales como respaldo acumulativo fiable.

Ctrl+C activa la parada del orquestador, solicita detener workers, espera tres segundos y cancela los restantes. Después intenta drenar resultados durante diez segundos y guardar pendientes del escritor, progreso y reportes. No garantiza completar todas las consultas en curso ni vaciar la cola. El reporte automático puede seguir diciendo completed.

No edite progress.json para forzar reintentos sin reconciliar CSV y lotes: puede duplicar datos o perder trazabilidad. Para reintentar fallidos, prepare un CSV de trabajo a partir de failed_rucs.csv con RUC como primera columna y use otro output; esto no recupera los falsos éxitos vacíos, que requieren revisión separada. Una corrida nueva con nuevo output puede volver a consultar RUC ya existentes: no hay deduplicación global.

No ejecute dos procesos con la misma entrada/output: no hay bloqueo entre procesos y el .tmp de progreso tiene un nombre común. Como práctica operativa, deje cerrar el proceso y sincronizar OneDrive antes de copiar o comparar resultados.

## Diagnóstico

| Síntoma | Comprobación |
|---|---|
| Error de importación | Asegurar intérprete del venv y dependencias instaladas |
| No abre navegador | Revisar log y resultado de python -m camoufox fetch |
| Proxy falla | Revisar config.py y log; is_configured solo verifica valores no vacíos, no autentica |
| Muchos éxitos vacíos | Contrastar una muestra con consultas válidas; no asumir ausencia de líneas |
| Menos filas que consultas | Fallidos no entran al CSV principal; revisar consumidor y errores de escritura |
| Reporte negativo o ETA extraña | Estadísticas restauradas se mezclan con el tamaño actual de una entrada que se va reduciendo |
| Consumo mayor al presupuesto | Corte desactivado y consumo fijo estimado, no medido |
| Lotes desaparecidos | Reanudación reinició parteN; conservar snapshot antes de continuar |

`remove_duplicates.py` no es diagnóstico: ejecuta operaciones al importar, usa rutas fijas a resultados.csv y rucs/ruc_faltante_osiptel_parte1.csv y reescribe este último sin backup propio. No se integra al flujo habitual. `download_geoip.py` llama una API ausente en la clase instalada durante la revisión local; GeoIP está desactivado en el navegador principal. Ninguno es requisito de instalación.
