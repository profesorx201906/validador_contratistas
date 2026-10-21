# Hallazgos de la aplicación sobre los PDF de muestra (CORPUS, v1.3.0)

Generado con `corpus_tools/hallazgos.py` a partir de la salida del motor real (Chromium). Lista **lo que la aplicación reportó**; no es una conclusión de auditoría. Cada punto se debe confirmar en la página indicada.

## Resumen por paquete

| Archivo | Cédula | Nombre | Págs | Estado global | ERROR | ADVERT. | INFO | OK |
|---|---|---|---|---|---|---|---|---|
| 1_GF_66825336_5726_SEP_2026.pdf | 66825336 | STELIA OSORIO PEÑUELA | 1-3 | VÁLIDO CON ADVERTENCIAS | 0 | 1 | 1 | 30 |
| 4_GF_31710078_5426_SEP_2026.pdf | 31710078 | LEYDA ALEJANDRA ATEHORTUA SANDOVAL | 1-2 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 1 | 29 |
| 8_GF_16797358_5126_SEP_2026.pdf | 16797358 | NESTOR EFREN AGREDA MOLINA | 1-29 | ERROR | 2 | 2 | 4 | 92 |
| 11_GF_15646465_4826_SEP_2026.pdf | 15646465 | SERGIO EDUARDO SANTOS GONZALEZ | 1-9 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 2 | 57 |
| GFs_Julio_2026.pdf | 66825336 | STELIA OSORIO PEÑUELA | 1-3 | VÁLIDO CON ADVERTENCIAS | 0 | 1 | 1 | 30 |
| GFs_Julio_2026.pdf | 1130637605 | TATIANA MARIA CAMPAZ LASSO | 4-5 | VÁLIDO | 0 | 0 | 2 | 31 |
| GFs_Julio_2026.pdf | 94377310 | JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE | 6-14 | VÁLIDO CON ADVERTENCIAS | 0 | 8 | 2 | 49 |
| GFs_Julio_2026.pdf | 31710078 | LEYDA ALEJANDRA ATEHORTUA SANDOVAL | 15-23 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 1 | 56 |
| GFs_Julio_2026.pdf | 94550027 | CARLOS ADRIAN RENGIFO QUINTERO | 24-31 | ERROR | 1 | 2 | 1 | 56 |
| GFs_Julio_2026.pdf | 77094907 | EVERTH DANIEL LOPEZ ARIZA | 32-43 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 2 | 58 |
| GFs_Julio_2026.pdf | 6343354 | JHON JAIRO CHAVEZ ANTE | 44-53 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 2 | 55 |
| GFs_Julio_2026.pdf | 16797358 | NESTOR EFREN AGREDA MOLINA | 54-72 | ERROR | 1 | 2 | 1 | 84 |
| GFs_Julio_2026.pdf | 1130586370 | CESAR ANDRES COSSIO GONZALEZ | 73-96 | ERROR | 1 | 7 | 1 | 110 |
| GFs_Julio_2026.pdf | 79418775 | ISMAEL ENRIQUE CARABALLO HERNANDEZ | 97-98 | ERROR | 5 | 1 | 1 | 25 |
| GFs_Julio_2026.pdf | 15646465 | SERGIO EDUARDO SANTOS GONZALEZ | 99-116 | VÁLIDO CON ADVERTENCIAS | 0 | 3 | 1 | 84 |
| GFs_Julio_2026.pdf | 16789038 | LUIS ENRIQUE SANCHEZ ARBOLEDA | 117-118 | VÁLIDO CON ADVERTENCIAS | 0 | 1 | 1 | 30 |
| GFs_Julio_2026.pdf | 76325057 | JULIO CESAR PALECHOR VALENCIA | 119-120 | ERROR | 4 | 1 | 1 | 26 |
| GFs_Julio_2026.pdf | 94387459 | GERMAN DARIO RODRIGUEZ TOLOZA | 121-122 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 1 | 29 |
| GFs_Julio_2026.pdf | 94551215 | JONNATHAN RAMIREZ PALOMINO | 123-124 | ERROR | 3 | 2 | 1 | 27 |

Total de paquetes: 19. Comprobaciones: 1045 (OK 958, INFO 27, ADVERTENCIA 43, NO VERIFICABLE 0, ERROR 17).

## Detalle de ERROR y ADVERTENCIA por paquete

### 66825336 — STELIA OSORIO PEÑUELA (2026-09) — págs 1-3 de 1_GF_66825336_5726_SEP_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 1) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 3)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._

### 31710078 — LEYDA ALEJANDRA ATEHORTUA SANDOVAL (2026-09) — págs 1-2 de 4_GF_31710078_5426_SEP_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 1) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 2)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 1) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 16797358 — NESTOR EFREN AGREDA MOLINA (2026-09) — págs 1-29 de 8_GF_16797358_5126_SEP_2026.pdf — **ERROR**

- **ERROR** `[V5]` Comisión 76726: orden de viaje del informe del 18/08/2026 = N.º de solicitud SIIF  
  N.º de solicitud · SIIF = 76726 (SIIF, pág. 4) | Orden de viaje · informe 18/08/2026 = 73126 (Informe, pág. 8)  
  _La orden de viaje del informe no corresponde al número de la comisión._
- **ERROR** `[V5]` Comisión 76726: orden de viaje del informe del 14/08/2026 = N.º de solicitud SIIF  
  N.º de solicitud · SIIF = 76726 (SIIF, pág. 4) | Orden de viaje · informe 14/08/2026 = 73126 (Informe, pág. 17)  
  _La orden de viaje del informe no corresponde al número de la comisión._
- **ADVERTENCIA** `[C9]` Comisión 76726: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 78826: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 15646465 — SERGIO EDUARDO SANTOS GONZALEZ (2026-09) — págs 1-9 de 11_GF_15646465_4826_SEP_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 1) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 2)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[C9]` Comisión 76826: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980938/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328220 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 66825336 — STELIA OSORIO PEÑUELA (2026-07) — págs 1-3 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 1) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 3)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._

### 1130637605 — TATIANA MARIA CAMPAZ LASSO (2026-07) — págs 4-5 de GFs_Julio_2026.pdf — **VÁLIDO**

Sin errores ni advertencias.

### 94377310 — JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (2026-07) — págs 6-14 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V1]` Nombre — Planilla SI (bloque de firma del contratista)  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (Planilla SI (bloque de firma del contratista)) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTENEGRO (Planilla SI (bloque de firma del contratista), pág. 6)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — PILA — aportante  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (PILA — aportante) = JOSE ALEXANDER GOMEZ MONTENEGRO (PILA — aportante, pág. 7)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — SIIF Comisión 62226  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (SIIF Comisión 62226) = JOSE ALEXANDER GOMEZ MONTENEGRO (SIIF Comisión 62226, pág. 8)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — Informe 22/06/2026 (Comisión 62226)  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (Informe 22/06/2026 (Comisión 62226)) = JOSE ALEXANDER GÓMEZ MONTENEGRO (Informe 22/06/2026 (Comisión 62226), pág. 11)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — Comprobante 30/06/2026 (Comisión 62226)  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (Comprobante 30/06/2026 (Comisión 62226)) = José Alexander Gómez Montenegro (Comprobante 30/06/2026 (Comisión 62226), pág. 13)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 6) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._
- **ADVERTENCIA** `[C6]` Comisión 62226: existe informe de legalización para el tramo del 22/06/2026  
  Tramo SIIF = 22/06/2026 (SIIF) | Informes (inicio–fin) = 22/02/2026–22/02/2026 (Informes)  
  _Ningún informe cubre esa fecha._
- **ADVERTENCIA** `[C6]` Comisión 62226: fechas de inicio y fin del informe 22/06/2026 dentro de las fechas autorizadas en el SIIF  
  Fechas autorizadas · SIIF = 22/06/2026 – 22/06/2026 (SIIF) | Inicio – fin · informe = 22/02/2026 – 22/02/2026 (Informe)  
  _El informe declara fechas de desplazamiento fuera de las autorizadas en el SIIF._

### 31710078 — LEYDA ALEJANDRA ATEHORTUA SANDOVAL (2026-07) — págs 15-23 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 15) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 16)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 15) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 94550027 — CARLOS ADRIAN RENGIFO QUINTERO (2026-07) — págs 24-31 de GFs_Julio_2026.pdf — **ERROR**

- **ERROR** `[V2]` c) La fecha de pago de la PILA está dentro del mes de elaboración de la planilla SI  
  Mes de elaboración = 07/2026 (Planilla SI) | PILA · fecha de pago = 30/06/2026 (PILA, pág. 25)  
  _La PILA se pagó fuera del mes de presentación._
- **ADVERTENCIA** `[C8]` Comisión 57726: fecha del comprobante ≥ fechas de los desplazamientos  
  Fecha del comprobante = 11/05/2026 (Comprobante) | Último desplazamiento = 12/06/2026 (SIIF/Informes)  
  _La fecha del comprobante es anterior al último desplazamiento: revise si es un error de digitación o si el comprobante corresponde a otra comisión._
- **ADVERTENCIA** `[C8]` Comisión 57726: campo «Ciudad / municipio – Fecha» del comprobante del 11/05/2026  
  Ciudad / municipio – Fecha = No encontrado (Comprobante)  
  _El campo está vacío o no contiene una fecha legible._

### 77094907 — EVERTH DANIEL LOPEZ ARIZA (2026-07) — págs 32-43 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 32) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 34)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[C8]` Comisión 58526: fecha del comprobante ≥ fechas de los desplazamientos  
  Fecha del comprobante = 04/04/2025 (Comprobante) | Último desplazamiento = 18/06/2026 (SIIF/Informes)  
  _La fecha del comprobante es anterior al último desplazamiento: revise si es un error de digitación o si el comprobante corresponde a otra comisión._

### 6343354 — JHON JAIRO CHAVEZ ANTE (2026-07) — págs 44-53 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 44) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 45)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 44) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Resumen general de pago» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 16797358 — NESTOR EFREN AGREDA MOLINA (2026-07) — págs 54-72 de GFs_Julio_2026.pdf — **ERROR**

- **ERROR** `[V7]` Comprobante 24/06/2026 — Supervisor: SIN FIRMA  
  Método A (imágenes/trazos en el ROI) = 0 imagen(es), 0 trazo(s) (Pág. 71) | Método B (tinta tras quitar texto y líneas) = 0 px, extensión 0 pt (Pág. 71)  
  _No se detectó firma._
- **ADVERTENCIA** `[C9]` Comisión 58926: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 61126: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 1130586370 — CESAR ANDRES COSSIO GONZALEZ (2026-07) — págs 73-96 de GFs_Julio_2026.pdf — **ERROR**

- **ERROR** `[V2]` c) La fecha de pago de la PILA está dentro del mes de elaboración de la planilla SI  
  Mes de elaboración = 07/2026 (Planilla SI) | PILA · fecha de pago = 30/06/2026 (PILA, pág. 74)  
  _La PILA se pagó fuera del mes de presentación._
- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 73) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 75)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[C8]` Comisión 42626: campo «Ciudad / municipio – Fecha» del comprobante del 20/05/2026  
  Ciudad / municipio – Fecha = 05/2026 (Comprobante, pág. 81)  
  _La fecha trae solo mes y año, sin día._
- **ADVERTENCIA** `[C8]` Comisión 59826: campo «Ciudad / municipio – Fecha» del comprobante del 25/06/2026  
  Ciudad / municipio – Fecha = 06/2026 (Comprobante, pág. 88)  
  _La fecha trae solo mes y año, sin día._
- **ADVERTENCIA** `[C8]` Comisión 61826: campo «Ciudad / municipio – Fecha» del comprobante del 25/06/2026  
  Ciudad / municipio – Fecha = 06/2026 (Comprobante, pág. 95)  
  _La fecha trae solo mes y año, sin día._
- **ADVERTENCIA** `[C9]` Comisión 42626: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980933/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7327942 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 59826: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980933/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7327942 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 61826: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980933/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7327942 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 79418775 — ISMAEL ENRIQUE CARABALLO HERNANDEZ (2026-07) — págs 97-98 de GFs_Julio_2026.pdf — **ERROR**

- **ERROR** `[V2]` c) La fecha de pago de la PILA está dentro del mes de elaboración de la planilla SI  
  Mes de elaboración = 07/2026 (Planilla SI) | PILA · fecha de pago = 30/06/2026 (PILA, pág. 98)  
  _La PILA se pagó fuera del mes de presentación._
- **ERROR** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 97) | IBC pensión · PILA = $ 1.900.000 (PILA, pág. 98)  
  _Los valores no coinciden (diferencia $ 5.001)._
- **ERROR** `[V3]` Salud: planilla SI = PILA  
  Salud · planilla SI = $ 236.900 (Planilla SI, pág. 97) | Salud · aporte PILA = $ 237.500 (PILA, pág. 98)  
  _Los valores no coinciden (diferencia $ 600)._
- **ERROR** `[V3]` Pensión: planilla SI = PILA  
  Pensión · planilla SI = $ 303.200 (Planilla SI, pág. 97) | Pensión · aporte PILA = $ 304.000 (PILA, pág. 98)  
  _Los valores no coinciden (diferencia $ 800)._
- **ERROR** `[V3]` ARL: planilla SI = PILA  
  ARL · planilla SI = $ 9.900 (Planilla SI, pág. 97) | ARL · aporte PILA = $ 10.000 (PILA, pág. 98)  
  _Los valores no coinciden (diferencia $ 100)._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 97) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 15646465 — SERGIO EDUARDO SANTOS GONZALEZ (2026-07) — págs 99-116 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 99) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 100)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[C9]` Comisión 60926: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980938/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328220 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 62426: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980938/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328220 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 16789038 — LUIS ENRIQUE SANCHEZ ARBOLEDA (2026-07) — págs 117-118 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 117) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 118)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._

### 76325057 — JULIO CESAR PALECHOR VALENCIA (2026-07) — págs 119-120 de GFs_Julio_2026.pdf — **ERROR**

- **ERROR** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.591.799 (Planilla SI, pág. 119) | IBC pensión · PILA = $ 1.634.178 (PILA, pág. 120)  
  _Los valores no coinciden (diferencia $ 42.379)._
- **ERROR** `[V3]` Salud: planilla SI = PILA  
  Salud · planilla SI = $ 199.000 (Planilla SI, pág. 119) | Salud · aporte PILA = $ 204.300 (PILA, pág. 120)  
  _Los valores no coinciden (diferencia $ 5.300)._
- **ERROR** `[V3]` Pensión: planilla SI = PILA  
  Pensión · planilla SI = $ 254.700 (Planilla SI, pág. 119) | Pensión · aporte PILA = $ 261.500 (PILA, pág. 120)  
  _Los valores no coinciden (diferencia $ 6.800)._
- **ERROR** `[V3]` ARL: planilla SI = PILA  
  ARL · planilla SI = $ 8.400 (Planilla SI, pág. 119) | ARL · aporte PILA = $ 8.600 (PILA, pág. 120)  
  _Los valores no coinciden (diferencia $ 200)._
- **ADVERTENCIA** `[C3]` IBC ≈ 40 % de los honorarios  
  IBC · planilla SI = $ 1.591.799 (Planilla SI, pág. 119) | Honorarios × 0.4 = $ 1.894.999 (Planilla SI)  
  _Tolerancia ± 1. El IBC de la planilla corresponde a los ingresos del mes anterior; aquí se compara con los honorarios del periodo actual, por lo que una diferencia puede ser legítima._

### 94387459 — GERMAN DARIO RODRIGUEZ TOLOZA (2026-07) — págs 121-122 de GFs_Julio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 121) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._
- **ADVERTENCIA** `[C3]` ARL (clase I) ≈ 0.522 % del IBC (aprox. al múltiplo de 100)  
  ARL (clase I) · planilla SI = $ 0 (Planilla SI, pág. 121) | IBC × 0.00522 = $ 9.900 (Cálculo)  
  _Tolerancia ± 100._

### 94551215 — JONNATHAN RAMIREZ PALOMINO (2026-07) — págs 123-124 de GFs_Julio_2026.pdf — **ERROR**

- **ERROR** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 123) | IBC pensión · PILA = $ 1.900.000 (PILA, pág. 124)  
  _Los valores no coinciden (diferencia $ 5.001)._
- **ERROR** `[V3]` Salud: planilla SI = PILA  
  Salud · planilla SI = $ 236.900 (Planilla SI, pág. 123) | Salud · aporte PILA = $ 237.500 (PILA, pág. 124)  
  _Los valores no coinciden (diferencia $ 600)._
- **ERROR** `[V3]` Pensión: planilla SI = PILA  
  Pensión · planilla SI = $ 303.200 (Planilla SI, pág. 123) | Pensión · aporte PILA = $ 304.000 (PILA, pág. 124)  
  _Los valores no coinciden (diferencia $ 800)._
- **ADVERTENCIA** `[V6]` PILA: aviso de lectura  
    
  _La PILA no incluye el bloque «Total aportes a riesgos profesionales»; se toma el aporte a ARL como $0._
- **ADVERTENCIA** `[C3]` ARL (clase I) ≈ 0.522 % del IBC (aprox. al múltiplo de 100)  
  ARL (clase I) · planilla SI = $ 0 (Planilla SI, pág. 123) | IBC × 0.00522 = $ 9.900 (Cálculo)  
  _Tolerancia ± 100._
