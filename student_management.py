import mysql.connector
from mysql.connector import Error


HOST = "localhost"
USER = "root"
PASSWORD = "gauri@1234"
DATABASE = "sms_Demo"



def connect_mysql():
    try:
        return mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
    except Error as e:
        print("MySQL Connection Error:", e)
        return None


def setup_database():
    conn = connect_mysql()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS sms_Demo")
        cursor.execute("USE sms_Demo")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                rollNo INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                mobileNo VARCHAR(15) UNIQUE,
                city VARCHAR(50),
                course VARCHAR(50)
            )
        """)

        conn.commit()
        return True

    except Error as e:
        print("Database Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()


def get_connection():
    try:
        return mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
    except Error as e:
        print("Connection Error:", e)
        return None




def add_student():
    print("\n========== ADD NEW STUDENT ==========")

    try:
        roll_no = int(input("Enter Roll Number: "))
    except ValueError:
        print("Invalid Roll Number!")
        return

    name = input("Enter Name: ").strip()
    mobile = input("Enter Mobile Number: ").strip()
    city = input("Enter City: ").strip()
    course = input("Enter Course: ").strip()

    if not name or not mobile or not city or not course:
        print("All fields are required!")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO students
            (rollNo, name, mobileNo, city, course)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (roll_no, name, mobile, city, course)

        cursor.execute(query, values)
        conn.commit()

        print("Student added successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()




def view_students():
    print("\n================ ALL STUDENTS ================")

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT rollNo, name, mobileNo, city, course
            FROM students
            ORDER BY rollNo
        """)

        records = cursor.fetchall()

        if not records:
            print("No student records found.")
            return

        print("-" * 80)
        print(
            f"{'Roll No':<10}"
            f"{'Name':<20}"
            f"{'Mobile':<16}"
            f"{'City':<15}"
            f"{'Course':<15}"
        )
        print("-" * 80)

        for student in records:
            print(
                f"{student[0]:<10}"
                f"{student[1]:<20}"
                f"{student[2]:<16}"
                f"{student[3]:<15}"
                f"{student[4]:<15}"
            )

        print("-" * 80)

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()




def update_student():
    print("\n========== UPDATE STUDENT ==========")

    try:
        roll_no = int(input("Enter Roll Number: "))
    except ValueError:
        print("Invalid Roll Number!")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM students WHERE rollNo = %s",
            (roll_no,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Roll Number does not exist!")
            return

        print("\nCurrent Student Details:")
        print("Name:", student[1])
        print("Mobile:", student[2])
        print("City:", student[3])
        print("Course:", student[4])

        print("\nEnter new details:")

        name = input("New Name: ").strip()
        mobile = input("New Mobile Number: ").strip()
        city = input("New City: ").strip()
        course = input("New Course: ").strip()

       
        if name == "":
            name = student[1]

        if mobile == "":
            mobile = student[2]

        if city == "":
            city = student[3]

        if course == "":
            course = student[4]

        query = """
            UPDATE students
            SET name = %s,
                mobileNo = %s,
                city = %s,
                course = %s
            WHERE rollNo = %s
        """

        values = (name, mobile, city, course, roll_no)

        cursor.execute(query, values)
        conn.commit()

        print("Student record updated successfully!")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()




def delete_student():
    print("\n========== DELETE STUDENT ==========")

    try:
        roll_no = int(input("Enter Roll Number: "))
    except ValueError:
        print("Invalid Roll Number!")
        return

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT name FROM students WHERE rollNo = %s",
            (roll_no,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Roll Number does not exist!")
            return

        print("Student Name:", student[0])

        confirm = input(
            "Are you sure you want to delete this record? (y/n): "
        ).lower()

        if confirm == "y":

            cursor.execute(
                "DELETE FROM students WHERE rollNo = %s",
                (roll_no,)
            )

            conn.commit()

            print("Student record deleted successfully!")

        else:
            print("Delete operation cancelled.")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()




def menu():
    while True:

        print("\n")
        print("=" * 50)
        print("          STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Update Student Record")
        print("4. Delete Student Record")
        print("5. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            update_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            print("\nThank you for using Student Management System!")
            print("Program exited successfully.")
            break

        else:
            print("Invalid choice! Please enter 1-5.")



if __name__ == "__main__":

    if setup_database():
        print("\nDatabase setup completed successfully.")
        menu()
    else:
        print("\nUnable to setup database.")
        print("Please check your MySQL server and password.")
