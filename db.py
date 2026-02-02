import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=LAPTOP-4B5G2VO0;"
        "DATABASE=HabitTrackerDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return conn
