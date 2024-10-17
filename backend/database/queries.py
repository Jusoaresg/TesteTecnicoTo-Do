from connection import get_cursor

def create_tables():

    with get_cursor() as cursor:
        try:
            cursor.execute("""
            
            CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id UUID PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                userId UUID NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                CONSTRAINT fk_user FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
            );
            """)
        except Exception as e:
            print(f"Can't create db tables: {e}")

create_tables()
