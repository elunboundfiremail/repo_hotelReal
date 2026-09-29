from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_admin_report(reservas):
    pdf_path = "/tmp/reporte_admin.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Hotel Real - Reporte Gerencial de Reservas")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Fecha de emision: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    y = 750
    total_ingresos = 0
    c.drawString(50, y, "ID | Cliente | Habitacion | Check-in | Check-out | Estado")
    c.line(50, y-5, 550, y-5)
    y -= 20
    
    for r in reservas:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 800
        
        texto = f"#{r['id']} | {r['nombre']} {r['apellido_paterno']} | Hab {r['numero']} ({r['tipo']}) | {r['fecha_entrada']} | {r['fecha_salida']} | {r['estado_pago'].upper()}"
        c.drawString(50, y, texto)
        if r['estado_pago'] == 'pagado':
            total_ingresos += r.get('precio_bs', 0)
        y -= 20
        
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y-20, f"Total Ingresos Confirmados: {total_ingresos} Bs.")
    
    c.save()
    return pdf_path
