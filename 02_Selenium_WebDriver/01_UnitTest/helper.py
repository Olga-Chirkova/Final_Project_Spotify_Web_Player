import time
import random
import requests
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from faker import Faker



# Set main variables
# URL - home page
main_url = 'https://open.spotify.com/'
# User's E-mail
test_email = " "  # type your user's E-mail for account
# User's password
test_pswrd = " "  # type your user's password for account
# test artist
artist = 'Whitney Houston'
# test song
song = 'I Wanna Dance with Somebody (Who Loves Me)'
# test album
album = 'The Bodyguard - Original Soundtrack Album'
# test audiobook
audiobook = 'Matthew McConaughey Greenlights'
# new name for playlist
new_name_plst = 'New favorite playlist_111'
# description to the playlist
description = 'This is my new playlist !!!'
# list of different names for playlist
list_names_plst = ["New name", "3456789", "!@#$%^&*()<>", "Мои песни"]
# long name for playlist with more than 100 characters (110) characters
long_name_plst = 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated the'


# MOST OFTEN USED X-PATHs

# Log-In button
login_btn =  "//span[contains(text(),'Log in')]"
# main Logo
main_logo = '//*[@class="BQ7wNkJFinJvGx2WCnwc"]'
# home button
home_btn ="//*[@class='link-subtle hNvCMxbfz7HwgzLjt3IZ Bh3b80dIrbc0keQ9kdso active']"
# search button
search_btn = "//*[@aria-label='Search']"
# your library button
library_btn = "//*[@class='Svg-sc-ytk21e-0 bneLcE']"
# create playlist button mtnu
crt_pl_btn_menu = "//span[contains(text(),'Create playlist')]"
# create playlist button
crt_pl_btn = "//*[@class='Button-sc-1dqy6lx-0 hidZeW cljOO1tpzixzXctKJucK nGWhztVvLY1BInXjcWYa NxEINIJHGytq4gF1r2N1 or84FBarW2zQhXfB9VFb XNjgtSbyhshr7YQcVvry O0AN8Ty_Cxd4iLwyKATB D8wJ9TPfJzLeLJYxnad2 zWWLnqWslTLHwq3wBgGB']"
crt_pl_btn_2 ="//span[contains(text(),'Create a new playlist')]"
#  liked songs button
like_sng_btn = "//*[@class='NxEINIJHGytq4gF1r2N1 or84FBarW2zQhXfB9VFb odS2IW9wfNVHhkhc0l_X O0AN8Ty_Cxd4iLwyKATB wQnUXn1m6Gy4PH8jhslb D8wJ9TPfJzLeLJYxnad2 oE8LAmRhbeQqsZrQo4lb mhuhir0ikRqXAPHU8ZZ1 pTvxY5yAQklZgb7VZFGS vSC5QuwmzUhqUNWdMTJ5']"
# name of playlist
pl_name = "//*[@class='rEN7ncpaUeSGL9z0NGQR']"
# field for changing of playlist name in pop-up window
pl_name_change_field = "//*[@class='f0GjZQZc4c_bKpqdyKbq JaGLdeBa2UaUMBT44vqI']"
# field for changing of playlist name in pop-up window for Firefox
pl_name_change_field_ff = "//*[@class='f0GjZQZc4c_bKpqdyKbq JaGLdeBa2UaUMBT44vqI UCj7uEr7vR_0DO3cQHcX']"
# searching field on Search page
search_field = "//*[@class='encore-text encore-text-body-small NtkAQg9R1r5CjuP0XHwl']"
# searching field on Playlist page
search_field_plst_page = "//*[@class='encore-text encore-text-body-small FeWwGSRANj36qpOBoxdx']"
# add to playlist button
add_btn = '//div[@aria-rowindex="1"]/div[@class="IjYxRc5luMiDPhKhZVUH UpiE7J6vPrJIa59qxts4 jDgf8MzZRbApYE6BW1qL"]/div[@class="PAqIqZXvse_3h6sDVxU0"]/button[@data-testid="add-to-playlist-button"]'
# add to liked songs button 'heart-button'
heart_btn = '//div[@aria-rowindex="2"]/div[@class="IjYxRc5luMiDPhKhZVUH UpiE7J6vPrJIa59qxts4"]/div[@class="PAqIqZXvse_3h6sDVxU0"]/button[@class="Button-sc-1dqy6lx-0 fpsDgO otqy2yIt_BVXLjoundpp"]'
description_btn = '//*[@class="f0GjZQZc4c_bKpqdyKbq c0CddR8wF7kDxvU6uM8B"]'


# MOST OFTEN USED FUNCTIONS

# Set random delay
def delay():
    time.sleep(random.randint(3, 5))

# switch the language
def switch_to_en(driver):
    driver.find_element(By.XPATH, "//*[@class='Button-sc-y0gtbx-0 IQVKX encore-text-body-small-bold']").click()
    delay()
    driver.find_element(By.XPATH, "//button[@id='en']").click()
    # delay()

# Verify Pages Title
def assert_title(driver, title):
    if title in driver.title:
        print(f"Page has '{driver.title}' as Page title")
    else:
        print (f"WARNING !!!!!Page has WRONG Title: '{title}' !!!!! WARNING ")
    driver.get_screenshot_as_file(f"Page {title}.png") # Screenshot of the page

# Log In into existing account
def login(driver):
    # Set wait until button 'Login' will be clickable
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, login_btn)))
    # Click on button 'Login'
    driver.find_element(By.XPATH, login_btn).click()
    delay()
    # Find email field, click on it, clear, and type test data
    driver.find_element(By.ID, 'login-username').click()
    driver.find_element(By.ID, 'login-username').clear()
    driver.find_element(By.ID, 'login-username').send_keys(test_email)
    # Find password field, click on it, clear, and type test data
    driver.find_element(By.ID, 'login-password').click()
    driver.find_element(By.ID, 'login-password').clear()
    driver.find_element(By.ID, 'login-password').send_keys(test_pswrd)
    # click Log In button
    driver.find_element(By.XPATH, '//*[@class="ButtonInner-sc-14ud5tc-0 liTfRZ encore-bright-accent-set"]').click()

    # searching a Song on a Search page
def searching_a_song(driver):
    driver.find_element(By.XPATH, search_btn).click()  # click on a Search button
    delay()
    driver.find_element(By.XPATH, search_field).click() # click on search field
    driver.find_element(By.XPATH, search_field).clear()  # clear the  Search field
    driver.find_element(By.XPATH, search_field).send_keys(song)  # enter a song name
    delay()
    driver.find_element(By.LINK_TEXT, 'Songs').click()
    delay()

    # searching a Song on Playlist page
def searching_a_song_pl_page(driver):
    driver.find_element(By.XPATH, search_field_plst_page).click() # click on search field
    driver.find_element(By.XPATH, search_field_plst_page).clear()  # clear the  Search field
    driver.find_element(By.XPATH, search_field_plst_page).send_keys(song)  # enter a song name
    delay()

