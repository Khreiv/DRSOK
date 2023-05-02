from main import pg
import config as cf

# INIT WINDOW
pg.init()
# WINDOW ATTRIBUTES
pg.display.set_caption(cf.CAPTION)
# CREATE WINDOW
root = pg.display.set_mode((cf.PLAYER_SIZE[0], cf.PLAYER_SIZE[1]))
# SET ICON PATH
icon = pg.image.load(cf.MAIN_ICON)
# DISPLAY ICON
pg.display.set_icon(icon)
# FONTS
font = pg.font.Font(None, 16)
# TIME CONTROL
time = pg.time.get_ticks()

bg01 = pg.image.load(cf.BG_01).convert_alpha()
bg02 = pg.image.load(cf.BG_02).convert_alpha()
player_title = pg.image.load(cf.DRSOK)
favourites_title = pg.image.load(cf.FAVOURITES).convert_alpha()


def load_button_image(image_path):
    # ADD IMAGE PATHS
    return pg.image.load(image_path).convert_alpha()


def enlist_buttons(positions, sizes, images):
    # COLLECT BUTTONS ON A LIST
    button_list = []
    for i in range(len(positions)):
        pos = positions[i]
        size = sizes[i]
        img = images[i]
        rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        button_list.append({'img': img, 'rect': rect, 'state': False})
    return button_list


def draw_buttons(button_list):
    # DRAW BUTTONS
    for button in button_list:
        root.blit(button['img'], button['rect'])


def draw_results(result, offset, surface, length):
    # DRAW ONE LINE OF RESULTS
    if len(result) > length:
        result = (result[:40] + "...")
    text = font.render(result.upper().strip(), True, cf.SEARCH_TERM_TEXT_COLOR)
    text_name_surface = text.get_rect()
    text_name_surface.topleft = surface.left + 3, surface.top + 5 + offset

    root.blit(text, text_name_surface)

    return text_name_surface


def draw_background(image, size1, size2):
    root.blit(image, (0, -30))
    pg.draw.rect(root, cf.PLAYER_TEXT_COLOR, (0, 0, size1, size2), 3)


def draw_surface(surface):
    # TEXT SURFACE FILL
    pg.draw.rect(root, cf.PLAYER_TEXT_BG_COLOR, surface)
    # TEXT SURFACE BORDER
    pg.draw.rect(root, cf.PLAYER_TEXT_COLOR, surface, 2)


def draw_debug(button_list):
    if cf.DEBUG:
        # DRAW CONTROL RECT
        for button in button_list:
            pg.draw.rect(root, cf.DEBUG_COLOR, button['rect'], 2)


class SearchInterface(object):
    def __init__(self):
        super(SearchInterface, self).__init__()

        # BUTTONS IMAGES
        self.back_button_img = load_button_image("graphics/shared/backw.png")
        self.search_button_img = load_button_image("graphics/search/searchw.png")
        self.next_page_img = load_button_image("graphics/search/next_pg.png")
        self.previous_page_img = load_button_image("graphics/search/prev_pg.png")
        self.search_by_name_img = load_button_image("graphics/search/by_name.png")
        self.search_by_tag_img = load_button_image("graphics/search/by_tag.png")
        self.search_by_country_img = load_button_image("graphics/search/by_country.png")
        self.clean_search_img = load_button_image("graphics/search/clean_search.png")

        # PRESSED BUTTONS IMAGES
        self.press_search_by_name_img = load_button_image("graphics/search/by_namew.png")
        self.press_search_by_tag_img = load_button_image("graphics/search/by_tagw.png")
        self.press_search_by_country_img = load_button_image("graphics/search/by_countryw.png")

        # BUTTONS ATTRIBUTES
        button_positions = [cf.BACK_BUTTON_POS, cf.SEARCH_ACTION_BUTTON_POS, cf.NEXT_PAGE_POS, cf.PREV_PAGE_POS,
                            cf.SEARCH_BY_NAME_POS, cf.SEARCH_BY_TAG_POS, cf.SEARCH_BY_COUNTRY_POS, cf.CLEAN_SEARCH_POS]

        button_sizes = [cf.BACK_BUTTON_SIZE, cf.SEARCH_ACTION_BUTTON_SIZE, cf.NEXT_PAGE_SIZE, cf.PREV_PAGE_SIZE,
                        cf.SEARCH_BY_NAME_SIZE, cf.SEARCH_BY_TAG_SIZE, cf.SEARCH_BY_COUNTRY_SIZE, cf.CLEAN_SEARCH_SIZE]

        self.button_images = [self.back_button_img, self.search_button_img, self.next_page_img, self.previous_page_img,
                              self.search_by_name_img, self.search_by_tag_img, self.search_by_country_img,
                              self. clean_search_img]

        # LIST OF BUTTONS
        self. buttons = enlist_buttons(button_positions, button_sizes, self.button_images)

        # TEXT SURFACE
        self.text_surface = pg.Rect(50, 12, cf.PLAYER_SIZE[0] - 140, 20)

        # RESULTS SURFACE
        self.results_surface = pg.Rect(50, 68, cf.PLAYER_SIZE[0] - 100, 330)

    def draw_search_text(self):
        # TEXT DRAW
        text = font.render(cf.SEARCH_TERM.upper().strip(), True, cf.SEARCH_TERM_TEXT_COLOR)
        text_name_surface = text.get_rect()
        text_name_surface.topleft = self.text_surface.left + 3, self.text_surface.top + 5
        root.blit(text, text_name_surface)

    def select_image_buttons_and_draw(self):
        # DRAW BUTTONS
        if cf.SEARCH_BY_NAME_ON:
            self.buttons[4]['img'] = self.press_search_by_name_img
            self.buttons[5]['img'] = self.search_by_tag_img
            self.buttons[6]['img'] = self.search_by_country_img
        elif cf.SEARCH_BY_TAGS_ON:
            self.buttons[4]['img'] = self.search_by_name_img
            self.buttons[5]['img'] = self.press_search_by_tag_img
            self.buttons[6]['img'] = self.search_by_country_img
        elif cf.SEARCH_BY_COUNTRY_ON:
            self.buttons[4]['img'] = self.search_by_name_img
            self.buttons[5]['img'] = self.search_by_tag_img
            self.buttons[6]['img'] = self.press_search_by_country_img

        draw_buttons(self.buttons)

    def draw(self):
        draw_background(bg02, cf.SEARCH_SIZE[0], cf.SEARCH_SIZE[1])
        draw_surface(self.results_surface)
        draw_surface(self.text_surface)
        self.draw_search_text()
        self.select_image_buttons_and_draw()
        # DRAW CONTROL RECT
        if cf.SEARCH_IS_OPEN:
            draw_debug(self.buttons)


class FavouritesInterface(object):
    def __init__(self):
        super(FavouritesInterface, self).__init__()

        # BUTTONS IMAGES
        self.back_button_img = load_button_image("graphics/shared/backw.png")
        self.trash_button_img = load_button_image("graphics/favourites/trash.png")
        self.next_page = load_button_image("graphics/favourites/next_pg.png")
        self.previous_page = load_button_image("graphics/favourites/prev_pg.png")

        # BUTTONS ATTRIBUTES
        button_positions = [cf.BACK_BUTTON_POS, cf.NEXT_FAVS_POS, cf.PREV_FAVS_POS]

        button_sizes = [cf.BACK_BUTTON_SIZE, cf.NEXT_FAVS_SIZE, cf.PREV_FAVS_SIZE]

        button_images = [self.back_button_img, self.next_page, self.previous_page]

        # LIST OF MAIN BUTTONS
        self.buttons = enlist_buttons(button_positions, button_sizes, button_images)

        # RESULTS SURFACE
        self.favs_surface = pg.Rect(70, 50, cf.FAVOURITES_SIZE[0] - 140, 140)

    def draw_favourites_delete(self, offset):
        button_rect = pg.Rect((cf.TRASH_BUTTON_POS[0], cf.TRASH_BUTTON_POS[1] + offset,
                               cf.TRASH_BUTTON_SIZE[0], cf.TRASH_BUTTON_SIZE[1]))

        root.blit(self.trash_button_img, button_rect)

        return button_rect

    def draw(self):
        draw_background(bg02, cf.FAVOURITES_SIZE[0], cf.FAVOURITES_SIZE[1])
        draw_buttons(self.buttons)
        draw_surface(self.favs_surface)
        root.blit(favourites_title, (cf.FAVOURITES_SIZE[0] / 2 - 60, 10))
        # DRAW CONTROL RECT
        if cf.FAVOURITES_IS_OPEN:
            draw_debug(self.buttons)


class PlayerInterface(object):
    def __init__(self):
        super(PlayerInterface, self).__init__()

        # BUTTONS IMAGES
        self.previous_button_img = load_button_image("graphics/player/prevw.png")
        self.play_button_img = load_button_image("graphics/player/playw.png")
        self.pause_button_img = load_button_image("graphics/player/pausew.png")
        self.next_button_img = load_button_image("graphics/player/nextw.png")

        self.favourites_button_img = load_button_image("graphics/player/openfavw.png")
        self.search_button_img = load_button_image("graphics/player/searchw.png")
        self.save_station_button_img = load_button_image("graphics/player/savefavw.png")

        # PRESSED BUTTONS IMAGES
        self.press_previous_button_img = load_button_image("graphics/player/prev.png")
        self.press_play_button_img = load_button_image("graphics/player/play.png")
        self.press_pause_button_img = load_button_image("graphics/player/pause.png")
        self.press_next_button_img = load_button_image("graphics/player/next.png")

        self.press_favourites_button_img = load_button_image("graphics/player/openfav.png")
        self.press_search_button_img = load_button_image("graphics/player/search.png")
        self.press_save_station_button_img = load_button_image("graphics/player/savefav.png")

        # BUTTONS ATTRIBUTES
        button_positions = [cf.PREV_BUTTON_POS, cf.PLAY_BUTTON_POS, cf.PAUSE_BUTTON_POS, cf.NEXT_BUTTON_POS,
                            cf.FAVOURITE_BUTTON_POS, cf.SEARCH_BUTTON_POS, cf.SAVE_BUTTON_POS]

        button_sizes = [cf.PREV_BUTTON_SIZE, cf.PLAY_BUTTON_SIZE, cf.PAUSE_BUTTON_SIZE, cf.NEXT_BUTTON_SIZE,
                        cf.FAVOURITE_BUTTON_SIZE, cf.SEARCH_BUTTON_SIZE, cf.SAVE_BUTTON_SIZE]

        self.button_images = [self.previous_button_img, self.play_button_img, self.pause_button_img,
                              self.next_button_img, self.favourites_button_img, self.search_button_img,
                              self.save_station_button_img]

        self.press_button_images = [self.press_previous_button_img, self.press_play_button_img,
                                    self.press_pause_button_img, self.press_next_button_img,
                                    self.press_favourites_button_img, self.press_search_button_img,
                                    self.press_save_station_button_img]

        # LIST OF BUTTONS
        self. buttons = enlist_buttons(button_positions, button_sizes, self.button_images)

        # TEXT FRAME
        self.text_surface = pg.Rect(0, 8, cf.PLAYER_SIZE[0], 20)

        # TEXT IN MOVEMENT
        self.text = font.render(cf.PLAYER_MESSAGE_DISPLAY.upper(), True, cf.PLAYER_TEXT_COLOR)
        self.text_rect = self.text.get_rect()
        self.text_x = cf.PLAYER_SIZE[0] + 280
        self.text_speed = -2

    def draw_text(self):
        # TEXT MOVEMENT
        self.text_x += self.text_speed
        # TEXT MARGIN
        if self.text_x < -len(cf.PLAYER_MESSAGE_DISPLAY)*2.3:
            self.text_x = cf.PLAYER_SIZE[0] * 1.8
        # TEXT CENTER
        self.text_rect.center = (self.text_x, 18)

        # DRAW TEXT
        root.blit(self.text, self.text_rect)

    def draw(self):
        draw_background(bg01, cf.PLAYER_SIZE[0], cf.PLAYER_SIZE[1])
        draw_surface(self.text_surface)
        self.draw_text()
        draw_buttons(self.buttons)
        root.blit(player_title, (-5, 8))
        # DRAW CONTROL RECT
        if cf.PLAYER_IS_OPEN:
            draw_debug(self.buttons)
