from selenium import webdriver
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.safari.options import Options as SafariOptions


import my_key
import helper as hp

from faker import Faker
import unittest
import time

faker_class = Faker()

BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or my_key.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or my_key.BROWSERSTACK_ACCESS_KEY
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
BUILD_NAME = "browserstack-build-002"

class BrowserStack(unittest.TestCase):

    def get_browser_option(browser):
        switcher = {
            "safari": SafariOptions(),
        }
        return switcher.get(browser,SafariOptions())

    def setUp(self):
        desired_cap = {
            'os_version': 'Sonoma',
            'os': 'OS X',
            'browser': 'Safari',
            'browser_version': '17.3',
            'name': 'BStack  parallel Safari OS X Sonoma',  # test name
            'build': 'browserstack-build-1'
        }

        bstack_options = {
            "osVersion": desired_cap["os_version"],
            "buildName": desired_cap["build"],
            "sessionName": desired_cap["name"],
            "userName": BROWSERSTACK_USERNAME,
            "accessKey": BROWSERSTACK_ACCESS_KEY
        }

        bstack_options["os"] = desired_cap["os"]
        options = self.get_browser_option()
        options.browser_version = desired_cap["browser_version"]
        options.set_capability('bstack:options', bstack_options)
        desired_cap['acceptSslCerts'] = True
        self.driver = webdriver.Remote(command_executor=URL,
                                       options = options)
        self.driver.maximize_window()

    def test_01_pos_link_leads_to_the_right_website(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 1, BR-001 - LINK LEADS TO THE RIGHT WEBSITE \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        driver.get_screenshot_as_file("./screenshots/Chrome/test 1 main page.png")  # get screenshot of the main page
        print("Check screenshot 'test 1 main page.png")

        driver.close()

    def test_02_pos_log_in(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)


        print("***********************************************************\n"
              "TEST 2, BR-003 - LOG IN \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # get screenshot
        driver.get_screenshot_as_file("./screenshots/Chrome/test 2 logged in page.png")
        driver.find_element(By.XPATH,
                            '//*[@class="Button-sc-1dqy6lx-0 hpNmgY encore-over-media-set SFgYidQmrqrFEVh65Zrg"]').click()  # click on account menu
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(),'Profile')]").click()  # click on profile button
        hp.delay()
        driver.get_screenshot_as_file("./screenshots/Chrome/test 2 profile page.png")  # get screenshot of profile page

        driver.close()

    def test_03_pos_main_menu_buttons(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
                "TEST 3, BR-004 - BR-007, BR-012  - CHECK MAIN MENU BUTTONS \n"
                "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, 'Spotify - Web Player: Music for everyone')
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()

        # check Search button
        driver.find_element(By.XPATH, hp.search_btn).click() # click on a button
        hp.delay()
        print('Search page title: ')
        hp.assert_title(driver, "Spotify – Search") # verify page title

        # check Home button
        wait.until(EC.visibility_of_element_located((By.XPATH, hp.home_btn)))
        driver.find_element(By.XPATH, hp.home_btn).click()  # click on a button
        print('Home page title: ')
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")  # verify page title
        time.sleep(random.randint(7, 9))

        # check Your Library button collapse/expand menu
        driver.find_element(By.XPATH, hp.library_btn).click()  # click on a button
        time.sleep(random.randint(7, 9))
        driver.get_screenshot_as_file('./screenshots/Chrome/test 3 Library button collapse.png')
        time.sleep(random.randint(7, 9))
        driver.find_element(By.XPATH, hp.library_btn).click()  # click on a button
        hp.delay()
        driver.get_screenshot_as_file('./screenshots/Chrome/test 3 Library button expand.png')
        print('check screenshots "test 3 Library button collapse" and "test 3 Library button expand"')

        # check Create Play List button
        driver.find_element(By.XPATH, hp.crt_pl_btn_menu).click()  # click on a button
        hp.delay()
        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "My Playlist #1")]')))  # check playlist created
            driver.get_screenshot_as_file('./screenshots/Chrome/test 3 Playlist created.png')
        except:
            print('!!!!Create playlist button is NOT OK!!!!!')
        # delete playlist
        driver.find_element(By.XPATH, "//*[@class ='RowButton-sc-xxkq4e-0 hIehTT']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()

        driver.close()

    def test_04_pos_search_module(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 4, BR-008 - BR-011  - CHECK SEARCH MODULE \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        driver.find_element(By.XPATH, hp.search_btn).click()  # click on a Search button
        hp.delay()
        # check searching an Artist
        driver.find_element(By.XPATH, hp.search_field).click()
        driver.find_element(By.XPATH, hp.search_field).clear()
        driver.find_element(By.XPATH, hp.search_field).send_keys(hp.artist)
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(),'Artists')]").click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, hp.artist)))
            print ('Artist was found successfully')
        except:
            print ('WARNING!!!!! Artist WAS NOT found!!!!! WARNING See screenshot "test 4 Search artist result.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 4 Search artist result.png')

        # check searching a Song
        driver.find_element(By.XPATH, hp.search_field).click()  # click on search field
        driver.find_element(By.XPATH, hp.search_field).clear()  # clear the  Search field
        driver.find_element(By.XPATH, hp.search_field).send_keys(hp.song)  # enter a song name
        hp.delay()
        driver.find_element(By.LINK_TEXT, 'Songs').click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "I Wanna Dance with Somebody (Who Loves Me)")))
            print('Song was found successfully')
        except:
            print('WARNING!!!!! Song WAS NOT found!!!!! WARNING  See screenshot "test 4 Search Song result.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 4 Search song result.png')
        hp.delay()

        # check searching an Albums
        driver.find_element(By.XPATH, hp.search_field).click()
        driver.find_element(By.XPATH, hp.search_field).clear()
        driver.find_element(By.XPATH, hp.search_field).send_keys(hp.album)
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(),'Albums')]").click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, hp.album)))
            print('Album was found successfully')
        except:
            print('WARNING!!!!! Album WAS NOT found!!!!! WARNING See screenshot "test 4 Search Album result.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 4 Search Album result.png')

        # check searching of Audiobook
        driver.find_element(By.XPATH, hp.search_field).click()
        driver.find_element(By.XPATH, hp.search_field).clear()
        driver.find_element(By.XPATH, hp.search_field).send_keys(hp.audiobook)
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(),'Audiobooks')]").click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located ((By.LINK_TEXT, 'Greenlights'))) and wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Matthew McConaughey')]")))
            print('Audiobook was found successfully')
        except:
            print('WARNING!!!!! Audiobook WAS NOT found!!!!! WARNING  See screenshot "test 4 Search Audiobook result.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 4 Search Audiobook result.png')

        driver.close()

    def test_05_pos_create_playlist_and_add_description_to_it(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 5, BR-012, BR-015  - CHECK CREATE PLAYLIST AND ADD DESCRIPTION TO IT \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # Create a Playlist
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located ((By.XPATH, "//span[contains(text(),'My Playlist')]" )))
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot "test 5 playlist creation.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 5 playlist creation.png')
        # adding a description to the playlist
        driver.find_element(By.XPATH, "//*[@class='rEN7ncpaUeSGL9z0NGQR']").click()
        driver.find_element(By.XPATH, "//*[@class='f0GjZQZc4c_bKpqdyKbq c0CddR8wF7kDxvU6uM8B']").click()
        driver.find_element(By.XPATH, "//*[@class='f0GjZQZc4c_bKpqdyKbq c0CddR8wF7kDxvU6uM8B']").clear()
        driver.find_element(By.XPATH, "//*[@class='f0GjZQZc4c_bKpqdyKbq c0CddR8wF7kDxvU6uM8B']").send_keys(hp.description)
        driver.find_element(By.XPATH, "//span[contains(text(),'Save')]").click()
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, hp.description_btn)))
            print('Description was added successfully')
        except:
            print('WARNING!!!!! Description was NOT ADDED!!!!! WARNING   See screenshot "test 5 playlist description.png"')
        driver.get_screenshot_as_file("./screenshots/Chrome/test 5 playlist description.png")

        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()


        driver.close()

    def test_06_pos_rename_playlist(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 6, BR-013 - BR-014  - CHECK RENAME PLAYLIST  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # Create a Playlist
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, hp.pl_name)))  # check playlist created
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot "test 6 playlist creation.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 6 playlist creation.png')
        # Change the name of Playlist
        driver.find_element(By.XPATH, "//*[@class ='RowButton-sc-xxkq4e-0 hIehTT']").click()
        hp.delay()
        driver.find_element(By.XPATH, hp.pl_name).click()
        driver.find_element(By.XPATH, hp.pl_name_change_field).click()
        driver.find_element(By.XPATH, hp.pl_name_change_field).clear()
        driver.find_element(By.XPATH, hp.pl_name_change_field).send_keys(hp.new_name_plst)
        driver.find_element(By.XPATH, "//span[contains(text(),'Save')]").click()
        hp.delay()


        # check that name field accept different type of data
        for x in hp.list_names_plst:
            driver.find_element(By.XPATH, hp.pl_name).click()
            driver.find_element(By.XPATH, hp.pl_name_change_field).click()
            driver.find_element(By.XPATH, hp.pl_name_change_field).clear()
            driver.find_element(By.XPATH, hp.pl_name_change_field).send_keys(x)
            driver.find_element(By.XPATH, "//span[contains(text(),'Save')]").click()
            hp.delay()
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), hp.list_names_plst[x])]")))
                print(f'Playlist was renamed successfully: {x}')
            except:
                print('WARNING!!!!! Playlist was NOT renamed!!!!! WARNING   See screenshot "test 6 playlist rename.png"')
            driver.get_screenshot_as_file(f'./screenshots/Chrome/test 6 playlist rename {x}.png')

        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()

        driver.close()

    def test_07_pos_add_song_to_playlist(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 7, BR-016  - CHECK ADD SONG TO PLAYLIST  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # Create a Playlist
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, hp.pl_name)))
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot "test 7 playlist creation.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 7 playlist creation.png')
        # searching a Song
        hp.searching_a_song_pl_page(driver)
        #  add a song to playlist
        driver.find_element(By.XPATH, hp.add_btn).click()
        try:
            wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, hp.song)))
            print('Song was added successfully')
        except:
            print('WARNING!!!!! Song was NOT ADDED!!!!! WARNING   See screenshot "test 7 add song to playlist.png"')
        hp.delay()
        driver.get_screenshot_as_file('./screenshots/Chrome/test 7 add song to playlist.png')

        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()

        driver.close()

    def test_08_pos_delete_song_from_playlist(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 8, BR-017  - DELETE SONG FROM PLAYLIST  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # Create a Playlist
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, hp.pl_name)))
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot "test 8playlist creation.png"')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 8 playlist creation.png')
        # searching a Song
        hp.searching_a_song_pl_page(driver)
        #  Add a song to playlist
        driver.find_element(By.XPATH, hp.add_btn).click()
        try:
            wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, hp.song)))
            print('Song was added successfully')
        except:
            print('WARNING!!!!! Song was NOT ADDED!!!!! WARNING   See screenshot "test 8 add song to playlist.png"')
        hp.delay()
        driver.get_screenshot_as_file('./screenshots/Chrome/test 8 add song to playlist.png')
        # delete song from playlist
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@aria-label='More options for I Wanna Dance with Somebody (Who Loves Me) by Whitney Houston']")))
            driver.find_element(By.XPATH, "//*[@aria-label='More options for I Wanna Dance with Somebody (Who Loves Me) by Whitney Houston']").click()
            # click song menu
            hp.delay()
            driver.find_element(By.XPATH, "//span[contains(text(),'Remove from this playlist')]").click()   # click on Remove from this playlist
            print('Song was DELETED successfully')
        except:
            print('WARNING!!!!! Song was NOT DELETED!!!!! WARNING   See screenshot "delete song from playlist.png"')
        hp.delay()
        driver.get_screenshot_as_file('./screenshots/Chrome/test 8 delete song from playlist.png')

        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()

        driver.close()

    def test_09_pos_delete_playlist(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 9, BR-018  - DELETE PLAYLIST  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # Create a Playlist   mouseDown(button='right')
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, hp.pl_name)))
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot "test 9playlist creation.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 9 playlist creation.png')
        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.get_screenshot_as_file('./screenshots/Chrome/test 9 delete playlist.png')
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'My Playlist')]")))
            print('WARNING!!!!! Playlist was NOT deleted!!!!! WARNING   See screenshot "test 9delete playlist.png"')
            print('DEBUGGING NEEDED')
        except:
            print('Playlist was deleted successfully')


        driver.close()

    def test_10_pos_add_song_to_liked_songs_list(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 10, BR-019  - CHECK ADD SONG TO LIKED SONGS LIST  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # searching a Song
        hp.searching_a_song(driver)
        # adding a song to liked songs playlist
        wait.until(EC.presence_of_element_located((By.XPATH, hp.heart_btn)))
        hp.delay()
        driver.find_element(By.XPATH, hp.heart_btn).click()
        hp.delay()
        driver.find_element(By.XPATH, hp.like_sng_btn).click()  # click on a button 'Liked songs"
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, hp.song)))
            print('Song was ADDED to liked songs successfully')
        except:
            print('WARNING!!!!! Song was NOT added to liked songs!!!!! WARNING   See screenshot " test 10 song added to liked songs.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 10 song added to liked songs.png')
        #delete song from liked songs
        driver.find_element(By.XPATH,
                            '//div[@class="PAqIqZXvse_3h6sDVxU0"]/button[@class="Button-sc-1dqy6lx-0 dJzPxg otqy2yIt_BVXLjoundpp z0zJ798TVq97lZgdRT2_"]').click()
        hp.delay()
        driver.find_element(By.XPATH, "//*[@class='XvgFwKtvocRdadc47KE9']").click()
        driver.find_element(By.XPATH, "//span[contains(text(),'Done')]").click()
        driver.close()

    def test_11_pos_delete_song_from_liked_songs_list(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 11, BR-020  - CHECK DELETE SONG FROM LIKED SONGS LIST  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()
        # searching a Song
        hp.searching_a_song(driver)
        # adding a song to liked songs list
        # wait.until(EC.presence_of_element_located((By.XPATH, hp.heart_btn)))
        # hp.delay()
        driver.find_element(By.XPATH, hp.heart_btn).click()
        hp.delay()
        driver.find_element(By.XPATH, hp.like_sng_btn).click()  # click on a button 'Liked songs"
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, hp.song)))
            print('Song was ADDED to liked songs successfully')
        except:
            print(
                'WARNING!!!!! Song was NOT added to liked songs!!!!! WARNING   See screenshot "test 11 song added to liked songs.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 11 song added to liked songs.png')
        # delete song from liked songs list
        driver.find_element(By.XPATH, '//div[@class="PAqIqZXvse_3h6sDVxU0"]/button[@class="Button-sc-1dqy6lx-0 dJzPxg otqy2yIt_BVXLjoundpp z0zJ798TVq97lZgdRT2_"]').click()
        hp.delay()
        driver.find_element(By.XPATH, "//*[@class='XvgFwKtvocRdadc47KE9']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(),'Done')]").click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, hp.song)))
            print('WARNING!!!!! Song was NOT deleted from liked songs!!!!! WARNING   See screenshot "test 11 song deleted from liked songs list.png"')
            print('DEBUGGING NEEDED')
        except:
            print('Song was DELETED from liked songs successfully')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 11 song deleted from liked songs list.png')

        driver.close()

    def test_12_neg_log_in_in_with_email_that_was_not_been_signed_up(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 12, BR-021  - LOG IN WITH WRONG EMAIL  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()

        # Set wait until button 'Login' will be clickable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, hp.login_btn)))
        # Click on button 'Login'
        driver.find_element(By.XPATH, hp.login_btn).click()
        hp.delay()
        # Find email field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-username').click()
        hp.delay()
        driver.find_element(By.ID, 'login-username').clear()
        hp.delay()
        driver.find_element(By.ID, 'login-username').send_keys("MAIL@MAIL.COM")
        # Find password field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-password').click()
        driver.find_element(By.ID, 'login-password').clear()
        driver.find_element(By.ID, 'login-password').send_keys(hp.test_pswrd)
        # click Log In button    Incorrect username or password.
        driver.find_element(By.XPATH, '//*[@class="ButtonInner-sc-14ud5tc-0 liTfRZ encore-bright-accent-set"]').click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Неправильное имя пользователя или пароль.")]')))
            print('warning message appeared')
        except:
            print(
                'WARNING!!!!! Warning message DID NOT appear!!!!! WARNING   See screenshot "test 12 wrong email log in.png"')
            print('DEBUGGING NEEDED')

        driver.get_screenshot_as_file('./screenshots/Chrome/test 12 wrong email log in.png')

        driver.close()

    def test_13_neg_log_in_with_wrong_password(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 13, BR-022  - LOG IN WITH WRONG PASSWORD  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # Set wait until button 'Login' will be clickable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, hp.login_btn)))
        # Click on button 'Login'
        driver.find_element(By.XPATH, hp.login_btn).click()
        hp.delay()
        # Find email field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-username').click()
        hp.delay()
        driver.find_element(By.ID, 'login-username').clear()
        hp.delay()
        driver.find_element(By.ID, 'login-username').send_keys(hp.test_email)
        # Find password field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-password').click()
        driver.find_element(By.ID, 'login-password').clear()
        driver.find_element(By.ID, 'login-password').send_keys('vhdvhvnxbvcj,hsdgdj')
        # click Log In button
        driver.find_element(By.XPATH, '//*[@class="ButtonInner-sc-14ud5tc-0 liTfRZ encore-bright-accent-set"]').click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Неправильное имя пользователя или пароль.")]')))
            print('Warning message appeared')
        except:
            print(
                'WARNING!!!!! Warning message DID NOT appear!!!!! WARNING   See screenshot "test 13 wrong password log in.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 13 wrong password log in.png')

        driver.close()

    def test_14_neg_log_in_without_password(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 14, BR-023  - LOG IN WITHOUT PASSWORD  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()

        # Set wait until button 'Login' will be clickable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, hp.login_btn)))
        # Click on button 'Login'
        driver.find_element(By.XPATH, hp.login_btn).click()
        hp.delay()
        # Find email field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-username').click()
        hp.delay()
        driver.find_element(By.ID, 'login-username').clear()
        hp.delay()
        driver.find_element(By.ID, 'login-username').send_keys(hp.test_email)
        # Find password field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-password').click()
        driver.find_element(By.ID, 'login-password').clear()
        # click Log In button
        driver.find_element(By.XPATH, '//*[@class="ButtonInner-sc-14ud5tc-0 liTfRZ encore-bright-accent-set"]').click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Неправильное имя пользователя или пароль.")]')))
            print('Warning message appeared')
        except:
            print(
                'WARNING!!!!! Warning message DID NOT appear!!!!! WARNING   See screenshot "test 14 no password log in.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 14 no password log in.png')

        driver.close()

    def test_15_neg_long_name_playlist(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 15, BR-024  - CHECK NAME OF PLAYLIST WITH MORE THAN 100 CHARACTERS  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        # hp.delay()
        time.sleep(random.randint(10, 15))
        # Create a Playlist
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, hp.pl_name)))  # check playlist created
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot " test 15 playlist creation.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 15 playlist creation.png')
        # Change the name of Playlist
        driver.find_element(By.XPATH, hp.pl_name).click()
        driver.find_element(By.XPATH, hp.pl_name_change_field).click()
        driver.find_element(By.XPATH, hp.pl_name_change_field).clear()
        driver.find_element(By.XPATH, hp.pl_name_change_field).send_keys(hp.long_name_plst)
        driver.find_element(By.XPATH, "//span[contains(text(),'Save')]").click()
        driver.get_screenshot_as_file('./screenshots/Chrome/test 15 playlist long name.png')
        hp.delay()
        # set name of playlist as var element
        element = driver.find_element(By.XPATH, "//button[@class='wCkmVGEQh3je1hrbsFBY']")
        element = element.get_attribute('aria-label')
        print('Playlist name is: ', element)
        pl_len = len(element) - 15
        if pl_len <= 100:
            print("Name of playlist is 100 or less characters. The length is: ", pl_len)
        else:
            print('WARNING!!!!! Name of playlist is more than 100 characters!!!!! WARNING   See screenshot "playlist long name.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 15 playlist long name.png')
        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()

        driver.close()

    def test_16_neg_create_playlist_with_no_name(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 16, BR-025  - CREATE PLAYLIST WITH NO NAME \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # LogIn into existing account
        hp.login(driver)
        hp.delay()

        # Create a Playlist
        driver.find_element(By.XPATH, hp.crt_pl_btn).click()  # click on a button "Create Playlist"
        hp.delay()
        driver.find_element(By.XPATH, hp.crt_pl_btn_2).click()
        hp.delay()
        hp.assert_title(driver, driver.title)
        # check that playlist created
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'My Playlist')]")))
            print('Playlist was created successfully')
        except:
            print('WARNING!!!!! Playlist was NOT created!!!!! WARNING   See screenshot "playlist creation.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 16 playlist creation.png')
        hp.delay()
        # Delete the name of Playlist
        driver.find_element(By.XPATH, hp.pl_name).click()
        hp.delay()
        driver.find_element(By.XPATH, hp.pl_name_change_field).send_keys(Keys.DELETE)
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(),'Save')]").click()
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='pIZVZOfjnJGth1BcoA1E ZBBTIITnUdwh05dCI0tm']")))
            alert=driver.find_element(By.XPATH, "//*[@class='pIZVZOfjnJGth1BcoA1E ZBBTIITnUdwh05dCI0tm']")
            alert.get_attribute('text')
            print('Alert sign appeared ')
        except:
            print('WARNING!!!!! Name field accepts zero characters!!!! WARNING   See screenshot "playlist with no name.png"')
            print('DEBUGGING NEEDED')
        driver.get_screenshot_as_file('./screenshots/Chrome/test 16 playlist with no name.png')
        # close editing window
        driver.find_element(By.XPATH, "//*[@class='MQQEonum615k8mGkliT_']").click()
        driver.find_element(By.XPATH, "//*[@class='MQQEonum615k8mGkliT_']").click()
        # delete playlist
        driver.find_element(By.XPATH, "//*[@class='Button-sc-1dqy6lx-0 lnKBlZ']").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Delete')]").click()
        hp.delay()

        driver.close()

    def test_17_ad_hoc_log_in_with_invalid_email(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(hp.main_url)
        hp.delay()
        wait = WebDriverWait(driver, 10)

        print("***********************************************************\n"
              "TEST 17, BR-026  - LOG IN WITH INVALID EMAIL  \n"
              "***********************************************************")
        # switch the language
        hp.switch_to_en(driver)
        # verify title
        hp.assert_title(driver, "Spotify - Web Player: Music for everyone")
        hp.delay()
        # Set wait until 'Login' button is clickable
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, hp.login_btn)))
        # Click on button 'Login'
        driver.find_element(By.XPATH, hp.login_btn).click()
        hp.delay()
        # Find email field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-username').click()
        driver.find_element(By.ID, 'login-username').clear()
        driver.find_element(By.ID, 'login-username').send_keys("email@mail.com@mail.com")
        # Find password field, click on it, clear, and type test data
        driver.find_element(By.ID, 'login-password').click()
        driver.find_element(By.ID, 'login-password').clear()
        driver.find_element(By.ID, 'login-password').send_keys(hp.test_pswrd)
        # click Log In button
        driver.find_element(By.XPATH, '//*[@class="ButtonInner-sc-14ud5tc-0 liTfRZ encore-bright-accent-set"]').click()
        hp.delay()
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Неправильное имя пользователя или пароль.")]')))
            print('warning message appeared')
        except:
            print(
                'WARNING!!!!! Warning message DID NOT appear!!!!! WARNING   See screenshot test 17 invalid email log in.png"')
            print('DEBUGGING NEEDED')

        driver.get_screenshot_as_file('./screenshots/Chrome/test 17 invalid email log in.png')

        driver.close()

    def tearDown(self):
        self.driver.quit()
