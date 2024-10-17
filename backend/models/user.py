import bcrypt
import uuid
from database.connection import get_cursor

class User:
    def __init__(self, name, email, password, id=None):
        if(id is None): self.id = uuid.uuid4()
        else: self.id = id
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        try:
            with get_cursor() as cursor:
                hashed_password = hash_password(self.password)
                cursor.execute(
                    """
                    INSERT INTO users (id, username, email, password)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    """, (str(self.id), self.name, self.email, hashed_password)
                )
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Can't create User: {e}")


    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("UTF-8"), self.password.encode("UTF-8"))

    @staticmethod
    def get_all_users():
        try:
            with get_cursor() as cursor:

                cursor.execute(
                        """
                        SELECT id, username, email FROM users;
                        """
                )
                result = cursor.fetchall()
                return result

        except Exception as e:
            print(f"Can't get all users: {e}")

    @staticmethod
    def get_user(id: str):
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        SELECT id, username, email, password FROM users WHERE id=%s;
                    """, (id,)
                )
                result = cursor.fetchone()
                user = User(result[1], result[2], result[3], result[0])
                return user

        except Exception as e:
            print(f"Can't get user by id: {e}")

    @staticmethod
    def get_user_email(email: str):
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        SELECT id, username, email, password FROM users WHERE email=%s;
                    """, (email,)
                )
                result = cursor.fetchone()
                user = User(result[1], result[2], result[3], result[0])
                return user

        except Exception as e:
            print(f"Can't get user by email: {e}")

    @staticmethod
    def delete_user(id: str):
        try:
            with get_cursor() as cursor:
                cursor.execute(
                """
                    DELETE FROM users WHERE id=%s RETURNING id;
                """, (id,)
                )
                return cursor.fetchone()

        except Exception as e:
                print(f"Can't delete user: {e}")



def hash_password(password) -> str:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("UTF-8"), salt)
    return hash.decode("UTF-8")
