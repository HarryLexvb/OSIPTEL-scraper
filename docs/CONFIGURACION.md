# Configuración efectiva

> Publicación en GitHub: esta distribución conserva el código auditado, con usuario y contraseña vacíos en `config.py` y `ProxyConfig`. Las referencias a credenciales embebidas describen la copia local auditada; la externalización sigue pendiente. Se conserva el archivo MIT `LICENSE` ya existente en el repositorio de destino. No se publican CSV operativos, resultados, ZIP ni cachés.

Revisado: 16/11/2026. [Índice](../README.md). Las cifras siguientes describen el código, no recomendaciones de capacidad ni garantías de ahorro.

## Fuentes de configuración

`run_auto.py` importa credenciales, host/puerto y BLOCK_IMAGES de config.py. Aunque importa MAX_BANDWIDTH_MB y OUTPUT_DIRECTORY, usa defaults propios de argumentos/constructor. No importa MAX_WORKERS, MIN_DELAY, MAX_DELAY, MAX_RETRIES o USE_PERU_IPS. Crea ScraperConfig, lo modifica con recursos y argumentos, y fuerza tres intentos totales.

`osiptel_main.py` ejecutado directamente instancia ScraperConfig con defaults embebidos y no lee config.py. Su menú deja elegir entre 1 y 20 workers; los cambios de credenciales del menú son temporales y no se guardan al archivo. El menú se procesa una sola vez.

| Parámetro | config.py | Flujo run_auto.py |
|---|---|---|
| Credenciales / host / puerto | Valores locales; no se reproducen secretos | Se copian a ProxyConfig |
| USE_PERU_IPS | False | No se importa; el código usa el username tal como está y agrega _session-ID |
| MAX_WORKERS | 12 | Ignorado; detección o entrada manual 1–50 |
| MIN_DELAY / MAX_DELAY | 1 / 2 s | Ignorados; detección inicial |
| MAX_RETRIES | 2 | Ignorado; fuerza 3 intentos totales, aunque consola muestra 2 |
| MAX_BANDWIDTH_MB | 999999999 | Ignorado como default; CLI usa 10000; no hay corte |
| BLOCK_IMAGES | True | Usado; el ahorro porcentual de comentarios no está medido |
| OUTPUT_DIRECTORY | osiptel_output | Default CLI independiente del mismo nombre; --output lo cambia |

El sufijo de sesión se construye como `<username>_session-<id>`. No se comprobó autenticación, geolocalización ni compatibilidad actual con el proveedor. `use_peru_ips`, peru_port y get_effective_port no implementan una selección geográfica activa en este flujo.

## Heurísticas de recursos

SystemOptimizer toma núcleos físicos (fallback 4), hilos (fallback 8), CPU y RAM de psutil. Las consultas de red son directas a Google, Cloudflare e ipify, con timeout de cinco segundos por URL. Usa la menor latencia y supone 300 ms si no obtiene mediciones. No mide el proxy ni el caudal real: los Mbps son categorías inferidas.

Workers calculados: entero de min(núcleos × 2.5, RAM disponible MB / 350, factor red), acotado entre 4 y 24. Factores de red: 20 con latencia <100 ms, 16 con <200, 12 con <400 y 8 para el resto. El mínimo de cuatro puede exceder recursos en equipos limitados. El modo manual reemplaza solo el número de workers.

| Latencia usada | Delay mínimo–máximo entre RUCs |
|---|---|
| <100 ms | 0.5–1 s |
| <200 ms | 0.8–1.5 s |
| <400 ms | 1–2 s |
| Resto | 1.5–3 s |

El optimizador calcula 50/100/150/200 páginas por navegador según RAM, pero ese resultado no llega a BrowserManager: el límite efectivo es 150. No hay adaptación continua por carga, errores o rendimiento.

## Valores efectivos internos

| Área | Valor y consecuencia |
|---|---|
| Navegador | headless=True, humanize=True, block_images según config.py, geoip=False |
| Navegación | 120000 ms y networkidle fijados en worker; ignora page_timeout=45000 |
| Selector inicial | 30000 ms fijados; ignora selector_timeout=20000 |
| Búsqueda | Espera inicial 10000 ms; estabilidad hasta 30 controles cada 2000 ms y 3000 ms finales |
| Relecturas vacías | Hasta cuatro de 5000 ms si hay filas visibles; intento final de 8000 ms en condición sospechosa |
| Reintento de RUC | 3 intentos totales; base 5 s, multiplicador 2, límite nominal 30 s, después jitter de hasta 30%; rotación para reintentar |
| Checkpoint | Cada 25 resultados consumidos; guardado final adicional |
| Lote | 1000 éxitos; subcarpeta save; tamaño no expuesto por CLI |
| Exportación | 100 líneas por RUC, 301 columnas; trunca excedentes |
| Tráfico | 550 KB añadidos por resultado; no por intento; sin medición real ni corte |
| Consumidor | Espera resultados hasta 60 s con condición de salida defectuosa; cierre hasta 10 s |

En ScraperConfig siguen declarados navigation_timeout, delay_after_error, warn_bandwidth_percent, max_rucs_for_10gb y track_bandwidth sin un control efectivo equivalente en el flujo. calculate_max_rucs y validate_ruc_count calculan límites nominales; el último no se invoca en la ejecución normal. BandwidthMonitor y BandwidthTracker son auxiliares desconectados del scraping; conectarlos sin cambios mediría tráfico global del equipo, no solo del proxy.

## Secretos y cambios futuros

Existen credenciales embebidas tanto en config.py como en ProxyConfig y ambos están versionados. No hay soporte .env implementado. La mejora pendiente es una sola fuente validada al inicio, secretos externos y configuración efectiva registrada sin secretos. No copie credenciales a ejemplos, issues o logs. Si se compartieron fuentes o historial, la retirada de valores actuales por sí sola no retira los secretos históricos.
