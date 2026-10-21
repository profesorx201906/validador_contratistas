# Recorrido con el PDF combinado de julio (124 páginas, 15 contratistas) + 4 PDFs de septiembre, desde la interfaz
import json, os, re, sys
from helpers import *
RES=[]
def check(id_, nombre, cond, detalle=''):
    RES.append({'id':id_,'nombre':nombre,'ok':bool(cond),'detalle':str(detalle)[:400]})
    print(('PASS ' if cond else 'FAIL ')+id_+' '+nombre+((' — '+str(detalle)[:300]) if (detalle and not cond) else ''))
C=MUESTRAS   # contiene julio.pdf, c1_66825336.pdf, c2_31710078.pdf, c3_16797358.pdf, c4_15646465.pdf
def filas(pg): return len(pg.query_selector_all('#tabla tbody tr'))
def reg(pg): return pg.evaluate("async () => (await VC.app_ui.S.app.store.allRegistros()).map(r => ({clave:r.clave, nombre:r.nombre, estado:r.validacion.global, e:r.validacion.resumen.errores, a:r.validacion.resumen.advertencias, nv:r.validacion.resumen.noVerificables, ncom:r.paquete.comisiones.length, pdf:r.pdfId}))")
with sync_playwright() as p:
    b, ctx, pg, logs, reqs = abrir(p)
    pg.set_viewport_size({'width':1400,'height':900})
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); await VC.app_ui.S.app.resetConfig(); }")
    pg.set_input_files('#file-pdf', [C+'julio.pdf'])
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>0 && q.every(x=>x.dataset.estado==='listo'); }", 180)
    R = reg(pg)
    check('M01','PDF combinado de 124 páginas: 15 contratistas detectados y 15 filas en la tabla', len(R)==15 and filas(pg)==15, (len(R), filas(pg)))
    check('M02','Ninguno quedó «NO IDENTIFICADO» (todos tienen cédula y mes)', all(r['clave'].endswith('|2026-07') for r in R), [r['clave'] for r in R])
    cedulas = sorted(r['clave'].split('|')[0] for r in R)
    check('M03','Las 15 cédulas esperadas', cedulas==sorted(['66825336','1130637605','94377310','31710078','94550027','77094907','6343354','16797358','1130586370','79418775','15646465','16789038','76325057','94387459','94551215']), cedulas)
    ncom = {r['clave'].split('|')[0]: r['ncom'] for r in R}
    check('M04','Comisiones por contratista: 0,0,1,1,1,1,1,2,3,0,2,0,0,0,0 (total 12)', sum(ncom.values())==12 and ncom['1130586370']==3 and ncom['16797358']==2 and ncom['15646465']==2, ncom)
    no_val = [r['clave'] for r in R if r['nv']>0]
    check('M05','Ningún paquete queda «NO VERIFICABLE» (todas las firmas se resolvieron automáticamente)', not no_val, no_val)
    estados = {}
    for r in R: estados[r['estado']] = estados.get(r['estado'],0)+1
    print('   estados:', estados)
    # hallazgos conocidos (verificados visualmente en las páginas del PDF)
    def items(clave, id_): return pg.evaluate("async (k) => (await VC.app_ui.S.app.store.getRegistro(k)).validacion.items.filter(i=>i.id==='%s').map(i=>[i.estado,i.regla])" % id_, clave)
    v2 = items('94550027|2026-07','V2'); check('M06','Carlos Rengifo: PILA pagada el 30/06 (fuera del mes de presentación) → V2 ERROR', any(x[0]=='ERROR' and x[1].startswith('c)') for x in v2), v2)
    v3 = items('79418775|2026-07','V3'); check('M07','Ismael Caraballo: IBC/aportes de la PILA ≠ planilla SI → V3 ERROR', sum(1 for x in v3 if x[0]=='ERROR')>=3, v3)
    v3b = items('1130637605|2026-07','V3'); check('M08','Tatiana Campaz (PILA con mora): V3 sin ERROR', not any(x[0]=='ERROR' for x in v3b), v3b)
    c8 = items('94550027|2026-07','C8'); check('M09','Carlos Rengifo: comprobante con fecha de elaboración anterior a la comisión y campo FECHA vacío → advertencias C8', sum(1 for x in c8 if x[0]=='ADVERTENCIA')>=2, c8)
    c6 = items('94377310|2026-07','C6'); check('M10','José A. Gómez: informe con fechas 22/02/2026 (la comisión es 22/06) → advertencias C6', sum(1 for x in c6 if x[0]=='ADVERTENCIA')>=2, c6)
    v7 = items('16797358|2026-07','V7'); check('M11','Néstor Agreda: comprobante 24/06/2026 sin firma del supervisor → V7 ERROR (1)', sum(1 for x in v7 if x[0]=='ERROR')==1 and any('Supervisor: SIN FIRMA' in x[1] for x in v7 if x[0]=='ERROR'), [x for x in v7 if x[0]!='OK'])
    # abrir el detalle y revisar visualmente
    pg.fill('#f-texto','94550027'); check('M12','Búsqueda por cédula en la lista de 15', filas(pg)==1); 
    pg.fill('#f-texto','79372-066979'); check('M12b','Búsqueda por «ID de Proceso» (79372-066979) encuentra a Carlos Rengifo y el listado lo muestra bajo la cédula', filas(pg)==1 and '79372-066979' in pg.inner_text('#tabla') and 'ID de Proceso' in pg.inner_text('#tabla'), pg.inner_text('#tabla')[:200])
    pg.fill('#f-texto','94550027')
    pg.click('#tabla tbody tr .nm button'); esperar(pg, "() => !!document.querySelector('#panel')", 10)
    for tab in ['resumen','planilla','pila','comisiones','validaciones','visual']:
        pg.click('#tab-'+tab); time.sleep(0.4)
    txt = pg.inner_text('#panel')
    check('M13','Pestañas del detalle abren sin error', len(txt)>200)
    pg.click('#tab-planilla'); tp = pg.inner_text('#panel')
    check('M13b','Pestaña Planilla SI: muestra «ID de Proceso» = 79372-066979', 'ID de Proceso' in tp and '79372-066979' in tp, tp[:300])
    pg.click('#tab-resumen'); tr = pg.inner_text('#panel')
    check('M13c','Pestaña Resumen: muestra «ID de Proceso» = 79372-066979', 'ID de Proceso' in tr and '79372-066979' in tr, tr[:300])
    pg.click('#tab-pila'); t = pg.inner_text('#panel')
    check('M14','La pestaña PILA indica el formato reconocido', 'Formato de PILA reconocido' in t and 'Planilla integrada' in t, t[:300])
    pg.click('button:has-text("Volver al listado")'); pg.fill('#f-texto','')
    # CSV
    pg.click('.menu > button:has-text("Exportar")')
    with pg.expect_download() as d: pg.click('button[role=menuitem]:has-text("CSV de resumen")')
    f = DL+'resumen_julio.csv'; d.value.save_as(f)
    lines = open(f,encoding='utf-8-sig',newline='').read().strip().split('\r\n')
    check('M15','CSV de resumen: 15 filas + encabezado', len(lines)==16, len(lines))
    cab = lines[0].split(';'); ids = {l.split(';')[0]: l.split(';')[-1] for l in lines[1:]}
    check('M15b','CSV de resumen: «ID de Proceso» es la última columna y las anteriores no se movieron', cab[-1]=='ID de Proceso' and cab[:3]==['Cédula','Nombre','Mes planilla'] and cab[-2]=='Con ediciones manuales', cab)
    check('M15c','CSV de resumen: los 15 ID de Proceso son exactos (con ceros a la izquierda y guion)', len(ids)==15 and ids['16797358']=='07696-646062' and ids['94550027']=='79372-066979' and ids['66825336']=='56586-234773' and ids['94551215']=='41998-577420' and all(re.fullmatch(r'\d{5}-\d{6}', v) for v in ids.values()), ids)
    # reemplazo con septiembre
    pg.set_input_files('#file-pdf', [C+'c1_66825336.pdf', C+'c2_31710078.pdf', C+'c3_16797358.pdf', C+'c4_15646465.pdf'])
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>0 && q.every(x=>x.dataset.estado==='listo'); }", 120)
    R2 = reg(pg)
    check('M16','Cargar septiembre: 4 registros nuevos (mes distinto) → 19 filas en total', len(R2)==19 and sum(1 for r in R2 if r['clave'].endswith('|2026-09'))==4, (len(R2),))
    # volver a cargar julio: reemplazo, no duplica
    pg.set_input_files('#file-pdf', [C+'julio.pdf'])
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>0 && q.every(x=>x.dataset.estado==='listo'); }", 180)
    R3 = reg(pg); check('M17','Recargar el PDF de julio reemplaza los 15 registros (sigue habiendo 19)', len(R3)==19, len(R3))
    errs=[l for l in logs if l.startswith(('error','PAGEERROR'))]
    check('M18','Sin errores en la consola', not errs, errs[:3])
    ext=[u for u in reqs if not u.startswith(('file://','data:','blob:'))]
    check('M19','Sin solicitudes de red externas', not ext, ext)
    b.close()
print('TOTAL', len(RES), 'PASS', sum(r['ok'] for r in RES), 'FAIL', sum(not r['ok'] for r in RES))
