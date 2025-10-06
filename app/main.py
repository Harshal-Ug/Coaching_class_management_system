from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .database import get_connection  # adjust import to your project structure

app = FastAPI(title="Coaching SMS - Query Catalog")

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Index & Health
# -------------------------------
@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# Student Login
# -------------------------------
@app.get("/students/{student_id}/login")
def student_login(student_id: int, password: str = Query(...)):
    sql = "SELECT id, first_name, last_name, password_hash FROM students WHERE id=%(sid)s"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Student ID not found")
    if row["password_hash"] != password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"id": row["id"], "first_name": row["first_name"], "last_name": row["last_name"]}

# -------------------------------
# Students & Teachers Lists
# -------------------------------
@app.get("/students")
def students():
    sql = "SELECT id, first_name, last_name, email, age FROM students ORDER BY last_name, first_name"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}

@app.get("/teachers")
def teachers():
    sql = "SELECT id, first_name, last_name, email FROM teachers ORDER BY last_name, first_name"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}

@app.get("/students/{student_id}")
def student_by_id(student_id: int):
    sql = "SELECT id, first_name, last_name, email, age FROM students WHERE id=%(sid)s"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        row = cur.fetchone()
    return {"query": sql.replace("%(sid)s", str(student_id)), "data": row}

# -------------------------------
# Student Dashboard Endpoints
# -------------------------------
@app.get("/students/{student_id}/profile")
def student_profile(student_id: int):
    sql = "SELECT id, first_name, last_name, email, age FROM students WHERE id=%(sid)s"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        row = cur.fetchone()
    return {"query": sql.replace("%(sid)s", str(student_id)), "data": row}

@app.get("/students/{student_id}/courses")
def student_courses(student_id: int):
    """Get all courses a student is enrolled in"""
    sql = (
        "SELECT c.id AS course_id, c.name AS course_name, c.description, "
        "b.name AS batch_name "
        "FROM enrollments e "
        "JOIN courses c ON c.id = e.course_id "
        "LEFT JOIN batches b ON b.id = e.batch_id "
        "WHERE e.student_id = %(sid)s "
        "ORDER BY c.name"
    )
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        rows = cur.fetchall()
    return {"query": sql.replace("%(sid)s", str(student_id)), "data": rows}

@app.get("/students/{student_id}/fees")
def student_fees(student_id: int):
    sql = (
        "SELECT c.id AS course_id, c.name AS course_name, cf.fee_amount, "
        "COALESCE(SUM(p.amount),0) AS paid, (cf.fee_amount - COALESCE(SUM(p.amount),0)) AS due "
        "FROM enrollments e JOIN courses c ON c.id=e.course_id "
        "LEFT JOIN course_fees cf ON cf.course_id=c.id "
        "LEFT JOIN payments p ON p.course_id=c.id AND p.student_id=e.student_id "
        "WHERE e.student_id=%(sid)s GROUP BY c.id, c.name, cf.fee_amount ORDER BY c.name"
    )
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        rows = cur.fetchall()
    return {"query": sql.replace("%(sid)s", str(student_id)), "data": rows}

@app.get("/students/{student_id}/attendance")
def student_attendance(student_id: int):
    sql = (
        "SELECT c.name AS course, b.name AS batch, "
        "COUNT(a.id) AS days_attended "
        "FROM attendance a "
        "JOIN batches b ON b.id = a.batch_id "
        "JOIN courses c ON c.id = b.course_id "
        "WHERE a.student_id = %(sid)s "
        "GROUP BY c.id, c.name, b.id, b.name "
        "ORDER BY c.name"
    )
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        rows = cur.fetchall()
    return {"query": sql.replace("%(sid)s", str(student_id)), "data": rows}

@app.get("/students/{student_id}/results")
def student_results(student_id: int):
    sql = (
        "SELECT c.name AS course, r.marks, r.grade FROM results r JOIN courses c ON c.id=r.course_id "
        "WHERE r.student_id=%(sid)s ORDER BY c.name"
    )
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, {"sid": student_id})
        rows = cur.fetchall()
    return {"query": sql.replace("%(sid)s", str(student_id)), "data": rows}

# -------------------------------
# Teacher Dashboard Endpoints
# -------------------------------
@app.get("/teachers/{teacher_id}/courses")
def courses_by_teacher(teacher_id: int):
    sql = "SELECT id, name, description FROM courses ORDER BY name"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql + " -- (demo: all courses)", "data": rows}

@app.get("/batches")
def list_batches():
    sql = "SELECT id, name, course_id FROM batches ORDER BY name"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}

@app.get("/courses")
def list_courses():
    sql = "SELECT id, name, description FROM courses ORDER BY name"
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}

@app.get("/students_per_batch")
def students_per_batch():
    sql = (
        "SELECT b.id AS batch_id, b.name AS batch_name, COUNT(e.id) AS total_students "
        "FROM batches b LEFT JOIN enrollments e ON e.batch_id=b.id GROUP BY b.id, b.name ORDER BY b.name"
    )
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}

@app.get("/students_per_course")
def students_per_course():
    sql = (
        "SELECT c.id AS course_id, c.name AS course_name, COUNT(e.id) AS total_students "
        "FROM courses c LEFT JOIN enrollments e ON e.course_id=c.id GROUP BY c.id, c.name ORDER BY c.name"
    )
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}

# -------------------------------
# Queries
# -------------------------------
# -------------------------------
# Add Student (Teacher)
# -------------------------------
@app.post("/students")
def add_student(first_name: str, last_name: str, email: str, age: int, password: str = "123", course_id: int = None, batch_id: int = None):
    with get_connection() as conn:
        cur = conn.cursor()
        # Insert student
        sql_student = "INSERT INTO students (first_name,last_name,email,age,password_hash) VALUES (%s,%s,%s,%s,%s)"
        cur.execute(sql_student, (first_name, last_name, email, age, password))
        student_id = cur.lastrowid
        
        # If course is selected, enroll student
        if course_id:
            sql_enroll = "INSERT INTO enrollments (student_id, course_id, batch_id) VALUES (%s, %s, %s)"
            cur.execute(sql_enroll, (student_id, course_id, batch_id))
        
        conn.commit()
    
    query_str = f"{sql_student}"
    if course_id:
        query_str += f"\n{sql_enroll}"
    
    return {"query": query_str, "data": {"created": True, "student_id": student_id}}


@app.get("/courses_with_batches")
def courses_with_batches():
    sql = """
        SELECT c.id AS course_id, c.name AS course_name,
               b.id AS batch_id, b.name AS batch_name
        FROM courses c
        LEFT JOIN batches b ON b.course_id = c.id
        ORDER BY c.name, b.name
    """
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}
# -------------------------------
# NEW: Teacher view - Students with their Courses
# -------------------------------
@app.get("/teachers/{teacher_id}/students")
def students_with_courses():
    sql = """
    SELECT s.id AS student_id, s.first_name, s.last_name, s.email, s.age,
           c.name AS course_name
    FROM students s
    JOIN enrollments e ON e.student_id = s.id
    JOIN courses c ON c.id = e.course_id
    ORDER BY s.last_name, s.first_name, c.name
    """
    with get_connection() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
    return {"query": sql, "data": rows}