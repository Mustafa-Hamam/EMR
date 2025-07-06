import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def auth_snflk():
    key_path = r"M:\snflk_rsa\mustafa_rsa.pem"
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )
    private_key_pkcs8 = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    conn = snowflake.connector.connect(
        user="MUSTAFAHAMAM12",
        private_key=private_key_pkcs8,
        account="YEPMQGJ-OQ89670",
        warehouse="COMPUTE_WH",
        role="ACCOUNTADMIN",
    )
    return conn

def add_patient(conn, patient_id, name, age, gender, occupation, marital_status, address,
                email, phone, national_id, insurance, insurance_card_id,
                diagnosis, chief_complaint, medications, investigations):
    cursor = conn.cursor()
    try:
        sql = f"""
        CALL CLINIC_A.PUBLIC.ADD_NEW_PATIENT(
            '{patient_id}', '{name}', {age}, '{gender}', '{occupation}', '{marital_status}', '{address}',
            '{email}', '{phone}', '{national_id}', '{insurance}', '{insurance_card_id}',
            '{diagnosis}', '{chief_complaint}', '{medications}', '{investigations}'
        )
        """
        cursor.execute(sql)
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
        sql = f"""
        CALL CLINIC_A.PUBLIC.ADD_NEW_DOCTOR(
            '{doctor_id}', '{name}', {age}, '{gender}', '{email}', '{address}', '{Phone}',
            '{national_id}', '{degree}', '{specialty}', '{certifications}', '{salary}',
            '{leaves}', '{schedule}'
        )
        """
        cursor.execute(sql)
        print("✅ Doctor added successfully!")
        return "Doctor added successfully!"
    except Exception as e:
        print(f"❌ Error adding Doctor: {e}")
        return f"Error adding Doctor: {e}"
    finally:
        cursor.close()
        conn.close()

