import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
from EMR_core.insertion import auth_snflk

def add_visit(conn, Doctor_ID, Doctor_Name, Patient_ID, Patient_name, Type, Date, Time, Notes, Prescription, 
              Status, Payment):
    cursor = conn.cursor()
    try:
        # ✅ Check Doctor_ID exists
        cursor.execute("SELECT 1 FROM CLINIC_A.PUBLIC.DOCTOR WHERE ID = %s", (Doctor_ID,))
        if cursor.fetchone() is None:
            raise ValueError(f"Doctor ID {Doctor_ID} does not exist in the database.")

        # ✅ Check Patient_ID exists
        cursor.execute("SELECT 1 FROM CLINIC_A.PUBLIC.PATIENT WHERE ID = %s", (Patient_ID,))
        if cursor.fetchone() is None:
            raise ValueError(f"Patient ID {Patient_ID} does not exist in the database.")

        # Insert the visit
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

        # Fetch the generated ID
        cursor.execute("""
            SELECT VISIT_ID FROM CLINIC_A.PUBLIC.VISIT 
            WHERE DOCTOR_ID = %s AND PATIENT_ID = %s AND DATE = %s
            ORDER BY VISIT_ID DESC LIMIT 1
        """, (Doctor_ID, Patient_ID, Date))

        visit_id = cursor.fetchone()[0]

        print("✅ Visit recorded successfully!")
        return visit_id

    except Exception as e:
        print(f"❌ Error adding Visit: {e}")
        return f"Error adding Visit: {e}"

    finally:
        cursor.close()
        conn.close()

def add_booking(conn,  Patient_Phone_Number, Patient_Name , Doctor_ID, Doctor_Name, Receptionist_ID,
                Type ,Date, Time, Status):
    cursor = conn.cursor()
    try:
        # ✅ Check Doctor_ID exists
        cursor.execute("SELECT 1 FROM CLINIC_A.PUBLIC.DOCTOR WHERE ID = %s", (Doctor_ID,))
        if cursor.fetchone() is None:
            raise ValueError(f"Doctor ID {Doctor_ID} does not exist in the database.")

        # ✅ Check Patient_ID exists
        cursor.execute("SELECT 1 FROM CLINIC_A.PUBLIC.PATIENT WHERE PHONE = %s", (Patient_Phone_Number,))
        if cursor.fetchone() is None:
            raise ValueError(f"Patient PHONE {Patient_Phone_Number} does not exist in the database.")
        cursor.execute("SELECT ID FROM CLINIC_A.PUBLIC.PATIENT WHERE PHONE = %s", (Patient_Phone_Number,))
        result = cursor.fetchone()
        if result is None:
            raise ValueError(f"Patient with phone {Patient_Phone_Number} does not exist in the database.")
        Patient_ID = result[0]
        # Insert the visit
        sql = """
        INSERT INTO CLINIC_A.PUBLIC.BOOKING (
            Patient_ID,  Patient_Phone_Number, Patient_Name, Doctor_ID, Doctor_Name, Receptionist_ID, Type,
              Date, Time, Status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                Patient_ID , Patient_Phone_Number, Patient_Name , Doctor_ID, Doctor_Name, Receptionist_ID,
                Type ,Date, Time, Status
            )
        )

        # Fetch the generated ID
        cursor.execute("""
            SELECT BOOKING_ID FROM CLINIC_A.PUBLIC.BOOKING 
            WHERE DOCTOR_ID = %s AND PATIENT_ID = %s AND DATE = %s
            ORDER BY BOOKING_ID DESC LIMIT 1
        """, (Doctor_ID, Patient_ID, Date))

        booking_id = cursor.fetchone()[0]

        print("✅ Booking recorded successfully!")
        return booking_id

    except Exception as e:
        print(f"❌ Error adding Booking: {e}")
        return f"Error adding Booking: {e}"

    finally:
        cursor.close()
        conn.close()        
        