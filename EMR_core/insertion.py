import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os


def auth_snflk():
    key_pem = os.environ["SNOWFLAKE_PRIVATE_KEY"].encode() 
    private_key = serialization.load_pem_private_key(
        key_pem, password=None, backend=default_backend()
    )
    private_key_pkcs8 = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    conn = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        private_key=private_key_pkcs8,
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ["SNOWFLAKE_ROLE"],
    )
    return conn

def add_patient(conn, name, age, gender, occupation, marital_status, address,
                email, phone, national_id, insurance, insurance_card_id,
                diagnosis, chief_complaint, medications, investigations,first_visit):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.PATIENT (
            NAME, AGE, GENDER, OCCUPATION, MARITAL_STATUS, ADDRESS,
            EMAIL, PHONE, NATIONAL_ID, INSURANCE, INSURANCE_CARD_ID,
            DIAGNOSIS, CHIEF_COMPLAINT, MEDICATIONS, INVESTIGATIONS,FIRST_VISIT
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(
            sql,
            (
                name, age, gender, occupation, marital_status, address,
                email, phone, national_id, insurance, insurance_card_id,
                diagnosis, chief_complaint, medications, investigations, first_visit
            )
        )
        cursor.execute(
        "SELECT ID FROM CLINIC_A.PUBLIC.PATIENT WHERE NATIONAL_ID = %s",
        (national_id,)
                        )
        patient_id = cursor.fetchone()[0]
        print("✅ Patient added successfully!")
        return patient_id
    except Exception as e:
        print(f"❌ Error adding patient: {e}")
        return f"Error adding patient: {e}"
    finally:
        cursor.close()
        conn.close()

def add_Doctor(conn, name, age, gender, email, address, Phone,
                national_id, degree, specialty, certifications, salary,
                leaves, schedule):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.DOCTOR (
            Name, Age, Gender, Email, Address, Phone,
            National_id, Degree, Specialty, Certifications, Salary,
            Leaves, Schedule
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                name, age, gender, email, address, Phone,
                national_id, degree, specialty, certifications, salary,
                leaves, schedule
            )
        )
        cursor.execute("SELECT ID FROM CLINIC_A.PUBLIC.DOCTOR WHERE NATIONAL_ID = %s",
        (national_id,)
                        )
        doctor_id = cursor.fetchone()[0]
        print("✅ Doctor added successfully!")
        return doctor_id
    except Exception as e:
        print(f"❌ Error adding Doctor: {e}")
        return f"Error adding Doctor: {e}"
    finally:
        cursor.close()
        conn.close()

def add_Receptionist(conn, name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.RECEPTIONIST (
            Name, Age, Gender, Phone, Email, Address,
            National_ID, Education, Leaves, Salary
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary
            )
        )
        cursor.execute("SELECT ID FROM CLINIC_A.PUBLIC.RECEPTIONIST WHERE NATIONAL_ID = %s",
        (national_id,)
                        )
        receptionist_id = cursor.fetchone()[0]
        print("✅ Receptionist added successfully!")
        return receptionist_id
    except Exception as e:
        print(f"❌ Error adding Receptionist: {e}")
        return f"Error adding Receptionist: {e}"
    finally:
        cursor.close()
        conn.close()
def add_HR(conn, name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.HR (
            Name, Age, Gender, Phone, Email, Address,
            National_ID, Education, Leaves, Salary
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary
            )
        )
        cursor.execute("SELECT ID FROM CLINIC_A.PUBLIC.HR WHERE NATIONAL_ID = %s",
        (national_id,)
                        )
        hr_id = cursor.fetchone()[0]
        print("✅ HR Member added successfully!")
        return hr_id
    except Exception as e:
        print(f"❌ Error adding HR Member: {e}")
        return f"Error adding HR Member: {e}"
    finally:
        cursor.close()
        conn.close()

def add_Case(conn, patient_phone, start_date, case_type, history, chronic_diseases, pain_scale, 
                signs_symptoms, chief_complaint, medications, investigations, special_tests,
                diagnosis, referred_diagnosis, treatment_plan, notes, end_date, end_note):
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM CLINIC_A.PUBLIC.PATIENT WHERE PHONE = %s", (patient_phone,))
    result = cursor.fetchone()
    patient_id = result[0]
    
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.CASES (
            PATIENT_ID, START_DATE,
            CASE_TYPE, HISTORY, CHRONIC_DISEASES, PAIN_SCALE,
            SIGNS_SYMPTOMS, CHIEF_COMPLAINT, MEDICATIONS, INVESTIGATIONS,
            SPECIAL_TESTS, DIAGNOSIS, REFERRED_DIAGNOSIS, TREATMENT_PLAN, NOTES ,
            END_DATE , END_NOTE 
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(
            sql,
            (
                patient_id, start_date, case_type, history, chronic_diseases, pain_scale, 
                signs_symptoms, chief_complaint, medications, investigations, special_tests,
                diagnosis, referred_diagnosis, treatment_plan, notes, end_date, end_note
            )
        )
        cursor.execute("SELECT CASE_ID FROM CLINIC_A.PUBLIC.CASES WHERE PATINET_ID = %s",
        (patient_id,)
                        )
        case_id = cursor.fetchone()[0]
        print("✅ Case {case_id} added successfully!")
        return case_id
    except Exception as e:
        print(f"❌ Error adding Case: {e}")
        return f"Error adding Case: {e}"
    finally:
        cursor.close()
        conn.close()        


