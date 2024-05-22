from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
import pymysql
import time
from config import host, user, password


class DataClient:
    DATABASE_NAME = "bar_guide_bot"
    TABLES = ["place_category", "announce_category", "user", "place",
              "announce", "menu", "review", "reserve", "place_admin"]
    drop_tables = ["place_admin", "reserve", "review", "menu", "announce",
                   "announce_category", "user", "place", "place_category"]

    def __init__(self, host: str, user: str, password: str):
        self.geolocator = Nominatim(user_agent="Bar Guide")
        self.con = pymysql.Connection(
            host=host,
            user=user,
            port=3306,
            password=password,
            use_unicode=True,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        # self.create_db()
        print(self.create_all_tables())

    def create_db(self, db_title: str = DATABASE_NAME) -> bool:
        try:
            request = f"CREATE DATABASE IF NOT EXISTS {db_title};"
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
                return True
        except Exception:
            return False

    def create_table(self, request: str) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
                return True
        except Exception as ex:
            print(ex)
            return False

    def create_place_category_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.place_category (id int AUTO_INCREMENT,
                      title VARCHAR(50),
                      description TEXT,

                      PRIMARY KEY(id),
                      UNIQUE(title))"""
        return self.create_table(request=request)

    def create_announce_category_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.announce_category (id int AUTO_INCREMENT,
                      title VARCHAR(50),
                      description TEXT,

                      PRIMARY KEY(id),
                      UNIQUE(title))"""
        return self.create_table(request=request)

    def create_place_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.place (id int AUTO_INCREMENT,
                      category_id int,
                      title VARCHAR(50),
                      description TEXT,
                      address VARCHAR(200),
                      rating float,
                      position VARCHAR(200),
                      site VARCHAR(100),
                      contact VARCHAR(100),
                      work_time VARCHAR(50),
                      photo_id VARCHAR(200),

                      PRIMARY KEY(id),
                      UNIQUE(title),
                      FOREIGN KEY(category_id) REFERENCES place_category(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_announce_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.announce (id int AUTO_INCREMENT,
                      category_id int,
                      place_id int,
                      title VARCHAR(50),
                      description TEXT,
                      ticker_price VARCHAR(50),
                      ticker_link VARCHAR(100),
                      date VARCHAR(50),
                      time VARCHAR(50),
                      photo_id VARCHAR(200),

                      PRIMARY KEY(id),
                      UNIQUE(title),
                      FOREIGN KEY(category_id) REFERENCES announce_category(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_user_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.user (id int AUTO_INCREMENT,
                      status VARCHAR(50),
                      name VARCHAR(100),
                      tg_id VARCHAR(50),
                      contact VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(tg_id))"""
        return self.create_table(request=request)

    def create_menu_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.menu (id int AUTO_INCREMENT,
                      place_id int,
                      title VARCHAR(50),
                      description TEXT,
                      composition TEXT,
                      price VARCHAR(20),
                      image_id VARCHAR(200),

                      PRIMARY KEY(id),
                      UNIQUE(title, place_id),
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_review_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.review (id int AUTO_INCREMENT,
                      place_id int,
                      user_name VARCHAR(50),
                      user_id VARCHAR(50),
                      text TEXT,
                      rating int,

                      PRIMARY KEY(id),
                      UNIQUE(id),
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_reserve_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.reserve (id int AUTO_INCREMENT,
                      place_id int,
                      user_name VARCHAR(50),
                      user_id VARCHAR(50),
                      date VARCHAR(50),
                      time VARCHAR(50),
                      user_number VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(id),
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_place_admin_table(self) -> bool:
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.place_admin (id int AUTO_INCREMENT,
                      place_id int,
                      user_name VARCHAR(50),
                      user_id VARCHAR(50),

                      PRIMARY KEY(id),
                      UNIQUE(place_id, user_id),
                      FOREIGN KEY(place_id) REFERENCES place(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_all_tables(self) -> bool:
        result = (self.create_place_category_table()
                  & self.create_place_table()
                  & self.create_announce_category_table()
                  & self.create_announce_table()
                  & self.create_user_table()
                  & self.create_menu_table()
                  & self.create_review_table()
                  & self.create_reserve_table()
                  & self.create_place_admin_table())
        return result

    def drop_table(self, table_title: str):
        request = f"DROP TABLE {self.DATABASE_NAME}.{table_title}"
        with self.con.cursor() as cur:
            cur.execute(request)
        print("ok")

    def drop_all_tables(self) -> bool:
        try:
            for elem in self.drop_tables:
                self.drop_table(elem)
            return True
        except Exception as ex:
            print(ex)
            return False

    def set_new_data(self,
                     request: str,
                     record: list) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.executemany(request, record)
                self.con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def set_place_category(self,
                           title: str,
                           description: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.place_category (title, description) " \
                  "VALUES (%s, %s);"
        record = [(title, description)]
        return self.set_new_data(request=request, record=record)

    def set_announce_category(self,
                              title: str,
                              description: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.announce_category (title, description) " \
                  "VALUES (%s, %s);"
        record = [(title, description)]
        return self.set_new_data(request=request, record=record)

    def set_place(self,
                  category_id: int,
                  title: str,
                  description: str,
                  address: str,
                  site: str,
                  contact: str,
                  work_time: str,
                  photo_id: str) -> bool:
        try:
            location = self.geolocator.geocode(address)
            position = f"{location.latitude}_{location.longitude}"
        except Exception:
            position = "0_0"
        rating = 0.
        request = f"INSERT INTO {self.DATABASE_NAME}.place (category_id, title, description," \
                  f"address, rating, position, site, contact, work_time, photo_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        record = [(category_id, title, description, address, rating, position, site, contact, work_time, photo_id)]
        return self.set_new_data(request=request, record=record)

    def set_announce(self,
                     category_id: int,
                     place_id: int,
                     title: str,
                     description: str,
                     ticker_price: str,
                     ticker_link: str,
                     date: str,
                     time_value: str,
                     photo_id: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.announce (category_id, place_id, title, " \
                  f"description, ticker_price, ticker_link, date, time, photo_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        record = [(category_id, place_id, title, description, ticker_price, ticker_link, date, time_value, photo_id)]
        return self.set_new_data(request=request, record=record)

    def set_user(self,
                 name: str,
                 tg_id: str,
                 contact: str = "0") -> bool:
        status = "base"
        request = f"INSERT INTO {self.DATABASE_NAME}.user (status, name, tg_id, contact) " \
                  "VALUES (%s, %s, %s, %s);"
        record = [(status, name, tg_id, contact)]
        return self.set_new_data(request=request, record=record)

    def set_menu(self,
                 place_id: int,
                 title: str,
                 description: str,
                 composition: str,
                 price: str,
                 image_id: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.menu (place_id, title, description," \
                  f"composition, price, image_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s);"
        record = [(place_id, title, description, composition, price, image_id)]
        return self.set_new_data(request=request, record=record)

    def set_review(self,
                   place_id: int,
                   user_name: str,
                   user_id: str,
                   text: str,
                   rating: int) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.review (place_id, user_name, user_id," \
                  f"text, rating) " \
                  "VALUES (%s, %s, %s, %s, %s);"
        record = [(place_id, user_name, user_id, text, rating)]
        return self.set_new_data(request=request, record=record)

    def set_reserve(self,
                    place_id: int,
                    user_name: str,
                    user_id: str,
                    date: str,
                    time_value: str,
                    user_number: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.reserve (place_id, user_name, user_id," \
                  f"date, time, user_number) " \
                  "VALUES (%s, %s, %s, %s, %s, %s);"
        record = [(place_id, user_name, user_id, date, time_value, user_number)]
        return self.set_new_data(request=request, record=record)

    def set_place_admin(self,
                        place_id: int,
                        user_name: str,
                        user_id: str) -> bool:
        request = f"INSERT INTO {self.DATABASE_NAME}.place_admin (place_id, user_name, user_id) " \
                  "VALUES (%s, %s, %s);"
        record = [(place_id, user_name, user_id)]
        return self.set_new_data(request=request, record=record)

    def get_table_info(self, table_title: str) -> dict:
        if table_title in self.TABLES:
            request = f"SELECT * FROM {self.DATABASE_NAME}.{table_title};"
            with self.con.cursor() as cur:
                cur.execute(request)
            return cur.fetchall()

    def get_info(self, request: str) -> list:
        with self.con.cursor() as cur:
            cur.execute(request)
        return cur.fetchall()

    def get_list_values(self, request: str, key: str = "title") -> list:
        values = list()
        with self.con.cursor() as cur:
            cur.execute(request)
            for elem in cur.fetchall():
                values.append(elem[key])
        return values

    def get_exist(self, request: str) -> bool:
        with self.con.cursor() as cur:
            cur.execute(request)
        return len(cur.fetchall()) != 0

    def update_table(self, request: str) -> bool:
        with self.con.cursor() as cur:
            cur.execute(request)
        return cur.fetchall()

    def get_place_info(self, title) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place WHERE title = '{title}';"
        return self.get_info(request=request)[0]

    def get_announce_info_for_title(self, title: str) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.announce WHERE title = '{title}';"
        return self.get_info(request=request)[0]

    def get_announce_info_for_place(self, place_id: int, title: str) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place WHERE title = '{title}' AND place_id = '{place_id}';"
        return self.get_info(request=request)[0]

    def get_place_category(self) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_announce_category(self) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_place_from_category(self, category_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place WHERE category_id = '{category_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_announce_from_category(self, category_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce WHERE category_id = '{category_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_suitable_place(self, title: str) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place;"
        result = self.get_list_values(request=request)
        new_result = [elem for elem in result if title in elem]
        return [len(new_result) > 0, new_result]

    def get_near_position_place(self, position: str, radius: float = 5.0) -> [bool, list]:
        request = f"SELECT title, position FROM {self.DATABASE_NAME}.place;"
        result = self.get_info(request=request)
        user_lat = position.split("_")[0]
        user_long = position.split("_")[1]
        places = list()
        for elem in result:
            place_pos = elem["position"].split("_")
            place_lat = place_pos[0]
            place_long = place_pos[1]
            distance = round(GD((user_lat, user_long), (place_lat, place_long)).km, 2)
            if distance <= radius:
                places.append(elem["title"])
        return [len(places) > 0, places]

    def get_meal_list(self, place_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.menu WHERE place_id = {place_id};"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_meal_info(self, title: str, place_id: int) -> dict:
        request = f"SELECT * FROM {self.DATABASE_NAME}.menu WHERE place_id = '{place_id}';"
        return self.get_info(request=request)[0]

    def get_all_place_review(self, place_id: int) -> [bool, [dict]]:
        request = f"SELECT * FROM {self.DATABASE_NAME}.review WHERE place_id = '{place_id}';"
        result = self.get_info(request=request)
        return [len(result) > 0, result]

    #
    # def get_all_review(self):
    #     for elem in self.data["review"]:
    #         print(elem["user_name"])

    def get_place_announce(self, place_id: int) -> [bool, list]:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce WHERE place_id = {place_id};"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    # def set_new_review(self,
    #                    place_id: int,
    #                    user_name: str,
    #                    user_link: str,
    #                    text: str,
    #                    rating: float):
    #     try:
    #         index = len(self.data["review"])
    #         template = self.templates["review"].copy()
    #         template["id"] = index
    #         template["place_id"] = place_id
    #         template["user_name"] = user_name
    #         template["user_link"] = user_link
    #         template["text"] = text
    #         template["rating"] = rating
    #         self.data["review"].append(template)
    #         return True
    #     except Exception:
    #         return False

    # def set_new_reserve(self,
    #                     place_id: int,
    #                     user_name: str,
    #                     user_link: str,
    #                     date: str,
    #                     time: str,
    #                     user_number: str):
    #     try:
    #         index = len(self.data["reserve"])
    #         template = self.templates["reserve"].copy()
    #         template["id"] = index
    #         template["place_id"] = place_id
    #         template["user_name"] = user_name
    #         template["user_link"] = user_link
    #         template["date"] = date
    #         template["time"] = time
    #         template["user_number"] = user_number
    #         self.data["reserve"].append(template)
    #         return True
    #     except Exception:
    #         return False

    def get_all_reserves(self, place_id: int):
        request = f"SELECT * FROM {self.DATABASE_NAME}.reserve WHERE place_id = '{place_id}';"
        result = self.get_info(request=request)
        return [len(result) > 0, result]

    ################################

    def user_exist(self, user_id: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.user WHERE tg_id = '{user_id}';"
        return self.get_exist(request)

    def set_new_admin(self, user_id: str) -> bool:
        request = f"UPDATE {self.DATABASE_NAME}.user SET status = 'admin' WHERE tg_id = '{user_id}';"
        return self.update_table(request=request)

    def user_is_admin(self, user_id: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.user WHERE tg_id = '{user_id}' AND status = 'admin';"
        return self.get_exist(request)

    def user_is_pa(self, user_id: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place_admin WHERE user_id = '{user_id}';"
        return self.get_exist(request)

    def place_category_exist(self, category_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place_category WHERE title = '{category_title}';"
        return self.get_exist(request)

    def place_exist(self, place_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.place WHERE title = '{place_title}';"
        return self.get_exist(request)

    def get_place_category_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_announce_category_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.announce_category;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_all_place_list(self) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place;"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def get_place_list(self, category_id: int) -> list:
        request = f"SELECT title FROM {self.DATABASE_NAME}.place WHERE category_id = '{category_id}';"
        result = self.get_list_values(request=request)
        return [len(result) > 0, result]

    def announce_category_exist(self, category_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.announce_category WHERE title = '{category_title}';"
        return self.get_exist(request)

    def announce_exist(self, announce_title: str) -> bool:
        request = f"SELECT * FROM {self.DATABASE_NAME}.announce WHERE title = '{announce_title}';"
        return self.get_exist(request)

    def get_place_category_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.place_category WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_announce_category_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.announce_category WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_place_id(self, title: str) -> int:
        request = f"SELECT id FROM {self.DATABASE_NAME}.place WHERE title = '{title}';"
        return self.get_info(request=request)[0]["id"]

    def get_place_description(self, place_id: int) -> str:
        request = f"SELECT description FROM {self.DATABASE_NAME}.place WHERE place_id = '{place_id}';"
        return self.get_info(request=request)[0]["description"]

    def get_place_contact(self, place_id: int) -> str:
        request = f"SELECT contact FROM {self.DATABASE_NAME}.place WHERE place_id = '{place_id}';"
        return self.get_info(request=request)[0]["contact"]

    def get_place_site(self, place_id: int) -> str:
        request = f"SELECT site FROM {self.DATABASE_NAME}.place WHERE place_id = '{place_id}';"
        return self.get_info(request=request)[0]["site"]


