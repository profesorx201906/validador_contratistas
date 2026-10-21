# Formato nuevo de la planilla SI (octubre de 2026): 2 PDF reales con sus nombres de archivo originales, y un PDF mixto (formato nuevo + anterior).
# Necesita en la carpeta de muestras: o1_16797358.pdf (8_GF_16797358_5126_OCT_2026.pdf, 33 págs.), o2_1130637605.pdf (2_GF_1130637605_5526_OCT_2026.pdf, 2 págs.)
# y, para la prueba del PDF mixto, c1_66825336.pdf y c3_16797358.pdf (septiembre, formato anterior).
import json, os, re, sys, io
from helpers import *
RES=[]
def check(id_, nombre, cond, detalle=''):
    RES.append({'id':id_,'nombre':nombre,'ok':bool(cond),'detalle':str(detalle)[:400]})
    print(('PASS ' if cond else 'FAIL ')+id_+' '+nombre+((' — '+str(detalle)[:300]) if (detalle and not cond) else ''))
C=MUESTRAS
N1, N2 = '8_GF_16797358_5126_OCT_2026.pdf', '2_GF_1130637605_5526_OCT_2026.pdf'
if not (os.path.exists(C+'o1_16797358.pdf') and os.path.exists(C+'o2_1130637605.pdf')):
    print('OMITIDA: faltan o1_16797358.pdf y o2_1130637605.pdf en', C); sys.exit(0)
def filas(pg): return len(pg.query_selector_all('#tabla tbody tr'))
def archivo(nombre, ruta): return {'name': nombre, 'mimeType': 'application/pdf', 'buffer': open(ruta,'rb').read()}
def reg(pg, clave): return pg.evaluate("async (k) => { const r = await VC.app_ui.S.app.store.getRegistro(k); return r && {estado:r.validacion.global, e:r.validacion.resumen.errores, a:r.validacion.resumen.advertencias, nv:r.validacion.resumen.noVerificables, ncom:r.paquete.comisiones.length, P:JSON.parse(JSON.stringify(r.paquete.planilla)), items:r.validacion.items.map(i=>[i.id,i.estado,i.regla,i.expl||''])} }", clave)
def v(P, k): return (P.get(k) or {}).get('v')
LISTO = "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>0 && q.every(x=>x.dataset.estado==='listo'); }"
with sync_playwright() as p:
    b, ctx, pg, logs, reqs = abrir(p)
    pg.set_viewport_size({'width':1400,'height':900})
    pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); await VC.app_ui.S.app.resetConfig(); }")
    pg.set_input_files('#file-pdf', [archivo(N1, C+'o1_16797358.pdf'), archivo(N2, C+'o2_1130637605.pdf')])
    esperar(pg, "() => { const q=[...document.querySelectorAll('.q-item')]; return q.length>=2 && q.every(x=>x.dataset.estado==='listo'); }", 120)
    check('O01','Los 2 PDF de octubre se registran (1 contratista cada uno) con cédula y mes 2026-10', filas(pg)==2 and pg.evaluate("async () => (await VC.app_ui.S.app.store.allRegistros()).map(r=>r.clave).sort().join()")=='1130637605|2026-10,16797358|2026-10')
    A = reg(pg,'16797358|2026-10'); B = reg(pg,'1130637605|2026-10')
    PA, PB = A['P'], B['P']
    check('O02','N.º de planilla PILA del mes anterior leído aunque venga fusionado con el rótulo vecino (95603627 y 6035492712)', v(PA,'pilaNro')=='95603627' and v(PB,'pilaNro')=='6035492712' and v(PA,'pilaNroTexto') is None, (v(PA,'pilaNro'), v(PB,'pilaNro')))
    check('O03','Fondo de solidaridad «$ -» = 0 en ambas planillas (no «No encontrado»)', v(PA,'fsp')==0 and v(PB,'fsp')==0, (v(PA,'fsp'), v(PB,'fsp')))
    check('O04','Campos de la planilla nueva de 16797358: compromiso 5126, contrato 8980930/2026, pago 10 de 12, periodo 01–31/10/2026, honorarios 4.737.497, comisiones 837.345, total 5.574.842, a pagar 4.709.623',
          v(PA,'compromiso')=='5126' and v(PA,'contrato')=='8980930/2026' and v(PA,'nroPago')=='10' and v(PA,'nroPagos')=='12' and v(PA,'periodoDel')=={'y':2026,'m':10,'d':1} and v(PA,'periodoAl')=={'y':2026,'m':10,'d':31}
          and v(PA,'honorarios')==4737497 and v(PA,'comisiones')==837345 and v(PA,'totalIngresos')==5574842 and v(PA,'valorAPagar')==4709623 and v(PA,'ibc')==1894999 and v(PA,'salud')==236900 and v(PA,'pension')==303200 and v(PA,'arl')==9900 and v(PA,'proUCEVA')==27874)
    check('O05','Campos de la planilla nueva de 1130637605: compromiso 5526, contrato 8980924/2026, pago 10 de 12, honorarios 4.737.497, comisiones 0, saldo anterior 12.317.492, a pagar 4.713.810',
          v(PB,'compromiso')=='5526' and v(PB,'contrato')=='8980924/2026' and v(PB,'nroPago')=='10' and v(PB,'honorarios')==4737497 and v(PB,'comisiones')==0 and v(PB,'saldoAnterior')==12317492 and v(PB,'valorAPagar')==4713810 and v(PB,'proUCEVA')==23687)
    check('O06','«ID de Proceso» de la planilla nueva: 20246-827984 y 33946-758134', v(PA,'idProceso')=='20246-827984' and v(PB,'idProceso')=='33946-758134', (v(PA,'idProceso'), v(PB,'idProceso')))
    check('O07','Bloque «ORDENADOR DEL GASTO» de la planilla: nombre y cargo leídos', v(PA,'ordenadorNombre')=='CESAR AUGUSTO VICTORIA CARDONA' and v(PA,'ordenadorCargo')=='SUBDIRECTOR DE CENTRO G02(E)' and v(PB,'ordenadorNombre')=='CESAR AUGUSTO VICTORIA CARDONA')
    est = lambda R, id_: [x for x in R['items'] if x[0]==id_]
    for nm, R in (('16797358',A),('1130637605',B)):
        check('O08-'+nm,'V1–V7 sin ERROR ni NO VERIFICABLE en '+nm, all(x[1] in ('OK','INFO','ADVERTENCIA') for g in 'V1 V2 V3 V4 V5 V6 V7'.split() for x in est(R,g)) and R['e']==0 and R['nv']==0, [(x[0],x[1],x[2]) for x in R['items'] if x[1] in ('ERROR','NO VERIFICABLE')])
    check('O09','Estados globales: 1130637605 VÁLIDO; 16797358 VÁLIDO CON ADVERTENCIAS', B['estado']=='VÁLIDO' and A['estado']=='VÁLIDO CON ADVERTENCIAS', (A['estado'], B['estado']))
    v2 = est(A,'V2')+est(B,'V2'); v3 = est(A,'V3')+est(B,'V3')
    check('O10','V2 (N.º de PILA igual y pago en el mes) y V3 (IBC, salud, pensión, FSP, ARL) en OK para ambos', all(x[1]=='OK' for x in v2) and all(x[1]=='OK' for x in v3) and len(v3)>=10, [(x[2],x[1]) for x in v2+v3 if x[1]!='OK'])
    c4 = est(A,'C4')+est(B,'C4')
    check('O11','Nombre del archivo (8_GF_16797358_5126_OCT_2026.pdf, 2_GF_1130637605_5526_OCT_2026.pdf) coincide con cédula, compromiso, mes y año de la planilla', len(c4)==8 and all(x[1]=='OK' for x in c4), [(x[2],x[1]) for x in c4])
    c7 = est(A,'C7')
    check('O12','Comprobante con celdas desfasadas ~4 pt: los 6 tramos suman el total (C7 OK en ambas comisiones)', len(c7)==2 and all(x[1]=='OK' for x in c7), c7)
    c8 = [x for x in est(A,'C8') if x[1]=='ADVERTENCIA']
    check('O13','Comprobante con «Yumbo - septiembre 23 y 24 2026»: C8 advierte mostrando el texto (no «vacío»)', len(c8)==1 and 'septiembre 23 y 24 2026' in c8[0][3] and 'vacío' not in c8[0][3], c8)
    check('O14','Firmas de la planilla: contratista y supervisor FIRMADA; ordenador (sin espacio de firma, no obligatoria) SIN FIRMA',
          pg.evaluate("async () => { const out=[]; for (const k of ['16797358|2026-10','1130637605|2026-10']) { const r = await VC.app_ui.S.app.store.getRegistro(k); const F=r.paquete.planilla.firmas; out.push(F.contratista.estado+'/'+F.supervisor.estado+'/'+F.ordenador.estado); } return out.join(); }")=='FIRMADA/FIRMADA/SIN FIRMA,FIRMADA/FIRMADA/SIN FIRMA')
    v7 = est(A,'V7')+est(B,'V7')
    check('O15','V7 sin ERROR (todas las firmas exigidas presentes)', all(x[1]!='ERROR' for x in v7), [x for x in v7 if x[1]=='ERROR'])
    # interfaz
    pg.fill('#f-texto','33946-758134'); check('O16','Búsqueda por ID de Proceso (33946-758134) encuentra a 1130637605', filas(pg)==1 and '1130637605' in pg.inner_text('#tabla'))
    pg.click('#tabla tbody tr .nm button'); esperar(pg, "() => !!document.querySelector('#panel')", 10)
    for tab in ['resumen','planilla','pila','comisiones','validaciones','visual']:
        pg.click('#tab-'+tab); time.sleep(0.4)
    pg.click('#tab-planilla'); tp = pg.inner_text('#panel')
    check('O17','Pestaña Planilla SI: muestra N.º de planilla PILA 6035492712 y fondo de solidaridad', '6035492712' in tp and 'solidaridad' in tp.lower(), tp[:300])
    pg.click('button:has-text("Volver al listado")'); pg.fill('#f-texto','')
    # CSV
    pg.click('.menu > button:has-text("Exportar")')
    with pg.expect_download() as d: pg.click('button[role=menuitem]:has-text("CSV de resumen")')
    f = DL+'resumen_octubre.csv'; d.value.save_as(f)
    lines = open(f,encoding='utf-8-sig',newline='').read().strip().split('\r\n')
    ids = {l.split(';')[0]: l.split(';')[-1] for l in lines[1:]}
    check('O18','CSV de resumen: 2 filas con su «ID de Proceso»', len(lines)==3 and ids=={'16797358':'20246-827984','1130637605':'33946-758134'}, ids)
    # PDF mixto: formato nuevo + formato anterior en el mismo archivo
    mix = C+'_mixto_oct_sep.pdf'
    if os.path.exists(C+'c1_66825336.pdf') and os.path.exists(C+'c3_16797358.pdf'):
        from pypdf import PdfWriter
        w = PdfWriter()
        for f_ in ('o2_1130637605.pdf','c1_66825336.pdf','o1_16797358.pdf'): w.append(C+f_)
        w.write(mix)
        pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); }"); pg.reload(); esperar(pg, '() => !!(window.VC && window.VC.listo === true)', 20)
        pg.set_input_files('#file-pdf', [mix])
        esperar(pg, LISTO, 120)
        keys = pg.evaluate("async () => (await VC.app_ui.S.app.store.allRegistros()).map(r=>r.clave).sort().join()")
        check('O19','PDF mixto (octubre nuevo + septiembre anterior + octubre nuevo): 3 contratistas detectados', keys=='1130637605|2026-10,16797358|2026-10,66825336|2026-09', keys)
        A2 = reg(pg,'16797358|2026-10'); S1 = reg(pg,'66825336|2026-09')
        check('O20','En el PDF mixto, el formato nuevo y el anterior dan lo mismo que por separado (N.º de PILA, estado, comisiones)', v(A2['P'],'pilaNro')=='95603627' and A2['estado']==A['estado'] and A2['ncom']==2 and v(S1['P'],'pilaNro')=='94271132' and S1['estado']=='VÁLIDO CON ADVERTENCIAS', (v(A2['P'],'pilaNro'), A2['estado'], S1['estado'], v(S1['P'],'pilaNro')))
        os.remove(mix)
    errs=[l for l in logs if l.startswith(('error','PAGEERROR'))]
    check('O21','Sin errores en la consola', not errs, errs[:3])
    ext=[u for u in reqs if not u.startswith(('file://','data:','blob:'))]
    check('O22','Sin solicitudes de red externas', not ext, ext)
    b.close()
print('TOTAL', len(RES), 'PASS', sum(r['ok'] for r in RES), 'FAIL', sum(not r['ok'] for r in RES))
