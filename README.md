# OSIPTEL Scraper

Scraper local asíncrono para consultar líneas telefónicas por RUC en OSIPTEL, con navegadores concurrentes, sesiones de proxy, reintentos, resultados CSV y checkpoints de progreso. El punto de entrada es `run_auto.py`.

**Autor:** Harold Alejandro Villanueva Borda

**Contacto:** [harrylex8@gmail.com](mailto:harrylex8@gmail.com)

## Índice

- [Documentación: qué necesitas consultar](#documentación-qué-necesitas-consultar)
- [Stack tecnológico](#stack-tecnológico)
- [Inicio rápido](#inicio-rápido)
- [Estado actual y limitaciones importantes](#estado-actual-y-limitaciones-importantes)
- [Estructura esencial](#estructura-esencial)
- [Mejoras pendientes](#mejoras-pendientes)
- [Validación y licencia](#validación-y-licencia)

## Documentación: qué necesitas consultar

| Necesidad | Lectura recomendada | Accesos directos |
|---|---|---|
| Instalar y ejecutar | [Operación](docs/OPERACION.md) | [Instalación](docs/OPERACION.md#entorno-e-instalación) · [Entrada CSV](docs/OPERACION.md#entrada-admitida-por-el-flujo-habitual) · [Ejecución](docs/OPERACION.md#ejecución) |
| Encontrar resultados o retomar una corrida | [Operación y recuperación](docs/OPERACION.md) | [Archivos de salida](docs/OPERACION.md#salidas-y-contratos) · [Reanudación](docs/OPERACION.md#reanudación-e-interrupciones) · [Diagnóstico](docs/OPERACION.md#diagnóstico) |
| Ajustar workers, delays, intentos o consumo | [Configuración efectiva](docs/CONFIGURACION.md) | [Precedencia real](docs/CONFIGURACION.md#fuentes-de-configuración) · [Recursos](docs/CONFIGURACION.md#heurísticas-de-recursos) · [Valores internos](docs/CONFIGURACION.md#valores-efectivos-internos) |
| Entender o modificar el código | [Arquitectura](docs/ARQUITECTURA.md) | [Flujo](docs/ARQUITECTURA.md#componentes-y-flujo) · [Extracción](docs/ARQUITECTURA.md#proxy-navegador-y-extracción) · [Persistencia](docs/ARQUITECTURA.md#persistencia-y-concurrencia) |
| Revisar errores y mejoras propuestas | [18 gaps y criterios de aceptación](docs/GAPS_Y_MEJORAS.md) | [Prioridades](docs/GAPS_Y_MEJORAS.md#prioridades) · [Orden de trabajo](docs/GAPS_Y_MEJORAS.md#secuencia-propuesta) · [Plan por etapas](docs/GAPS_Y_MEJORAS.md#plan-de-implementación-por-etapas) |
| Localizar clases y funciones o conocer la evidencia | [Revisión del código](docs/REVISION_CODIGO.md) | [Validaciones](docs/REVISION_CODIGO.md#evidencia-y-límites) · [Índice de símbolos](docs/REVISION_CODIGO.md#inventario-de-archivos-y-símbolos) |

La documentación describe el código revisado el **16/11/2026**. Las propuestas están identificadas como pendientes; documentarlas no significa que estén implementadas.

## Stack tecnológico

| Componente | Tecnología y uso |
|---|---|
| Lenguaje y concurrencia | **Python 3.10+**, asyncio: tareas, colas y coordinación de workers |
| Automatización | **Camoufox**, navegador basado en Firefox; JavaScript/DOM para formularios y tablas |
| Procesamiento y archivos | **pandas**, **openpyxl** y **aiofiles**; resultados/progreso en CSV y JSON |
| Red y recursos | **aiohttp**, **psutil** y proxy residencial SmartProxy |
| Entorno y herramientas | Windows, Batch/PowerShell, venv/pip, Git y GitHub |

Los rangos de versiones están en [requirements.txt](requirements.txt). No hay lockfile, base de datos, framework web ni API implementada. El soporte interno de Excel no convierte al lanzador automático en compatible con Excel: actualmente exige CSV.

## Inicio rápido

Desde la raíz del proyecto, prepare el entorno:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m camoufox fetch
```

En la copia de OneDrive, la raíz real es la carpeta interior:

```text
C:\Users\harry\OneDrive\Documentos\osiptel scraper v2\osiptel scraper v2
```

Revise las credenciales de proxy en `config.py`. La distribución de GitHub las publica vacías; la copia local auditada conserva su configuración privada. Consulte la [configuración efectiva](docs/CONFIGURACION.md#fuentes-de-configuración): varios parámetros de config.py no se aplican al ejecutar run_auto.py.

Prepare una **copia de trabajo** del CSV con cabecera `RUC` en la primera columna. Conserve el original por separado: el flujo actual puede retirar de la entrada tanto éxitos como fallidos. Para una corrida nueva, elija un output nuevo:

```powershell
.\venv\Scripts\python.exe run_auto.py 'rucs/mi_copia.csv' --output 'osiptel_output/corrida_001'
```

El programa solicita modo automático o manual de workers. Los pasos completos, el instalador alternativo y los contratos de entrada/salida están en [Operación](docs/OPERACION.md).

## Estado actual y limitaciones importantes

El motor implementa workers, reintentos, guardado incremental, lotes y progreso, pero **todavía tiene gaps de integridad y recuperación**:

- Puede aceptar una consulta vacía sin verificar que terminó correctamente; un `success` no demuestra ausencia de líneas.
- No recorre toda la paginación y el escritor guarda como máximo 100 líneas por RUC.
- Al reanudar puede sobrescribir lotes anteriores; los fallidos también quedan marcados como procesados.
- El cierre no garantiza vaciar la cola de resultados y no hay transacción entre CSV y progreso.
- `--bandwidth` no detiene el consumo: la cifra registrada es una estimación, no tráfico medido.

Antes de reanudar, preserve el CSV y el output y consulte [Recuperación](docs/OPERACION.md#reanudación-e-interrupciones). El detalle de problemas, evidencia y criterios de corrección está en [Gaps y mejoras](docs/GAPS_Y_MEJORAS.md).

## Estructura esencial

| Archivo / carpeta | Responsabilidad |
|---|---|
| run_auto.py | Preparación, menú de workers, ejecución y reporte final |
| osiptel_main.py | Orquestación, colas, coordinación y cierre |
| osiptel_worker.py | Proxy, navegador, extracción y reintentos |
| osiptel_core.py | Modelos, progreso, estadísticas, CSV y lotes |
| system_optimizer.py | Recursos del equipo, heurísticas y gestión de entrada |
| config.py / requirements.txt / start.bat | Configuración, dependencias e instalación Windows |
| docs/ | Manuales técnicos, gaps y revisión del código |
| rucs/ / osiptel_output/ | Entradas y salidas locales; output se crea al ejecutar |

Los auxiliares `download_geoip.py` y `remove_duplicates.py` tienen limitaciones y no son pasos requeridos del flujo principal; consulte [Diagnóstico](docs/OPERACION.md#diagnóstico). El ZIP local es un respaldo histórico, no documentación vigente ni un componente de runtime. CSV operativos, resultados, ZIP y cachés se excluyen de la publicación.

## Mejoras pendientes

| Prioridad | Resultado buscado | Dónde leer |
|---|---|---|
| **P0 — Integridad y recuperación** | Validar vacíos, extraer/exportar todo, conservar lotes, recuperar fallidos y cerrar sin pérdida | [G01–G06](docs/GAPS_Y_MEJORAS.md#g01--p0--éxitos-vacíos-sin-evidencia) |
| **P1 — Operación y validación** | Configuración unificada, secretos externos, presupuesto efectivo, aislamiento, reportes fieles y pruebas | [Registro de gaps](docs/GAPS_Y_MEJORAS.md) |
| **P2 — Mantenimiento y eficiencia** | Mejorar heurísticas, esperas, instalador, auxiliares y versionado | [Plan por etapas](docs/GAPS_Y_MEJORAS.md#plan-de-implementación-por-etapas) |

Cada gap incluye impacto, referencia al código, mejora propuesta y aceptación. El [plan de implementación](docs/GAPS_Y_MEJORAS.md#plan-de-implementación-por-etapas) conserva las propuestas de almacenamiento transaccional y exportación normalizada; son opciones futuras, no componentes actuales.

## Validación y licencia

No hay suite automatizada ni CI. La revisión combina análisis estático y pruebas locales controladas; no certifica compatibilidad actual con OSIPTEL, funcionamiento del proveedor o rendimiento real. Consulte [Evidencia y límites](docs/REVISION_CODIGO.md#evidencia-y-límites).

El repositorio publicado conserva la [licencia MIT](https://github.com/HarryLexvb/OSIPTEL-scraper/blob/main/LICENSE). Las etiquetas históricas 1.0/3.0/6.0 no representan un versionado consistente ni una garantía de estabilidad productiva.
