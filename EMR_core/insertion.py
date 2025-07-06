import snowflake.connector
import pandas as pd
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

def add_patient(conn):
    conn = auth_snflk()
    cursor = conn.cursor()
    try:
        # Prompt for all required fields
        id = input("ID: ")
        name = input("Name: ")
        age = input("Age: ")
        gender = input("Gender: ")
        occupation = input("Occupation: ")
        marital_status = input("Marital Status: ")
        address = input("Address: ")
        email = input("Email: ")
        phone = input("Phone: ")
        national_id = input("National ID: ")
        insurance = input("Insurance: ")
        insurance_card_id = input("Insurance Card ID: ")
        diagnosis = input("Diagnosis: ")
        chief_complaint = input("Chief Complaint: ")
        medications = input("Medications: ")
        investigations = input("Investigations: ")

        # Call the stored procedure with positional parameters
        sql = """
        CALL Add_New_Patient(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Parameters must be in the exact order the stored proc expects
        params = (
            id, name, age, gender, occupation, marital_status, address, email, phone,
            national_id, insurance, insurance_card_id, diagnosis, chief_complaint,
            medications, investigations
        )

        cursor.execute(sql, params)
        print("✅ Patient added successfully!")

    except Exception as e:
        print(f"❌ Error adding patient: {e}")

    finally:
        cursor.close()
        conn.close()

