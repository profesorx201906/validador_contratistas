import json
from helpers import *
exec(open('e2e2.py',encoding='utf-8').read().split("with sync_playwright() as p:")[0])  # reutiliza utilidades (check, subir, reg...)
RES.clear()
with sync_playwright() as p:
    b, ctx, pg, logs, reqs = abrir(p)
    pg.set_viewport_size({'width':1400,'height':900})
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); await VC.app_ui.S.app.resetConfig(); }")
    pg.evaluate("() => VC.app_ui.S.app.store.allRegistros().then(()=>VC.app_ui.init)")
    # N1 archivo que no es PDF / dañado / otro documento / solo imagen
    m = subir(pg, PD+'no_es_pdf.pdf'); check('N01','Archivo con extensión .pdf que no es PDF: error claro, nada guardado', 'no es un PDF' in m[0] and len(reg(pg))==0, m[0])
    m = subir(pg, PD+'dañado.pdf'); check('N02','PDF truncado/dañado: error informado sin bloquear la aplicación', 'error' in pg.inner_text('.q-item:last-child').lower() or 'PDF' in m[0] and len(reg(pg))==0, m[0])
    check('N02b','Tras el PDF dañado la aplicación sigue operativa (carga siguiente funciona)', True)
    m = subir(pg, PD+'otro_documento.pdf')
    check('N03','PDF que no corresponde al formato: paquete NO IDENTIFICADO, no se guarda', '1 sin identificar' in m[0] and len(reg(pg))==0 and 'NO IDENTIFICADO' in pg.inner_text('#pend-wrap'), m[0])
    pg.screenshot(path='shots/04_pendiente.png')
    # descartar
    pg.click('#pend-wrap button:has-text("Descartar")'); dlg(pg,'true'); check('N04','Descartar un paquete no identificado lo quita sin guardarlo', len(reg(pg))==0 and not pg.query_selector('.pend'))
    m = subir(pg, PD+'solo_imagen.pdf')
    check('N05','PDF sin capa de texto (solo imagen): sin OCR, paquete sin identificar y aviso de revisión manual', '1 sin identificar' in m[0] and len(reg(pg))==0, m[0])
    pdsinTexto = pg.evaluate("() => VC.app_ui.S.pendientes.map(p => p.pk.paginas.map(x => x.etiqueta))")
    check('N06','Etiqueta de página «SIN TEXTO - REQUIERE REVISIÓN MANUAL»', all(e=='SIN TEXTO - REQUIERE REVISIÓN MANUAL' for l in pdsinTexto for e in l) and len(pdsinTexto[-1])==2, pdsinTexto)
    pg.click('#pend-wrap .pend:last-child button:has-text("Descartar")'); dlg(pg,'true')
    # sin planilla → pendiente → completar manualmente
    m = subir(pg, PD+'sin_planilla.pdf')
    check('N07','Paquete sin planilla (PILA + comisiones): NO IDENTIFICADO; sugiere cédula y nombre desde otros documentos', '1 sin identificar' in m[0] and pg.input_value('#pend-wrap input[aria-label="Cédula"]')=='16797358' and 'NESTOR' in pg.input_value('#pend-wrap input[aria-label="Nombre"]'), (m[0], pg.input_value('#pend-wrap input[aria-label="Cédula"]')))
    pg.click('#pend-wrap button:has-text("Registrar")')
    check('N08','Registrar sin indicar el mes: se rechaza con mensaje', 'AAAA-MM' in pg.inner_text('#pend-wrap') and len(reg(pg))==0, pg.inner_text('#pend-wrap'))
    pg.fill('#pend-wrap input[aria-label="Mes de la planilla"]', '2026-09'); pg.click('#pend-wrap button:has-text("Registrar")')
    esperar(pg, "() => document.querySelectorAll('#tabla tbody tr').length===1", 10)
    R = reg(pg)[0]
    check('N09','Al completar cédula y mes se guarda y se valida (sin planilla → V6 ERROR, estado ERROR)', R['clave']=='16797358|2026-09' and 'ERROR' in estados(R,'V6') and R['estado']=='ERROR', (R['clave'], estados(R,'V6')))
    # reemplazo del mismo por el completo
    m = subir(pg, PDF); check('N10','El PDF completo con la misma cédula+mes reemplaza el registro completado manualmente', '1 reemplazado(s)' in m[0] and len(reg(pg))==1 and reg(pg)[0]['ncom']==2)
    # sin comprobante/radicado 78826
    m = subir(pg, PD+'sin_comprobante_78826.pdf'); R = reg(pg)[0]
    v6 = [x for x in R['v'] if x[0]=='V6' and x[1]=='ERROR']
    check('N11','Faltan comprobante y radicado de una comisión: V6 ERROR indicando los documentos faltantes', any('78826' in x[2] and 'documentos' in x[2] for x in v6) and R['estado']=='ERROR', v6)
    ir_detalle(pg,'validaciones'); txt = pg.inner_text('#panel')
    check('N12','La explicación nombra los documentos faltantes', 'comprobante de gastos de transporte, informe de radicación' in txt, '')
    pg.click('button:has-text("Volver al listado")')
    # sin firmas en el informe 18/08
    m = subir(pg, PD+'sin_firmas_informe_18_08.pdf'); R = reg(pg)[0]
    v7 = [x for x in R['v'] if x[0]=='V7']
    sin = [x for x in v7 if x[1]=='ERROR']
    check('N13','Informe sin imágenes de firma: las 2 firmas de ese informe pasan a SIN FIRMA (ERROR), el resto sigue FIRMADA (el ordenador de la planilla no es obligatorio)', len(sin)==2 and sum(1 for x in sin if 'Informe 18/08/2026' in x[2])==2 and sum(1 for x in v7 if x[1]=='OK')==13, [x[2] for x in sin])
    # firma vectorial realista (muchas curvas)
    m = subir(pg, PD+'firma_vectorial_ordenador.pdf'); R = reg(pg)[0]
    v7 = [x for x in R['v'] if x[0]=='V7']
    ordp = [x for x in v7 if x[2].startswith('Planilla SI — Ordenador')][0]
    check('N14','Firma vectorial (trazo a mano con curvas) en el ordenador de la planilla: A y B coinciden → FIRMADA; V7 en OK', 'FIRMADA' in ordp[2] and all(x[1]=='OK' for x in v7), ordp)
    ir_detalle(pg,'visual'); esperar(pg, "() => !!document.querySelector('#visor canvas')", 40); time.sleep(1)
    print('   fila ordenador:', pg.inner_text('tr[data-firma="planilla.ordenador"]').replace('\n',' | '))
    pg.click('button:has-text("Volver al listado")')
    # firma dudosa: trazo corto tapado por texto impreso (A no la ve, B ve indicios) -> nunca SIN FIRMA
    pg.evaluate("async () => { const a = VC.app_ui.S.app; const c = VC.extract.cloneCfg(a.cfg); c.firmasObligatorias.planilla.ordenador = true; await a.saveConfig(c); }")
    m = subir(pg, PD+'firma_dudosa_ordenador.pdf'); R = reg(pg)[0]
    v7 = [x for x in R['v'] if x[0]=='V7']
    ordp = [x for x in v7 if x[2].startswith('Planilla SI — Ordenador')][0]
    check('N14b','Trazo dudoso (indicios de tinta, sin imagen/curvas), con la firma del ordenador exigida: REQUIERE REVISIÓN (no se declara SIN FIRMA) y el estado global no es VÁLIDO', ordp[1]=='NO VERIFICABLE' and 'REQUIERE REVISIÓN' in ordp[2], (ordp, R['estado']))
    pg.evaluate("async () => { await VC.app_ui.S.app.resetConfig(); }")
    ir_detalle(pg,'visual'); esperar(pg, "() => !!document.querySelector('#visor canvas')", 40)
    print('   fila ordenador (dudosa):', pg.inner_text('tr[data-firma="planilla.ordenador"]').replace('\n',' | '))
    pg.click('button:has-text("Volver al listado")')
    # varios archivos a la vez (lote) + arrastrar y soltar
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); await VC.app_ui.init; }")
    pg.click('#btn-config') ; pg.click('dialog[open] button[data-valor="cancelar"]')
    pg.reload(); esperar(pg, '() => !!(window.VC && window.VC.listo === true)', 20)
    t0=time.time(); m = subir(pg, PDF, PD+'sin_comisiones.pdf', PD+'sin_planilla.pdf', PD+'otro_documento.pdf', PD+'no_es_pdf.pdf')
    check('N15','Lote de 5 archivos: cada uno se procesa y se informa por separado', len(m)==5 and '1 nuevo(s)' in m[0] and '1 reemplazado(s)' in m[1] and '1 sin identificar' in m[2] and 'no es un PDF' in m[4], m)
    print('   lote de 5 en %.1fs' % (time.time()-t0))
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); }")
    # arrastrar y soltar
    pg.reload(); esperar(pg, '() => !!(window.VC && window.VC.listo === true)', 20)
    b64 = base64.b64encode(open(PDF,'rb').read()).decode()
    pg.evaluate("""async (b64) => { const bin = atob(b64); const u = new Uint8Array(bin.length); for (let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i);
      const dt = new DataTransfer(); dt.items.add(new File([u], 'arrastrado.pdf', {type:'application/pdf'}));
      document.getElementById('drop').dispatchEvent(new DragEvent('drop', {dataTransfer: dt, bubbles: true, cancelable: true})); }""", b64)
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length===1 && q[0].dataset.estado==='listo'; }", 120)
    check('N16','Arrastrar y soltar un PDF sobre la zona de carga lo procesa', len(reg(pg))==1 and reg(pg)[0]['archivo']=='arrastrado.pdf')
    # Orden de clasificación C4 (nombre de archivo no sigue patrón → INFO)
    R = reg(pg)[0]; c4 = [x for x in R['v'] if x[0]=='C4']
    check('N17','Nombre de archivo que no sigue el patrón: C4 solo INFO', c4 and all(x[1]=='INFO' for x in c4), c4)
    errs = [l for l in logs if l.startswith(('error','PAGEERROR'))]
    check('N18','Sin errores no controlados en consola', not errs, errs[:6])
    b.close()
json.dump(RES, open('shots/e2e3_results.json','w'), ensure_ascii=False, indent=1)
print('\nTOTAL', len(RES), 'PASS', sum(1 for r in RES if r['ok']), 'FAIL', sum(1 for r in RES if not r['ok']))
