# TITLES
CAPTION = 'Digital Radio Stations'

""" ------------------------------- """
""" --------- WINDOW SIZE --------- """
""" ------------------------------- """
# PLAYER WINDOW SIZES
PLAYER_SIZE = [400, 150]
# FAVOURITES WINDOW SIZES
FAVOURITES_SIZE = [400, 200]
# SEARCH WINDOW SIZES
SEARCH_SIZE = [400, 400]

LOGO_POS = [95, 30]
LOGO_SIZE = [200, 50]

""" ------------------------------- """
""" --------- PLAYER BTNS --------- """
""" ------------------------------- """
# PLAYER BUTTONS POSITIONS
PREV_BUTTON_POS = [60, 90]
PLAY_BUTTON_POS = [120, 90]
PAUSE_BUTTON_POS = [180, 90]
NEXT_BUTTON_POS = [240, 90]
FAVOURITE_BUTTON_POS = [365, 35]
SEARCH_BUTTON_POS = [365, 72]
SAVE_BUTTON_POS = [365, 110]
# PLAYER BUTTONS SIZES
PREV_BUTTON_SIZE = [50, 50]
PLAY_BUTTON_SIZE = [50, 50]
PAUSE_BUTTON_SIZE = [50, 50]
NEXT_BUTTON_SIZE = [50, 50]
FAVOURITE_BUTTON_SIZE = [25, 25]
SEARCH_BUTTON_SIZE = [25, 25]
SAVE_BUTTON_SIZE = [25, 25]

""" ------------------------------- """
""" --------- FAVOUR BTNS --------- """
""" ------------------------------- """
# FAVOURITES BUTTONS POSITIONS
TRASH_BUTTON_POS = [310, 53]
NEXT_FAVS_POS = [350, 90]
PREV_FAVS_POS = [12, 90]
# FAVOURITES BUTTONS SIZES
TRASH_BUTTON_SIZE = [15, 15]
NEXT_FAVS_SIZE = [38, 38]
PREV_FAVS_SIZE = [38, 38]
""" ------------------------------- """
""" --------- SEARCH BTNS --------- """
""" ------------------------------- """
# SEARCH BUTTONS POSITIONS
SEARCH_ACTION_BUTTON_POS = [360, 10]
NEXT_PAGE_POS = [350, 200]
PREV_PAGE_POS = [0, 200]
SEARCH_BY_NAME_POS = [50, 35]
SEARCH_BY_TAG_POS = [154, 35]
SEARCH_BY_COUNTRY_POS = [258, 35]
CLEAN_SEARCH_POS = [320, 14]
# SEARCH BUTTONS SIZES
SEARCH_ACTION_BUTTON_SIZE = [25, 25]
NEXT_PAGE_SIZE = [50, 50]
PREV_PAGE_SIZE = [50, 50]
SEARCH_BY_NAME_SIZE = [90, 30]
SEARCH_BY_TAG_SIZE = [90, 30]
SEARCH_BY_COUNTRY_SIZE = [90, 30]
CLEAN_SEARCH_SIZE = [18, 18]

""" ------------------------------- """
""" --------- SHARED BTNS --------- """
""" ------------------------------- """
# SHARED BUTTONS POSITIONS
BACK_BUTTON_POS = [10, 10]
# SHARED BUTTONS SIZES
BACK_BUTTON_SIZE = [25, 25]

# PATH TO:
MAIN_ICON = "graphics/misc/icon.ico"
BG_01 = 'graphics/misc/bgplayer.png'
BG_02 = 'graphics/misc/bggeneric.png'
DRSOK = 'graphics/misc/drsok.png'
FAVOURITES = 'graphics/favourites/title.png'

# HEXADECIMAL COLORS
DEBUG_COLOR = "#d50000"                 # RED HEX
SCREEN_FILL = "#000000"                 # BLACK HEX

# RGB COLORS
PLAYER_TEXT_COLOR = (0, 0, 0)           # BLACK RGB
PLAYER_TEXT_BG_COLOR = (250, 250, 250)  # WHITE RGB
SEARCH_TERM_TEXT_COLOR = (0, 0, 0)      # BLACK RGB

""" -------------------------------- """
""" --------- PROGRAM VARS --------- """
""" -------------------------------- """
# CONTROL VARS
DEBUG = False
PLAYER_IS_OPEN = True
FAVOURITES_IS_OPEN = False
SEARCH_IS_OPEN = False
STATION_IS_SELECTED = False

# SEARCH VARS
NEW_SEARCH = False
GO_SEARCH = False
RESULTS = False
COUNTRIES = False
SEARCH_BY_NAME_ON = True
SEARCH_BY_TAGS_ON = False
SEARCH_BY_COUNTRY_ON = False

# FAVOURITES VARS
DELETE_FAV = False
FAV_DATA_FILE_NAME = "favourites.json"

# EVENTS
MOUSE_POSITION = None
CLICK_COUNT = 0

# TEXTS
PLAYER_MESSAGE_DISPLAY = "BIENVENID@ A DRSOK, MÁS DE 37000 EMISORAS DE RADIO DE TODO EL MUNDO, EN UNOS POCOS PÍXELES!"
SEARCH_TERM = ""
SEARCH_RESULT = []
SEARCH_RESULT_LENGTH = 40
FAVOURITES_RESULT_LENGTH = 30
