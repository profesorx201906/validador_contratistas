import io, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from reportlab.pdfgen import canvas
from helpers import PDF as SRC, PD as OUT
import os; os.makedirs(OUT, exist_ok=True)
r = PdfReader(SRC)
print('páginas', len(r.pages), [ (float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height)) ])

def guardar(nombre, paginas, mod=None):
    w = PdfWriter()
    for i in paginas:
        w.add_page(r.pages[i])
    if mod: mod(w)
    with open(OUT+nombre,'wb') as f: w.write(f)
    print('creado', nombre, len(w.pages), 'págs')

# 1) Sin comisiones: solo planilla + PILA (págs 1-3)  -> misma cédula/mes; planilla declara comisiones
guardar('sin_comisiones.pdf', [0,1,2])
# 2) Sin planilla: solo PILA + comisiones (págs 2..29) -> NO IDENTIFICADO
guardar('sin_planilla.pdf', list(range(1,29)))
# 3) Faltan el comprobante y radicado de la comisión 78826 (págs 28,29 eliminadas)
guardar('sin_comprobante_78826.pdf', list(range(0,27)))
# 4) Imagen sola (sin texto): rasterizar con pdftoppm luego a PDF de imágenes
# 5) Sin firmas en informe 18/08 (pág 9): quitar imágenes de esa página
def quitar_imagenes(pg):
    from pypdf.generic import ContentStream
    cs = ContentStream(pg.get_contents(), pg.pdf)
    xo = pg['/Resources'].get('/XObject', {})
    nombres = {k for k,v in xo.items() if v.get_object().get('/Subtype') == '/Image'}
    ops = [(o,op) for (o,op) in cs.operations if not (op == b'Do' and o and o[0] in nombres)]
    n_quit = len(cs.operations) - len(ops)
    cs.operations = ops
    pg[NameObject('/Contents')] = cs
    print('  imágenes removidas de la página:', n_quit)
def mod_sin_firmas(w):
    quitar_imagenes(w.pages[8])
guardar('sin_firmas_informe_18_08.pdf', list(range(29)), mod_sin_firmas)
# 6) Firma vectorial añadida en el ordenador de la planilla (pág 1): garabato con curvas
H = float(r.pages[0].mediabox.height); W = float(r.pages[0].mediabox.width)
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W,H))
c.setStrokeColorRGB(0.05,0.1,0.5); c.setLineWidth(1.6)
yb = H - 912   # zona del ordenador (ROI ~ y 888-922 desde arriba)
p = c.beginPath(); p.moveTo(250, yb); p.curveTo(270, yb+25, 290, yb-20, 310, yb+18); p.curveTo(325, yb+30, 345, yb-12, 375, yb+8); c.drawPath(p, stroke=1, fill=0)
c.save(); buf.seek(0)
ov = PdfReader(buf).pages[0]
def mod_vector(w):
    w.pages[0].merge_page(ov)
guardar('firma_dudosa_ordenador.pdf', list(range(29)), mod_vector)
# 6b) Firma vectorial realista (muchas curvas), sobre el espacio del ordenador
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W,H))
c.setStrokeColorRGB(0.05,0.1,0.5); c.setLineWidth(1.6)
p = c.beginPath(); x = 232; p.moveTo(x, yb)
import math
for k in range(10):
    p.curveTo(x+6, yb+22*(1 if k%2==0 else -1), x+14, yb+18*(-1 if k%2==0 else 1), x+17, yb+4*(1 if k%2==0 else -1)); x += 17
c.drawPath(p, stroke=1, fill=0); c.save(); buf.seek(0)
ov2 = PdfReader(buf).pages[0]
def mod_vector2(w):
    w.pages[0].merge_page(ov2)
guardar('firma_vectorial_ordenador.pdf', list(range(29)), mod_vector2)
# 7) PDF cualquiera (no corresponde al formato)
buf = io.BytesIO(); c = canvas.Canvas(buf); c.drawString(72,720,'Factura de venta 123 - documento que no corresponde al formato'); c.drawString(72,700,'Total: $ 1.000.000'); c.save()
open(OUT+'otro_documento.pdf','wb').write(buf.getvalue()); print('creado otro_documento.pdf')
# 8) archivo no PDF y PDF dañado
open(OUT+'no_es_pdf.pdf','wb').write(b'Esto es un texto plano con extension pdf')
data = open(SRC,'rb').read()
open(OUT+'dañado.pdf','wb').write(data[:200000])
print('creado dañado.pdf (truncado)')
# 9) PDF sin capa de texto (solo imágenes, como un escaneo): páginas 1-2 de la muestra convertidas a imagen (requiere poppler-utils y Pillow)
try:
    import subprocess, tempfile, glob
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm', '-jpeg', '-r', '72', '-f', '1', '-l', '2', SRC, td + '/p'], check=True)
        imgs = [Image.open(f).convert('RGB') for f in sorted(glob.glob(td + '/p*.jpg'))]
        imgs[0].save(OUT + 'solo_imagen.pdf', save_all=True, append_images=imgs[1:])
    print('creado solo_imagen.pdf (%d págs, sin texto)' % len(imgs))
except Exception as e:
    print('NO se creó solo_imagen.pdf (necesita pdftoppm y Pillow):', e)
