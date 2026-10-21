import json, os, re, base64, sys
from helpers import *
RES=[]
def check(id_, nombre, cond, detalle=''):
    RES.append({'id':id_,'nombre':nombre,'ok':bool(cond),'detalle':str(detalle)[:400]})
    print(('PASS ' if cond else 'FAIL ')+id_+' '+nombre+((' — '+str(detalle)[:300]) if (detalle and not cond) else ''))

def subir(pg, *paths):
    n0 = len(pg.query_selector_all('.q-item'))
    pg.set_input_files('#file-pdf', list(paths))
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>=%d && q.every(x=>x.dataset.estado==='listo'||x.dataset.estado==='error'); }" % (n0+len(paths)), 180)
    return [q.inner_text().replace('\n',' | ') for q in pg.query_selector_all('.q-item')][n0:]
def dlg(pg, valor):
    pg.click('dialog[open] button[data-valor="%s"]' % valor)
    esperar(pg, "() => !document.querySelector('dialog[open]')", 10)
def reg(pg):
    return pg.evaluate("async () => (await VC.app_ui.S.app.store.allRegistros()).map(r => ({clave:r.clave, nombre:r.nombre, estado:r.validacion.global, archivo:r.archivo, pdfId:r.pdfId, ed:r.ediciones.length, v:r.validacion.items.map(i=>[i.id,i.estado,i.regla]), hon:r.paquete.planilla&&r.paquete.planilla.honorarios&&r.paquete.planilla.honorarios.v, com:r.paquete.planilla&&r.paquete.planilla.comisiones&&r.paquete.planilla.comisiones.v, ncom:r.paquete.comisiones.length}))")
def estados(r, id_): return [x[1] for x in r['v'] if x[0]==id_]
def npdfs(pg): return pg.evaluate("async () => (await VC.app_ui.S.app.store.allPdfs()).length")
def filas(pg): return len(pg.query_selector_all('#tabla tbody tr'))
def ir_detalle(pg, tab='resumen'):
    pg.click('#tabla tbody tr .nm button'); esperar(pg, "() => !!document.querySelector('#panel')", 10); pg.click('#tab-'+tab)

with sync_playwright() as p:
    b, ctx, pg, logs, reqs = abrir(p)
    pg.set_viewport_size({'width':1400,'height':900})
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); await VC.app_ui.S.app.resetConfig(); }")
    # ---------- A. Extracción con el PDF de muestra
    m = subir(pg, PDF)
    check('E01','Carga del PDF de muestra: 1 paquete nuevo', '1 nuevo(s)' in m[0] and filas(pg)==1, m[0])
    R = reg(pg)[0]
    check('E02','Estado global ERROR (esperado por los hallazgos del PDF)', R['estado']=='ERROR', R['estado'])
    for v in ['V1','V2','V3','V4','V6']: check('E03-'+v, v+' en OK', set(estados(R,v))=={'OK'}, estados(R,v))
    v5 = [x for x in R['v'] if x[0]=='V5']
    check('E04','V5: errores solo en la comisión 76726 (2 informes con orden 73126)', sum(1 for x in v5 if x[1]=='ERROR')==2 and all('76726' in x[2] for x in v5 if x[1]=='ERROR'), v5)
    v7 = [x for x in R['v'] if x[0]=='V7']
    check('E05','V7: 14 firmas FIRMADA; la del ordenador de la planilla SIN FIRMA no es obligatoria (el formato no trae espacio de firma) y queda en OK', len(v7)==15 and all(x[1]=='OK' for x in v7) and sum(1 for x in v7 if x[2].endswith('FIRMADA'))==14 and any(x[2].startswith('Planilla SI — Ordenador') and x[2].endswith('SIN FIRMA') for x in v7), v7)
    c9 = [x for x in R['v'] if x[0]=='C9']
    check('E06','C9: diferencias de supervisor/ordenador como INFO y contrato distinto como ADVERTENCIA (sin error)', sum(1 for x in c9 if x[1]=='INFO')>=3 and sum(1 for x in c9 if x[1]=='ADVERTENCIA' and 'contrato' in x[2])>=2 and not any(x[1]=='ERROR' for x in c9), [(x[1],x[2][:50]) for x in c9])
    # valores extraídos vs. texto del PDF (pdftotext)
    vals = pg.evaluate("async () => { const r=(await VC.app_ui.S.app.store.allRegistros())[0]; const P=r.paquete.planilla, L=r.paquete.pila; const v=(f)=>f&&f.v; return {nombre:v(P.nombre), cedula:v(P.cedula), fe:v(P.fechaElab), comp:v(P.compromiso), hon:v(P.honorarios), com:v(P.comisiones), pilaSI:v(P.pilaNro), ibc:v(P.ibc), salud:v(P.salud), pen:v(P.pension), arl:v(P.arl), uceva:v(P.proUCEVA), pilaNro:v(L.numero), pced:v(L.cedula), fpago:v(L.fechaPago), per:v(L.periodoSalud), op:v(L.operador), psalud:v(L.salud), ppen:v(L.pension), parl:v(L.arl), coms:r.paquete.comisiones.map(g=>({nro:v(g.siif.nro), total:v(g.siif.total), fs:v(g.siif.fechaSolicitud), inf:g.informes.map(d=>[v(d.orden),v(d.fechaInforme)]), comp:g.comprobantes.map(e=>[v(e.nroComision),v(e.total),v(e.fechaElab)]), rad:g.radicados.map(x=>v(x.radicado))}))}; }")
    esp = {'nombre':'NESTOR EFREN AGREDA MOLINA','cedula':'16797358','comp':'5126','hon':4737497,'com':502407,'pilaSI':'94754522','ibc':1894999,'salud':236900,'pen':303200,'arl':9900,'uceva':26200,'pilaNro':'94754522','pced':'16797358','psalud':236900,'ppen':303200,'parl':9900}
    mal = {k:(vals[k],e) for k,e in esp.items() if vals[k]!=e}
    check('E07','Campos de planilla SI y PILA = valores del texto del PDF', not mal, mal)
    check('E08','Fechas: elaboración 09/2026, pago PILA 01/09/2026, periodo 08/2026', vals['fe']['m']==9 and vals['fpago']=={'y':2026,'m':9,'d':1} and vals['per']['m']==8, vals)
    check('E09','Operador = Compensar (miplanilla.com)', 'Compensar' in (vals['op'] or ''), vals['op'])
    c = {g['nro']:g for g in vals['coms']}
    check('E10','Comisión 76726: total 334.938; informes con orden 73126; comprobante 20.000; radicado 72026371215', c['76726']['total']==334938 and [i[0] for i in c['76726']['inf']]==['73126','73126'] and c['76726']['comp'][0][1]==20000 and c['76726']['rad']==['72026371215'], c['76726'])
    check('E11','Comisión 78826: total 167.469; informe orden 78826; comprobante 8.000; radicado 72026397876', c['78826']['total']==167469 and c['78826']['inf'][0][0]=='78826' and c['78826']['comp'][0][1]==8000 and c['78826']['rad']==['72026397876'], c['78826'])
    check('E12','Suma comisiones únicas 334.938+167.469 = 502.407 (no se triplican los SIIF repetidos)', c['76726']['total']+c['78826']['total']==502407)
    # ---------- B. Persistencia
    pg.reload(); esperar(pg, '() => !!(window.VC && window.VC.listo === true)', 20); esperar(pg, "() => document.querySelectorAll('#tabla tbody tr').length===1", 10)
    check('E13','Persistencia: tras recargar la página el registro sigue', filas(pg)==1)
    # ---------- C. Reemplazo con el mismo archivo
    id1 = reg(pg)[0]['pdfId']
    m = subir(pg, PDF)
    check('E14','Reemplazo: misma cédula+mes → 1 reemplazado, sigue 1 fila', '1 reemplazado(s)' in m[0] and filas(pg)==1 and len(reg(pg))==1, m[0])
    check('E15','Al reemplazar se libera el PDF anterior (1 solo PDF guardado)', npdfs(pg)==1 and reg(pg)[0]['pdfId']!=id1)
    # ---------- D. Reemplazo con paquete distinto (sin comisiones) mismo cédula+mes
    m = subir(pg, PD+'sin_comisiones.pdf')
    R = reg(pg)[0]
    check('E16','PDF recortado (planilla+PILA, sin comisiones) reemplaza el registro y detecta que faltan documentos de comisión', '1 reemplazado(s)' in m[0] and R['ncom']==0 and 'ERROR' in estados(R,'V6') and 'ERROR' in estados(R,'V4'), (m[0], R['estado'], estados(R,'V4'), estados(R,'V6')))
    m = subir(pg, PDF)
    check('E17','Volver a cargar el PDF completo restituye el resultado anterior', reg(pg)[0]['ncom']==2 and 'ERROR'==reg(pg)[0]['estado'] and estados(reg(pg)[0],'V4')==['OK','OK'])
    # ---------- E. Nombre distinto → confirmación
    ir_detalle(pg,'planilla')
    pg.click('button[aria-label="Editar Nombre del contratista"]'); pg.fill('dialog[open] input[aria-label="Nombre del contratista"]', 'OTRA PERSONA DISTINTA'); dlg(pg,'guardar')
    esperar(pg, "() => /OTRA PERSONA/.test(document.querySelector('#panel').textContent)", 10)
    check('E18','Edición manual del nombre: se muestra «editado» y el valor leído del PDF', 'editado' in pg.inner_text('#panel') and 'NESTOR EFREN AGREDA MOLINA' in pg.inner_text('#panel'))
    pg.click('button:has-text("Volver al listado")'); esperar(pg, "() => !!document.querySelector('#tabla')", 10)
    esperar(pg, "() => /OTRA PERSONA/.test(document.querySelector('#tabla').textContent)", 10)
    nq = len(pg.query_selector_all('.q-item'))
    pg.set_input_files('#file-pdf', PDF)
    pg.wait_for_selector('dialog[open]'); txt = pg.inner_text('dialog[open]')
    check('E19','Misma cédula+mes con nombre distinto: pide confirmación mostrando ambos nombres', 'OTRA PERSONA DISTINTA' in txt and 'NESTOR EFREN AGREDA MOLINA' in txt, txt)
    dlg(pg,'false')
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length===%d && q.every(x=>x.dataset.estado==='listo'||x.dataset.estado==='error'); }" % (nq+1), 60)
    check('E20','Al rechazar el reemplazo se conserva el registro existente', reg(pg)[0]['nombre']=='OTRA PERSONA DISTINTA' and '1 omitido(s)' in pg.inner_text('.q-item:last-child'), pg.inner_text('.q-item:last-child'))
    pg.set_input_files('#file-pdf', PDF); pg.wait_for_selector('dialog[open]'); dlg(pg,'true')
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length===%d && q.every(x=>x.dataset.estado==='listo'||x.dataset.estado==='error'); }" % (nq+2), 60)
    check('E21','Al aceptar se reemplaza y el nombre vuelve al del PDF', reg(pg)[0]['nombre']=='NESTOR EFREN AGREDA MOLINA' and filas(pg)==1, reg(pg)[0]['nombre'])
    # ---------- F. Edición de monto y restauración
    ir_detalle(pg,'planilla')
    pg.click('button[aria-label="Editar Ingresos por comisiones"]'); pg.fill('dialog[open] input[aria-label="Ingresos por comisiones"]', '400.000'); pg.fill('dialog[open] input[placeholder^="Motivo"]', 'prueba de auditoría'); dlg(pg,'guardar')
    esperar(pg, "() => /400\\.000/.test(document.querySelector('#panel').textContent)", 10)
    R = reg(pg)[0]
    check('E22','Editar «Ingresos por comisiones» a 400.000: V4 pasa a ERROR, se registra la edición', R['com']==400000 and 'ERROR' in estados(R,'V4') and R['ed']==1, (R['com'], estados(R,'V4'), R['ed']))
    pg.click('button[aria-label="Editar Ingresos por comisiones"]'); 
    pg.click('dialog[open] button[data-valor="restaurar"]'); esperar(pg, "() => !document.querySelector('dialog[open]')", 10)
    esperar(pg, "() => /Valor restaurado/.test(document.getElementById('toasts').textContent)", 10); time.sleep(0.5)
    R = reg(pg)[0]
    check('E23','Restaurar el valor del PDF recalcula V4 a OK', R['com']==502407 and set(estados(R,'V4'))=={'OK'}, (R['com'], estados(R,'V4')))
    pg.click('button[aria-label="Editar Ingresos por comisiones"]'); pg.fill('dialog[open] input[aria-label="Ingresos por comisiones"]', 'abc'); pg.click('dialog[open] button[data-valor="guardar"]')
    check('E24','Valor inválido en la edición: se rechaza con mensaje y el diálogo sigue abierto', pg.query_selector('dialog[open]') is not None and 'no es válido' in pg.inner_text('dialog[open]'))
    dlg(pg,'cancelar')
    # ---------- G. Revisión manual de firma (se exige la firma del ordenador de la planilla para poder probar el flujo)
    pg.evaluate("async () => { const a = VC.app_ui.S.app; const c = VC.extract.cloneCfg(a.cfg); c.firmasObligatorias.planilla.ordenador = true; await a.saveConfig(c); await a.revalidarTodos(); }")
    pg.click('button:has-text("Volver al listado")'); esperar(pg, "() => !!document.querySelector('#tabla')", 10)
    check('E24b','Con «ordenador de la planilla» obligatorio, V7 vuelve a dar ERROR por su falta de firma', 'ERROR' in estados(reg(pg)[0],'V7'), estados(reg(pg)[0],'V7'))
    ir_detalle(pg,'resumen')
    pg.click('#tab-visual'); esperar(pg, "() => !!document.querySelector('#visor canvas')", 40)
    fila = pg.locator('tr[data-firma="planilla.ordenador"]')
    fila.locator('select').select_option('FIRMADA'); fila.locator('input').fill('verificado en el original'); fila.locator('button:has-text("Aplicar")').click()
    esperar(pg, "() => /FIRMADA/.test(document.querySelector('tr[data-firma=\"planilla.ordenador\"]').textContent) && !/SIN FIRMA/.test(document.querySelector('tr[data-firma=\"planilla.ordenador\"] td:nth-child(6)').textContent)", 10)
    R = reg(pg)[0]
    v7 = [x for x in R['v'] if x[0]=='V7']
    check('E25','Confirmación manual de la firma del ordenador: V7 pasa a OK y el automático sigue visible', all(x[1]=='OK' for x in v7) and 'SIN FIRMA' in pg.inner_text('tr[data-firma="planilla.ordenador"] td:nth-child(5)'), v7)
    pg.click('tr[data-firma="planilla.ordenador"] button.link'); esperar(pg, "() => !!document.querySelector('#sig-crop canvas')", 20)
    pg.screenshot(path='shots/03_visual_sel.png', full_page=False)
    check('E26','Recorte ampliado de la zona de firma disponible', True)
    # reprocesar descarta la confirmación manual
    pg.click('.d-head button:has-text("Reprocesar")'); pg.click('dialog[open] button[data-valor="true"]')
    esperar(pg, "() => /reprocesado/i.test(document.getElementById('toasts').textContent)", 60)
    R = reg(pg)[0]
    check('E27','Reprocesar vuelve a leer el PDF guardado y descarta ediciones/confirmaciones manuales', R['ed']==0 and 'ERROR' in [x[1] for x in R['v'] if x[0]=='V7'], (R['ed'], R['estado']))
    pg.click('button:has-text("Volver al listado")'); esperar(pg, "() => !!document.querySelector('#tabla')", 10)
    # ---------- H. CSV
    pg.click('.menu > button:has-text("Exportar")')
    with pg.expect_download() as d: pg.click('button[role=menuitem]:has-text("CSV de resumen")')
    f = DL+'resumen.csv'; d.value.save_as(f)
    raw = open(f,'rb').read(); txt = raw.decode('utf-8')
    lines = txt.strip().split('\r\n'); cols = lines[0].lstrip('﻿').split(';')
    row = lines[1].split(';')
    check('E28','CSV de resumen: BOM UTF-8, separador «;», 1 fila con los valores', raw[:3]==b'\xef\xbb\xbf' and len(lines)==2 and 'NESTOR EFREN AGREDA MOLINA' in lines[1] and '4737497' in row and '502407' in row and 'ERROR' in row, lines[1][:300])
    pg.click('.menu > button:has-text("Exportar")')
    with pg.expect_download() as d: pg.click('button[role=menuitem]:has-text("CSV de validaciones")')
    f2 = DL+'validaciones.csv'; d.value.save_as(f2); t2 = open(f2,encoding='utf-8-sig',newline='').read()
    check('E29','CSV de validaciones con una fila por comprobación', len(t2.strip().split('\r\n'))>90 and 'V5;' in t2.replace('"',''), len(t2.split('\r\n')))
    # ---------- I. Respaldo / restauración
    pg.click('.menu > button:has-text("Respaldo")')
    with pg.expect_download() as d: pg.click('button[role=menuitem]:has-text("con PDF originales")')
    fb = DL+'respaldo.json'; d.value.save_as(fb)
    j = json.load(open(fb, encoding='utf-8'))
    check('E30','Respaldo JSON con registro y PDF original incluido', j['formato']=='validador-contratistas' and len(j['registros'])==1 and len(j['pdfs'])==1 and len(j['pdfs'][0]['b64'])>1e6, (len(j['registros']), len(j['pdfs'])))
    # ---------- J. Eliminar
    pg.click('.btn-eliminar'); pg.wait_for_selector('dialog[open]')
    check('E31','Eliminar pide confirmación e indica nombre, cédula y mes', 'NESTOR EFREN' in pg.inner_text('dialog[open]') and '16797358' in pg.inner_text('dialog[open]'))
    dlg(pg,'false'); check('E32','Cancelar la eliminación conserva el registro', filas(pg)==1 and len(reg(pg))==1)
    pg.click('.btn-eliminar'); pg.wait_for_selector('dialog[open]'); dlg(pg,'true')
    esperar(pg, "() => document.querySelectorAll('#tabla tbody tr').length===0", 10)
    check('E33','Eliminar borra el registro, su PDF guardado y actualiza la tabla', len(reg(pg))==0 and npdfs(pg)==0 and 'Aún no hay' in pg.inner_text('#tabla'))
    # ---------- K. Importar respaldo
    pg.click('.menu > button:has-text("Respaldo")')
    with pg.expect_file_chooser() as fc: pg.click('button[role=menuitem]:has-text("combinar")')
    fc.value.set_files(fb)
    esperar(pg, "() => document.querySelectorAll('#tabla tbody tr').length===1", 20)
    R = reg(pg)[0]
    check('E34','Importar respaldo restituye el registro, sus validaciones y el PDF', R['nombre']=='NESTOR EFREN AGREDA MOLINA' and R['estado']=='ERROR' and npdfs(pg)==1)
    ir_detalle(pg,'visual'); esperar(pg, "() => !!document.querySelector('#visor canvas')", 40)
    check('E35','Tras importar, la revisión visual funciona (PDF restaurado)', True)
    pg.click('button:has-text("Volver al listado")')
    # ---------- L. Imprimir informe
    ir_detalle(pg,'resumen'); pg.click('.d-head button:has-text("Imprimir informe")'); time.sleep(0.6)
    rep = pg.inner_text('#reporte')
    check('E36','Informe imprimible generado con estado, validaciones, firmas y valores', 'Estado global: ERROR' in rep and 'V5' in rep and 'Planilla SI — Ordenador' in rep and 'Aplicativo v' in rep, rep[:200])
    pg.pdf(path=DL+'informe.pdf', format='Letter')
    pg.click('button:has-text("Volver al listado")')
    # ---------- M. Configuración
    pg.click('#btn-config'); pg.wait_for_selector('dialog[open]')
    pg.fill('dialog[open] fieldset:has-text("Recálculo") label:has-text("Salud (fracción)") input', '0.2'); dlg(pg,'guardar')
    esperar(pg, "() => /Configuración guardada/.test(document.getElementById('toasts').textContent)", 10)
    R = reg(pg)[0]
    c3 = [x for x in R['v'] if x[0]=='C3' and x[2].startswith('Salud')]
    check('E37','Cambiar el porcentaje de salud en Configuración recalcula C3 de los registros guardados', c3 and c3[0][1]=='ADVERTENCIA', c3)
    pg.click('#btn-config'); pg.wait_for_selector('dialog[open]'); pg.click('dialog[open] button[data-valor="reset"]'); pg.wait_for_selector('dialog[open] button[data-valor="true"]'); dlg(pg,'true')   # el diálogo de configuración se cierra y el de confirmación se abre casi a la vez: no esperar «sin diálogos» entre los dos
    esperar(pg, "() => /restaurada/.test(document.getElementById('toasts').textContent)", 10)
    c3 = [x for x in reg(pg)[0]['v'] if x[0]=='C3' and x[2].startswith('Salud')]
    check('E38','Restaurar valores por defecto devuelve C3 a OK', c3 and c3[0][1]=='OK', c3)
    # ---------- N. Filtros y búsqueda
    pg.fill('#f-texto','zzzz'); check('E39','Búsqueda sin coincidencias muestra mensaje', 'Ningún registro' in pg.inner_text('#tabla'))
    pg.fill('#f-texto','16797358'); check('E40','Búsqueda por cédula encuentra el registro', filas(pg)==1)
    pg.fill('#f-texto',''); pg.select_option('#f-estado','VÁLIDO'); check('E41','Filtro por estado VÁLIDO oculta el registro con ERROR', filas(pg)==0); pg.select_option('#f-estado','')
    # ---------- Final
    errs = [l for l in logs if l.startswith(('error','PAGEERROR'))]
    check('E42','Sin errores en la consola durante todo el recorrido', not errs, errs[:5])
    ext = [u for u in reqs if not u.startswith(('data:','blob:','file:'))]
    check('E43','Sin solicitudes de red externas (solo file://)', not ext, ext)
    b.close()
json.dump(RES, open('shots/e2e2_results.json','w'), ensure_ascii=False, indent=1)
print('\nTOTAL', len(RES), 'PASS', sum(1 for r in RES if r['ok']), 'FAIL', sum(1 for r in RES if not r['ok']))
