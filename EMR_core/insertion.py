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

def add_patient(conn, patient_id, name, age, gender, occupation, marital_status, address,
                email, phone, national_id, insurance, insurance_card_id,
                diagnosis, chief_complaint, medications, investigations,first_visit):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.PATIENT (
            ID, NAME, AGE, GENDER, OCCUPATION, MARITAL_STATUS, ADDRESS,
            EMAIL, PHONE, NATIONAL_ID, INSURANCE, INSURANCE_CARD_ID,
            DIAGNOSIS, CHIEF_COMPLAINT, MEDICATIONS, INVESTIGATIONS,FIRST_VISIT
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(
            sql,
            (
                patient_id, name, age, gender, occupation, marital_status, address,
                email, phone, national_id, insurance, insurance_card_id,
                diagnosis, chief_complaint, medications, investigations, first_visit
            )
        )
        print("✅ Patient added successfully!")
        return "Patient added successfully!"
    except Exception as e:
        print(f"❌ Error adding patient: {e}")
        return f"Error adding patient: {e}"
    finally:
        cursor.close()
        conn.close()

def add_Doctor(conn, doctor_id, name, age, gender, email, address, Phone,
                national_id, degree, specialty, certifications, salary,
                leaves, schedule):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.DOCTOR (
            ID, Name, Age, Gender, Email, Address, Phone,
            National_id, Degree, Specialty, Certifications, Salary,
            Leaves, Schedule
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                doctor_id, name, age, gender, email, address, Phone,
                national_id, degree, specialty, certifications, salary,
                leaves, schedule
            )
        )
        print("✅ Doctor added successfully!")
        return "Doctor added successfully!"
    except Exception as e:
        print(f"❌ Error adding Doctor: {e}")
        return f"Error adding Doctor: {e}"
    finally:
        cursor.close()
        conn.close()

def add_Receptionist(conn, receptionist_id, name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.RECEPTIONIST (
            ID, Name, Age, Gender, Phone, Email, Address,
            National_ID, Education, Leaves, Salary
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                receptionist_id, name, age, gender, Phone, email, address, 
                national_id, education, leaves, salary
            )
        )
        print("✅ Receptionist added successfully!")
        return "Receptionist added successfully!"
    except Exception as e:
        print(f"❌ Error adding Receptionist: {e}")
        return f"Error adding Receptionist: {e}"
    finally:
        cursor.close()
        conn.close()

