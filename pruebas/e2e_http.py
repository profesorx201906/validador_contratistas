# Mismo flujo básico servido por http://localhost (como iniciar.bat): pdf.js usa un Web Worker real
import subprocess, time, json
from helpers import *
srv = subprocess.Popen(['python3','-m','http.server','8765','--bind','127.0.0.1'], cwd=APP_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b, ctx, pg, logs, reqs = abrir(p, url='http://127.0.0.1:8765/index.html')
        pg.evaluate("async () => { await VC.app_ui.S.app.store.clearAll(); }")
        print('modo pdf.js:', pg.evaluate("() => VC.proc.initPdfjs()"))
        pg.set_input_files('#file-pdf', PDF)
        esperar(pg, "() => { const q=document.querySelector('.q-item'); return q && q.dataset.estado==='listo'; }", 120)
        r = pg.evaluate("async () => (await VC.app_ui.S.app.store.allRegistros()).map(r => [r.clave, r.validacion.global, r.validacion.resumen.errores])")
        print('registro:', r)
        pg.click('#btn-pruebas'); esperar(pg, "() => /PASS/.test((document.querySelector('#tests-sum')||{}).textContent||'')", 90)
        print(pg.inner_text('#tests-sum'))
        print('workers/consola:', [l for l in logs if l.startswith(('error','PAGEERROR','warning'))][:5])
        print('requests no locales:', [u for u in reqs if not u.startswith(('http://127.0.0.1','data:','blob:'))])
        b.close()
finally:
    srv.terminate()
