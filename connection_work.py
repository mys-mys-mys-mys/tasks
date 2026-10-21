from file_work import *
from db_context_manager import get_cursor
from views_queries import views_queries_dict
from itertools import islice

class ConnectionWork:

    def __init__(self):
        self.conn_dict = get_connection_info()
        self.default_database = "dorms"
        #One style using context manager
        #put views into separate file lalallalallala :pppppp

    # Database creation separately to connect to it right away with context manager later
    def create_schema(self):
        with get_cursor(database=None) as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.default_database}`")

    def schema_initialisation(self):
        with get_cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS rooms"
                "(id int NOT NULL AUTO_INCREMENT,"
                "name varchar(25) DEFAULT 'Room #',"
                "PRIMARY KEY (`id`));")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS students"
                "(birthday datetime NOT NULL,"
                "id int unsigned NOT NULL AUTO_INCREMENT,"
                "name varchar(255) NOT NULL,"
                "room int NOT NULL,"
                "sex char(1) NOT NULL,"
                "PRIMARY KEY (id),"
                "CONSTRAINT students_room FOREIGN KEY (room) REFERENCES rooms(id));")

    def index_creation(self):
         with get_cursor(dictionary=False) as cursor_obj:
            cursor_obj.execute(f"SELECT COUNT(1) FROM INFORMATION_SCHEMA.STATISTICS "
            f"WHERE table_schema=DATABASE() AND table_name='students' AND index_name='idx_room_birthday';")
            if cursor_obj.fetchone()[0] == 0:
                cursor_obj.execute(
                    f"ALTER TABLE students ADD INDEX idx_room_birthday (room, birthday)")
            cursor_obj.execute(f"SELECT COUNT(1) FROM INFORMATION_SCHEMA.STATISTICS "
                               f"WHERE table_schema=DATABASE() AND table_name='students' AND index_name='idx_room_sex';")
            if cursor_obj.fetchone()[0] == 0:
                cursor_obj.execute(
                    f"ALTER TABLE students ADD INDEX idx_room_sex (room, sex)")

    def views_creation(self):
        with get_cursor() as cursor_obj:
            cursor_obj.execute(
                """CREATE OR REPLACE VIEW rooms_count_students_view AS
                SELECT r.name, COUNT(*) AS number_of_students 
                FROM rooms AS r
                INNER JOIN
                students AS s
                ON r.id = s.room
                GROUP BY r.id""")
            cursor_obj.execute(
                """CREATE OR REPLACE VIEW smallest_avg_age AS
                SELECT r.*, top_rooms.avg_age
                FROM(
                SELECT room, avg(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
                FROM students AS s
                GROUP BY room
                ORDER BY avg_age
                LIMIT 5) AS top_rooms
                INNER JOIN rooms AS r
                ON r.id = top_rooms.room;""")
            cursor_obj.execute(
                """CREATE OR REPLACE VIEW largest_age_diff AS
                SELECT r.*, top_rooms.age_diff
                FROM(
                SELECT room, TIMESTAMPDIFF(YEAR, min(s.birthday), max(s.birthday)) AS age_diff
                FROM students AS s
                GROUP BY room
                ORDER BY age_diff DESC
                LIMIT 5) AS top_rooms
                INNER JOIN rooms AS r
                ON r.id = top_rooms.room;""")
            cursor_obj.execute(
                """CREATE OR REPLACE VIEW rooms_with_diff_sex AS
                SELECT room FROM students
                GROUP BY room
                HAVING COUNT(DISTINCT sex) = 2;""")

    def json_info_uploading(self):
        rooms_data, students_data = upload_json()
        with get_cursor() as cursor_obj:
            cursor_obj.executemany(
                "INSERT IGNORE INTO rooms(id, name) VALUES(%s,%s)",
                [(item['id'],item['name']) for item in rooms_data]
            )
        with get_cursor() as cursor_obj:
            cursor_obj.executemany(
                "INSERT IGNORE INTO students(birthday,id, name, room, sex) VALUES(%s,%s,%s,%s,%s)",
                [(item['birthday'],item['id'],item['name'],item['room'],item['sex']) for item in students_data]
            )

    def get_info_for_download(self, view_index : int):
        # Goes through views_queries_dict until view_index to get the key (name of the view)
        view_name = next(islice(views_queries_dict, view_index, None))
        with get_cursor() as cursor_obj:
                cursor_obj.execute(
                    f"SELECT * FROM {view_name}")
                rows = cursor_obj.fetchall()
        return rows

