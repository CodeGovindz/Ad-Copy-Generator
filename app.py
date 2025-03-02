import streamlit as st
import mysql.connector

# Database configuration
db_config = {
    "host": "database-2.czcecg0i4453.ap-south-1.rds.amazonaws.com",  # Your RDS endpoint
    "user": "admin",
    "password": "Govind9311",  # Your database password
    "database": "mydatabase"  # Update with the correct database name
}

# Function to insert user data
def insert_user(name, email):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return False

# Streamlit UI
st.title("📩 User Registration")

name = st.text_input("Enter your name")
email = st.text_input("Enter your email")

if st.button("Submit"):
    if name and email:
        if insert_user(name, email):
            st.success(f"✅ User '{name}' added successfully!")
        else:
            st.error("❌ Failed to add user.")
    else:
        st.warning("⚠️ Please enter both name and email.")

# Show all users
st.subheader("📜 Registered Users")
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    if users:
        for user in users:
            st.write(f"🆔 {user[0]} | **{user[1]}** - 📧 {user[2]}")
    else:
        st.info("No users found.")
except mysql.connector.Error as err:
    st.error(f"Failed to fetch users: {err}")

