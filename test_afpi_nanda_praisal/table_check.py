import sqlite3


def inspect_database(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("🔍 Inspecting database structure...\n")

    # Get all tables and views
    cursor.execute("""
        SELECT name, type 
        FROM sqlite_master 
        WHERE type IN ('table', 'view') 
        AND name NOT LIKE 'sqlite_%'
        ORDER BY type, name;
    """)
    objects = cursor.fetchall()

    if not objects:
        print("❌ No tables or views found in the database")
        return

    print("📋 Tables and Views:")
    for obj_name, obj_type in objects:
        # Get column info for each table/view
        cursor.execute(f"PRAGMA table_info({obj_name});")
        columns = cursor.fetchall()

        print(f"\n📊 {obj_name} ({obj_type.upper()})")
        print("┌───────────────┬───────────────┬───────────┬───────────┬───────────┐")
        print("│ Column Name   │ Type          │ Not Null  │ Default   │ Primary   │")
        print("├───────────────┼───────────────┼───────────┼───────────┼───────────┤")

        for col in columns:
            cid, name, type_, notnull, dflt_value, pk = col
            print(f"│ {name:<13} │ {type_:<13} │ {notnull:^9} │ {str(dflt_value or ''):<9} │ {pk:^9} │")

        print("└───────────────┴───────────────┴───────────┴───────────┴───────────┘")

        # For views, show the SQL definition
        if obj_type == 'view':
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE name = '{obj_name}';")
            view_sql = cursor.fetchone()[0]
            print(f"\nView definition:\n{view_sql}\n")

    conn.close()


if __name__ == "__main__":
    db_file = 'test-afpi.db'
    try:
        inspect_database(db_file)
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print(f"❌ Database file not found: {db_file}")