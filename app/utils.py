from openpyxl import Workbook
from fastapi.responses import StreamingResponse
import io

def export_to_excel(items):
    wb = Workbook()
    ws = wb.active
    ws.append(["ID", "Name", "Description"])
    for item in items:
        ws.append([item.id, item.name, item.description])
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=items.xlsx"})