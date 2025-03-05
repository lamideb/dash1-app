import psycopg2
from psycopg2 import OperationalError

# Database connection parameters
host = "pg-14263e7d-lamze-f101.d.aivencloud.com"
database = "defaultdb"
user = "avnadmin"
password = "AVNS_8zJAiWm3qy_ienDTSDx"
port = "24724"        # PostgreSQL port
sslmode = "require"     #"verify-ca"  # You can set to 'verify-full' for full verification
#sslrootcert = "/home/lamze/tmp/ca_aiven.pem"  # Path to your CA certificate (ca.pem)

def create_connection():
    try:
        # Connect to the PostgreSQL server with SSL enabled
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port,
            sslmode=sslmode
#            sslrootcert=sslrootcert
        )
        print("Connection successful!")
        return conn
    except OperationalError as e:
        print(f"Error: Unable to connect to the database\n{e}")
        return None

def fetch_data(conn):
    try:
        # Create a cursor object
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM tbl_sports")

        # Fetch all the results
        rows = cursor.fetchall()

        # Print the result
        print("Query result:")
        for row in rows:
            print(row)

        # Close the cursor
        cursor.close()
    except Exception as e:
        print(f"Error fetching data: {e}")

def main():
    conn = create_connection()

    if conn:
        fetch_data(conn)

        # Close the connection after use
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
