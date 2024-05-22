from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import MAIN_TOKEN, host, user, password
###############
from dataClient.db_mysql import DataClient


data_client = DataClient(host=host, user=user, password=password)


# data_client = DBClient(host=host, user=user, password=password)
# data_client.drop_all_tables()
# data_client = DBClient(host=host, user=user, password=password)
# testing
# data_client.set_place_category(title="test 11", description="testings")
# data_client.set_place(category_id=1, title="test 2", description="testings 2",
#                       address="some_address", site="some_site", contact="some contact",
#                       work_time="7-20", photo_id="AgACAgIAAxkBAAIHMGXBAWcxTpDHJpFBczoqSCF40PBaAALe1jEbDBsJSkEMJpgpnF_eAQADAgADeQADNAQ")
# data_client.set_announce_category(title="test 3", description="testings 3")
# data_client.set_announce(category_id=1, place_id=1, title="test 4", description="testings 4",
#                          ticker_price="1200rub", ticker_link="some link", date="10.02.2024",
#                          time_value="20:00", photo_id="AgACAgIAAxkBAAIHMGXBAWcxTpDHJpFBczoqSCF40PBaAALe1jEbDBsJSkEMJpgpnF_eAQADAgADeQADNAQ")
# data_client.set_user(name="some_name", tg_id="some tg id", contact="some contact")
# data_client.set_menu(place_id=1, title="test 5", description="testings 5", composition="some products",
#                      price="720rub", image_id="AgACAgIAAxkBAAIHMGXBAWcxTpDHJpFBczoqSCF40PBaAALe1jEbDBsJSkEMJpgpnF_eAQADAgADeQADNAQ")
# data_client.set_review(place_id=1, user_name="some user", user_id="some_id", text="some review", rating=5)
# data_client.set_reserve(place_id=1, user_name="some name", user_id="some id", date="12.02.2024",
#                         time_value="18:00", user_number="some number")
# data_client.set_place_admin(place_id=1, user_name="some name", user_id="some_id")
# print(data_client.get_table_info("user"))
# print(data_client.get_suitable_place(title="test 2"))
# print(data_client.get_place_list(1))
#
# print(data_client.get_place_from_category(1))
# print(data_client.get_place_category_id("test 1"))
# print("dassfdasf")
# print(data_client.get_place_category_list())
# print(data_client.get_announce_category_list())
# print(data_client.get_place_list(0))
# print(data_client.get_exist(f"EXIST (SELECT * FROM {data_client.DATABASE_NAME}.user);"))

##############
storage = MemoryStorage()

bot = Bot(token=MAIN_TOKEN)
dp = Dispatcher(bot, storage=storage)


