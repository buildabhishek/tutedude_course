# Assignment 33: Chat with SQL Database using LangChain

## Objective

Build a Chat-with-SQL application - an LLM that reads a natural language
question, generates the actual SQL for it, executes it against a real
database, and answers from the result, without any query being hardcoded
anywhere in advance.

## Resubmission Note

The first submission was rejected because the agent's answers didn't
actually come from querying the database - `get_llm()` in `sql_lib.py`
defaulted to `llama3`, which doesn't support Ollama's tool calling API.
`create_sql_agent(..., agent_type="tool-calling")` needs the model to
genuinely call `sql_db_query` itself; on a model without tool support it
doesn't error, it just answers directly from whatever the model already
"knows" (or invents), never touching `company.db` at all. That produces a
hallucinated answer that can sound completely correct and still not match a
single row in the database - which is exactly what the feedback flagged.

Two concrete fixes, not just a different explanation:

1. `get_llm()` now defaults to `llama3.1`, which does support tool calling
   in Ollama.
2. `build_sql_agent()` now sets `return_intermediate_steps=True`, and a new
   `run_sql_agent()` function reports the exact SQL string (if any) the
   agent sent to `sql_db_query`. If that comes back empty, the notebook
   prints an explicit warning that the answer isn't grounded in the
   database - instead of trusting the final text at face value the way the
   first submission implicitly did. There's also a new `get_ground_truth()`
   function that computes the real answers directly with SQL, independent
   of any LLM, so the agent's answers have something concrete to be checked
   against.

## Project Structure

```text
GenAI-Task33-Abhishek/
├── Assignment33_Chat_with_SQL_Database.ipynb   # build + test, all parts
├── sql_lib.py                                    # DB setup, engines, toolkit/agent, grounding checks
├── schema.sql                                    # MySQL Workbench schema + sample data
├── requirements.txt
├── .env.example
└── README.md
```

## Tasks Covered

1. Create SQLite database (`company.db`) with `employees` and `sales` tables
2. Insert sample data (10 employees, 12 sales) and verify with basic queries
3. Create a SQLAlchemy engine and confirm the connection by fetching table names
4. Create a LangChain `SQLDatabase` object and inspect tables/schema
5. Create a matching database in MySQL Workbench and connect to it with code
6. Initialize `SQLDatabaseToolkit` with the `SQLDatabase` object and an LLM
7. Build a SQL agent (`create_sql_agent`) with verbose reasoning and intermediate-step tracking enabled
8. Chat with the database - 4 natural language questions, each checked against ground truth and against whether the agent actually queried the database
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
ollama pull llama3.1
ollama serve

pip install -r requirements.txt
cp .env.example .env        # only needed for Part 3 (MySQL Workbench)
```

For Part 3: open MySQL Workbench, create a connection, and run `schema.sql`
against it to get a `company` database with the same tables and sample data
as the SQLite version. Then fill in `MYSQL_USER` / `MYSQL_PASSWORD` /
`MYSQL_HOST` / `MYSQL_DATABASE` in `.env`.

## A note on testing

I don't have Ollama or MySQL installed in the environment I authored this
in, so Parts 4 and 5 (the actual agent runs) and Part 3's live connection
are marked **not run here** in the notebook - explicitly, at each cell,
rather than narrated as if they'd happened.

What I did genuinely run: all of Part 1 and Part 2 (SQLite table creation,
sample data insertion, row-count verification, the SQLAlchemy engine
inspection, and the LangChain `SQLDatabase` schema dump) - no LLM or network
dependency, real output. I also ran `get_ground_truth()` for real against
the actual `company.db` (highest salary: Karan Verma at 102000; total
sales: 171700; department counts and averages all computed directly with
SQL) - these are the numbers Part 4's agent answers should be checked
against once it actually runs. And I unit-tested `run_sql_agent()`'s
grounding-check logic against two hand-built fake agent results - one that
included a real `sql_db_query` call in its intermediate steps, one that
didn't - to confirm the function correctly reports the SQL in the first
case and correctly flags the second as ungrounded, before ever needing a
real model.

What's genuinely unverified: whether `llama3.1` reliably calls
`sql_db_query` for these specific questions and returns answers that match
`get_ground_truth()`. That's on whoever runs this next, with Ollama
actually running - the notebook is built so that check is automatic and
visible (ground truth printed next to each answer, a warning if no query
was executed) rather than something that has to be taken on faith.

## Experiments Performed

- Actually ran SQLite creation, sample data insertion, and verification - genuine row counts and department breakdown.
- Actually ran the SQLAlchemy engine inspection and the LangChain `SQLDatabase` schema dump against the real `company.db`.
- Actually ran `get_ground_truth()` against the real database to get independent, LLM-free correct answers for all four Task 7 questions.
- Actually confirmed `SQLDatabaseToolkit` and `create_sql_agent()` construct cleanly (tool list included) without needing a live Ollama connection, since only `.invoke()` actually reaches out to the model.
- Actually unit-tested `run_sql_agent()`'s grounding-check logic with fake agent objects, confirming it correctly distinguishes a real `sql_db_query` call from an ungrounded direct answer.
- Confirmed `get_mysql_db()` fails cleanly with a real connection-refused error rather than crashing, in the absence of a MySQL server.

## Key Observations

The core issue in the first submission wasn't really about SQL or LangChain
syntax - `create_sql_agent()` built and looked completely normal, the
failure was invisible at the code level. It only shows up if you actually
check whether `sql_db_query` got called, which is why the fix is a
verification mechanism (`return_intermediate_steps` + `run_sql_agent()`),
not just a different default model. A better model makes grounded answers
likely; the grounding check is what makes them provable.

## Challenges Faced

Not having Ollama or MySQL in the authoring environment meant the actual
agent behavior - the part the previous feedback was specifically about -
still can't be confirmed from here. Handled that by pushing as much
verification as possible into code that doesn't need a live model (the
ground-truth function, the grounding-check unit tests) so the parts that do
need Ollama are set up to be checked immediately and automatically once
someone with a working setup runs them, instead of relying on hand-written
claims either way.

## Learning Outcomes

The distinction that mattered most here: an agent framework not raising an
exception is not the same as the agent doing the thing it's supposed to do.
`create_sql_agent()` with a non-tool-calling model runs successfully and
returns a normal `AgentExecutor` result every time - the only way to catch
the failure is to check the actual tool calls it made, not just whether the
call succeeded or how confident the output sounds.

## Submitted By

Abhishek Thakare
