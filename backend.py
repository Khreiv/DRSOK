from main import pg
import json
import vlc
import sys
import os

import api
import config as cf
import interface as gui


def button_count():
    """ Function counting back for restoring the 'click image' """
    if cf.CLICK_COUNT == 1000:
        cf.CLICK_COUNT = 0
        return False
    else:
        cf.CLICK_COUNT += 1


def restore_buttons(all_buttons, on_images, off_images):
    """ Changing states based on the button counting """
    for button in range(len(all_buttons)):
        if all_buttons[button]['state']:
            all_buttons[button]['img'] = off_images[button]
            all_buttons[button]['state'] = button_count()
        else:
            all_buttons[button]['img'] = on_images[button]


def switch_player_mode(player, favourites, search):
    """ Switch between player modes: Player, Favourites and Search """
    cf.PLAYER_IS_OPEN = player
    cf.FAVOURITES_IS_OPEN = favourites
    cf.SEARCH_IS_OPEN = search


def click_back_to_player_btn():
    """ Switch back to player mode """
    if cf.FAVOURITES_IS_OPEN or cf.SEARCH_IS_OPEN:
        print("BACK")
        cf.PLAYER_IS_OPEN = True
        cf.FAVOURITES_IS_OPEN = False
        cf.SEARCH_IS_OPEN = False
        gui.root = pg.display.set_mode((cf.PLAYER_SIZE[0], cf.PLAYER_SIZE[1]))


class Backend:
    def __init__(self):
        super(Backend, self).__init__()
        # INIT INTERFACE CLASSES
        self.player = gui.PlayerInterface()
        self.favourites = gui.FavouritesInterface()
        self.search = gui.SearchInterface()
        # MEDIA PLAYER CONFIG
        self.options_audio = '--aout=directx'
        self.options_video = '--no-video'
        self.instance = vlc.Instance(self.options_audio, self.options_video)
        self.media_player = self.instance.media_player_new()
        # SEARCH TERM
        self.text = ""
        # API DATA VARS
        self.names = []
        self.links = []
        self.countries = []
        # SELECTED DATA
        self.selected_link = ""
        self.selected_name = ""
        self.selected_country = ""
        # DATA RECT LISTS
        self.result_rects = []
        self.link_rects = []
        self.name_rects = []
        self.country_rects = []
        # FAVOURITE DATA LISTS
        self.loaded_data = []
        self.data_names = []
        self.data_links = []
        self.favourite_rects = []
        self.delete_rects = []
        self.favourites_to_show = []
        # DATA VOLUMES MANAGEMENT VARS
        self.favourite_index = 0
        self.max_number_of_results = 20
        self.min_number_of_results = 0
        self.max_number_of_favourites = 7
        self.min_number_of_favourites = 0

        self.player_functions = [lambda: self.click_pev_next_station(True),
                                 self.click_play_station,
                                 self.click_pause_station,
                                 lambda:self.click_pev_next_station(False),
                                 self.click_favourites,
                                 self.click_search,
                                 self.click_save_favourite]

        self.search_functions = [click_back_to_player_btn,
                                 lambda: self.click_search_action_btn(True),
                                 lambda: self.click_prev_next_result_page(False),
                                 lambda: self.click_prev_next_result_page(True),
                                 lambda: self.switch_search_mode(True, False, False),
                                 lambda: self.switch_search_mode(False, True, False),
                                 self.click_search_by_country,
                                 self.click_clean_search]

        self.favourites_functions = [click_back_to_player_btn,
                                     lambda: self.click_prev_next_favourites(False),
                                     lambda: self.click_prev_next_favourites(True)]

    """ PLAYER INTERFACE BUTTONS """
    def click_save_favourite(self):
        self.player.buttons[6]['state'] = not self.player.buttons[6]['state']
        if cf.PLAYER_IS_OPEN:
            if cf.STATION_IS_SELECTED:
                try:
                    self.load_data()
                    self.loaded_data.append([self.selected_name, self.selected_link])

                    with open(cf.FAV_DATA_FILE_NAME, 'w') as favs:
                        json.dump(self.loaded_data, favs)

                except Exception as e:
                    print(f"BACKEND: func: SAVE RADIO STATION {e}")
                    pass

    def click_search(self):
        print("SEARCH")
        self.player.buttons[5]['state'] = not self.player.buttons[5]['state']
        switch_player_mode(False, False, True)
        gui.root = pg.display.set_mode((cf.SEARCH_SIZE[0], cf.SEARCH_SIZE[1]))

    def click_favourites(self):
        print("FAVOURITES")
        self.player.buttons[4]['state'] = not self.player.buttons[4]['state']
        switch_player_mode(False, True, False)

        self.max_number_of_favourites = 8
        self.min_number_of_favourites = 0

        self.load_data()

        gui.root = pg.display.set_mode((cf.FAVOURITES_SIZE[0], cf.FAVOURITES_SIZE[1]))

    def click_play_station(self):
        print("PLAY")
        self.player.buttons[1]['state'] = not self.player.buttons[1]['state']
        self.play_protocol()

    def click_pause_station(self):
        print("PAUSE")
        self.player.buttons[2]['state'] = not self.player.buttons[2]['state']
        self.media_player.stop()

    def click_pev_next_station(self, prev):
        if prev:
            self.player.buttons[0]['state'] = not self.player.buttons[0]['state']
            if self.favourite_index > 0:
                self.favourite_index -= 1
        else:
            self.player.buttons[3]['state'] = not self.player.buttons[3]['state']
            if self.favourite_index < len(self.data_links) - 1:
                self.favourite_index += 1

        self.selected_link = self.data_links[self.favourite_index]
        self.selected_name = self.data_names[self.favourite_index]

        self.play_protocol()

    """ SEARCH INTERFACE BUTTONS """
    def switch_search_mode(self, by_name, by_tag, by_country):
        """ Switch states between search modes """
        cf.GO_SEARCH = False
        cf.SEARCH_BY_NAME_ON = by_name
        cf.SEARCH_BY_TAGS_ON = by_tag
        cf.SEARCH_BY_COUNTRY_ON = by_country
        self.reset_stats()

    def click_search_by_country(self):
        self.switch_search_mode(False, False, True)
        cf.COUNTRIES = True
        cf.GO_SEARCH = True
        self.reset_results_number()
        try:
            self.countries = api.collect_country_info('name')
            print(self.countries)
        except Exception as e:
            print(f"BACKEND: func: GET COUNTRIES {e}")

    def click_search_action_btn(self, new_search):
        print("SEARCHING")
        cf.GO_SEARCH = True
        self.reset_stats()
        if new_search:
            self.reset_results_number()

        self.get_data()

    def click_prev_next_result_page(self, prev):
        print("NEXT PAGE")
        self.reset_stats()

        if cf.COUNTRIES:
            if prev:
                if self.min_number_of_results > 0:
                    self.max_number_of_results -= 20
                    self.min_number_of_results -= 20
            else:
                if len(self.countries) > self.max_number_of_results:
                    self.max_number_of_results += 20
                    self.min_number_of_results += 20

            self.draw_countries()

        else:
            if prev:
                if self.min_number_of_results > 0:
                    self.max_number_of_results -= 20
                    self.min_number_of_results -= 20
            else:
                if len(self.names) > self.max_number_of_results:
                    self.max_number_of_results += 20
                    self.min_number_of_results += 20

            self.click_search_action_btn(False)

    def click_clean_search(self):
        self.reset_results_number()
        self.reset_stats()

        self.text = ""
        cf.SEARCH_TERM = str(self.text)

    """ SEARCH BY COUNTRY PROTOCOLS """
    def draw_countries(self):
        j = 0
        try:
            for i, result in enumerate(self.countries[self.min_number_of_results:self.max_number_of_results]):
                result_rect = gui.draw_results(result, j * 15,
                                               self.search.results_surface,
                                               cf.SEARCH_RESULT_LENGTH)
                self.result_rects.append(result_rect)
                self.country_rects.append(result)
                j += 1
            cf.RESULTS = True
            cf.COUNTRIES = True
        except Exception as e:
            print(f"BACKEND: func: DRAW COUNTRIES {e}")

    def select_country(self):
        try:
            for i, result_rect in enumerate(self.result_rects):
                if result_rect.collidepoint(cf.MOUSE_POSITION):
                    self.selected_country = self.country_rects[i]
                    self.get_data()
                    self.reset_stats()
                    self.reset_results_number()
                    cf.COUNTRIES = False
                    break
        except Exception as e:
            print(f"BACKEND: func: SELECT COUNTRY {e}")

    """ FAVOURITES INTERFACE BUTTONS """
    def load_data(self):
        try:
            self.reset_stats()
            self.loaded_data.clear()
            self.data_links.clear()
            self.data_names.clear()
            self.favourites_to_show.clear()

            # LOAD DATA
            if os.path.isfile(cf.FAV_DATA_FILE_NAME) and os.stat(cf.FAV_DATA_FILE_NAME).st_size != 0:
                with open(cf.FAV_DATA_FILE_NAME, 'r') as data:
                    self.loaded_data = json.load(data)

                # SELECT LENGTH OF MAX DATA TO SHOW IN ONE PAGE
                if len(self.loaded_data) < self.max_number_of_favourites:
                    max_index = len(self.loaded_data)
                else:
                    max_index = self.max_number_of_favourites

                # GET SLICE OF LOADED DATA
                self.favourites_to_show = self.loaded_data[self.min_number_of_favourites:max_index]

                print(self.favourites_to_show)

                for data in self.favourites_to_show:
                    self.data_names.append(data[0])
                    self.data_links.append(data[1])

        except Exception as e:
            print(f"BACKEND: func: LOAD DATA FROM JSON {e}")
            print(e)
            pass

    def draw_favs(self):
        try:
            for i, data in enumerate(self.data_names):
                fav_rect = gui.draw_results(data, i * 15,
                                            self.favourites.favs_surface,
                                            cf.FAVOURITES_RESULT_LENGTH)
                self.favourite_rects.append(fav_rect)

                delete_rect = self.favourites.draw_favourites_delete(i * 15)
                self.delete_rects.append(delete_rect)

        except Exception as e:
            print(f"BACKEND: func: DRAW FAVS {e}")
            pass

    def delete_fav(self):
        try:
            for i, data in enumerate(self.delete_rects):
                if data.collidepoint(cf.MOUSE_POSITION):
                    del self.loaded_data[self.min_number_of_favourites + i]

                    cf.DELETE_FAV = True
                    break

        except Exception as e:
            print(f"BAKEND: func: DELETE FAV {e}")
            pass

    def save_data(self):
        try:
            with open(cf.FAV_DATA_FILE_NAME, 'w') as favs:
                json.dump(self.loaded_data, favs)

        except Exception as e:
            print(f"BAKEND: func: SAVE DATA IN JSON {e}")
            pass

    def select_favourite(self):
        # SELECT RADIO STATION FROM SEARCH
        try:
            for i, item in enumerate(self.favourite_rects):
                if self.favourite_rects[i].collidepoint(cf.MOUSE_POSITION):
                    self.favourite_index = i
                    self.selected_link = self.data_links[i]
                    self.selected_name = self.data_names[i]

                    self.play_protocol()
                    click_back_to_player_btn()
                    cf.STATION_IS_SELECTED = True
                    break

        except Exception as e:
            print(f"BAKEND: func: SELECT FAVOURITE {e}")
            pass

    def click_prev_next_favourites(self, prev):
        if prev:
            if self.min_number_of_favourites > 0:
                self.max_number_of_favourites -= 8
                self.min_number_of_favourites -= 8
        else:
            if len(self.loaded_data) > self.max_number_of_favourites:
                self.max_number_of_favourites += 8
                self.min_number_of_favourites += 8

        self.load_data()
        self.draw_favs()

    """ COMMON FUNCTIONS """
    def reset_results_number(self):
        self.max_number_of_results = 20
        self.min_number_of_results = 0

    def reset_stats(self):
        # CLEAN RECTS
        self.favourite_rects.clear()
        self.delete_rects.clear()
        self.result_rects.clear()
        self.name_rects.clear()
        self.link_rects.clear()
        self.country_rects.clear()

    def play_protocol(self):
        # STANDARD PROCEDURE FOR PLAYING STATION
        self.player.text_x = cf.PLAYER_SIZE[0] * 1.8
        cf.PLAYER_MESSAGE_DISPLAY = ("--- " + self.selected_name + " --- " + self.selected_link + " ---")
        self.player.text = gui.font.render(cf.PLAYER_MESSAGE_DISPLAY.upper(), True, cf.PLAYER_TEXT_COLOR)

        print(self.selected_link)

        media = self.instance.media_new(self.selected_link)
        self.media_player.set_media(media)
        self.media_player.play()

        self.player.draw_text()

    def get_data(self):
        try:
            if cf.SEARCH_BY_NAME_ON:
                self.names = api.search_by_name('name', cf.SEARCH_TERM.lower())
                self.links = api.search_by_name('url', cf.SEARCH_TERM.lower())
            elif cf.SEARCH_BY_TAGS_ON:
                self.names = api.search_by_tag('name', cf.SEARCH_TERM.lower())
                self.links = api.search_by_tag('url', cf.SEARCH_TERM.lower())
            elif cf.SEARCH_BY_COUNTRY_ON:
                self.names = api.search_by_country('name', self.selected_country)
                self.links = api.search_by_country('url', self.selected_country)

        except Exception as e:
            print(f"BACKEND: func: GET DATA {e}")
            pass

    def draw_results(self):
        try:
            self.name_rects.clear()
            self.link_rects.clear()
            j = 0
            for i, result in enumerate(self.names):
                if self.min_number_of_results <= i <= self.max_number_of_results:
                    result_rect = gui.draw_results(self.names[i], j * 15,
                                                   self.search.results_surface,
                                                   cf.SEARCH_RESULT_LENGTH)
                    self.result_rects.append(result_rect)
                    self.name_rects.append(self.names[i])
                    self.link_rects.append(self.links[i])
                    j += 1
                    cf.RESULTS = True

        except Exception as e:
            print(f"BACKEND: func: DRAW RESULTS {e}")
            pass

    def select_station(self):
        # SELECT RADIO STATION FROM SEARCH
        try:
            for i in range(len(self.result_rects)):
                if self.result_rects[i].collidepoint(cf.MOUSE_POSITION):
                    self.selected_link = self.link_rects[i]
                    self.selected_name = self.name_rects[i]

                    self.play_protocol()
                    click_back_to_player_btn()
                    cf.STATION_IS_SELECTED = True
                    break

        except Exception as e:
            print(f"BAKEND: func: SELECT STATION {e}")
            pass

    """ KEYBOARD INPUT """
    def insert_search_term(self, event):
        # PRESS DELETE
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            cf.SEARCH_TERM = str(self.text)
        # PRESS INTRO OR SEARCH
        elif event.key == pg.K_RETURN:
            self.click_search_action_btn(True)
        # WRITE NAME
        else:
            if len(cf.SEARCH_TERM) < 15:
                self.text += event.unicode
                cf.SEARCH_TERM = str(self.text)

    """ EVENTS INPUT """
    def event_catcher(self):
        # CATCH PROGRAM EVENTS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if cf.SEARCH_IS_OPEN:
                    # INSERT TERM FOR SEARCHING
                    self.insert_search_term(event)

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                cf.MOUSE_POSITION = pg.mouse.get_pos()

                if cf.PLAYER_IS_OPEN:
                    """ PLAYER INTERFACE BUTTONS """
                    for i, btn in enumerate(self.player.buttons):
                        if btn['rect'].collidepoint(cf.MOUSE_POSITION):
                            self.player_functions[i]()

                elif cf.SEARCH_IS_OPEN:
                    """ SEARCH INTERFACE BUTTONS """
                    for i, btn in enumerate(self.search.buttons):
                        if btn['rect'].collidepoint(cf.MOUSE_POSITION):
                            self.search_functions[i]()

                    # CHOOSE RADIO STATION
                    if cf.RESULTS:
                        if cf.SEARCH_BY_COUNTRY_ON and cf.COUNTRIES:
                            self.select_country()
                        else:
                            self.select_station()

                elif cf.FAVOURITES_IS_OPEN:
                    """ FAVOURITES INTERFACE BUTTONS """
                    for i, btn in enumerate(self.favourites.buttons):
                        if btn['rect'].collidepoint(cf.MOUSE_POSITION):
                            self.favourites_functions[i]()

                    # SELECT FAVOURITE
                    self.select_favourite()
                    self.delete_fav()

    """ CORE """
    def draw(self):
        restore_buttons(self.player.buttons, self.player.button_images, self.player.press_button_images)

        # MODE PLAYER
        if cf.PLAYER_IS_OPEN:
            self.player.draw()

        # MODE FAVOURITES
        elif cf.FAVOURITES_IS_OPEN:
            self.favourites.draw()
            self.draw_favs()

        # MODE SEARCH
        elif cf.SEARCH_IS_OPEN:
            self.search.draw()
            if cf.GO_SEARCH:
                if cf.SEARCH_BY_NAME_ON or cf.SEARCH_BY_TAGS_ON:
                    self.draw_results()
                elif cf.SEARCH_BY_COUNTRY_ON:
                    if cf.COUNTRIES:
                        self.draw_countries()
                    else:
                        self.draw_results()
                else:
                    self.reset_stats()

    def update(self):
        self.event_catcher()
        if cf.FAVOURITES_IS_OPEN:
            if cf.DELETE_FAV:
                self.save_data()
                self.load_data()
                self.draw_favs()
                cf.DELETE_FAV = False
