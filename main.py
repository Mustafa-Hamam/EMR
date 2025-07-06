from fastapi import FastAPI
from fastapi import Request, Form,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from EMR_core.insertion import auth_snflk, add_patient, add_Doctor

app = FastAPI()
templates = Jinja2Templates(directory="EMR_core/templates")


@app.get("/",response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/newpatient", response_class=HTMLResponse)
async def new_patient_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newpatient.html", {"request": request})

@app.post("/newpatient", response_class=HTMLResponse)
async def submit_patient(
    request: Request,
    patient_id: str = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    occupation: str = Form(...),
    marital_status: str = Form(...),
    address: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    national_id: str = Form(...),
    insurance: str = Form(...),
    insurance_card_id: str = Form(...),
    diagnosis: str = Form(...),
    chief_complaint: str = Form(...),
    medications: str = Form(...),
    investigations: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_patient(
            conn, patient_id, name, age, gender, occupation, marital_status, address,
            email, phone, national_id, insurance, insurance_card_id,
            diagnosis, chief_complaint, medications, investigations
        )

        # Check for error indication
        if result.lower().startswith("error"):
            raise HTTPException(status_code=500, detail=result)

    except HTTPException as e:
        # Let FastAPI handle raised HTTPExceptions properly
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        conn.close()

    # Only show success if no error occurred
    return templates.TemplateResponse(
        "confirmation.html",
        {"request": request, "message": f"✅ Added new patient {name} with ID {patient_id}"}
    )

@app.post("/newdoctor", response_class=HTMLResponse)
async def submit_doctor(
    request: Request,
    doctor_id: str = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    Phone: str = Form(...),
    national_id: str = Form(...),
    degree: str = Form(...),
    specialty: str = Form(...),
    certifications: str = Form(...),
    salary: str = Form(...),
    leaves: str = Form(...),
    schedule: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_Doctor(
            conn, doctor_id, name, age, gender, email, address, 
            Phone, national_id, degree, specialty, certifications,
            salary, leaves, schedule
        )

        # Check for error indication
        if result.lower().startswith("error"):
            raise HTTPException(status_code=500, detail=result)

    except HTTPException as e:
        # Let FastAPI handle raised HTTPExceptions properly
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        conn.close()

    # Only show success if no error occurred
    return templates.TemplateResponse(
        "confirmation.html",
        {"request": request, "message": f"✅ Added new doctor {name} with ID {doctor_id}"}
    )

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
