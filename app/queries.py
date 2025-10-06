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
    QueryDef(
        key="all_students",
        title="All Students",
        sql="""
            SELECT s.id, s.first_name, s.last_name, s.email, s.age,
                   GROUP_CONCAT(c.name ORDER BY c.name SEPARATOR ', ') AS courses
            FROM students s
            LEFT JOIN enrollments e ON e.student_id = s.id
            LEFT JOIN courses c ON c.id = e.course_id
            GROUP BY s.id, s.first_name, s.last_name, s.email, s.age
            ORDER BY s.last_name, s.first_name
        """.strip(),
        description="List all registered students along with their enrolled courses.",
    ),
    QueryDef(
        key="student_details",
        title="Student Details: Courses, Attendance, Results",
        sql="""
            SELECT s.id AS student_id,
                   CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                   c.id AS course_id,
                   c.name AS course_name,
                   COALESCE(att.present_days, 0) AS present_days,
                   COALESCE(att.total_days, 0) AS total_days,
                   COALESCE(r.marks, 0) AS marks,
                   r.grade
            FROM students s
            LEFT JOIN enrollments e ON e.student_id = s.id
            LEFT JOIN courses c ON c.id = e.course_id
            LEFT JOIN attendance att ON att.student_id = s.id AND att.course_id = c.id
            LEFT JOIN results r ON r.student_id = s.id AND r.course_id = c.id
            WHERE s.id = %(student_id)s
            ORDER BY c.name
        """.strip(),
        params=[("student_id", "int")],
        description="Detailed view for a single student including courses, attendance, and results.",
    ),
    QueryDef(
        key="avg_age_per_course",
        title="Average Student Age per Course",
        sql="""
            SELECT c.id AS course_id,
                   c.name AS course_name,
                   AVG(s.age) AS average_age,
                   COUNT(*) AS total_students
            FROM courses c
            JOIN enrollments e ON e.course_id = c.id
            JOIN students s ON s.id = e.student_id
            GROUP BY c.id, c.name
            ORDER BY c.name
        """.strip(),
        description="Analytics: average age and total students per course.",
    ),
    QueryDef(
        key="students_by_course",
        title="Students by Course",
        sql="""
            SELECT s.id, s.first_name, s.last_name, s.email
            FROM students s
            JOIN enrollments e ON e.student_id = s.id
            WHERE e.course_id = %(course_id)s
            ORDER BY s.last_name, s.first_name
        """.strip(),
        params=[("course_id", "int")],
        description="List students enrolled in a given course.",
    ),
    QueryDef(
        key="student_courses",
        title="Courses for a Student",
        sql="""
            SELECT c.id AS course_id, c.name AS course_name
            FROM courses c
            JOIN enrollments e ON c.id = e.course_id
            WHERE e.student_id = %(student_id)s
            ORDER BY c.name
        """.strip(),
        params=[("student_id", "int")],
        description="List all courses that a student is enrolled in.",
    ),
]


def list_queries() -> List[Dict[str, Any]]:
    return [q.to_dict() for q in QUERIES]


def get_query(key: str) -> Optional[QueryDef]:
    for q in QUERIES:
        if q.key == key:
            return q
    return None
