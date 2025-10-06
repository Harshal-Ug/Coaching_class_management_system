from typing import Any, Dict, List, Optional, Tuple

class QueryDef:
    def __init__(
        self,
        key: str,
        title: str,
        sql: str,
        params: Optional[List[Tuple[str, str]]] = None,
        description: Optional[str] = None,
    ) -> None:
        self.key = key
        self.title = title
        self.sql = sql
        self.params = params or []
        self.description = description or ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "sql": self.sql,
            "params": [{"name": n, "type": t} for (n, t) in self.params],
            "description": self.description,
        }

QUERIES: List[QueryDef] = [
    # All students
    QueryDef(
        key="all_students",
        title="All Students",
        sql="""
            SELECT id, first_name, last_name, email, age
            FROM students
            ORDER BY last_name, first_name
        """.strip(),
        description="List all registered students (basic select).",
    ),
    # Student profile
    QueryDef(
        key="student_profile",
        title="Student Profile",
        sql="""
            SELECT id, first_name, last_name, email, age
            FROM students
            WHERE id = %(student_id)s
        """.strip(),
        params=[("student_id", "int")],
        description="View a single student's profile.",
    ),
    # Courses a student is enrolled in
    QueryDef(
        key="student_courses",
        title="Courses for a Student",
        sql="""
            SELECT course_id, batch_id
            FROM enrollments
            WHERE student_id = %(student_id)s
        """.strip(),
        params=[("student_id", "int")],
        description="List course IDs and batch IDs for a student.",
    ),
    # Fee details (simple)
    QueryDef(
        key="student_fees",
        title="Student Fees",
        sql="""
            SELECT course_id, fee_amount, paid_amount, due_amount
            FROM payments
            WHERE student_id = %(student_id)s
        """.strip(),
        params=[("student_id", "int")],
        description="View fees for a student in each course.",
    ),
    # Attendance records
    QueryDef(
        key="student_attendance",
        title="Attendance Records",
        sql="""
            SELECT course_id, batch_id, date, status
            FROM attendance
            WHERE student_id = %(student_id)s
        """.strip(),
        params=[("student_id", "int")],
        description="View raw attendance records for a student.",
    ),
    # Exam results (simple)
    QueryDef(
        key="student_results",
        title="Exam Results",
        sql="""
            SELECT course_id, marks, grade
            FROM results
            WHERE student_id = %(student_id)s
        """.strip(),
        params=[("student_id", "int")],
        description="View exam results for a student.",
    ),
    # All courses
    QueryDef(
        key="all_courses",
        title="All Courses",
        sql="""
            SELECT id, name, description
            FROM courses
            ORDER BY name
        """.strip(),
        description="List all courses.",
    ),
    # All batches
    QueryDef(
        key="all_batches",
        title="All Batches",
        sql="""
            SELECT id, name
            FROM batches
            ORDER BY name
        """.strip(),
        description="List all batches.",
    ),
    # Students in a course
    QueryDef(
        key="students_by_course",
        title="Students by Course",
        sql="""
            SELECT student_id
            FROM enrollments
            WHERE course_id = %(course_id)s
        """.strip(),
        params=[("course_id", "int")],
        description="List student IDs enrolled in a given course.",
    ),
]

def list_queries() -> List[Dict[str, Any]]:
    return [q.to_dict() for q in QUERIES]

def get_query(key: str) -> Optional[QueryDef]:
    for q in QUERIES:
        if q.key == key:
            return q
    return None
