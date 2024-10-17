import uuid
from cache.redis import RedisCache, set_to_cache, get_from_cache
from database.connection import get_cursor

redis_cache = RedisCache()

class Task:
    def __init__(self, name, desc, userId, completed):
        self.id = uuid.uuid4()
        self.name = name
        self.desc = desc
        self.userId = userId
        self.completed = completed

    def change_name(self, new_name):
        self.name = new_name

    def change_desc(self, new_desc):
        self.desc = new_desc
    

    def save(self):
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (id, name, description, userId, completed)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """, (str(self.id), self.name, self.desc, self.userId, self.completed)
                )
                result = cursor.fetchone()
                print(result)
        except Exception as e:
            print(f"Can't create Task: {e}")

    @staticmethod
    def delete_task(id: str):
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        DELETE FROM tasks WHERE id=%s
                        RETURNING id;
                    """, (str(id),))
                result = cursor.fetchone()
                return result

        except Exception as e:
            print(f"Can't delete Task: {e}")

    @staticmethod
    async def get_task(id: str):
        
        cache_response = await redis_cache.get(id)

        if cache_response is not None:
            return {"source": "cache", "task": cache_response}

        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        SELECT * FROM tasks WHERE id=%s LIMIT 1;
                    """, (id,)
                )
                result = cursor.fetchone()

                if result is not None:
                    await set_to_cache(str(id), str(result), 30)

                return result
        except Exception as e:
            print(f"Can't get Task: {e}")

    @staticmethod
    def edit_task(task):
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE tasks
                        SET name = %s,
                            description = %s,
                            completed =  %s
                        WHERE id = %s;
                    """, (task.name, task.desc, task.completed, task.id)
                )
        except Exception as e:
            print(f"Can't edit Task: {e}")

    @staticmethod
    async def get_user_tasks(user_id: str):
        cache_response = await redis_cache.get(user_id)

        if cache_response is not None:
            return {"source": "cache", "task": cache_response}
        try:
            with get_cursor() as cursor:
                cursor.execute(
                        """
                            SELECT * FROM tasks WHERE userId=%s
                        """, (str(user_id),)
                )
                result = cursor.fetchall()

                if result is not None:
                    await set_to_cache(str(user_id), str(result), 30)

                return result
        except Exception as e:
            print(f"Can't get user tasks: {e}")

