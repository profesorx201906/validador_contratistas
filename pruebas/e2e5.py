# Recorrido con el PDF combinado de junio (83 páginas, 13 contratistas) desde la interfaz.
# Necesita junio.pdf en la carpeta de muestras (variable VC_MUESTRAS o pruebas/muestras/).
import json, os, re, sys
from helpers import *
RES=[]
def check(id_, nombre, cond, detalle=''):
    RES.append({'id':id_,'nombre':nombre,'ok':bool(cond),'detalle':str(detalle)[:400]})
    print(('PASS ' if cond else 'FAIL ')+id_+' '+nombre+((' — '+str(detalle)[:300]) if (detalle and not cond) else ''))
C=MUESTRAS
if not os.path.exists(C+'junio.pdf'):
    print('OMITIDA: falta junio.pdf en', C); sys.exit(0)
def filas(pg): return len(pg.query_selector_all('#tabla tbody tr'))
def reg(pg): return pg.evaluate("async () => (await VC.app_ui.S.app.store.allRegistros()).map(r => ({clave:r.clave, nombre:r.nombre, estado:r.validacion.global, e:r.validacion.resumen.errores, a:r.validacion.resumen.advertencias, nv:r.validacion.resumen.noVerificables, ncom:r.paquete.comisiones.length, fam:(r.paquete.pila||{}).fam, ileg:(r.paquete.paginas||[]).filter(x=>x.tipo==='ILEGIBLE').length}))")
with sync_playwright() as p:
    b, ctx, pg, logs, reqs = abrir(p)
    pg.set_viewport_size({'width':1400,'height':900})
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); await VC.app_ui.S.app.resetConfig(); }")
    pg.set_input_files('#file-pdf', [C+'junio.pdf'])
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>0 && q.every(x=>x.dataset.estado==='listo'); }", 240)
    R = reg(pg)
    check('J01','PDF combinado de junio (83 páginas): 13 contratistas detectados y 13 filas en la tabla', len(R)==13 and filas(pg)==13, (len(R), filas(pg)))
    check('J02','Ninguno quedó «NO IDENTIFICADO» (todos con cédula y mes 2026-06)', all(r['clave'].endswith('|2026-06') for r in R), [r['clave'] for r in R])
    ced = sorted(r['clave'].split('|')[0] for r in R)
    check('J03','Las 13 cédulas esperadas', ced==sorted(['66825336','1130637605','94377310','31710078','94550027','77094907','6343354','16797358','1130586370','79418775','15646465','16789038','76325057']), ced)
    nc = {r['clave'].split('|')[0]: r['ncom'] for r in R}
    check('J04','Comisiones por contratista (total 9; 31710078 y 15646465 con 2)', sum(nc.values())==9 and nc['31710078']==2 and nc['15646465']==2, nc)
    fam = {r['clave'].split('|')[0]: r['fam'] for r in R}
    check('J05','Formato de PILA reconocido en 12 paquetes; el 15646465 es «cotizante»; ninguno «desconocida»', fam['15646465']=='cotizante' and sum(1 for v in fam.values() if v)==12 and 'desconocida' not in fam.values(), fam)
    il = {r['clave'].split('|')[0]: r['ileg'] for r in R}
    check('J06','Solo el 77094907 tiene páginas con texto ilegible (3), y no se confunden con «falta documento»', il['77094907']==3 and sum(il.values())==3, il)
    def items(clave, id_): return pg.evaluate("async (k) => (await VC.app_ui.S.app.store.getRegistro(k)).validacion.items.filter(i=>i.id==='%s').map(i=>[i.estado,i.regla,i.expl||''])" % id_, clave)
    v2 = items('94377310|2026-06','V2'); check('J07','94377310: PILA pagada fuera del mes de presentación → V2 ERROR', any(x[0]=='ERROR' and x[1].startswith('c)') for x in v2), v2)
    v2b = items('79418775|2026-06','V2'); check('J08','79418775: PILA pagada fuera del mes de presentación → V2 ERROR', any(x[0]=='ERROR' and x[1].startswith('c)') for x in v2b), v2b)
    v3 = items('79418775|2026-06','V3'); check('J09','79418775: IBC/salud/pensión/ARL de la PILA ≠ planilla SI → 4 V3 ERROR', sum(1 for x in v3 if x[0]=='ERROR')==4, v3)
    v6 = items('77094907|2026-06','V6')
    nv = [x for x in v6 if x[0]=='NO VERIFICABLE' and 'documentos que debe incluir' in x[1]]
    check('J10','77094907: páginas ilegibles → «documentos que debe incluir» queda NO VERIFICABLE (no ERROR por falta de informe)', len(nv)==1 and not any(x[0]=='ERROR' and 'documentos que debe incluir' in x[1] for x in v6), v6)
    v6b = items('76325057|2026-06','V6'); 
    check('J11','76325057 (primer pago): el aviso cita el texto «Decreto 1273 de» de la casilla de la PILA', any('Decreto 1273 de' in x[2] and 'pago n.º 1' in x[2] for x in v6b), v6b)
    c8 = items('94550027|2026-06','C8'); check('J12','94550027: comprobante anterior al desplazamiento y fecha vacía → 2 advertencias C8', sum(1 for x in c8 if x[0]=='ADVERTENCIA')>=2, c8)
    v5 = items('31710078|2026-06','V5'); check('J13','31710078: informe de la comisión 32426 sin SIIF → V5 ERROR', any(x[0]=='ERROR' and '32426' in x[1] for x in v5), v5)
    c9 = items('1130586370|2026-06','C9'); check('J14','1130586370: contrato del comprobante distinto → C9 ADVERTENCIA', any(x[0]=='ADVERTENCIA' for x in c9), c9)
    # detalle
    pg.fill('#f-texto','06435-743216'); check('J14b','Búsqueda por «ID de Proceso» (06435-743216, con cero inicial) encuentra a 94377310 y el listado lo muestra', filas(pg)==1 and '94377310' in pg.inner_text('#tabla') and '06435-743216' in pg.inner_text('#tabla'), pg.inner_text('#tabla')[:200])
    pg.fill('#f-texto','')
    pg.click('.menu > button:has-text("Exportar")')
    with pg.expect_download() as d: pg.click('button[role=menuitem]:has-text("CSV de resumen")')
    f = DL+'resumen_junio.csv'; d.value.save_as(f)
    lines = open(f,encoding='utf-8-sig',newline='').read().strip().split('\r\n')
    cab = lines[0].split(';'); ids = {l.split(';')[0]: l.split(';')[-1] for l in lines[1:]}
    esperado = {'66825336':'34771-739812','1130637605':'83241-520178','94377310':'06435-743216','31710078':'80762-469402','94550027':'52588-878408','77094907':'68176-172195','6343354':'86132-307035','16797358':'43471-487067','1130586370':'27472-572779','79418775':'97401-694578','15646465':'36412-526935','16789038':'10141-209856','76325057':'35340-092733'}
    check('J14c','CSV de resumen: «ID de Proceso» última columna y los 13 valores exactos', cab[-1]=='ID de Proceso' and ids==esperado, (cab[-2:], ids))
    pg.fill('#f-texto','77094907'); check('J15','Búsqueda por cédula en la lista de 13', filas(pg)==1)
    pg.click('#tabla tbody tr .nm button'); esperar(pg, "() => !!document.querySelector('#panel')", 10)
    for tab in ['resumen','planilla','pila','comisiones','validaciones','visual']:
        pg.click('#tab-'+tab); time.sleep(0.4)
    txt = pg.inner_text('#panel')
    check('J16','Detalle del paquete con páginas ilegibles abre sin error y muestra la etiqueta de texto ilegible', 'ILEGIBLE' in txt.upper(), txt[:200])
    pg.click('#tab-planilla'); tp = pg.inner_text('#panel')
    check('J15b','Pestaña Planilla SI de 77094907: «ID de Proceso» = 68176-172195', 'ID de Proceso' in tp and '68176-172195' in tp, tp[:300])
    pg.click('button:has-text("Volver al listado")'); pg.fill('#f-texto','')
    errs=[l for l in logs if l.startswith(('error','PAGEERROR'))]
    check('J17','Sin errores en la consola', not errs, errs[:3])
    ext=[u for u in reqs if not u.startswith(('file://','data:','blob:'))]
    check('J18','Sin solicitudes de red externas', not ext, ext)
    b.close()
print('TOTAL', len(RES), 'PASS', sum(r['ok'] for r in RES), 'FAIL', sum(not r['ok'] for r in RES))
