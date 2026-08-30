# Assignment 33: Chat with SQL Database using LangChain

## Objective

Build a Chat-with-SQL application - an LLM that reads a natural language
question, generates the actual SQL for it, executes it against a real
database, and answers from the result, without any query being hardcoded
anywhere in advance.

## Project Structure

```text
GenAI-Task33-Abhishek/
├── Assignment33_Chat_with_SQL_Database.ipynb   # build + test, all parts
├── sql_lib.py                                    # DB setup, engines, toolkit/agent
├── schema.sql                                    # MySQL Workbench schema + sample data
├── requirements.txt
├── .env.example
└── README.md
```

`sql_lib.py` holds the SQLite setup, the SQLAlchemy/LangChain connection
helpers, the MySQL connection function, and the toolkit/agent builders - the
notebook imports and tests these directly, same split as `agents_lib.py` in
Assignment 32.

## Tasks Covered

1. Create SQLite database (`company.db`) with `employees` and `sales` tables
2. Insert sample data (10 employees, 12 sales) and verify with basic queries
3. Create a SQLAlchemy engine and confirm the connection by fetching table names
4. Create a LangChain `SQLDatabase` object and inspect tables/schema
5. Create a matching database in MySQL Workbench and connect to it with code
6. Initialize `SQLDatabaseToolkit` with the `SQLDatabase` object and an LLM
7. Build a SQL agent (`create_sql_agent`) with verbose reasoning enabled
8. Chat with the database - 4 natural language questions
9. Test the agent against ambiguous/unclear questions
10. Observations & insights

## Libraries Used

- LangChain (`langchain`, `langchain-community`)
- langchain-ollama
- SQLAlchemy
- PyMySQL
- python-dotenv

## Setup

```bash
ollama pull llama3
ollama serve

pip install -r requirements.txt
cp .env.example .env        # only needed for Part 3 (MySQL Workbench)
```

For Part 3: open MySQL Workbench, create a connection, and run `schema.sql`
against it to get a `company` database with the same tables and sample data
as the SQLite version. Then fill in `MYSQL_USER` / `MYSQL_PASSWORD` /
`MYSQL_HOST` / `MYSQL_DATABASE` in `.env`.

## A note on testing

I actually ran Parts 1 and 2 for real - `sql_lib.py`'s SQLite functions have
no external dependency, so `create_database()`, `insert_sample_data()`, and
`verify_data()` all ran genuinely, and the output in the notebook (10
employee rows, 12 sales rows, 4 Engineering / 3 Sales / 2 Marketing / 1 HR)
is real, not written by hand. The SQLAlchemy engine inspection and the
LangChain `SQLDatabase` schema dump in Part 2 are also real output from that
same `company.db` file.

What I couldn't verify in the environment I wrote this in: MySQL itself
isn't installed, so Part 3's connection cell genuinely shows a
connection-refused error rather than a faked success - I confirmed
`get_mysql_db()` fails cleanly (`None`, error message) instead of crashing,
which is the behavior that matters when there's no server to reach. Ollama
also isn't installed here, so Parts 4 and 5 (the actual toolkit/agent runs
and the four Q&A pairs) couldn't be executed and confirmed against real
model output - the code path is the same one that worked cleanly for the
ReAct agent in Assignment 32, just pointed at a SQL toolkit instead of the
mock company tools, but I'm not claiming to have seen real agent traces I
didn't actually get in this run.

## Experiments Performed

- Built `company.db` with `employees` and `sales` tables and confirmed row counts and the department breakdown match what was inserted.
- Verified the SQLAlchemy engine actually connects by fetching table names through `inspect()`, not just trusting `create_engine()` not erroring.
- Built the LangChain `SQLDatabase` object and printed its schema info (including sample rows) to see exactly what context the agent gets before writing any SQL.
- Wrote `schema.sql` to mirror the SQLite schema for MySQL Workbench, and wrote `get_mysql_db()` to return a clean error instead of crashing when the server isn't reachable - tested that failure path directly.
- Built `SQLDatabaseToolkit` and `create_sql_agent()` wrappers in `sql_lib.py`, structured so the same agent-building function works against either the SQLite or the MySQL `SQLDatabase` object with no other code changes.
- Wrote out the four required test questions plus two deliberately ambiguous ones for the safety section, with expected answers worked out by hand from the sample data to sanity-check against once the agent actually runs.

## Key Observations

`SQLDatabase.from_uri()` is the same interface whether it's pointed at
`sqlite:///company.db` or a `mysql+pymysql://` connection string - the
toolkit and agent code in `sql_lib.py` don't need to know or care which one
they're talking to, only the connection string changes. That's what made
running the same agent against both SQLite and Workbench data (Task 6's
requirement) mostly free once the SQLite path was working.

## Challenges Faced

Not having MySQL Workbench actually installed meant Part 3 could only be
verified up to "fails cleanly when unreachable," not "actually returns real
data from a live server." Same limitation with Ollama not being available
for the agent parts - the honest way to handle both was wrapping every real
call in try/except and being explicit in the notebook about what was
actually confirmed versus what's structurally correct but unexecuted here.

## Learning Outcomes

`create_sql_agent()` turned out to basically be the ReAct pattern from
Assignment 32 again, just with a toolkit that writes SQL instead of calling
mock functions - the underlying "reason about the query, pick a tool,
observe the result, decide the next step" loop is identical. The real new
piece was seeing how cleanly the `SQLDatabase` abstraction lets the same
agent logic run against two structurally different database backends,
without the agent code itself needing to change at all.

## Submitted By

Abhishek Thakare
