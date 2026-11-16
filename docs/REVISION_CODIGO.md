# Revisión del código y trazabilidad

> Publicación en GitHub: esta distribución conserva el código auditado, con usuario y contraseña vacíos en `config.py` y `ProxyConfig`. Las referencias a credenciales embebidas describen la copia local auditada; la externalización sigue pendiente. Se conserva el archivo MIT `LICENSE` ya existente en el repositorio de destino. No se publican CSV operativos, resultados, ZIP ni cachés.

Fecha: 16/11/2026. [Índice](../README.md).

## Alcance y método

Revisión de los ocho archivos Python completos (2964 líneas físicas), configuración, requirements, instalador BAT de 238 líneas y .gitignore. Se analizaron flujo, ramas, JavaScript embebido, excepciones, efectos secundarios, concurrencia, lectura/escritura y consumidores de configuración. La lectura se complementó con las comparaciones previas del mismo código y pruebas locales controladas. No se afirma corrección formal ni cobertura exhaustiva de todos los estados del sitio.

La única documentación Markdown editable existente era README.md. Se reescribió y se añadieron documentos de referencia. No se editaron .md empaquetados en ZIP: son parte de un respaldo histórico, no documentación activa. No se editaron fuentes, CSV, ZIP, dependencias ni cachés.

## Evidencia y límites

| Comprobación | Resultado y alcance |
|---|---|
| Sintaxis AST | Ocho fuentes Python válidas; no demuestra corrección semántica |
| CSV con 1, 12 y 101 líneas simuladas | Siempre 301 columnas; se omite la línea 101 |
| Dos escritores consecutivos sobre mismo output temporal | Reanudar reemplaza parte1 y su historial de tiempos |
| Progreso de un RUC FAILED simulado | No vuelve a get_pending_rucs |
| Página simulada sin tabla | scrape_ruc retorna SUCCESS con cero líneas |
| API local GeoIP | AsyncCamoufox instalado carecía de download_geoip; no se extrapola a todas las versiones del rango |
| Lectura de Git | último commit base e036086 del 05/04/2026; no se contactó remoto |

Las reproducciones corresponden a la revisión local de esta conversación anterior a la edición documental; no se ejecutaron consultas reales de RUC ni se autenticó contra el proxy. Importar dependencias durante esa revisión descargó definiciones auxiliares de fingerprints. El instalador y el deduplicador no se ejecutaron. Los riesgos de concurrencia y BAT se derivan de lectura, no de pruebas de integración. No se certifican velocidad, capacidad del plan, fiabilidad del proveedor ni estado actual del DOM remoto.

## Inventario de archivos y símbolos

El Índice siguiente se deriva del AST del código revisado para localizar cada clase, método y función. Las filas de clases cubren el cuerpo completo; sus métodos se detallan aparte. Los hashes identifican el contenido fuente de esta distribución (credenciales vacías); las líneas corresponden al código auditado. Los hashes identifican el contenido fuente; no se incluyen valores de secretos. Las líneas deben actualizarse si cambia el código. Para explicación de responsabilidades y contratos consulte [Arquitectura](ARQUITECTURA.md), para parámetros [Configuración](CONFIGURACION.md), y para defectos [Gaps](GAPS_Y_MEJORAS.md).

### config.py

56 líneas. SHA-256: `bcccccfacf0bc3b50333c2f7632b8ccee4bc9dd7f4eb091a3860239118d830c5`.

Archivo de configuración o script a nivel de módulo; sin clases ni funciones.

### download_geoip.py

11 líneas. SHA-256: `b8681e66b2a225d168dabe3d777eb06a4939023abb0b9b79d071199b6363b9c9`.

| Símbolo | Tipo | Líneas |
|---|---|---|
| `download` | async | [5–8](../download_geoip.py#L5) |

### osiptel_core.py

780 líneas. SHA-256: `c840e047345c4151c6e285f7cf54deaf90871fa8f5f43d3beae1e0235e5c65ce`.

| Símbolo | Tipo | Líneas |
|---|---|---|
| `TaskStatus` | clase | [55–61](../osiptel_core.py#L55) |
| `ErrorType` | clase | [64–73](../osiptel_core.py#L64) |
| `ProxyConfig` | clase | [81–96](../osiptel_core.py#L81) |
| `ProxyConfig.get_effective_port` | función | [92–93](../osiptel_core.py#L92) |
| `ProxyConfig.is_configured` | función | [95–96](../osiptel_core.py#L95) |
| `ScraperConfig` | clase | [100–178](../osiptel_core.py#L100) |
| `ScraperConfig.calculate_max_rucs` | función | [172–175](../osiptel_core.py#L172) |
| `ScraperConfig.get_output_path` | función | [177–178](../osiptel_core.py#L177) |
| `ColoredFormatter` | clase | [185–201](../osiptel_core.py#L185) |
| `ColoredFormatter.format` | función | [197–201](../osiptel_core.py#L197) |
| `setup_logging` | función | [204–237](../osiptel_core.py#L204) |
| `PhoneLine` | clase | [245–252](../osiptel_core.py#L245) |
| `PhoneLine.to_dict` | función | [251–252](../osiptel_core.py#L251) |
| `RUCResult` | clase | [256–285](../osiptel_core.py#L256) |
| `RUCResult.success` | función | [268–269](../osiptel_core.py#L268) |
| `RUCResult.line_count` | función | [272–273](../osiptel_core.py#L272) |
| `RUCResult.to_dict` | función | [275–285](../osiptel_core.py#L275) |
| `Statistics` | clase | [293–399](../osiptel_core.py#L293) |
| `Statistics.update` | función | [310–324](../osiptel_core.py#L310) |
| `Statistics.success_rate` | función | [327–330](../osiptel_core.py#L327) |
| `Statistics.bandwidth_mb` | función | [333–334](../osiptel_core.py#L333) |
| `Statistics.elapsed_seconds` | función | [337–341](../osiptel_core.py#L337) |
| `Statistics.rate_per_hour` | función | [344–348](../osiptel_core.py#L344) |
| `Statistics.eta_seconds` | función | [351–356](../osiptel_core.py#L351) |
| `Statistics.to_dict` | función | [358–374](../osiptel_core.py#L358) |
| `Statistics.print_summary` | función | [376–399](../osiptel_core.py#L376) |
| `ProgressManager` | clase | [406–495](../osiptel_core.py#L406) |
| `ProgressManager.__init__` | función | [409–417](../osiptel_core.py#L409) |
| `ProgressManager.load` | async | [419–452](../osiptel_core.py#L419) |
| `ProgressManager.save` | async | [454–470](../osiptel_core.py#L454) |
| `ProgressManager.add_result` | función | [472–482](../osiptel_core.py#L472) |
| `ProgressManager.get_pending_rucs` | función | [484–486](../osiptel_core.py#L484) |
| `ProgressManager.is_bandwidth_exceeded` | función | [488–491](../osiptel_core.py#L488) |
| `ProgressManager.get_remaining_bandwidth_mb` | función | [493–495](../osiptel_core.py#L493) |
| `ResultsWriter` | clase | [502–719](../osiptel_core.py#L502) |
| `ResultsWriter.__init__` | función | [505–522](../osiptel_core.py#L505) |
| `ResultsWriter.initialize` | async | [524–538](../osiptel_core.py#L524) |
| `ResultsWriter._generate_header` | función | [540–549](../osiptel_core.py#L540) |
| `ResultsWriter.write_result` | async | [551–590](../osiptel_core.py#L551) |
| `ResultsWriter._save_batch` | async | [592–660](../osiptel_core.py#L592) |
| `ResultsWriter._save_timing_report` | async | [662–688](../osiptel_core.py#L662) |
| `ResultsWriter.finalize` | async | [690–701](../osiptel_core.py#L690) |
| `ResultsWriter._escape_csv` | función | [703–707](../osiptel_core.py#L703) |
| `ResultsWriter.write_failed_rucs` | async | [709–719](../osiptel_core.py#L709) |
| `read_rucs_from_file` | función | [726–753](../osiptel_core.py#L726) |
| `validate_ruc_count` | función | [756–780](../osiptel_core.py#L756) |

### osiptel_main.py

454 líneas. SHA-256: `5c5734541b6d64420de562edc342eb5a09c19376895144b43abae06a841882f2`.

| Símbolo | Tipo | Líneas |
|---|---|---|
| `ScraperOrchestrator` | clase | [28–329](../osiptel_main.py#L28) |
| `ScraperOrchestrator.__init__` | función | [40–60](../osiptel_main.py#L40) |
| `ScraperOrchestrator._delayed_worker_start` | async | [62–71](../osiptel_main.py#L62) |
| `ScraperOrchestrator._setup_signal_handlers` | función | [73–81](../osiptel_main.py#L73) |
| `ScraperOrchestrator._setup_signal_handlers.signal_handler` | función | [75–78](../osiptel_main.py#L75) |
| `ScraperOrchestrator._result_callback` | async | [83–85](../osiptel_main.py#L83) |
| `ScraperOrchestrator._process_results` | async | [87–140](../osiptel_main.py#L87) |
| `ScraperOrchestrator.run` | async | [142–329](../osiptel_main.py#L142) |
| `main` | async | [336–450](../osiptel_main.py#L336) |

### osiptel_worker.py

646 líneas. SHA-256: `d9921d8d1aa63aa7715077a10e62c5cc5c012fd9e225f054bcc5b0d1455605e6`.

| Símbolo | Tipo | Líneas |
|---|---|---|
| `ProxyManager` | clase | [28–77](../osiptel_worker.py#L28) |
| `ProxyManager.__init__` | función | [38–42](../osiptel_worker.py#L38) |
| `ProxyManager.get_session_id` | async | [44–50](../osiptel_worker.py#L44) |
| `ProxyManager.get_proxy_config_for_camoufox` | función | [52–71](../osiptel_worker.py#L52) |
| `ProxyManager.get_proxy_url` | función | [73–77](../osiptel_worker.py#L73) |
| `BrowserManager` | clase | [84–179](../osiptel_worker.py#L84) |
| `BrowserManager.__init__` | función | [89–104](../osiptel_worker.py#L89) |
| `BrowserManager._create_browser` | async | [106–134](../osiptel_worker.py#L106) |
| `BrowserManager._cleanup` | async | [136–145](../osiptel_worker.py#L136) |
| `BrowserManager.get_browser` | async | [147–161](../osiptel_worker.py#L147) |
| `BrowserManager.new_page` | async | [163–168](../osiptel_worker.py#L163) |
| `BrowserManager.rotate_ip` | async | [170–174](../osiptel_worker.py#L170) |
| `BrowserManager.close` | async | [176–179](../osiptel_worker.py#L176) |
| `OSIPTELPageScraper` | clase | [186–484](../osiptel_worker.py#L186) |
| `OSIPTELPageScraper.__init__` | función | [194–196](../osiptel_worker.py#L194) |
| `OSIPTELPageScraper.scrape_ruc` | async | [198–342](../osiptel_worker.py#L198) |
| `OSIPTELPageScraper._wait_for_table_complete` | async | [344–391](../osiptel_worker.py#L344) |
| `OSIPTELPageScraper._set_page_size` | async | [393–418](../osiptel_worker.py#L393) |
| `OSIPTELPageScraper._extract_table_data` | async | [420–465](../osiptel_worker.py#L420) |
| `OSIPTELPageScraper._classify_error` | función | [467–484](../osiptel_worker.py#L467) |
| `Worker` | clase | [491–646](../osiptel_worker.py#L491) |
| `Worker.__init__` | función | [497–516](../osiptel_worker.py#L497) |
| `Worker.stop` | async | [518–520](../osiptel_worker.py#L518) |
| `Worker.run` | async | [522–567](../osiptel_worker.py#L522) |
| `Worker._process_ruc_with_retries` | async | [569–646](../osiptel_worker.py#L569) |

### remove_duplicates.py

46 líneas. SHA-256: `7b2c73f88dcefbd016552b21cfb76b9f137dece3063844b2dfe90a4307aab540`.

Archivo de configuración o script a nivel de módulo; sin clases ni funciones.

### run_auto.py

377 líneas. SHA-256: `cc9cfcf9d77fa1f883cbd13beae8d85a52941d0ed2f10388077ba12c677e824b`.

| Símbolo | Tipo | Líneas |
|---|---|---|
| `create_optimized_config` | función | [54–80](../run_auto.py#L54) |
| `AutoScraper` | clase | [83–274](../run_auto.py#L83) |
| `AutoScraper.__init__` | función | [88–121](../run_auto.py#L88) |
| `AutoScraper._signal_handler` | función | [123–126](../run_auto.py#L123) |
| `AutoScraper.initialize` | async | [128–180](../run_auto.py#L128) |
| `AutoScraper.run` | async | [182–229](../run_auto.py#L182) |
| `AutoScraper.finalize` | async | [231–274](../run_auto.py#L231) |
| `main` | async | [277–371](../run_auto.py#L277) |

### system_optimizer.py

594 líneas. SHA-256: `941c9aa31520350c94e41fc3248fcec047150358c6c20b465f69c424ac9b168a`.

| Símbolo | Tipo | Líneas |
|---|---|---|
| `SystemResources` | clase | [34–53](../system_optimizer.py#L34) |
| `BandwidthTracker` | clase | [57–91](../system_optimizer.py#L57) |
| `BandwidthTracker.get_used_mb` | función | [76–77](../system_optimizer.py#L76) |
| `BandwidthTracker.get_used_percent` | función | [79–80](../system_optimizer.py#L79) |
| `BandwidthTracker.get_remaining_mb` | función | [82–83](../system_optimizer.py#L82) |
| `BandwidthTracker.is_near_limit` | función | [85–86](../system_optimizer.py#L85) |
| `BandwidthTracker.update` | función | [88–91](../system_optimizer.py#L88) |
| `PerformanceReport` | clase | [95–233](../system_optimizer.py#L95) |
| `PerformanceReport.calculate_metrics` | función | [130–148](../system_optimizer.py#L130) |
| `PerformanceReport.to_dict` | función | [150–185](../system_optimizer.py#L150) |
| `PerformanceReport.print_report` | función | [187–233](../system_optimizer.py#L187) |
| `SystemOptimizer` | clase | [236–443](../system_optimizer.py#L236) |
| `SystemOptimizer.__init__` | función | [241–243](../system_optimizer.py#L241) |
| `SystemOptimizer.detect_system_resources` | función | [245–263](../system_optimizer.py#L245) |
| `SystemOptimizer.test_network_speed` | async | [265–313](../system_optimizer.py#L265) |
| `SystemOptimizer.calculate_optimal_workers` | función | [315–350](../system_optimizer.py#L315) |
| `SystemOptimizer.calculate_optimal_delays` | función | [352–375](../system_optimizer.py#L352) |
| `SystemOptimizer.calculate_pages_per_browser` | función | [377–392](../system_optimizer.py#L377) |
| `SystemOptimizer.optimize` | async | [394–423](../system_optimizer.py#L394) |
| `SystemOptimizer.print_summary` | función | [425–443](../system_optimizer.py#L425) |
| `BandwidthMonitor` | clase | [446–527](../system_optimizer.py#L446) |
| `BandwidthMonitor.__init__` | función | [451–461](../system_optimizer.py#L451) |
| `BandwidthMonitor.update_from_system` | función | [463–472](../system_optimizer.py#L463) |
| `BandwidthMonitor.record_ruc_bandwidth` | función | [474–481](../system_optimizer.py#L474) |
| `BandwidthMonitor.record_proxy_error` | función | [483–485](../system_optimizer.py#L483) |
| `BandwidthMonitor.record_success` | función | [487–489](../system_optimizer.py#L487) |
| `BandwidthMonitor.check_exhaustion` | función | [491–511](../system_optimizer.py#L491) |
| `BandwidthMonitor.estimate_remaining_rucs` | función | [513–516](../system_optimizer.py#L513) |
| `BandwidthMonitor.get_status` | función | [518–527](../system_optimizer.py#L518) |
| `RUCFileManager` | clase | [530–594](../system_optimizer.py#L530) |
| `RUCFileManager.__init__` | función | [535–538](../system_optimizer.py#L535) |
| `RUCFileManager.create_backup` | función | [540–545](../system_optimizer.py#L540) |
| `RUCFileManager.remove_processed_rucs` | función | [547–585](../system_optimizer.py#L547) |
| `RUCFileManager.get_remaining_count` | función | [587–594](../system_optimizer.py#L587) |

## Código auxiliar y archivos fuera del Índice AST

- `config.py`: constantes y credenciales locales; precedencia efectiva explicada en Configuración.
- `remove_duplicates.py`: 46 líneas ejecutadas a nivel de módulo; lee ambos CSV fijos y reescribe el pendiente con solo RUC; no elimina repetidos internos ni tiene protección main/backup.
- `start.bat`: etapas de comprobación/instalación Python (24–124), entorno (127–154), pip/dependencias (156–179), navegador (181–192) y carpeta/instrucciones (194–238).
- `requirements.txt`: seis dependencias por rangos, no versiones exactas.
- `.gitignore`: excluye cachés, venv, salidas, ZIP, backups y CSV de entrada, pero no config.py.
- `rucs/*.csv`: datos operativos; no deben presentarse como fixtures ni demostración de exactitud.
- `osiptel_main.zip`: respaldo con fuentes y resultados históricos, fuera del flujo normal.
- `__pycache__`: artefactos de ejecución; no fuente alternativa mantenida.

## Mantenimiento documental

Cuando cambien fuentes, revisar primero contrato de entrada/salida, configuración efectiva, estados de recuperación y criterios de aceptación de gaps afectados. Actualizar fecha, inventario y evidencia solo después de verificar. Cerrar un gap requiere implementación y validación: editar su descripción no lo resuelve. No documentar flags o funciones propuestas como disponibles.
