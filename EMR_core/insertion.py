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

def add_patient(conn, patient_data):
    cursor = conn.cursor()
    try:
        sql = """
        CALL Add_New_Patient(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, patient_data)
        result = cursor.fetchone()
        print("✅ Stored proc result:", result)
        return result
    except Exception as e:
        print(f"❌ Error adding patient: {e}")
        raise
    finally:
        cursor.close()

