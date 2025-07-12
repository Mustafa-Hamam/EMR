from typing import List
from fastapi import FastAPI
from fastapi import UploadFile, File, Form, Request,HTTPException, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os, re
import uvicorn
from EMR_core.insertion import auth_snflk, add_patient, add_Doctor, add_Receptionist, add_HR, add_Case
from EMR_core.visits import add_visit, add_booking
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
async def new_hr_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newhr.html", {"request": request})

@app.get("/newvisit", response_class=HTMLResponse)
async def new_visit_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newvisit.html", {"request": request})

@app.get("/newbooking", response_class=HTMLResponse)
async def new_booking_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newbooking.html", {"request": request})

@app.get("/newcase", response_class=HTMLResponse)
async def new_case_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("newcase.html", {"request": request})

@app.get("/upload_case_file", response_class=HTMLResponse)
async def new_case_file_form(request: Request):
    # Serve the form template
    return templates.TemplateResponse("casefiles.html", {"request": request})

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
        if isinstance(result, str) and result.lower().startswith("error"):
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
        if isinstance(result, str) and result.lower().startswith("error"):
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
        if isinstance(result, str) and result.lower().startswith("error"):
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
        if isinstance(result, str) and result.lower().startswith("error"):
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
@app.post("/newbooking", response_class=HTMLResponse)
async def submit_booking(
    request: Request,
    patient_phone: int = Form(...),
    patient_name: str = Form(...),
    national_id: int = Form(...),
    doctor_id: int = Form(...),
    doctor_name: str = Form(...),
    receptionist_id: int = Form(...),
    type: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    status: str = Form(...)
):
    conn = auth_snflk()
    try:
        booking_id = add_booking(
            conn, patient_phone, patient_name, national_id, doctor_id, doctor_name,
            receptionist_id, type, date, time, status
        )

        if isinstance(booking_id, str) and booking_id.lower().startswith("error"):
            raise HTTPException(status_code=500, detail=booking_id)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        conn.close()

    return templates.TemplateResponse(
        "confirmation.html",
        {"request": request, "message": f"✅ Booking recorded successfully with ID {booking_id}"}
    )
@app.post("/newcase", response_class=HTMLResponse)
async def submit_case(
    request: Request,
    patient_phone: int = Form(...),
    start_date: str = Form(...),
    case_type: str = Form(...),
    history: str = Form(...),
    chronic_diseases: str = Form(...),
    pain_scale: str = Form(...),
    signs_symptoms: str = Form(...),
    chief_complaint: str = Form(...),
    medications: str = Form(...),
    investigations: str = Form(...),
    special_tests: str = Form(...),
    diagnosis: str = Form(...),
    referred_diagnosis: str = Form(...),
    treatment_plan: str = Form(...),
    notes: str = Form(...),
    end_date: str = Form(...),
    end_note: str = Form(...)
):
    conn = auth_snflk()
    try:
        result = add_Case(
            conn, patient_phone, start_date, case_type, history, chronic_diseases, 
            pain_scale, signs_symptoms, chief_complaint, medications, investigations,
            special_tests, diagnosis, referred_diagnosis, treatment_plan, notes,
            end_date, end_note
        )
        # Check for error indication
        if isinstance(result, str) and result.lower().startswith("error"):
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
        {"request": request, "message": f"✅ Added new case with ID {result}"}
    )

@app.post("/upload_case_file", response_class=HTMLResponse)
async def upload_case_file(
    request: Request,
    phone: int = Form(...),
    files: List[UploadFile] = File(...)
):
    conn = auth_snflk()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT CASE_ID
            FROM CLINIC_A.PUBLIC.PATIENT P
            JOIN CLINIC_A.PUBLIC.CASES C ON P.ID = C.PATIENT_ID
            WHERE P.PHONE = %s
            ORDER BY C.START_DATE DESC
            LIMIT 1
        """, (phone,))
        result = cursor.fetchone()

        if not result:
            return HTMLResponse("<h3>❌ No case found for this patient phone number.</h3>")

        case_id = result[0]

        os.makedirs("/tmp/case_files", exist_ok=True)
        uploaded = []

        for file in files:
            file_bytes = await file.read()
            safe_filename = re.sub(r"[()\s]", "_", file.filename)
            filename = f"case_{case_id}__{safe_filename}"
            temp_path = f"/tmp/case_files/{filename}"

            with open(temp_path, "wb") as f:
                f.write(file_bytes)
            put_command = f"PUT file://{temp_path} @CLINIC_A.PUBLIC.CASE_FILES_STAGE auto_compress=true"
            cursor.execute(put_command)
            uploaded.append(safe_filename)

            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return HTMLResponse(f"<h3>✅ Uploaded files: {', '.join(uploaded)}</h3>")

    except Exception as e:
        return HTMLResponse(f"<h3>❌ Error uploading files: {e}</h3>")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/patient_by_phone")
async def get_patient_by_phone(phone: int):
    conn = auth_snflk()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT NAME, NATIONAL_ID, ID 
            FROM CLINIC_A.PUBLIC.PATIENT 
            WHERE PHONE = %s
        """, (phone,))
        result = cursor.fetchone()

        if result:
            return {
                "name": result[0],
                "national_id": result[1],
                "id": result[2]  #Return the ID
            }
        else:
            return {
                "name": "",
                "national_id": "",
                "id": ""
            }
    except Exception as e:
        return {
            "name": "",
            "national_id": "",
            "id": ""
        }
    finally:
        conn.close()
@app.get("/api/doctors")
async def get_doctors():
    conn = auth_snflk()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME FROM CLINIC_A.PUBLIC.DOCTOR")
        rows = cursor.fetchall()
        doctors = [{"id": row[0], "name": row[1]} for row in rows]
        return doctors
    except Exception as e:
        return []
    finally:
        conn.close()        

# if __name__ == "__main__":
#     uvicorn.run(app, port=10000, host="0.0.0.0")
