from typing import List
from fastapi import FastAPI
from fastapi import Request, Form,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from EMR_core.insertion import auth_snflk, add_patient, add_Doctor, add_Receptionist, add_HR

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
    investigations: str = Form(...),
    first_visit: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_patient(
            conn, patient_id, name, age, gender, occupation, marital_status, address,
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
    schedule: List[str] = Form(...)
):
    conn = auth_snflk()
    try:
        schedule_str = ", ".join(schedule)
        result = add_Doctor(
            conn, doctor_id, name, age, gender, email, address, 
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
        {"request": request, "message": f"✅ Added new doctor {name} with ID {doctor_id}"}
    )

@app.post("/newreceptionist", response_class=HTMLResponse)
async def submit_receptionist(
    request: Request,
    receptionist_id: str = Form(...),
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
            conn, receptionist_id, name, age, gender, Phone, email, address, 
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
        {"request": request, "message": f"✅ Added new receptionist {name} with ID {receptionist_id}"}
    )

@app.post("/newhr", response_class=HTMLResponse)
async def submit_receptionist(
    request: Request,
    hr_id: str = Form(...),
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
            conn, hr_id, name, age, gender, Phone, email, address, 
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
        {"request": request, "message": f"✅ Added new HR {name} with ID {hr_id}"}
    )


# if __name__ == "__main__":
#     uvicorn.run(app, port=10000, host="0.0.0.0")
