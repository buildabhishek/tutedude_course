"""
Shared logic for Assignment 33 - same reasoning as agents_lib.py in
Assignment 32 and rag_groq.py in Assignment 30: the real database setup,
connection, and agent-building code lives here so the notebook is testing
these functions directly instead of a simplified inline copy of them.

Resubmission note: get_llm() defaulted to "llama3", which does not support
Ollama's tool calling API. create_sql_agent(..., agent_type="tool-calling")
needs the model to actually call sql_db_query itself - on a model without
tool support, it doesn't error, it just answers directly from whatever the
model already "knows" (or invents) about the question, without ever
touching the database. That's a hallucinated answer that can look
completely plausible and still not match a single row in company.db, which
is exactly what happened in the first submission. Switched the default to
"llama3.1" here, same fix as agents_lib.py in Assignment 32.
"""

import os
import sqlite3

from sqlalchemy import create_engine, inspect, text
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_ollama import ChatOllama


# ---------------------------------------------------------------------------
# PART 1 - SQLite setup
# ---------------------------------------------------------------------------

def create_database(db_path="company.db", reset=True):
    """Creates company.db with the employees and sales tables from the
    assignment spec. reset=True drops existing tables first so re-running
    this cell doesn't just keep appending duplicate sample rows."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if reset:
        cur.execute("DROP TABLE IF EXISTS sales")
        cur.execute("DROP TABLE IF EXISTS employees")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            amount INTEGER,
            sale_date TEXT
        )
    """)

    conn.commit()
    conn.close()
    return db_path


def insert_sample_data(db_path="company.db"):
    """Inserts 10 employees across a few departments and 12 sales rows
    linked to some of them, enough to make the department/salary questions
    from Task 7 actually meaningful instead of trivial."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    employees = [
        (1, "Aditi Rao", "Engineering", 95000),
        (2, "Rohan Mehta", "Sales", 62000),
        (3, "Neha Kulkarni", "Engineering", 88000),
        (4, "Sameer Joshi", "Sales", 71000),
        (5, "Priya Nair", "Marketing", 58000),
        (6, "Karan Verma", "Engineering", 102000),
        (7, "Ishita Sharma", "HR", 54000),
        (8, "Arjun Patil", "Sales", 67000),
        (9, "Meera Iyer", "Marketing", 60000),
        (10, "Devansh Gupta", "Engineering", 91000),
    ]
    cur.executemany(
        "INSERT OR REPLACE INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)",
        employees,
    )

    sales = [
        (1, 2, 15000, "2025-01-14"),
        (2, 2, 9800, "2025-02-03"),
        (3, 4, 21000, "2025-01-22"),
        (4, 4, 13500, "2025-03-11"),
        (5, 8, 18700, "2025-02-19"),
        (6, 8, 9400, "2025-04-02"),
        (7, 2, 12300, "2025-04-18"),
        (8, 4, 16800, "2025-05-05"),
        (9, 8, 11200, "2025-05-21"),
        (10, 2, 20500, "2025-06-09"),
        (11, 4, 8900, "2025-06-27"),
        (12, 8, 14600, "2025-07-15"),
    ]
    cur.executemany(
        "INSERT OR REPLACE INTO sales (sale_id, employee_id, amount, sale_date) VALUES (?, ?, ?, ?)",
        sales,
    )

    conn.commit()
    conn.close()
    return len(employees), len(sales)


def verify_data(db_path="company.db"):
    """Basic row-count + spot-check queries for Task 2's verification step."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM employees")
    emp_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sales")
    sales_count = cur.fetchone()[0]

    cur.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
    by_department = cur.fetchall()

    conn.close()
    return {
        "employee_rows": emp_count,
        "sales_rows": sales_count,
        "employees_by_department": by_department,
    }


# ---------------------------------------------------------------------------
# PART 2 - SQLAlchemy engine + LangChain SQLDatabase (SQLite)
# ---------------------------------------------------------------------------

def get_sqlite_engine(db_path="company.db"):
    """Task 3 - a plain SQLAlchemy engine, tested by fetching table names
    through it rather than just assuming create_engine() succeeding means
    the connection actually works."""
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return engine, tables


def get_langchain_sqlite_db(db_path="company.db"):
    """Task 4 - LangChain's own SQLDatabase wrapper, which is what the
    toolkit/agent actually need rather than the raw SQLAlchemy engine."""
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    return db


# ---------------------------------------------------------------------------
# PART 3 - MySQL Workbench connection
# ---------------------------------------------------------------------------

def get_mysql_db(
    user=None,
    password=None,
    host=None,
    port=None,
    database=None,
):
    """Builds a LangChain SQLDatabase against a MySQL Workbench database.
    Reads from env vars if arguments aren't passed directly. Returns
    (db, error) instead of raising, so a missing/unreachable MySQL server
    doesn't take down anything else that's using the SQLite side."""
    user = user or os.getenv("MYSQL_USER")
    password = password or os.getenv("MYSQL_PASSWORD")
    host = host or os.getenv("MYSQL_HOST", "127.0.0.1")
    port = port or os.getenv("MYSQL_PORT", "3306")
    database = database or os.getenv("MYSQL_DATABASE")

    if not all([user, password, database]):
        return None, "Missing MySQL credentials (MYSQL_USER / MYSQL_PASSWORD / MYSQL_DATABASE not set)."

    uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    try:
        db = SQLDatabase.from_uri(uri)
        return db, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# PART 4 - SQL Toolkit & Agent
# ---------------------------------------------------------------------------

def get_llm(model="llama3.1", temperature=0):
    """Defaults to llama3.1, not llama3 - see the module docstring's
    resubmission note for why that switch matters specifically here."""
    return ChatOllama(model=model, temperature=temperature)


def build_sql_toolkit(db, llm):
    """Task 5 - the toolkit exposes query/schema/table-info tools built
    from the given SQLDatabase, which is what the agent below actually
    calls instead of us writing SQL by hand anywhere."""
    return SQLDatabaseToolkit(db=db, llm=llm)


def build_sql_agent(db, llm, verbose=True):
    """Task 6 - LangChain's prebuilt SQL agent, which already wires the
    toolkit's tools together with a ReAct-style loop, so there's no reason
    to hand-roll one the way agents_lib.py did for the generic tools in
    Assignment 32.

    return_intermediate_steps=True is the important part for this
    resubmission - it's what lets run_sql_agent() below actually show
    which tool the agent called and with what SQL, instead of only the
    final text. That's the difference between trusting the answer and
    being able to check it."""
    toolkit = build_sql_toolkit(db, llm)
    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=verbose,
        agent_type="tool-calling",
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )


def run_sql_agent(agent, question):
    """Runs the agent and reports whether it actually called sql_db_query
    at all - a model without real tool support will happily return a
    normal-looking final answer having never touched the database, which
    is precisely the failure the mentor flagged in the first submission.
    Returns (answer, queries_run) where queries_run is the list of actual
    SQL strings the agent sent to sql_db_query, empty if it never queried."""
    result = agent.invoke({"input": question})
    steps = result.get("intermediate_steps", [])

    queries_run = []
    for action, observation in steps:
        if action.tool == "sql_db_query":
            queries_run.append(action.tool_input)

    return result["output"], queries_run


def get_ground_truth(db_path="company.db"):
    """Computes the real answers to the Task 7 questions directly with
    SQL, bypassing the LLM entirely, so the agent's answers can be checked
    against something independent instead of just trusted."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
    by_department = dict(cur.fetchall())

    cur.execute("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1")
    highest_paid = cur.fetchone()

    cur.execute("SELECT SUM(amount) FROM sales")
    total_sales = cur.fetchone()[0]

    cur.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
    avg_salary_by_department = dict(cur.fetchall())

    conn.close()
    return {
        "employees_by_department": by_department,
        "highest_paid_employee": highest_paid,
        "total_sales_amount": total_sales,
        "avg_salary_by_department": avg_salary_by_department,
    }
