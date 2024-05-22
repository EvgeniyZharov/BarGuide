from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD


class DataClient:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent="Bar Guide")
        self.data = dict()
        self.data["place_category"] = list()
        self.data["announce_category"] = list()
        self.data["user"] = list()
        self.data["place"] = list()
        self.data["announce"] = list()
        self.data["menu"] = list()
        self.data["review"] = list()
        self.data["reserve"] = list()
        self.data["place_admin"] = list()

        self.templates = dict()
        self.templates["place_category"] = {
            "id": 0,
            "title": "",
            "description": ""
        }
        self.templates["announce_category"] = {
            "id": 0,
            "title": "",
            "description": ""
        }
        self.templates["place"] = {
            "id": 0,
            "category_id": 0,
            "title": "",
            "description": "",
            "address": "",
            "rating": 0.,
            "position": "",
            "site": "",
            "contact": "",
            "work_time": "",
            "photo_link": ""
        }
        self.templates["user"] = {
            "id": 0,
            "status": "",
            "name": "",
            "tg_link": "",
            "contact": "",
        }
        self.templates["announce"] = {
            "id": 0,
            "category_id": 0,
            "place_id": "",
            "title": "",
            "description": "",
            "ticket_price": "",
            "tickers_link": "",
            "date": "",
            "time": "",
            "photo_link": ""
        }
        self.templates["menu"] = {
            "id": 0,
            "place_id": "",
            "title": "",
            "description": "",
            "composition": "",
            "price": "",
            "image_link": "",
        }
        self.templates["review"] = {
            "id": 0,
            "place_id": "",
            "user_name": "",
            "user_link": "",
            "text": "",
            "rating": 0.,
        }
        self.templates["reserve"] = {
            "id": 0,
            "place_id": "",
            "user_name": "",
            "user_link": "",
            "date": "",
            "time": "",
            "user_number": ""
        }
        self.templates["place_admin"] = {
            "id": 0,
            "place_id": "",
            "user_name": "",
            "user_id": "",
        }

    def set_place_category(self,
                           title: str,
                           description: str,
                           ) -> bool:
        try:
            index = len(self.data["place_category"])
            template = self.templates["place_category"].copy()
            template["id"] = index
            template["title"] = title
            template["description"] = description
            self.data["place_category"].append(template)
            return True
        except Exception:
            return False

    def set_announce_category(self,
                              title: str,
                              description: str,
                              ) -> bool:
        try:
            index = len(self.data["announce_category"])
            template = self.templates["announce_category"].copy()
            template["id"] = index
            template["title"] = title
            template["description"] = description
            self.data["announce_category"].append(template)
            return True
        except Exception:
            return False

    def set_place(self,
                  category_id: int,
                  title: str,
                  description: str,
                  address: str,
                  site: str,
                  contact: str,
                  work_time: str,
                  photo_link: str
                  ) -> bool:
        try:
            try:
                location = self.geolocator.geocode(address)
                position = f"{location.latitude}_{location.longitude}"
            except Exception:
                position = "0_0"
            index = len(self.data["place"])
            template = self.templates["place"].copy()
            template["id"] = index
            template["category_id"] = category_id
            template["title"] = title
            template["description"] = description
            template["address"] = address
            template["site"] = site
            template["contact"] = contact
            template["work_time"] = work_time
            template["photo_link"] = photo_link
            template["position"] = position
            self.data["place"].append(template)
            return True
        except Exception:
            return False

    def set_menu(self,
                 place_id: int,
                 title: str,
                 description: str,
                 composition: str,
                 price: float,
                 link_image: str
                 ) -> bool:
        try:
            index = len(self.data["menu"])
            template = self.templates["menu"].copy()
            template["id"] = index
            template["place_id"] = place_id
            template["title"] = title
            template["description"] = description
            template["composition"] = composition
            template["price"] = price
            template["link_image"] = link_image
            self.data["menu"].append(template)
            return True
        except Exception:
            return False

    def set_announce(self,
                     category_id: int,
                     place_id: int,
                     title: str,
                     description: str,
                     price: str,
                     link_ticker: str,
                     date: str,
                     time: str,
                     photo_link: str
                     ) -> bool:
        try:
            index = len(self.data["announce"])
            template = self.templates["announce"].copy()
            template["id"] = index
            template["category_id"] = category_id
            template["place_id"] = place_id
            template["title"] = title
            template["description"] = description
            template["price"] = price
            template["link_ticker"] = link_ticker
            template["date"] = date
            template["time"] = time
            template["photo_link"] = photo_link
            self.data["announce"].append(template)
            return True
        except Exception:
            return False

    def set_user(self,
                 user_name: str,
                 user_id: str,
                 contact: str = None,
                 status: str = "base",
                 ) -> bool:
        try:
            index = len(self.data["user"])
            template = self.templates["user"].copy()
            template["id"] = index
            template["status"] = status
            template["user_name"] = user_name
            template["user_id"] = user_id
            template["contact"] = contact
            self.data["user"].append(template)
            return True
        except Exception:
            return False

    def set_review(self,
                   place_id: int,
                   user_name: str,
                   user_link: str,
                   text: str,
                   rating: float):
        try:
            index = len(self.data["review"])
            template = self.templates["review"].copy()
            template["id"] = index
            template["place_id"] = place_id
            template["user_name"] = user_name
            template["user_link"] = user_link
            template["text"] = text
            template["rating"] = rating
            self.data["review"].append(template)
            return True
        except Exception:
            return False

    def set_reserve(self,
                    place_id: int,
                    user_name: str,
                    user_link: str,
                    date: str,
                    time: str,
                    user_number: str):
        try:
            index = len(self.data["reserve"])
            template = self.templates["reserve"].copy()
            template["id"] = index
            template["place_id"] = place_id
            template["user_name"] = user_name
            template["user_link"] = user_link
            template["date"] = date
            template["time"] = time
            template["user_name"] = user_name
            self.data["reserve"].append(template)
            return True
        except Exception:
            return False

    def set_place_admin(self,
                        place_id: int,
                        user_name: str,
                        user_id: str):
        index = len(self.data["place_admin"])
        template = self.templates["place_admin"].copy()
        template["id"] = index
        template["place_id"] = place_id
        template["user_name"] = user_name
        template["user_id"] = user_id
        self.data["place_admin"].append(template)

    def get_all_data(self, table: str) -> list:
        places = list()
        for elem in self.data[table]:
            places.append(elem)
        return places

    def get_one_from_one(self,
                         table: str,
                         key: str) -> list:
        data_back = list()
        for elem in self.data[table]:
            data_back.append(elem[key])
        return data_back

    def get_one_from_one_if(self,
                            table: str,
                            key: str,
                            if_key: str,
                            if_value: str,
                            value_type: str = "str",
                            ) -> list:
        data_back = list()
        for elem in self.data[table]:
            if value_type == "int":
                if_value = int(if_value)
            if elem[if_key] == if_value:
                data_back.append(elem[key])
        return data_back

    def get_object(self, table: str, object_id: int) -> dict:
        for elem in self.data[table]:
            if elem["id"] == object_id:
                return elem

    def get_places_titles(self) -> list:
        data_back = list()
        for elem in self.data["place"]:
            data_back.append(elem["title"])
        return data_back

    def get_place_data(self, title: str) -> dict:
        for elem in self.data["place"]:
            if elem["title"] == title:
                return elem

    #######################

    def get_place_info(self, title) -> dict:
        for elem in self.data["place"]:
            if elem["title"] == title:
                return elem

    def get_announce_info_for_title(self, title: str) -> dict:
        for elem in self.data["announce"]:
            if elem["title"] == title:
                return elem

    def get_announce_info_for_place(self, place_id: int, title: str) -> dict:
        for elem in self.data["announce"]:
            if elem["title"] == title and elem["place_id"] == place_id:
                return elem

    def get_place_category(self) -> [bool, list]:
        titles = list()
        for elem in self.data["place_category"]:
            titles.append(elem["title"])
        return [len(titles) > 0, titles]

    def get_announce_category(self) -> [bool, list]:
        titles = list()
        for elem in self.data["announce_category"]:
            titles.append(elem["title"])
        return [len(titles) > 0, titles]

    def get_place_from_category(self, category_id: int) -> [bool, list]:
        places = list()
        for elem in self.data["place"]:
            if elem["category_id"] == category_id:
                places.append(elem["title"])
        return [len(places) > 0, places]

    def get_announce_from_category(self, category_id: int) -> [bool, list]:
        announces = list()
        for elem in self.data["announce"]:
            if elem["category_id"] == category_id:
                announces.append(elem["title"])
        return [len(announces) > 0, announces]

    def get_suitable_place(self, title: str) -> [bool, list]:
        places = list()
        for elem in self.data["place"]:
            if title in elem["title"]:
                places.append(elem["title"])
        return [len(places) > 0, places]

    def get_near_position_place(self, position: str, radius: float = 5.0) -> [bool, list]:
        user_lat = position.split("_")[0]
        user_long = position.split("_")[1]
        places = list()
        for elem in self.data["place"]:
            place_pos = elem["position"].split("_")
            place_lat = place_pos[0]
            place_long = place_pos[1]
            distance = round(GD((user_lat, user_long), (place_lat, place_long)).km, 2)
            if distance <= radius:
                places.append(elem["title"])
        return [len(places) > 0, places]

    def get_meal_list(self, place_id: int) -> [bool, list]:
        meal_list = list()
        for elem in self.data["menu"]:
            if elem["place_id"] == place_id:
                meal_list.append(elem["title"])
        return [len(meal_list) > 0, meal_list]

    def get_meal_info(self, title: str, place_id: int) -> dict:
        for elem in self.data["menu"]:
            if elem["title"] == title and elem["place_id"] == place_id:
                return elem

    def get_all_place_review(self, place_id: int) -> [bool, [dict]]:
        reviews = list()
        for elem in self.data["review"]:
            if elem["place_id"] == place_id:
                reviews.append(elem)
        return [len(reviews) > 0, reviews]
    #
    # def get_all_review(self):
    #     for elem in self.data["review"]:
    #         print(elem["user_name"])

    def get_place_announce(self, place_id: int) -> [bool, list]:
        announces = list()
        for elem in self.data["announce"]:
            if elem["place_id"] == place_id:
                announces.append(elem["title"])
        return [len(announces) > 0, announces]

    def set_new_review(self,
                       place_id: int,
                       user_name: str,
                       user_link: str,
                       text: str,
                       rating: float):
        try:
            index = len(self.data["review"])
            template = self.templates["review"].copy()
            template["id"] = index
            template["place_id"] = place_id
            template["user_name"] = user_name
            template["user_link"] = user_link
            template["text"] = text
            template["rating"] = rating
            self.data["review"].append(template)
            return True
        except Exception:
            return False

    def set_new_reserve(self,
                        place_id: int,
                        user_name: str,
                        user_link: str,
                        date: str,
                        time: str,
                        user_number: str):
        try:
            index = len(self.data["reserve"])
            template = self.templates["reserve"].copy()
            template["id"] = index
            template["place_id"] = place_id
            template["user_name"] = user_name
            template["user_link"] = user_link
            template["date"] = date
            template["time"] = time
            template["user_number"] = user_number
            self.data["reserve"].append(template)
            return True
        except Exception:
            return False

    def get_all_reserves(self):
        for elem in self.data["reserve"]:
            print(elem)

    ################################

    def user_exist(self, user_id: str) -> bool:
        for elem in self.data["user"]:
            if elem["user_id"] == user_id:
                return True
        return False

    def set_new_admin(self, user_id: str) -> bool:
        for elem in self.data["user"]:
            if elem["user_id"] == user_id:
                elem["status"] = "admin"
                return True
        return False

    def user_is_admin(self, user_id: str) -> bool:
        for elem in self.data["user"]:
            if elem["user_id"] == user_id:
                if elem["status"] == "admin":
                    return True
        return False

    def user_is_pa(self, user_id: str) -> bool:
        for elem in self.data["place_admin"]:
            if elem["user_id"] == user_id:
                if elem["place_admin"] == "admin":
                    return True
        return False

    def place_category_exist(self, place_category_title: str) -> bool:
        for elem in self.data["place_category"]:
            if elem["title"] == place_category_title:
                return True
        return False

    def place_exist(self, place_title: str) -> bool:
        for elem in self.data["place"]:
            if elem["title"] == place_title:
                return True
        return False

    def get_place_category_list(self) -> list:
        category_list = list()
        for elem in self.data["place_category"]:
            category_list.append(elem["title"])
        return category_list

    def get_announce_category_list(self) -> list:
        category_list = list()
        for elem in self.data["announce_category"]:
            category_list.append(elem["title"])
        return category_list

    def get_place_list(self) -> list:
        place_list = list()
        for elem in self.data["place"]:
            place_list.append(elem["title"])
        return place_list

    def announce_category_exist(self, category_title: str) -> bool:
        for elem in self.data["announce_category"]:
            if elem["title"] == category_title:
                return True
        return False

    def announce_exist(self, announce_title: str) -> bool:
        for elem in self.data["announce"]:
            if elem["title"] == announce_title:
                return True
        return False

    def get_place_category_id(self, title: str) -> int:
        for elem in self.data["place_category"]:
            if elem["title"] == title:
                return elem["id"]

    def get_announce_category_id(self, title: str) -> int:
        for elem in self.data["announce_category"]:
            if elem["title"] == title:
                return elem["id"]

    def get_place_id(self, title: str) -> int:
        for elem in self.data["place"]:
            if elem["title"] == title:
                return elem["id"]

    def get_place_description(self, place_id: int) -> str:
        for elem in self.data["place"]:
            if elem["id"] == place_id:
                return elem["description"]

    def get_place_contact(self, place_id: int) -> str:
        for elem in self.data["place"]:
            if elem["id"] == place_id:
                return elem["contact"]

    def get_place_site(self, place_id: int) -> str:
        for elem in self.data["place"]:
            if elem["id"] == place_id:
                return elem["site"]
    """
    Also needed function:
    set_user
    set_category_place
    set_category_announce
    set_place
    set_announce
    """

