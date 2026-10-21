# Auditoría del Validador de pagos a contratistas (SENA) — v1.3.0

Fecha de las pruebas: 14/10/2026. Alcance: `index.html` + `libs/` (la aplicación), los scripts de `pruebas/` y `regresion/`, y los informes `HALLAZGOS_CORPUS.md/.csv` (julio + septiembre), `HALLAZGOS_JUNIO.md/.csv` y `HALLAZGOS_OCTUBRE.md/.csv`.
Este documento dice **qué se ejecutó de verdad, con qué resultado y qué no se probó o no se puede garantizar**.

## 0. Qué cambió en la v1.3.0 (formato nuevo de la planilla SI contratistas, octubre de 2026)

Con los 2 PDF de octubre (16797358, 33 págs.; 1130637605, 2 págs.) se comparó el diseño nuevo de la planilla contra el anterior (segmentos de texto de la página 1 de ambos, más la imagen) y se ajustó la lectura **conservando el formato anterior** (la regresión sobre los 6 PDF previos sigue **IGUAL**).

| Qué cambió en el formato | Efecto antes del ajuste | Ajuste en la v1.3.0 |
|---|---|---|
| El N.º de planilla PILA del mes anterior queda **pegado al rótulo vecino** en un solo trozo de texto («95603627 Base retencion en la fuente a titulo de RENTA») | No se leía el número: «Falta: N.º planilla PILA», V2 y V6 en NO VERIFICABLE/ERROR | Se acepta una casilla que **empieza** con un número de 4 o más cifras seguido de texto, se toma solo ese primer número y se ubica la columna con la parte numérica. Una casilla que empieza con letras («Decreto 1273 de…») **no** se interpreta como número; su texto se conserva sin el rótulo pegado |
| Fondo de solidaridad pensional ahora es «$ -» (cero contable) en una sola casilla | `fsp` = «No encontrado» → V3 NO VERIFICABLE | «$ -», «$-» y «-» se leen como 0, igual que antes |
| Rótulo del ordenador: «ORDENADOR DEL GASTO» (antes «EL ORDENADOR DEL PAGO») | Nombre y cargo del ordenador de la planilla no se leían; firma del ordenador en «REQUIERE REVISIÓN» | Se aceptan ambos rótulos; el bloque no tiene espacio de firma, así que queda «SIN FIRMA» y no obligatoria, como en el formato anterior |
| Hoja A4 (antes tamaño personalizado), «Versión ENERO - 1», título con texto duplicado | Sin efecto: la lectura va por etiquetas y columnas, no por coordenadas fijas | — |

Otros dos defectos que aparecieron al revisar los mismos PDF (no son del formato de la planilla, pero afectaban estos paquetes):

| Defecto | Efecto | Ajuste |
|---|---|---|
| Comprobante con las celdas de una fila desfasadas hasta ~4 pt (hoja ligeramente inclinada): el valor del último tramo no se tomaba (quedaba el «$») | C7 «suma de tramos = total» en NO VERIFICABLE | Tolerancia de fila de 3,2 a 5,2 pt (las filas distan más de 13 pt) |
| «Ciudad / municipio – Fecha» con varios días («Yumbo - septiembre 23 y 24 2026») | C8 decía «El campo está vacío…» y mostraba «No encontrado» | El valor sigue sin interpretarse (no se adivina un día), pero el aviso **cita el texto** y pide confirmar la fecha en el PDF |

Resultado: 16797358 **VÁLIDO CON ADVERTENCIAS** (3 advertencias de C8/C9, ver §3) y 1130637605 **VÁLIDO**; V1–V7 en OK en los dos. Pruebas añadidas: autopruebas X12 (diseño nuevo, con mutación comprobada: las tres correcciones hacen fallar X12 si se revierten) y X13; `e2e6.py` (23 comprobaciones, con los nombres de archivo reales y un PDF mixto formato nuevo + anterior).

**Límite:** el formato nuevo se vio en **2 paquetes** (1 con comisiones, 1 sin comisiones). No hay muestra de un primer pago, de una planilla de varias páginas ni de un mes distinto en el formato nuevo.

## 0a. Qué cambió en la v1.2.1 (nuevo dato: «ID de Proceso»)

Se **anexó** un dato nuevo de la planilla SI contratistas, sin cambiar lecturas, validaciones ni estados existentes:

| Qué | Detalle |
|---|---|
| Lectura | Campo `idProceso` de la planilla SI: etiqueta «ID de Proceso» del encabezado (junto a «Versión»), leído como **texto exacto** (guion y ceros a la izquierda se conservan: `02547-055485`). Si no hay etiqueta o valor, queda «No encontrado»; no se inventa. Código: una línea en `extractPlanilla` |
| Dónde se ve | Listado (bajo la cédula de cada contratista; también se puede buscar por el ID), pestañas **Resumen** y **Planilla SI** (con la página de origen y el lápiz para corregirlo, como los demás campos) e informe imprimible |
| Exportación | CSV de resumen: columna nueva **«ID de Proceso» al final**, para que ninguna columna existente cambie de posición. El respaldo JSON lo incluye porque guarda la planilla completa |
| Validaciones | **Ninguna nueva y ninguna modificada**: el ID no se compara ni es requisito (la prueba X11 verifica que las validaciones de un paquete son idénticas con y sin el campo) |
| Verificación | 32 de 32 planillas del corpus leen el ID y coinciden uno a uno con el texto del PDF (`pdftotext`); la regresión sobre los 6 PDF muestra **una única diferencia por paquete: el campo nuevo** (32 diferencias en total, ninguna otra). Referencia actualizada tras esa revisión |
| Registros ya guardados | Los guardados con una versión anterior **no tienen** el dato: el listado muestra «—» y el Resumen dice «Sin leer… pulse Reprocesar». Al reprocesar se lee del PDF guardado (**reprocesar descarta las ediciones y confirmaciones manuales de ese registro**, como ya advertía el diálogo) o se vuelve a cargar el PDF |
| Diseño | Se probó primero como columna del listado, pero ensanchaba la tabla y empujaba el botón «Eliminar» fuera de la pantalla a 1400 px; por eso se muestra bajo la cédula |

Pruebas añadidas: autoprueba X11; `e2e4.py` M12b, M13b, M13c, M15b, M15c; `e2e5.py` J14b, J14c, J15b. Se comprobó por mutación que X11 falla si se quita la lectura.

## 0b. Qué cambió en la v1.2 (prueba con el PDF combinado de junio) y por qué

El PDF de junio (83 págs., 13 contratistas) se procesó **sin ajustes previos** y mostró cinco huecos de generalización que julio y septiembre no habían mostrado. Todos se corrigieron y se comprobó con la regresión que las lecturas de los otros 5 PDF **no cambiaron** (solo se añadió un campo nuevo, `pilaNroTexto`, vacío salvo en un paquete).

| Hueco encontrado en junio | Efecto antes del arreglo | Arreglo en la v1.2 |
|---|---|---|
| Texto girado dentro de una hoja vertical (la hoja no trae atributo de rotación, pero el contenido está girado) | Etiquetas y valores en el orden equivocado; firmas medidas en la zona equivocada | Se detecta la dirección dominante del texto y se usa **la misma vista girada** para el modelo de página, la imagen que se muestra y la medición de firmas (`pagemodel.js`) |
| Texto sobrescrito (el mismo fragmento impreso dos veces con desfase) | Nombres y números duplicados («JOSE JOSE …») | Se descartan los fragmentos contenidos dentro de otro más largo en la misma zona (`quitarSobreescritura`); toda la lectura legítima se conserva (prueba X8) |
| Informe de legalización repartido en varias páginas (datos / firmas / hoja de control de cambios) | Páginas del mismo informe tratadas como informes distintos o como «no reconocidas» | Clasificación por subtipo (`datos`, `firmas`, `control`); la hoja de «Generalidades» que repite el título ya no se toma como informe nuevo (prueba X7) |
| Sexto formato de PILA: «Soporte de pago para el cotizante» (SOI) | Marcado como formato desconocido | Familia `cotizante` con su lector (número, periodo, aportes, totales; prueba X9) |
| Páginas con fuente sin codificación (el texto extraído son símbolos sin sentido) | «Falta el informe / el comprobante» como ERROR, cuando en realidad el documento está en la página pero no se puede leer | Tipo de página `ILEGIBLE`; si faltan documentos y hay páginas ilegibles, la regla pasa a **NO VERIFICABLE** y nombra las páginas |
| Columna del nombre de la PILA `soi1` y aporte a la caja de compensación en un diseño con otra posición | Nombre mal tomado; CCF no leído | Columna relativa al encabezado; ancla del bloque CCF corregida |
| Casilla «N.º planilla PILA» de la planilla SI con texto en lugar de número («Decreto 1273 de…», primer pago) | Solo «Falta: N.º planilla PILA» | Se conserva el texto de la casilla (`pilaNroTexto`) y el aviso lo cita y indica si es el pago n.º 1 (prueba X10) |
| Explicación de C8 contradictoria | Texto fijo que no coincidía con el estado | La explicación depende del estado |

**Lo que sigue sin poder hacer la aplicación (v1.2):** sin OCR no puede leer las 3 páginas de 77094907 con fuente sin codificación (págs. 35–37: informe y comprobante), el número del radicado de esa misma comisión (pág. 38, visible solo en la imagen) ni la RUT escaneada de 76325057 (págs. 82–83). Los marca como «REQUIERE REVISIÓN MANUAL / NO VERIFICABLE» en lugar de inventar. El único caso que sigue siendo ERROR por esta causa es «Falta: N.º de radicado» de 77094907 (el campo no se lee, aunque el documento existe).

### Cambios de la v1.1 (se mantienen)

La v1.0 se calibró con **un solo PDF**. Con 19 paquetes reales (4 de septiembre + 15 de julio) se comprobó que varias lecturas dependían de ese único formato: coordenadas fijas, un solo diseño de PILA, estructura fija del informe de legalización, firmas pegadas como anotación (sello) invisibles para el método A, y una firma de «ordenador» exigida en la planilla SI aunque el formato no tiene espacio para ella. Por eso la v1.0 «dejaba de reconocer mucha información». Cambios de la v1.1:

| Área | Cambio |
|---|---|
| PILA | 5 formatos reconocidos (+ «desconocida», que **avisa** en vez de adivinar): planilla integrada 2 págs. (`soi1`), soporte de pago general (`soporte`), autoliquidación consolidada PagoSimple/SuAporte (`consolidada`), planilla individual (`individual`) y resumen general de pago (`resumen`). Código en `src/pila.js` |
| Comparación PILA ↔ planilla SI | Se compara el **aporte obligatorio** (sin mora). El «valor pagado» (con mora/redondeo) solo se informa (INFO). IBC con tolerancia de $1 (ADVERTENCIA, configurable). Fondo de solidaridad: en los formatos que no lo discriminan (`consolidada`, `resumen`) queda ADVERTENCIA explicada, no «no verificable» |
| Informe, SIIF, comprobante | Lectura por columnas y etiquetas (no por posición fija); orden de viaje en varias disposiciones; fechas en formatos «1 julio 2026», «20 de mayo del 2026», «30 de jun. de 26», «mayo 2026» |
| Nombres | Tolerancia a nombres truncados/repetidos en la planilla («MONTE» por «MONTENEGRO»): ADVERTENCIA, no ERROR |
| Firmas | Se incluyen firmas pegadas como anotación (Stamp); ROI ampliados; umbral propio cuando hay imagen; la firma del **ordenador en la planilla SI ya no es obligatoria por defecto** (configurable) |
| Validaciones | C6 (fechas del informe dentro del rango SIIF), C8 (fecha del comprobante), C9 (contrato) afinadas; avisos de lectura de la PILA pasan a V6 |
| Interfaz | La pestaña PILA muestra el formato reconocido (o la advertencia de formato desconocido) |
| Pruebas | Corpus de 19 paquetes; regresión «golden master»; nueva suite `e2e4.py` |

## 1. Entorno de las pruebas

| Elemento | Detalle |
|---|---|
| Navegador | Chromium 141 (headless) en Linux, controlado con Playwright |
| Formas de apertura probadas | `file://` (doble clic) y `http://127.0.0.1` (equivalente a `iniciar.bat`) |
| Lector de PDF | pdf.js 3.11.174 |
| Corpus real | **8 PDF → 34 paquetes**: 4 de septiembre (`1_GF_66825336_5726`, `4_GF_31710078_5426`, `8_GF_16797358_5126`, `11_GF_15646465_4826`; 3, 2, 29 y 9 págs.), el combinado de julio (124 págs., 15 contratistas, 12 comisiones), el combinado de junio (83 págs., 13 contratistas, 9 comisiones) y **2 de octubre en el formato nuevo de la planilla SI** (`8_GF_16797358_5126_OCT`, 33 págs., 2 comisiones; `2_GF_1130637605_5526_OCT`, 2 págs.) |
| Formatos PILA presentes en el corpus | soi1: 13 · consolidada: 8 · soporte: 7 · resumen: **2** · individual: **2** · cotizante: **1** (el menos respaldado) · sin PILA en el paquete: 1 (76325057, primer pago) |
| Seguridad | CSP que bloquea conexiones externas; todas las pruebas se hicieron con la CSP activa |

## 2. Resumen de lo ejecutado

| Suite | Cómo se ejecuta | Resultado (build final 1.2.0) |
|---|---|---|
| Autopruebas internas (37) | Botón **Ejecutar pruebas** (código real, datos sintéticos, IndexedDB temporal) | 37 PASS / 0 FAIL |
| Recorrido completo con un PDF real y derivados (48) | `pruebas/e2e2.py` | 48 PASS / 0 FAIL |
| Casos negativos y de lote (20) | `pruebas/e2e3.py` (PDF alterados) | 20 PASS / 0 FAIL |
| Mismo flujo por `http://` (37 autopruebas + registro) | `pruebas/e2e_http.py` | 37 PASS / 0 FAIL, sin solicitudes externas |
| Corpus de julio + septiembre desde la interfaz (24) | `pruebas/e2e4.py` | 24 PASS / 0 FAIL (15 + 4 registros, reemplazo al recargar, CSV, ID de Proceso, sin red) |
| Corpus de junio desde la interfaz (21) | `pruebas/e2e5.py` | 21 PASS / 0 FAIL (13 contratistas, formato `cotizante`, páginas ilegibles, hallazgos conocidos, ID de Proceso, sin red) |
| Corpus de octubre (formato nuevo de la planilla SI) desde la interfaz (23) | `pruebas/e2e6.py` | 23 PASS / 0 FAIL (2 PDF con sus nombres reales, PDF mixto nuevo + anterior, CSV, sin red) |
| Regresión «golden master» | `regresion/regresion.py` | IGUAL en los 8 PDF (103, 103, 272, 177, 2389, 1814, 308 y 103 campos). Los 6 anteriores no cambiaron con la v1.3.0; los 2 de octubre se fijaron tras revisar a mano sus lecturas contra el texto del PDF |
| Procedencia de los valores | Cada valor extraído se busca en el texto de la página que dice ser su origen (`pdftotext`) | 3369 valores con procedencia; 3356 hallados; los 13 restantes son valores que la app **compone** a partir de varios fragmentos del formato `soporte` («MES junio AÑO 2026» ×6, «MES agosto AÑO 2026» ×2, «MES mayo AÑO 2026» ×2, «MES septiembre AÑO 2026» ×2) o el nombre del supervisor de 77094907 (pág. 30), que la app lee después de descartar el texto sobrescrito; revisados a mano: están en la página |
| Revisión visual de firmas | 230 recortes de firma del corpus (134 de julio/septiembre + 74 de junio + 22 de octubre) revisados a ojo contra la decisión de la app | Sin discrepancias en la versión final (ver §6 para los límites); en junio y octubre solo el bloque opcional del ordenador de la planilla aparece «SIN FIRMA» |

Tiempos medidos una vez: PDF de 124 págs./18 MB ≈ 12 s en Chromium headless; PDF de 83 págs./8 MB ≈ 5 s; PDF de 29 págs. ≈ 2 s. No es una prueba de carga.

## 3. Resultado sobre el corpus (detalle en `HALLAZGOS_CORPUS.md/.csv` —julio y septiembre—, `HALLAZGOS_JUNIO.md/.csv` y `HALLAZGOS_OCTUBRE.md/.csv`)

34 paquetes: **3 VÁLIDO, 19 VÁLIDO CON ADVERTENCIAS, 12 ERROR**; ninguno «REQUIERE REVISIÓN» ni «NO IDENTIFICADO». 1803 comprobaciones: 1650 OK, 47 INFO, 74 ADVERTENCIA, 4 NO VERIFICABLE, 28 ERROR.

| Grupo | Paquetes | VÁLIDO | CON ADVERT. | ERROR | Comprobaciones (OK / INFO / ADV. / NO VERIF. / ERROR) |
|---|---|---|---|---|---|
| Septiembre (4 PDF) | 4 | 0 | 3 | 1 | 208 / 8 / 7 / 0 / 2 |
| Julio (combinado) | 15 | 1 | 8 | 6 | 750 / 19 / 36 / 0 / 15 |
| Junio (combinado) | 13 | 1 | 7 | 5 | 551 / 18 / 28 / 4 / 11 |
| Octubre (formato nuevo de la planilla SI) | 2 | 1 | 1 | 0 | 141 / 2 / 3 / 0 / 0 |

Las cédulas de las cuatro tandas se identificaron correctamente (15 de julio, 4 de septiembre, 13 de junio, 2 de octubre) y el número de comisiones por contratista coincide con el conteo manual (julio: 0,0,1,1,1,1,1,2,3,0,2,0,0,0,0 = 12; junio: 0,0,1,2,1,1,0,1,1,0,2,0,0 = 9).

**Cómo se verificó que lo leído es correcto.** No existe una lectura «de referencia» independiente de estos 34 paquetes. Se usaron cuatro controles que se complementan:
1. *Consistencia entre documentos*: el mismo dato sale de documentos distintos con maquetaciones distintas (cédula y nombre en 6–10 documentos por paquete, suma de SIIF = ingresos por comisiones, número de comisión SIIF/informe/comprobante). Una lectura errónea habría producido discrepancias en bloque; los ERROR que quedan son discrepancias reales en el PDF (confirmadas en la página).
2. *Procedencia* (§2).
3. *Revisión visual* de las firmas y de los hallazgos listados abajo.
4. *Regresión* (golden master): detecta que un cambio de código altere una lectura que hoy se considera correcta. **No** es un oráculo independiente: si una lectura estuviera mal desde el principio, la referencia la repite.

**Hallazgos de julio y septiembre** (lo que la aplicación reporta; el auditor debe confirmarlos en las páginas indicadas en `HALLAZGOS_CORPUS.md`):
- *Orden de viaje distinta de la comisión*: 8_GF_16797358 (sep.), comisión 76726, dos informes dicen 73126.
- *PILA pagada fuera del mes de presentación* (30/06/2026 en planilla de julio): 94550027, 1130586370, 79418775.
- *Aportes/IBC de la planilla SI ≠ PILA*: 79418775 y 94551215 (IBC 1.894.999 vs 1.900.000; salud, pensión y ARL difieren); 76325057 (IBC 1.591.799 vs 1.634.178 y todos los aportes).
- *Planilla SI con ARL = $0* (94387459, 94551215) mientras el cálculo de referencia da $9.900 (advertencia C3); en 94551215 la PILA no trae bloque de riesgos laborales.
- *Comprobante sin firma del supervisor*: 16797358 (julio), comprobante del 24/06/2026.
- *Fechas*: informe con fechas de febrero para un tramo SIIF de junio (94377310); comprobantes con fecha de 2025 (77094907) o 11/05/2026 anterior al desplazamiento (94550027); comprobantes con «ciudad–fecha» vacío o solo mes/año (94550027, 1130586370).
- *N.º de contrato del comprobante distinto al de la planilla SI* (16797358, 1130586370, 15646465): puede ser legítimo (otro contrato/vigencia); se informa como ADVERTENCIA.
- *Nombre con defectos en la planilla SI* (94377310: «JOSE JOSE … GOMEZ GOMEZ MONTE»).
- *Diferencia de $1 en el IBC* (1.894.999 vs 1.895.000) en 10 paquetes: ADVERTENCIA por redondeo, no error.

**Hallazgos de junio** (lo que la aplicación reporta; confírmelos en las páginas indicadas en `HALLAZGOS_JUNIO.md`; todos son del PDF, ninguno es una conclusión de auditoría):
- *PILA pagada fuera del mes de presentación* (29/05/2026 en planilla de junio): 94377310 (pág. 7) y 79418775 (pág. 62) → V2 ERROR.
- *Aportes de la planilla SI ≠ PILA* en 79418775 (pág. 61 vs 62): IBC 1.894.999 vs 1.900.000 (dif. $5.001), salud 236.900 vs 237.500, pensión 303.200 vs 304.000, ARL 9.900 vs 10.000 → V3 ERROR (4).
- *31710078*: hay un informe con orden de viaje 32426 y ningún SIIF con ese número (V5/V6 ERROR); la comisión SIIF 48926 queda sin informe (V6 ERROR, C6). Puede ser una orden mal digitada en el informe (como el caso 73126 ≠ 76726 de septiembre): verifíquelo en las págs. 14–21.
- *94550027* (comisión 45926): comprobante con fecha 14/04/2026 anterior al desplazamiento (22/05/2026) y el campo «Ciudad / municipio – Fecha» vacío (C8).
- *1130586370*: «Ciudad / municipio – Fecha» solo con mes y año (05/2026, pág. 59) y número de contrato del comprobante distinto (C8, C9). *15646465*: contrato del comprobante distinto en las dos comisiones (C9).
- *94377310*: nombre de la planilla SI con defectos («JOSE JOSE … GOMEZ GOMEZ MONTE») frente a «… MONTENEGRO» en los demás documentos (V1 ADVERTENCIA).
- *76325057* (primer pago, n.º de pago 1 de 7): no hay PILA en el paquete; la casilla del N.º de PILA del mes anterior trae «Decreto 1273 de»; IBC y aportes de la planilla SI en $0. Los anexos (págs. 80–83) son EPS, certificado de pensiones y RUT escaneada. La app lo informa como ERROR (falta el número) y NO VERIFICABLE (PILA y aportes); la decisión de si corresponde es del auditor.
- *77094907* (págs. 35–37 con fuente sin codificación, pág. 38 radicado): documentos de la comisión 51226 NO VERIFICABLES sin OCR; «Falta: N.º de radicado» sigue como ERROR.
- *Diferencia de $1 en el IBC* (1.894.999 vs 1.895.000) en 7 de los 13 paquetes: ADVERTENCIA por redondeo.
- *Fondo de solidaridad no comparable* en los formatos `consolidada` y `resumen`: ADVERTENCIA explicada.


**Hallazgos de octubre** (lo que la aplicación reporta; ver `HALLAZGOS_OCTUBRE.md`; ninguno es un ERROR):
- *16797358* (comisiones 79626 y 81226): el comprobante de la comisión 79626 trae «Yumbo - septiembre 23 y 24 2026» en «Ciudad / municipio – Fecha» (varios días: C8 pide confirmar la fecha); el N.º de contrato del comprobante («CO1.PCCNTR.7328111 DE 2025») difiere del de la planilla SI («8980930/2026») en las dos comisiones (C9; mismo patrón que en septiembre y junio, puede ser legítimo: otro identificador del contrato).
- *1130637605* (sin comisiones): sin advertencias ni errores.
- Los dos: IBC, salud, pensión, FSP (0) y ARL de la planilla SI = PILA; N.º de PILA del mes anterior de la planilla SI = N.º de la PILA (95603627 y 6035492712); PILA de septiembre pagada el 01/10/2026, dentro del mes de elaboración de la planilla.

## 4. Matriz de trazabilidad (requisito → implementación → prueba)

| Req. | Requisito del encargo | Dónde se implementa | Pruebas | Resultado |
|---|---|---|---|---|
| R01 | Planilla SI: nombre, cédula, fecha de elaboración, N.º compromiso SIIF, honorarios, comisiones | `extract.js` `extractPlanilla` | E07, E08, M01–M04 | PASS |
| R02 | N.º de planilla PILA = el del **mes anterior** a la fecha de presentación | `extractPlanilla` (columna por mes; «Setiembre» reconocido) | E07, E03-V2 | PASS |
| R03 | IBC, aportes salud y pensión, ARL, Pro-UCEVA | `extractPlanilla` | E07 | PASS |
| R04 | Firmas de la planilla (supervisor, ordenador) | ROI + método A en `extract.js`; método B en `proc.js`; `resolveFirma` | E05, N13, N14, N14b, V8, V9, M05, M11 | PASS (ver §6) |
| R05 | PILA: cédula, N.º, periodo, fecha de pago, empresa que recauda, salud, pensión, ARL | `pila.js` (6 formatos) | E07–E09, M08, M14, J05, X9, regresión | PASS en los 6 formatos del corpus |
| R06 | SIIF: fecha de solicitud, N.º de solicitud, total | `extractSiif` | E10, E11, X2 | PASS |
| R07 | Informe de legalización: fecha, orden de viaje, firmas contratista y supervisor | `extractInforme` | E10, E11, E04, N13, M10 | PASS |
| R08 | Comprobante: fecha, documento de identidad, N.º de comisión, 3 firmas | `extractComprobante` | E10, E11, E05 | PASS |
| R09 | Radicado: número | `extractRadicado` | E10, E11 | PASS |
| R10 | Varias comisiones en el mes: verificar cada una | Agrupación por comisión (`analyze`), V4–V6 por comisión | E10–E12, X2, X3, M04 | PASS |
| R11 | Admitir muchos documentos | Cola de carga, lote, arrastrar-soltar; un PDF combinado puede traer muchos paquetes | N15, N16, M01, M16, M17 | PASS (124 págs./15 contratistas; no se probó con cientos de PDF) |
| R12 | V1: cédula y nombre iguales en todos los documentos | `validate.js` V1 | E03-V1, U2 | PASS |
| R13 | V2: N.º de planilla SI = PILA y pago en el mes de presentación | V2 | E03-V2; M06 | PASS |
| R14 | V3: montos de seguridad social correctos | V3 | E03-V3, M07, M08; autopruebas V4 | PASS |
| R15 | V4: Σ totales de comisiones SIIF = ingresos por comisiones | V4 | E03-V4, E12, E22; X2, V5 | PASS |
| R16 | V5: todos los documentos corresponden al número de la comisión | V5 | E04 | PASS |
| R17 | Presentar y validar todos los contratistas con anexos | Listado con filtros y detalle por pestañas | E01, E39–E41, N15, M01, M13 | PASS |
| R18 | Reemplazar si existe misma cédula + mes (+ nombre) | `core.js` `guardarPaquete` | E14–E21, N10, M17; S1 | PASS |
| R19 | Funcionamiento local, sin red | CSP, sin llamadas de red, IndexedDB | E43, E13, M19, J18, e2e_http | PASS |
| R20 | Botón de eliminar el registro de un contratista | `eliminarDlg`, `core.eliminar` | E31–E33; S2 | PASS |
| R21 | Auditar y no suponer | Este informe; datos ausentes → «No encontrado»; formato desconocido → aviso | Procedencia (§2), revisión estática | PASS |
| R22 | Persistencia local | `store.js` (IndexedDB: registros y PDF originales) | E13; S8 | PASS |
| R23 | Exportar CSV, respaldo e informe imprimible | `core.js`, `ui-detalle.js` | E28–E30, E34, E36, M15; S6, S7 | PASS (la impresión se verificó generando el PDF, no con impresora) |
| R24 | Sin OCR: páginas sin texto o con texto ilegible → revisión manual, sin declarar «falta documento» | `classifyPage` SIN_TEXTO / ILEGIBLE; V6 (NO VERIFICABLE) | N05, N06, X4, X7, J06, J10, J16 | PASS |
| R25 | Seguridad: texto del PDF nunca como HTML | `h()` solo usa textContent | U4, revisión estática | PASS |
| R26 | Pantalla de configuración | `ui.js` `configDlg` | E37, E38; S9 | PASS |
| R27 | Edición manual conservando el original | `core.editarCampo` | E18, E22–E24; S4 | PASS |
| R28 | Paquete no identificado no se guarda hasta completar cédula y mes | `core.identificar`, `completarPendiente` | N03, N07–N09; S3 | PASS |
| R29 | Hojas con el contenido girado y texto sobrescrito se leen igual que las normales | `pagemodel.js` (`rotacionContenido`, `viewport`, `quitarSobreescritura`) | X8, regresión (junio), J01–J04 | PASS (casos reales: PDF de junio) |
| R30 | Informe de varias páginas = un solo informe | `classifyPage` (`datos` / `firmas` / `control`), `analyze` | X7, J01, J04 | PASS |
| R31 | Casilla de PILA con texto (primer pago) se informa sin adivinar | `extractPlanilla` (`pilaNroTexto`), V6 | X10, J11 | PASS |
| R32 | Extraer, ver y exportar el «ID de Proceso» de la planilla SI, sin alterar lo existente | `extractPlanilla` (`idProceso`), `core.js` (`resumenRegistro`, `csvResumen`), `ui.js`, `ui-detalle.js` | X11, M12b, M13b, M13c, M15b, M15c, J14b, J14c, J15b, O06, O16, O18, regresión | PASS (34/34 planillas del corpus) |
| R33 | Leer la planilla SI en el formato nuevo de octubre de 2026 sin perder el formato anterior | `extractPlanilla` (casilla fusionada del N.º de PILA, cero contable «$ -», rótulo «ORDENADOR DEL GASTO»), `extractComprobante` (tolerancia de fila), V6/C8 | X12, X13, O01–O20, regresión (8 PDF) | PASS (2 paquetes en el formato nuevo; ver límite en §0) |

(M09 verifica además C8 y M10 verifica C6. Los identificadores E/N/M/J son las pruebas de `e2e2.py`, `e2e3.py`, `e2e4.py` y `e2e5.py`; los de una letra y número —S, U, V, X— son las autopruebas internas.)

## 5. Fallos encontrados y corregidos durante la v1.1, la v1.2 y la v1.3

1. Informe: fecha en formatos no previstos («1 julio 2026», «20 de mayo del 2026», «30 de jun. de 26») no se leía → `parseFecha` ampliado. Fecha de comprobante solo con mes y año → se acepta sin día y se avisa (C8).
2. Informe: orden de viaje nula cuando la etiqueta y el número quedan en segmentos o líneas distintas → lectura por fila y por columna.
3. Comprobante: cargo y nombre mezclados, columnas desplazadas → lectura por columnas.
4. Informe: el nombre del supervisor incorporaba el texto «Instructor G17» de la columna de la firma → columna limitada.
5. V1: falsos ERROR por nombres truncados o repetidos en la planilla → comparación con tolerancia a prefijo (ADVERTENCIA).
6. V3: falsos «no verificable» por fondo de solidaridad en formatos que no lo traen; falso ERROR de IBC cuando no hay bloque ARL; «No encontrado» en C2 → reglas corregidas (§0b, tabla «Cambios de la v1.1»).
7. Firmas: firma pegada como anotación (Stamp) no detectada; imagen diminuta del supervisor en el comprobante de 15646465 quedaba en «REQUIERE REVISIÓN»; firma del supervisor de la planilla fuera del ROI → detección por anotaciones, umbral `minInkConAPx`, ROI ampliado.
8. Planilla SI: «Ordenador SIN FIRMA» como ERROR en todos los paquetes (el formato no tiene espacio de firma) → no obligatoria por defecto.
9. **PILA `soi1` (Compensar): el aporte a la caja de compensación (CCF, ej. $37.900 en 16797358) no se leía** → C2 daba una advertencia falsa («total a pagar ≠ suma»). Se encontró al revisar el informe de hallazgos, no con las pruebas automáticas; corregido y reflejado en la referencia de regresión (3 diferencias esperadas: `PILA.ccf`, C2 y C3-CCF).
10. Fallos de las propias pruebas (no de la aplicación): clasificación de página solo con título (X1), orden INFO/OK en el grupo V3 (V4), lectura en modo texto que convertía `\r\n` (M15).

11. **(v1.2, junio)** Contenido girado dentro de una hoja vertical, texto sobrescrito, informe repartido en varias páginas, sexto formato de PILA, páginas con fuente sin codificación y diseño distinto de la PILA `soi1` (columna del nombre, bloque CCF): ver §0b. Ninguno lo habrían detectado las pruebas de julio/septiembre; los destapó un PDF nuevo. Se añadieron X7–X10 y `e2e5.py` y se actualizó la referencia de regresión **después** de revisar a mano las lecturas de junio.
12. **(v1.2)** Explicación de C8 contradictoria con su estado; pruebas de la v1.1 con rutas fijas del entorno de desarrollo y `solo_imagen.pdf` que `make_pdfs.py` no generaba (fallaba en una carpeta limpia) → corregido y verificado desde un zip limpio.

13. **(v1.3.0, octubre)** Formato nuevo de la planilla SI: N.º de PILA fusionado con el rótulo vecino, fondo de solidaridad «$ -», rótulo «ORDENADOR DEL GASTO» (ver §0); y, en los mismos PDF, tolerancia de fila del comprobante (C7 en NO VERIFICABLE por un tramo no leído) y aviso C8 engañoso («vacío») con varios días en «Ciudad – Fecha».
14. **(v1.3.0, prueba)** `e2e2.py` falló 2 de 4 veces al correr justo después de las autopruebas: esperaba un instante «sin diálogos abiertos» entre el diálogo de Configuración (que se cierra) y el de confirmación (que se abre casi a la vez), una carrera de la propia prueba, no de la aplicación. Se corrigió la prueba (espera el botón de confirmación) y se repitió 4 veces seguidas con 48/48.

Lección: las pruebas automáticas **no** detectan información que simplemente no se lee (el caso 9), ni un formato que no han visto (casos 11 y 13). Lo detectó una revisión humana del informe en el primer caso y un PDF nuevo en el segundo. Ver §7.

## 6. Decisiones, supuestos y límites (léalos antes de usarla en producción)

**Interpretaciones del encargo (configurables en «Configuración»)**
- «Supervisado» se interpretó como el **contratista**. Firmas exigidas por defecto: planilla SI = contratista y supervisor (el ordenador es opcional porque el formato no tiene espacio); informe = contratista y supervisor; comprobante = las tres.
- El estado global depende solo de V1–V7. Una firma no confirmada da «REQUIERE REVISIÓN», nunca «VÁLIDO». C1–C9 solo agregan advertencias o información.
- Un documento repetido con los mismos datos se cuenta **una vez**; si se repite con datos distintos se muestra una advertencia.
- Un informe se asocia a su comisión por el N.º de orden de viaje; si no coincide con ningún SIIF se asocia a la comisión inmediatamente anterior en el PDF (así se detecta la orden 73126 ≠ 76726). El radicado se asocia al comprobante anterior.
- Los nombres se comparan como conjunto de palabras (sin tildes ni orden); si uno contiene al otro o hay una palabra truncada, es advertencia.
- IBC: diferencia de $1 = ADVERTENCIA (`pila.tolIBC`). Salud, pensión y ARL se comparan exactos con el aporte (no con el valor pagado).
- Los porcentajes de la validación complementaria C3 (IBC 40 % de honorarios, salud 12,5 %, pensión 16 %, ARL 0,522 %, CCF 2 %) son valores por defecto editables; coinciden con las muestras, pero no los confirmó ninguna norma consultada en esta sesión.

**Qué NO se probó o no se puede garantizar**
- **Formatos nuevos.** La lectura reconoce los formatos del corpus (6 PDF, 32 paquetes). Un operador de PILA o un diseño de planilla/informe/comprobante distinto puede dar «No encontrado» o una lectura parcial; la app lo muestra (no inventa) y, para la PILA, avisa «formato desconocido». Los formatos `resumen` e `individual` se vieron **dos veces** cada uno y `cotizante` **una vez**. **Evidencia de que esto importa:** el PDF de junio, que llegó después de calibrar con julio y septiembre, mostró cinco huecos (§0b). Octubre lo confirmó: la planilla SI cambió de diseño y exigió ajustes (§0). Es razonable esperar que un lote nuevo vuelva a mostrar alguno: por eso la regla de operación es revisar primero los paquetes con avisos y enviar el PDF problemático para ajustar la lectura (§7).
- **Sin OCR.** Una página escaneada o con fuente sin codificación no se puede leer: se marca «REQUIERE REVISIÓN MANUAL» y las reglas que dependen de ella quedan NO VERIFICABLE. Un campo que solo se ve en la imagen (p. ej. el número del radicado de 77094907) se reporta como «No encontrado». Agregar OCR es posible (tesseract.js incrustado) pero exige relajar la política de seguridad del navegador (CSP) y se decidió no hacerlo sin su aprobación.
- **Completitud.** La procedencia prueba que lo leído está en la página, no que se leyó *todo* lo que había (caso 9 de §5). Hay que revisar «No encontrado» y los avisos de lectura.
- **Método B de firmas** (tinta medida sobre la página renderizada) solo corre en un navegador real; en el arnés de desarrollo en Node queda «PENDIENTE». Las pruebas con navegador sí lo ejercen.
- **Firmas.** Calibradas con las firmas del corpus (208 recortes revisados) más casos sintéticos; no distingue una firma auténtica de cualquier imagen o trazo, ni detecta firmas muy tenues o escaneadas con distinta resolución. La validez de la firma es decisión del auditor.
- Otros navegadores (Firefox, Safari, Edge real) y Windows; **`iniciar.bat` no se ejecutó** (se probó el mismo servidor con `python3 -m http.server` en Linux).
- Volumen: no se probó con cientos de PDF ni con la cuota de almacenamiento del navegador (el PDF original se guarda por contratista; según el código, el combinado de 18 MB se guarda una sola vez y los 15 registros lo referencian; no se midió el consumo real).
- Accesibilidad con lector de pantalla; impresión física.
- El chequeo de mutación (romper a propósito partes del código para ver que las pruebas fallen) se hizo en la v1.0 y **no se repitió** en la v1.1; la v1.1 añadió casos negativos (IBC ±, FSP, firmas pequeñas, nombres truncados).
- Datos personales: `regresion/gold/*.json`, `HALLAZGOS_CORPUS.*` y `HALLAZGOS_JUNIO.*` contienen cédulas, nombres y montos de los contratistas de las muestras; trátelos con la misma reserva que los PDF. Los PDF de muestra **no** se incluyen en la entrega.

## 7. Mantenimiento recomendado (cómo mantener la confiabilidad)

1. Antes de usar la app con un lote nuevo, revise primero los paquetes con avisos de lectura, «No encontrado» o «REQUIERE REVISIÓN»; no los dé por buenos.
2. Cuando aparezca un formato nuevo: guarde el PDF (anonimizado si es necesario) en `pruebas/muestras/`, añada el lector o ajuste el existente en `src/pila.js` / `src/extract.js`, y ejecute `regresion/regresion.py`: debe seguir diciendo IGUAL en los PDF anteriores. Después `--actualizar` para fijar el nuevo caso **solo tras revisarlo a mano contra el PDF**.
3. Tras cualquier cambio, repita todas las suites (§2: autopruebas, e2e2, e2e3, e2e_http, e2e4, e2e5, e2e6 y la regresión).
4. Al ver un resultado extraño, use «Reprocesar» y la pestaña «Revisión visual»; corrija el valor con el lápiz (queda el historial).

## 8. Cómo repetir las pruebas

Requisitos: Python 3, `pip install playwright pypdf reportlab` y Chromium instalado para Playwright. Coloque sus PDF en `pruebas/muestras/` con los nombres `julio.pdf`, `junio.pdf`, `o1_16797358.pdf` (8_GF_16797358_5126_OCT_2026.pdf), `o2_1130637605.pdf` (2_GF_1130637605_5526_OCT_2026.pdf), `c1_66825336.pdf`, `c2_31710078.pdf`, `c3_16797358.pdf` y `c4_15646465.pdf` (o apunte `VC_MUESTRAS` a la carpeta que los tenga; `VC_INDEX` fuerza otra ruta de `index.html`).

1. En la aplicación: **Ejecutar pruebas** (autopruebas; no tocan sus datos).
2. Desde la carpeta `pruebas/`: `python3 make_pdfs.py` (crea los PDF alterados a partir de `c3_16797358.pdf`), luego `python3 e2e2.py`, `e2e3.py`, `e2e_http.py`, `e2e4.py`, `e2e5.py` (se omite si falta `junio.pdf`), `e2e6.py` (se omite si faltan los PDF de octubre) y `smoke.py`.
3. Desde la carpeta `regresion/`: `python3 regresion.py ../pruebas/muestras` (agregue `--actualizar` solo para fijar una nueva referencia).
