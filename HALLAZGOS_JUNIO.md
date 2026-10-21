# Hallazgos de la aplicación sobre los PDF de muestra (JUNIO, v1.3.0)

Generado con `corpus_tools/hallazgos.py` a partir de la salida del motor real (Chromium). Lista **lo que la aplicación reportó**; no es una conclusión de auditoría. Cada punto se debe confirmar en la página indicada.

## Resumen por paquete

| Archivo | Cédula | Nombre | Págs | Estado global | ERROR | ADVERT. | INFO | OK |
|---|---|---|---|---|---|---|---|---|
| GFs_Junio_2026.pdf | 66825336 | STELIA OSORIO PEÑUELA | 1-3 | VÁLIDO CON ADVERTENCIAS | 0 | 1 | 1 | 30 |
| GFs_Junio_2026.pdf | 1130637605 | TATIANA MARIA CAMPAZ LASSO | 4-5 | VÁLIDO | 0 | 0 | 1 | 31 |
| GFs_Junio_2026.pdf | 94377310 | JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE | 6-13 | ERROR | 1 | 6 | 2 | 50 |
| GFs_Junio_2026.pdf | 31710078 | LEYDA ALEJANDRA ATEHORTUA SANDOVAL | 14-21 | ERROR | 3 | 3 | 1 | 52 |
| GFs_Junio_2026.pdf | 94550027 | CARLOS ADRIAN RENGIFO QUINTERO | 22-29 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 1 | 57 |
| GFs_Junio_2026.pdf | 77094907 | EVERTH DANIEL LOPEZ ARIZA | 30-38 | ERROR | 1 | 4 | 2 | 36 |
| GFs_Junio_2026.pdf | 6343354 | JHON JAIRO CHAVEZ ANTE | 39-41 | VÁLIDO CON ADVERTENCIAS | 0 | 2 | 2 | 28 |
| GFs_Junio_2026.pdf | 16797358 | NESTOR EFREN AGREDA MOLINA | 42-51 | VÁLIDO CON ADVERTENCIAS | 0 | 1 | 1 | 58 |
| GFs_Junio_2026.pdf | 1130586370 | CESAR ANDRES COSSIO GONZALEZ | 52-60 | VÁLIDO CON ADVERTENCIAS | 0 | 3 | 1 | 57 |
| GFs_Junio_2026.pdf | 79418775 | ISMAEL ENRIQUE CARABALLO HERNANDEZ | 61-62 | ERROR | 5 | 1 | 1 | 25 |
| GFs_Junio_2026.pdf | 15646465 | SERGIO EDUARDO SANTOS GONZALEZ | 63-76 | VÁLIDO CON ADVERTENCIAS | 0 | 3 | 3 | 84 |
| GFs_Junio_2026.pdf | 16789038 | LUIS ENRIQUE SANCHEZ ARBOLEDA | 77-78 | VÁLIDO CON ADVERTENCIAS | 0 | 1 | 1 | 30 |
| GFs_Junio_2026.pdf | 76325057 | JULIO CESAR PALECHOR VALENCIA | 79-83 | ERROR | 1 | 5 | 1 | 13 |

Total de paquetes: 13. Comprobaciones: 612 (OK 551, INFO 18, ADVERTENCIA 28, NO VERIFICABLE 4, ERROR 11).

## Detalle de ERROR y ADVERTENCIA por paquete

### 66825336 — STELIA OSORIO PEÑUELA (2026-06) — págs 1-3 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 1) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 3)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._

### 1130637605 — TATIANA MARIA CAMPAZ LASSO (2026-06) — págs 4-5 de GFs_Junio_2026.pdf — **VÁLIDO**

Sin errores ni advertencias.

### 94377310 — JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (2026-06) — págs 6-13 de GFs_Junio_2026.pdf — **ERROR**

- **ERROR** `[V2]` c) La fecha de pago de la PILA está dentro del mes de elaboración de la planilla SI  
  Mes de elaboración = 06/2026 (Planilla SI) | PILA · fecha de pago = 29/05/2026 (PILA, pág. 7)  
  _La PILA se pagó fuera del mes de presentación._
- **ADVERTENCIA** `[V1]` Nombre — Planilla SI (bloque de firma del contratista)  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (Planilla SI (bloque de firma del contratista)) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTENEGRO (Planilla SI (bloque de firma del contratista), pág. 6)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — PILA — aportante  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (PILA — aportante) = JOSE ALEXANDER GOMEZ MONTENEGRO (PILA — aportante, pág. 7)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — SIIF Comisión 47026  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (SIIF Comisión 47026) = JOSE ALEXANDER GOMEZ MONTENEGRO (SIIF Comisión 47026, pág. 8)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — Informe 25/05/2026 (Comisión 47026)  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (Informe 25/05/2026 (Comisión 47026)) = JOSE ALEXANDER GÓMEZ MONTENEGRO (Informe 25/05/2026 (Comisión 47026), pág. 11)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V1]` Nombre — Comprobante 25/05/2026 (Comisión 47026)  
  Nombre (Planilla SI) = JOSE JOSE ALEXANDER GOMEZ GOMEZ MONTE (Planilla SI, pág. 6) | Nombre (Comprobante 25/05/2026 (Comisión 47026)) = José Alexander Gómez Montenegro (Comprobante 25/05/2026 (Comisión 47026), pág. 12)  
  _Un nombre contiene al otro o trae una palabra truncada: puede faltar un nombre o apellido en uno de los documentos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 6) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 31710078 — LEYDA ALEJANDRA ATEHORTUA SANDOVAL (2026-06) — págs 14-21 de GFs_Junio_2026.pdf — **ERROR**

- **ERROR** `[V5]` Comisión 32426: documento SIIF  
    
  _Hay informes, comprobantes o radicados de esta comisión pero ningún documento SIIF con ese número._
- **ERROR** `[V6]` Comisión 32426: documentos que debe incluir  
    
  _Falta: SIIF (autorización y ordenación del pago), comprobante de gastos de transporte, informe de radicación._
- **ERROR** `[V6]` Comisión 48926: documentos que debe incluir  
    
  _Falta: informe de legalización de desplazamiento._
- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 14) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 15)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 14) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._
- **ADVERTENCIA** `[C6]` Comisión 48926: existe informe de legalización para el tramo del 27/05/2026  
  Tramo SIIF = 27/05/2026 (SIIF) | Informes (inicio–fin) = ninguno (Informes)  
  _Ningún informe cubre esa fecha._

### 94550027 — CARLOS ADRIAN RENGIFO QUINTERO (2026-06) — págs 22-29 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[C8]` Comisión 45926: fecha del comprobante ≥ fechas de los desplazamientos  
  Fecha del comprobante = 14/04/2026 (Comprobante) | Último desplazamiento = 22/05/2026 (SIIF/Informes)  
  _La fecha del comprobante es anterior al último desplazamiento: revise si es un error de digitación o si el comprobante corresponde a otra comisión._
- **ADVERTENCIA** `[C8]` Comisión 45926: campo «Ciudad / municipio – Fecha» del comprobante del 14/04/2026  
  Ciudad / municipio – Fecha = No encontrado (Comprobante)  
  _El campo está vacío o no contiene una fecha legible._

### 77094907 — EVERTH DANIEL LOPEZ ARIZA (2026-06) — págs 30-38 de GFs_Junio_2026.pdf — **ERROR**

- **ERROR** `[V6]` Comisión 51226 · Radicado: campos requeridos  
    
  _Falta: N.º de radicado._
- **NO VERIFICABLE** `[V6]` Comisión 51226: documentos que debe incluir  
    
  _Falta: informe de legalización de desplazamiento, comprobante de gastos de transporte. Hay 3 página(s) sin texto legible (pág. 35, 36, 37) que podrían ser ese documento: revíselas en «Revisión visual»._
- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 30) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 32)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[V6]` Páginas no reconocidas  
    
  _Páginas sin clasificar: 35 (TEXTO ILEGIBLE (fuente sin codificación) - REQUIERE REVISIÓN MANUAL); 36 (TEXTO ILEGIBLE (fuente sin codificación) - REQUIERE REVISIÓN MANUAL); 37 (TEXTO ILEGIBLE (fuente sin codificación) - REQUIERE REVISIÓN MANUAL). Revíselas en la pestaña «Revisión visual»._
- **ADVERTENCIA** `[C6]` Comisión 51226: existe informe de legalización para el tramo del 04/06/2026  
  Tramo SIIF = 04/06/2026 (SIIF) | Informes (inicio–fin) = ninguno (Informes)  
  _Ningún informe cubre esa fecha._

### 6343354 — JHON JAIRO CHAVEZ ANTE (2026-06) — págs 39-41 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 39) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 40)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 39) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Resumen general de pago» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 16797358 — NESTOR EFREN AGREDA MOLINA (2026-06) — págs 42-51 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[C9]` Comisión 43026: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 1130586370 — CESAR ANDRES COSSIO GONZALEZ (2026-06) — págs 52-60 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 52) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 54)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[C8]` Comisión 47526: campo «Ciudad / municipio – Fecha» del comprobante del 30/05/2026  
  Ciudad / municipio – Fecha = 05/2026 (Comprobante, pág. 59)  
  _La fecha trae solo mes y año, sin día._
- **ADVERTENCIA** `[C9]` Comisión 47526: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980933/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7327942 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 79418775 — ISMAEL ENRIQUE CARABALLO HERNANDEZ (2026-06) — págs 61-62 de GFs_Junio_2026.pdf — **ERROR**

- **ERROR** `[V2]` c) La fecha de pago de la PILA está dentro del mes de elaboración de la planilla SI  
  Mes de elaboración = 06/2026 (Planilla SI) | PILA · fecha de pago = 29/05/2026 (PILA, pág. 62)  
  _La PILA se pagó fuera del mes de presentación._
- **ERROR** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 61) | IBC pensión · PILA = $ 1.900.000 (PILA, pág. 62)  
  _Los valores no coinciden (diferencia $ 5.001)._
- **ERROR** `[V3]` Salud: planilla SI = PILA  
  Salud · planilla SI = $ 236.900 (Planilla SI, pág. 61) | Salud · aporte PILA = $ 237.500 (PILA, pág. 62)  
  _Los valores no coinciden (diferencia $ 600)._
- **ERROR** `[V3]` Pensión: planilla SI = PILA  
  Pensión · planilla SI = $ 303.200 (Planilla SI, pág. 61) | Pensión · aporte PILA = $ 304.000 (PILA, pág. 62)  
  _Los valores no coinciden (diferencia $ 800)._
- **ERROR** `[V3]` ARL: planilla SI = PILA  
  ARL · planilla SI = $ 9.900 (Planilla SI, pág. 61) | ARL · aporte PILA = $ 10.000 (PILA, pág. 62)  
  _Los valores no coinciden (diferencia $ 100)._
- **ADVERTENCIA** `[V3]` Fondo de solidaridad pensional: planilla SI = PILA  
  Fondo de solidaridad · planilla SI = $ 0 (Planilla SI, pág. 61) | Fondo de solidaridad + subsistencia · PILA = No encontrado (PILA)  
  _El formato de PILA «Autoliquidación consolidada (PagoSimple / SuAporte)» no discrimina el aporte al fondo de solidaridad, por lo que no se puede comparar directamente. La planilla SI reporta $0 y la cotización a pensión sí coincide._

### 15646465 — SERGIO EDUARDO SANTOS GONZALEZ (2026-06) — págs 63-76 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 63) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 64)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._
- **ADVERTENCIA** `[C9]` Comisión 43226: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980938/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328220 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 45726: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980938/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328220 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 16789038 — LUIS ENRIQUE SANCHEZ ARBOLEDA (2026-06) — págs 77-78 de GFs_Junio_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[V3]` IBC: planilla SI = PILA  
  IBC · planilla SI = $ 1.894.999 (Planilla SI, pág. 77) | IBC pensión · PILA = $ 1.895.000 (PILA, pág. 78)  
  _Difieren en $ 1: dentro de la tolerancia de redondeo (± $ 1), pero no son idénticos._

### 76325057 — JULIO CESAR PALECHOR VALENCIA (2026-06) — págs 79-83 de GFs_Junio_2026.pdf — **ERROR**

- **ERROR** `[V6]` Planilla SI: campos requeridos  
    
  _Falta: N.º planilla PILA (mes anterior). La planilla SI trae en esa casilla el texto «Decreto 1273 de» en lugar de un número (es el pago n.º 1 del contrato): verifique si corresponde._
- **NO VERIFICABLE** `[V2]` Planilla PILA coherente con la planilla SI  
    
  _No hay planilla PILA en el paquete._
- **NO VERIFICABLE** `[V3]` Aportes de seguridad social coherentes  
    
  _Se requieren la planilla SI y la PILA._
- **NO VERIFICABLE** `[V6]` Planilla PILA presente  
    
  _No se encontró planilla PILA en el paquete. Hay 2 página(s) sin texto legible (pág. 82, 83) que podrían ser ese documento: revíselas en «Revisión visual»._
- **ADVERTENCIA** `[V6]` Páginas no reconocidas  
    
  _Páginas sin clasificar: 80 (No reconocida); 81 (No reconocida); 82 (SIN TEXTO - REQUIERE REVISIÓN MANUAL); 83 (SIN TEXTO - REQUIERE REVISIÓN MANUAL). Revíselas en la pestaña «Revisión visual»._
- **ADVERTENCIA** `[C3]` IBC ≈ 40 % de los honorarios  
  IBC · planilla SI = $ 0 (Planilla SI, pág. 79) | Honorarios × 0.4 = $ 1.768.666 (Planilla SI)  
  _Tolerancia ± 1. El IBC de la planilla corresponde a los ingresos del mes anterior; aquí se compara con los honorarios del periodo actual, por lo que una diferencia puede ser legítima._
