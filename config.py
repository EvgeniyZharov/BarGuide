from aiogram.dispatcher.filters.state import StatesGroup, State


MAIN_TOKEN = "6486870977:AAHeE8jNCvaGlmFfmWsLTHPzxhr0lKeAR40"

host = "185.212.148.117"
user = "user_4"
password = "passWORD1234!"


class FSMWorkProgram(StatesGroup):
    # Status for main menu
    main_menu = State()

    # 1-st variation work - get all places for category
    get_place_category = State()

    # 2-nd variation work - find place for it`s title
    set_title_place = State()

    # 3-rd variation work - find place for location
    set_self_location = State()

    # 4-st variation work - get all announces for category
    get_announce_category = State()
    get_announce = State()

    # Base states 1. For work with places info
    get_place = State()
    choice_place = State()
    # get_reviews = State()
    get_menu = State()
    get_meal = State()
    get_announces = State()
    set_review = State()
    set_review_rating = State()
    set_review_text = State()
    save_new_review = State()
    set_name_reservist = State()
    set_phone_reservist = State()
    set_date_reserve = State()
    set_time_reserve = State()
    set_count_visitors = State()
    save_reserve = State()
    save_new_reserve = State()

    # Admin work
    to_admin_main_menu = State()
    admin_main_menu = State()
    admin_settings = State()

    place_settings_option = State()
    # Place category settings
    set_place_category = State()
    set_place_category_title = State()
    set_place_category_description = State()
    save_new_place_category = State()
    # Place settings
    set_place = State()
    set_place_category_id = State()
    set_place_title = State()
    set_place_description = State()
    set_place_address = State()
    set_place_site_link = State()
    set_place_photo = State()
    set_place_contact = State()
    set_place_work_time = State()
    save_new_place = State()

    announce_settings_option = State()
    # Announce category settings
    set_announce_category = State()
    set_announce_category_title = State()
    set_announce_category_description = State()
    save_new_announce_category = State()
    # Announce settings
    set_announce = State()
    set_announce_category_id = State()
    set_announce_place_id = State()
    set_announce_title = State()
    set_announce_description = State()
    set_announce_price = State()
    set_announce_link_ticker = State()
    set_announce_date = State()
    set_announce_time = State()
    set_announce_photo = State()

    # Place admin work
    start_create_pa = State()
    pa_main_menu = State()

    pa_settings_menu = State()
    # Settings of place information

    # Settings of announce information

    # Settings of menu information

    pa_reserve_menu = State()
    # Show list of reserves

