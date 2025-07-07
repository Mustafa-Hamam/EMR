from typing import List
from fastapi import FastAPI
from fastapi import Request, Form,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from EMR_core.insertion import auth_snflk, add_patient, add_Doctor, add_Receptionist, add_HR
from EMR_core.visits import add_visit
app = FastAPI()
templates = Jinja2Templates(directory="EMR_core/templates")


@app.get("/",response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/newpatient", response_class=HTMLResponse)
async def new_patient_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newpatient.html", {"request": request})

@app.get("/newdoctor", response_class=HTMLResponse)
async def new_doctor_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newdoctor.html", {"request": request})

@app.get("/newreceptionist", response_class=HTMLResponse)
async def new_receptionist_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newreceptionist.html", {"request": request})

@app.get("/newhr", response_class=HTMLResponse)
async def new_receptionist_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newhr.html", {"request": request})

@app.get("/newvisit", response_class=HTMLResponse)
async def new_receptionist_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newvisit.html", {"request": request})

@app.post("/newpatient", response_class=HTMLResponse)
async def submit_patient(
    request: Request,
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
    investigations: str = Form(...),
    first_visit: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_patient(
            conn, name, age, gender, occupation, marital_status, address,
            email, phone, national_id, insurance, insurance_card_id,
            diagnosis, chief_complaint, medications, investigations,first_visit
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
        {"request": request, "message": f"✅ Added new patient {name} with ID {result}"}
    )

@app.post("/newdoctor", response_class=HTMLResponse)
async def submit_doctor(
    request: Request,
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
    schedule: List[str] = Form(...)
):
    conn = auth_snflk()
    try:
        schedule_str = ", ".join(schedule)
        result = add_Doctor(
            conn, name, age, gender, email, address, 
            Phone, national_id, degree, specialty, certifications,
            salary, leaves, schedule_str
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
        {"request": request, "message": f"✅ Added new doctor {name} with ID {result}"}
    )

@app.post("/newreceptionist", response_class=HTMLResponse)
async def submit_receptionist(
    request: Request,
    name: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    Phone: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),   
    national_id: str = Form(...),
    education: str = Form(...),
    leaves: str = Form(...),
    salary: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_Receptionist(
            conn, name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary
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
        {"request": request, "message": f"✅ Added new receptionist {name} with ID {result}"}
    )

@app.post("/newhr", response_class=HTMLResponse)
async def submit_receptionist(
    request: Request,
    name: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    Phone: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),   
    national_id: str = Form(...),
    education: str = Form(...),
    leaves: str = Form(...),
    salary: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_HR(
            conn, name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary)
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
        {"request": request, "message": f"✅ Added new HR {name} with ID {result}"}
    )
@app.post("/newvisit", response_class=HTMLResponse)
async def submit_visit(
    request: Request,
    Doctor_ID: str = Form(...),
    Doctor_Name: str = Form(...),
    Patient_ID: str = Form(...),
    Patient_name: str = Form(...),
    Type: str = Form(...),
    Date: str = Form(...),
    Time: str = Form(...),
    Notes: str = Form(...),
    Prescription: str = Form(...),
    Status: str = Form(...),
    Payment: str = Form(...)
):
    conn = auth_snflk()
    try:
        visit_id = add_visit(
            conn, Doctor_ID, Doctor_Name, Patient_ID, Patient_name, Type, Date,
            Time, Notes, Prescription, Status, Payment
        )

        # Check for error indication
        if isinstance(visit_id, str) and visit_id.lower().startswith("error"):
            raise HTTPException(status_code=500, detail=visit_id)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        conn.close()

    return templates.TemplateResponse(
        "confirmation.html",
        {
            "request": request,
            "message": f"✅ Visit recorded successfully with ID: {visit_id}"
        }
    )

# if __name__ == "__main__":
#     uvicorn.run(app, port=10000, host="0.0.0.0")
