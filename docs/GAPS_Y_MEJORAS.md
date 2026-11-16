# Gaps y mejoras futuras

> Publicación en GitHub: esta distribución conserva el código auditado, con usuario y contraseña vacíos en `config.py` y `ProxyConfig`. Las referencias a credenciales embebidas describen la copia local auditada; la externalización sigue pendiente. Se conserva el archivo MIT `LICENSE` ya existente en el repositorio de destino. No se publican CSV operativos, resultados, ZIP ni cachés.

Revisado el 16/11/2026. [Índice](../README.md). **Todos los hallazgos siguientes siguen abiertos**: esta actualización modifica documentación, no corrige el motor. Las referencias señalan el código fuente revisado.

## Prioridades

P0: integridad, recuperación y resultados fiables. P1: controles operativos, configuración y validación. P2: mantenibilidad y eficiencia. Son prioridades técnicas propuestas, sin compromiso de fecha ni estimación de esfuerzo.

## G01 · P0 · éxitos vacíos sin evidencia

Evidencia: [osiptel_worker.py:198](../osiptel_worker.py#L198).

**Gap:** Puede persistir ausencia de datos como éxito y retirarla de pendientes.

**Mejora pendiente:** Distinguir consulta válida sin líneas, carga incompleta, bloqueo y error; exigir señal explícita del sitio.

**Aceptación:** Página sin tabla, carga tardía y bloqueo nunca terminan como éxito vacío; cero válido tiene evidencia verificable.

## G02 · P0 · Extracción y exportación incompletas

Evidencia: [osiptel_worker.py:393](../osiptel_worker.py#L393).

**Gap:** Sin recorrido de paginación; escritor limita a cien líneas.

**Mejora pendiente:** Recorrer páginas hasta total y exportar sin pérdida, preferiblemente una fila por línea con identidad de consulta.

**Aceptación:** Casos 0, 1, 100 y más de 100 líneas concilian el total y todos los registros persisten.

## G03 · P0 · Sobrescritura al reanudar lotes

Evidencia: [osiptel_core.py:505](../osiptel_core.py#L505).

**Gap:** Índice y tiempos reinician; modo w reemplaza parciales existentes.

**Mejora pendiente:** Recuperar manifiesto de lotes o usar nombres únicos por ejecución; escrituras atómicas.

**Aceptación:** Interrumpir/reanudar varias veces conserva hashes de lotes cerrados y un historial acumulativo coherente.

## G04 · P0 · Fallo y éxito comparten procesados

Evidencia: [osiptel_core.py:472](../osiptel_core.py#L472).

**Gap:** Fallidos no vuelven a pendientes y run_auto los borra de entrada.

**Mejora pendiente:** Separar estados y hacer limpieza de entrada opcional, solo tras persistencia confirmada.

**Aceptación:** Fallo agotado sigue recuperable; entrada se conserva por defecto; ningún fallo se elimina como éxito.

## G05 · P0 · Consumidor y cierre incompletos

Evidencia: [osiptel_main.py:87](../osiptel_main.py#L87).

**Gap:** Un worker terminado permite salida del consumidor tras timeout aunque queden activos; cierre cancela tras diez segundos.

**Mejora pendiente:** Protocolo de fin explícito, drenado y propagación de errores; supervisar productor/consumidor juntos.

**Aceptación:** Un worker lento junto a uno terminado no pierde resultados; backlog y fallo de disco no producen completed engañoso.

## G06 · P0 · Persistencia sin transacción ni idempotencia

Evidencia: [osiptel_main.py:110](../osiptel_main.py#L110).

**Gap:** Marca procesado antes del CSV; caída entre archivos permite pérdida o duplicados.

**Mejora pendiente:** Resultado y estado durables por identidad, transacción o journal reconciliable y exportación derivada.

**Aceptación:** Inyectar caída en cada frontera de escritura y reanudar sin perder ni duplicar resultados.

## G07 · P1 · Presupuesto nominal sin corte

Evidencia: [osiptel_core.py:488](../osiptel_core.py#L488).

**Gap:** --bandwidth no limita; monitor desconectado; 550 KB por resultado ignora tráfico real.

**Mejora pendiente:** Definir estimación frente a medición y modo ilimitado explícito; integrar corte configurable.

**Aceptación:** Con presupuesto pequeño se detienen nuevas consultas y se guardan pendientes; reporte distingue medido/estimado.

## G08 · P1 · Credenciales en código e historial

Evidencia: [config.py:18](../config.py#L18).

**Gap:** Secretos también embebidos en ProxyConfig versionado.

**Mejora pendiente:** Externalizar credenciales y validar al inicio; revisar exposición histórica y rotar cuando corresponda.

**Aceptación:** Clonado sin secretos falla con mensaje claro; logs y documentación no revelan credenciales.

## G09 · P1 · Config dispersa y flags ausentes

Evidencia: [run_auto.py:54](../run_auto.py#L54).

**Gap:** Constantes ignoradas, tres intentos efectivos y dos impresos; menú impide automatización.

**Mejora pendiente:** Fuente única y config efectiva; flags de workers, modo no interactivo, resume y limpieza.

**Aceptación:** Cada ajuste cambia conducta comprobable; --help no pide entrada ni hace red.

## G10 · P1 · Entradas y columnas inconsistentes

Evidencia: [run_auto.py:160](../run_auto.py#L160).

**Gap:** Preconteo, lector y limpieza usan reglas diferentes; Excel falla en automático; duplicados se encolan.

**Mejora pendiente:** Lector común con esquema explícito, validación y deduplicación; soporte Excel declarado según motores.

**Aceptación:** Columnas reordenadas, repetidos, CSV sin cabecera y Excel producen resultado o error explícito coherente.

## G11 · P1 · Estado compartido sin identidad

Evidencia: [osiptel_main.py:179](../osiptel_main.py#L179).

**Gap:** Output fijo mezcla trabajos; no hay bloqueo entre procesos; resume=False no borra CSV existente.

**Mejora pendiente:** Identidad de dataset/corrida, directorios propios, bloqueo y políticas explícitas de anexado.

**Aceptación:** Dos entradas y dos procesos no mezclan progreso ni corrompen temporales.

## G12 · P1 · Reportes y señales ambiguos

Evidencia: [run_auto.py:182](../run_auto.py#L182).

**Gap:** completed tras interrupción; estadísticas restauradas frente a total reducido; errores/reintentos no copiados al reporte.

**Mejora pendiente:** Estado de salida común, métricas de sesión separadas de acumuladas y cierre ante fallo de inicialización.

**Aceptación:** Ctrl+C y errores reportan su causa real; remaining no es negativo y reportes concilian con registros persistidos.

## G13 · P2 · Optimizador heurístico desconectado en parte

Evidencia: [system_optimizer.py:265](../system_optimizer.py#L265).

**Gap:** Mide endpoints directos; Mbps inferidos; páginas calculadas no se aplican; mínimo cuatro workers.

**Mejora pendiente:** Medir ruta relevante y memoria efectiva; aplicar parámetros y permitir uno o menos workers según recursos.

**Aceptación:** Telemetría identifica ruta medida, no llama latencia del proxy a conexión directa, y respeta memoria disponible.

## G14 · P2 · Esperas y clasificación frágiles

Evidencia: [osiptel_worker.py:209](../osiptel_worker.py#L209).

**Gap:** Timeouts hardcodeados, estabilidad cero aceptada, silencios en selector de tamaño y clasificación por texto.

**Mejora pendiente:** Esperar estados observables con timeouts configurables y clasificar errores con contexto.

**Aceptación:** Configuración cambia tiempos; cargas incompletas y errores de selector generan diagnósticos y reintentos adecuados.

## G15 · P2 · Instalador y auxiliares sin contrato

Evidencia: [start.bat:24](../start.bat#L24).

**Gap:** CWD relativo, refresco PATH defectuoso y éxito tras fetch fallido; GeoIP incompatible localmente y deduplicador destructivo ad hoc.

**Mejora pendiente:** Instalador reproducible con comprobaciones y auxiliares con argumentos, main guard, backup y dry-run.

**Aceptación:** Instalación desde otra carpeta y fallos de descarga producen estado correcto; importar auxiliar no modifica archivos.

## G16 · P2 · Higiene de mantenimiento

Evidencia: [osiptel_core.py:185](../osiptel_core.py#L185).

**Gap:** Imports/campos sin uso, formatter muta LogRecord, handlers se limpian sin cierre explícito; excepciones amplias.

**Mejora pendiente:** Eliminar código muerto tras verificar referencias y centralizar logging/errores con recursos cerrados.

**Aceptación:** Reinicialización no fuga handlers; ambos destinos reciben nivel legible; fallos no quedan ocultos.

## G17 · P1 · Sin pruebas de recuperación ni entorno fijado

Evidencia: [requirements.txt:8](../requirements.txt#L8).

**Gap:** Rangos no fijan entorno exacto; no hay tests/CI ni cobertura de corrupción y reinicio.

**Mejora pendiente:** Suite local con fixtures de DOM y fallos de I/O, lockfile y CI antes de depender de corridas grandes.

**Aceptación:** Pruebas de G01–G06 pasan sin red y una instalación limpia usa versiones reproducibles.

## G18 · P2 · Versionado, licencia y documentación

Evidencia: [README.md:1](../README.md#L1).

**Gap:** Etiquetas de versión incompatibles y necesidad de unificar la referencia a LICENSE; README histórico del ZIP contradice código actual.

**Mejora pendiente:** Definir versión/release y confirmar licencia; mantener documentación ligada a cambios de comportamiento.

**Aceptación:** Release identificable, licencia confirmada y documentación validada contra código sin promesas de capacidad no medidas.

## Secuencia propuesta

1. Crear pruebas de reproducción de G01–G06 y definir estados/contrato de persistencia.
2. Corregir validación de extracción, paginación y exportación completa; implementar recuperación idempotente y drenado de colas.
3. Separar fallidos/éxitos, identidades de corrida y política de limpieza de entrada.
4. Unificar configuración, secretos, presupuesto y estados de salida; añadir CLI no interactiva.
5. Validar compatibilidad en una corrida pequeña controlada con conciliación de resultados; medir rendimiento antes de ajustar concurrencia.
6. Endurecer instalación, retirar auxiliares obsoletos tras sustituirlos, fijar dependencias y definir releases/licencia.

No se propone una reescritura completa como requisito inicial. Una base transaccional local y una exportación normalizada son opciones de diseño a evaluar, no componentes existentes. Una API, dashboard, scheduler o despliegue remoto solo se justifican después de resolver integridad y según necesidades concretas.

## Información obsoleta retirada de la guía principal

Se retiraron garantías implícitas de operación productiva, soporte Excel general del lanzador y reanudación segura sin condiciones. No se conservan cifras de RUC/hora, consumo real o ahorro porcentual como hechos medidos. Las etiquetas históricas no se usan para presentar una versión oficial. Las cabeceras y comentarios de las fuentes mantienen esas afirmaciones antiguas porque esta tarea solo autoriza cambios documentales; la documentación vigente describe la ejecución real y registra las discrepancias.
