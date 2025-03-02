import mysql.connector

# Database connection details
db_config = {
    "host": "database-2.czcecg0i4453.ap-south-1.rds.amazonaws.com",  # RDS endpoint
    "user": "admin",
    "password": "Govind9311",  # Updated password
    "database": "mydatabase"  # Updated database name
}

try:
    # Establish connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Update query
    update_query = "UPDATE users SET email = %s WHERE name = %s"
    new_email = "newalice@example.com"
    name = "Alice"

    # Execute query
    cursor.execute(update_query, (new_email, name))
    conn.commit()

    print(f"Updated {cursor.rowcount} row(s) successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()

