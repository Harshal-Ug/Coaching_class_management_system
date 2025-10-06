import pathlib
import sys
from dotenv import load_dotenv
from app.db import get_connection


def main():
    load_dotenv()
    schema_path = pathlib.Path("sql/schema.sql")
    seed_path = pathlib.Path("sql/seed.sql")

    with get_connection() as conn:
        cur = conn.cursor()
        for path in (schema_path, seed_path):
            sql = path.read_text(encoding="utf-8")
            for statement in [s.strip() for s in sql.split(";") if s.strip()]:
                cur.execute(statement)
        conn.commit()
    print("Database initialized with schema and seed data.")


if __name__ == "__main__":
    sys.exit(main())


