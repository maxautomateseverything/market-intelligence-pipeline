import duckdb
from src.config import DATABASE_PATH

con = duckdb.connect(DATABASE_PATH)

table_names = con.sql("""
                        SHOW TABLES
                        """).fetchdf()["name"].tolist()

print("Database tables currently existing:")
print(table_names)

for table in table_names:
    con.execute(f"""
                DROP TABLE IF EXISTS {table}
                """)

remaining_tables = con.sql("""
                        SHOW TABLES
                        """).fetchdf()["name"].tolist()

print("Tables left:")
print(remaining_tables)

if not remaining_tables:
    print("All tables dropped")
else:
    print("Failed to drop tables")

con.close