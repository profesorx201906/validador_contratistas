#!/usr/bin/env python3
"""Regresión de lectura sobre PDF reales (golden master).

Uso:
  python3 regresion.py CARPETA_CON_PDF            # compara contra gold/
  python3 regresion.py CARPETA_CON_PDF --actualizar   # guarda la lectura actual como nueva referencia

Procesa cada PDF con el motor REAL de dist/index.html (Chromium + Playwright), reduce el resultado a una tabla plana
(campo → valor) y la compara con gold/<archivo>.json. Cualquier diferencia se imprime: así se detecta de inmediato
si un cambio de código rompe la lectura de un formato que antes funcionaba.
La referencia gold/ fue revisada a mano contra las páginas (ver AUDITORIA.md); NO es un oráculo independiente.
"""
import sys, os, json, glob, base64
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
# La aplicación: ../index.html (carpeta de entrega) o ../dist/index.html (árbol de desarrollo); VC_INDEX la fuerza.
_c = [os.path.join(AQUI, '..', 'index.html'), os.path.join(AQUI, '..', 'dist', 'index.html')]
URL = 'file://' + os.path.abspath(os.environ.get('VC_INDEX') or next((x for x in _c if os.path.exists(x)), _c[0]))
GOLD = os.path.join(AQUI, 'gold')

JS = """async (b64) => {
  const bin = atob(b64); const u8 = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
  const cfg = VC.extract.cloneCfg(VC.extract.DEFAULT_CFG);
  const res = await VC.proc.procesarPdf(u8.buffer, 'x.pdf', cfg, null);
  const out = { nPaginas: res.nPaginas, paquetes: [] };
  for (const pk of res.paquetes) {
    delete pk.pilas;
    for (const f of VC.extract.listFirmas(pk)) VC.extract.resolveFirma(f.ref, cfg);
    const val = VC.validate.validate(pk, cfg, { fileName: 'x.pdf' });
    out.paquetes.push({ pk, val });
  }
  return JSON.parse(JSON.stringify(out));
}"""

def fv(f):
    if isinstance(f, dict) and 'tipo' in f:
        v = f.get('v')
        if isinstance(v, dict) and 'y' in v: return '%04d-%02d-%s' % (v['y'], v['m'], '??' if not v.get('d') else '%02d' % v['d'])
        return v
    return f

def plano(res):
    """Reduce el resultado a {clave_plana: valor}."""
    t = {'paginas': res['nPaginas'], 'paquetes': len(res['paquetes'])}
    for i, p in enumerate(res['paquetes'], 1):
        pk, val = p['pk'], p['val']
        pre = 'p%02d.' % i
        t[pre + 'paginas'] = [x['n'] for x in pk['paginas']][0:1] + [x['n'] for x in pk['paginas']][-1:]
        t[pre + 'noReconocidas'] = [x['n'] for x in pk['noReconocidas']]
        P, L = pk.get('planilla'), pk.get('pila')
        if P:
            for k, f in P.items():
                if isinstance(f, dict) and 'tipo' in f: t[pre + 'SI.' + k] = fv(f)
            for rol, f in P['firmas'].items(): t[pre + 'SI.firma.' + rol] = f['estado']
        if L:
            t[pre + 'PILA.formato'] = L['fam']
            for k, f in L.items():
                if isinstance(f, dict) and 'tipo' in f: t[pre + 'PILA.' + k] = fv(f)
        for g in pk['comisiones']:
            gp = pre + 'COM%s.' % g['clave']
            S = g.get('siif')
            if S:
                for k, f in S.items():
                    if isinstance(f, dict) and 'tipo' in f: t[gp + 'SIIF.' + k] = fv(f)
                t[gp + 'SIIF.tramos'] = [fv(x) for x in S['tramos']]
                t[gp + 'SIIF.dup'] = S['dup']
            for j, D in enumerate(g['informes']):
                for k, f in D.items():
                    if isinstance(f, dict) and 'tipo' in f: t[gp + 'INF%d.' % j + k] = fv(f)
                for rol, f in D['firmas'].items(): t[gp + 'INF%d.firma.' % j + rol] = f['estado']
            for j, E in enumerate(g['comprobantes']):
                for k, f in E.items():
                    if isinstance(f, dict) and 'tipo' in f: t[gp + 'COMP%d.' % j + k] = fv(f)
                t[gp + 'COMP%d.tramos' % j] = [[fv(x['fecha']), fv(x['trayecto']), fv(x['medio']), fv(x['valor'])] for x in E['tramos']]
                for rol, f in E['firmas'].items(): t[gp + 'COMP%d.firma.' % j + rol] = f['estado']
            for j, R in enumerate(g['radicados']):
                for k, f in R.items():
                    if isinstance(f, dict) and 'tipo' in f: t[gp + 'RAD%d.' % j + k] = fv(f)
        t[pre + 'estado'] = val['global']
        for it in val['items']:
            t[pre + 'val.' + it['id'] + '.' + it['regla'][:90]] = it['estado']
    return t

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    upd = '--actualizar' in sys.argv
    if not args:
        print(__doc__); sys.exit(2)
    pdfs = sorted(glob.glob(os.path.join(args[0], '*.pdf')))
    if not pdfs: print('No hay PDF en', args[0]); sys.exit(2)
    os.makedirs(GOLD, exist_ok=True)
    total_dif = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_context().new_page()
        pg.goto(URL); pg.wait_for_function('() => window.VC && window.VC.listo === true', timeout=30000)
        for f in pdfs:
            nombre = os.path.basename(f)
            r = pg.evaluate(JS, base64.b64encode(open(f, 'rb').read()).decode())
            t = plano(r)
            g = os.path.join(GOLD, nombre.replace('.pdf', '.json'))
            if upd or not os.path.exists(g):
                json.dump(t, open(g, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
                print('%-40s referencia %s (%d campos)' % (nombre, 'actualizada' if upd else 'creada', len(t))); continue
            ref = json.load(open(g, encoding='utf-8'))
            difs = [(k, ref.get(k, '<falta>'), t.get(k, '<falta>')) for k in sorted(set(ref) | set(t)) if ref.get(k, '<falta>') != t.get(k, '<falta>')]
            print('%-40s %s (%d campos)' % (nombre, 'IGUAL' if not difs else '%d DIFERENCIAS' % len(difs), len(t)))
            for k, a, c in difs[:60]: print('    ', k, '\n        antes:', a, '\n        ahora:', c)
            total_dif += len(difs)
        b.close()
    sys.exit(1 if total_dif else 0)
main()
