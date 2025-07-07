import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
from EMR_core.insertion import auth_snflk

def add_visit(conn, Doctor_ID, Doctor_Name, Patient_ID, Patient_name, Type, Date, Time, Notes, Prescription, 
                Status, Payment):
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.VISIT (
             Doctor_ID, Doctor_Name, Patient_ID, Patient_name, Type, Date, Time, Notes, Prescription, 
                Status, Payment
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                Doctor_ID, Doctor_Name, Patient_ID, Patient_name, Type, Date, Time, Notes, Prescription, 
                Status, Payment
            )
        )
        cursor.execute("SELECT ID FROM CLINIC_A.PUBLIC.VISIT WHERE DOCTOR_ID = {Doctor_ID} and Patient_ID = {Patient_ID} and Date = {Date}")
        visit_id = cursor.fetchone()[0]

        print("✅ Visit recorded successfully!")
        return visit_id

    except Exception as e:
        print(f"❌ Error adding Visit: {e}")
        return f"Error adding Visit: {e}"

    finally:
        cursor.close()
        conn.close()