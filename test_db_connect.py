import psycopg2

# Replace these with your actual connection details
host = "pg-18e273d7-nxtwave-content-gen.j.aivencloud.com"
database = "defaultdb"
user = "avnadmin"
password = "AVNS_NCw9qGvuPn3l3A-E0SM"
port = "23382"  # default is usually 5432

# Establishing the connection
try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

    # Create a cursor object
    cursor = connection.cursor()

    # You can now execute SQL queries using the cursor
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"PostgreSQL version: {db_version[0]}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Closing the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed")
