---
name: db-query
description: Query databases in read-only mode. Use when the user asks to find, check, or look up data in a database. Triggers on phrases like "query the database", "check in the DB", "find in the database", "look up in the table", "SELECT", "show me data from". The database-specialist agent also uses this skill for live queries — prefer delegating to that agent for complex data investigations.
user-invocable: true
argument-hint: "<what you want to find>"
allowed-tools: Read, Bash
---

# Database Query Skill

## Objective

Execute read-only SQL queries against configured databases to help the user find data.

## Available Databases Configuration

The database connections are stored in a `databases.yaml` file. Search for it using:
1. Look in the project's Claude memory directory (glob: `~/.claude/projects/*/memory/databases.yaml`)
2. Or look in `~/.claude/databases.yaml` as a fallback

Always read this file first to know which databases are available.

## Python Script

The query executor script `db_query.py` is bundled alongside this SKILL.md file, in the same directory.

## Instructions

When the user asks to find or query data:

1. **Read the databases config** to see which databases are available and what each contains.

2. **Identify the right database** based on the user's request and the database descriptions.
   - If multiple databases could match, ask the user which one.
   - If no databases are configured, tell the user to add one to the YAML config.

3. **Build the SQL query** based on what the user wants to find.
   - If you're not sure about the schema, first run a discovery query:
     - PostgreSQL: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name`
     - To see columns: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '<table>' ORDER BY ordinal_position`
   - Always use `LIMIT` to avoid returning too many rows unless the user explicitly needs all data.
   - NEVER use write operations (INSERT, UPDATE, DELETE, DROP, etc.) — the script blocks them, but don't even try.

4. **Execute the query** using the Python script (resolve the actual paths at runtime):
   ```bash
   python3 <path-to-db_query.py> \
     --config <path-to-databases.yaml> \
     --db <alias> \
     --query "<SQL query>" \
     --format table \
     --limit 100
   ```

5. **Present the results** clearly to the user. Summarize findings when appropriate.

## Output Formats

- `--format table` — Human-readable table (default)
- `--format json` — JSON array of objects
- `--format csv` — CSV output

## Usage Examples

```
/db-query quantos usuários ativos temos?
/db-query qual o saldo médio das contas?
/db-query listar as últimas 10 transações do usuário 12345
```

## Adding a New Database

Tell the user to edit their `databases.yaml` file (the one discovered in step 1) and add an entry following this format:

```yaml
databases:
  my_alias:
    type: postgresql    # postgresql | mysql | mssql
    host: hostname
    port: 5432
    database: db_name
    username: user
    password: pass
    description: "Short description of what data lives here"
```
