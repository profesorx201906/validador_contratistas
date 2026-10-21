# Hallazgos de la aplicación sobre los PDF de muestra (OCTUBRE, v1.3.0)

Generado con `corpus_tools/hallazgos.py` a partir de la salida del motor real (Chromium). Lista **lo que la aplicación reportó**; no es una conclusión de auditoría. Cada punto se debe confirmar en la página indicada.

## Resumen por paquete

| Archivo | Cédula | Nombre | Págs | Estado global | ERROR | ADVERT. | INFO | OK |
|---|---|---|---|---|---|---|---|---|
| 8_GF_16797358_5126_OCT_2026.pdf | 16797358 | NESTOR EFREN AGREDA MOLINA | 1-33 | VÁLIDO CON ADVERTENCIAS | 0 | 3 | 1 | 110 |
| 2_GF_1130637605_5526_OCT_2026.pdf | 1130637605 | TATIANA MARIA CAMPAZ LASSO | 1-2 | VÁLIDO | 0 | 0 | 1 | 31 |

Total de paquetes: 2. Comprobaciones: 146 (OK 141, INFO 2, ADVERTENCIA 3, NO VERIFICABLE 0, ERROR 0).

## Detalle de ERROR y ADVERTENCIA por paquete

### 16797358 — NESTOR EFREN AGREDA MOLINA (2026-10) — págs 1-33 de 8_GF_16797358_5126_OCT_2026.pdf — **VÁLIDO CON ADVERTENCIAS**

- **ADVERTENCIA** `[C8]` Comisión 79626: campo «Ciudad / municipio – Fecha» del comprobante del 28/09/2026  
  Ciudad / municipio – Fecha = No encontrado (Comprobante, pág. 15)  
  _El campo trae «Yumbo - septiembre 23 y 24 2026» (pág. 15), que no se pudo interpretar como una fecha única (¿varios días?): confirme la fecha en el PDF._
- **ADVERTENCIA** `[C9]` Comisión 79626: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._
- **ADVERTENCIA** `[C9]` Comisión 81226: N.º de contrato de la planilla SI distinto al del comprobante  
  Contrato · planilla SI = 8980930/2026 (Planilla SI) | Contrato · comprobante = CO1.PCCNTR.7328111 DE 2025 (Comprobante)  
  _Los números de contrato no coinciden: el comprobante cita otro contrato._

### 1130637605 — TATIANA MARIA CAMPAZ LASSO (2026-10) — págs 1-2 de 2_GF_1130637605_5526_OCT_2026.pdf — **VÁLIDO**

Sin errores ni advertencias.
