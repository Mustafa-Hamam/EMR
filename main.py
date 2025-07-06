from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from EMR_core.insertion import auth_snflk, add_patient

app = FastAPI()
templates = Jinja2Templates(directory="report_core/templates")


@app.get("/",response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/newpatient", response_class=HTMLResponse)
async def new_patient_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newpatient.html", {"request": request})

@app.post("/newpatient")
async def submit_new_patient(
    request: Request,
    id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    occupation: str = Form(...),
    marital_status: str = Form(...),
    address: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    national_id: str = Form(...),
    insurance: str = Form(...),
    insurance_card_id: str = Form(...),
    diagnosis: str = Form(""),
    chief_complaint: str = Form(""),
    medications: str = Form(""),
    investigations: str = Form("")
):
    conn = auth_snflk()
    cursor = conn.cursor()
    try:
        sql = """
        CALL add_new_patient(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            id, name, age, gender, occupation, marital_status, address, email, phone,
            national_id, insurance, insurance_card_id, diagnosis, chief_complaint,
            medications, investigations
        )
        cursor.execute(sql, params)
        message = f"✅ Added New Patient {name} with ID: {id}"
    except Exception as e:
        message = f"❌ Error adding patient: {e}"
    finally:
        cursor.close()
        conn.close()

    # Show result page
    return templates.TemplateResponse("newpatient.html", {"request": request, "message": message})

# @app.get("/newpatients",  response_class=HTMLResponse)
# async def patients_report(request: Request):
#     conn = auth_snflk()
#     report = new_patients(conn)
#     html_table = report.to_html(
#         classes="table table-striped table-bordered", index=False, escape=False
#     )
#     return templates.TemplateResponse("table.html", {
#         "request": request,
#         "title": "New Patients Report",
#         "heading": "New Patients Report",
#         "table": html_table})
# @app.get("/casesperclinic",  response_class=HTMLResponse)
# async def cases_report(request: Request):
#     conn = auth_snflk()
#     report = cases_clinic(conn)
#     html_table = report.to_html(
#         classes="table table-striped table-bordered", index=False, escape=False
#     )
#     return templates.TemplateResponse("table.html", {
#         "request": request,
#         "title": "Clinic_Cases_Report",
#         "heading": "Clinic Cases Report",
#         "table": html_table})
# @app.get("/monthlyperformance",  response_class=HTMLResponse)
# async def monthly_report(request: Request):
#     conn = auth_snflk()
#     report = monthly_performance(conn)
#     html_table = report.to_html(
#         classes="table table-striped table-bordered", index=False, escape=False
#     )
#     return templates.TemplateResponse("table.html", {
#         "request": request,
#         "title": "Monthly Performance Report",
#         "heading": "Monthly Performance Report",
#         "table": html_table})
if __name__ == "__main__":
    uvicorn.run(app, port=10000, host="0.0.0.0")
