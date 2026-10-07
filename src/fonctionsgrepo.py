from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time, random
from datetime import datetime
#from selenium.webdriver import ActionChains
import json
from variables import *

options = Options()
# Avoids sending WebDriver signatures
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)

with open('data/data.txt') as json_file:
    data = json.load(json_file)
    firefox_profile_path = data['path_to_driver']

options.set_preference("profile", firefox_profile_path)

service = Service("/home/phileas/code/geckodriver")
try :
    driver = webdriver.Firefox(service=service, options=options)
except :
    print("Couldn't find driver's path")

# Sends current city name
def selected_city():
    return driver.find_element(By.XPATH,"//div[@class='town_name js-townname-caption js-rename-caption ui-game-selectable']").text

def city_view():
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(((By.NAME, "city_overview")))).click()

def island_view():
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(((By.NAME, "island_view")))).click()

def delay(a=1.5, b=3):
    time.sleep(random.uniform(a, b))

# login, password, and server to put in data.txt
def login():
    driver.get("https://fr.grepolis.com/")
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "pop-up_cookie_button_accept"))).click()
    with open('data/data.txt') as json_file:
        data = json.load(json_file)
        name = data['name']
        passw = data['pass']
        path = f"//*[contains(text(), '{data['server']}')]"
        driver.find_element(By.ID, "page_login_always-visible_input_player-identifier").send_keys(name)
        driver.find_element(By.ID, "page_login_always-visible_input_password").send_keys(passw)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "page_login_always-visible_button_login"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,path))).click() # à adapter

def collecte(duree_farm):
    print('Je commence la collecte à  {}'.format(datetime.now().time()))
    close_time = time.time() + duree_farm
    try:
        island_view()
        # insérer code pour fermer les fenêtres indésirables
        delay()
        while True:
            if time.time() > close_time:
                break
            city = driver.find_element(By.XPATH,"//div[@class='town_name js-townname-caption js-rename-caption ui-game-selectable']").text
            #print("The bot is in : ", city, "city")
            if city not in non_farm_cities:
                delay()
                try:
                    ids = [btn.get_attribute("id") for btn in driver.find_elements(By.CLASS_NAME, "claim")]
                    for bid in ids:
                        try:
                            driver.find_element(By.ID, bid).click()
                            delay()
                            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(((By.CLASS_NAME, "btn_claim_resources")))).click()
                            delay()
                            driver.find_element(By.XPATH,"//div[@class='btn_wnd close']").click()
                            #print("ressources récupérées")
                            delay()
                        except StaleElementReferenceException:
                            print(f"L’élément {bid} est stale, je réessaye")
                            driver.find_element(By.ID, bid).click()
                    print('Ressources récupérées dans ', str(city), ' à  {}'.format(datetime.now().time()))
                except Exception as e:
                    print(e.msg)
                next_city()
            else :
                print("La ville ", str(city), " a été indiquée comme exception, le bot ne récupère donc pas de ressources dessus. Pour changer cela, retirer ", str(city)," de la liste non_farm_cities")
    except Exception as e:
        print(e.msg)
        reconnect()


flag = True
def init_commerce():
    print("procédure d'initialisation en cours")



def commerce():
    if flag:
        init_commerce()
    else:
        pass


# clic incorrect, à modifier
def construction():
    start_city = selected_city()
    while True:
        present_city = selected_city()
        if str(present_city) in building_queue.keys():
            city_view()
            delay()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "construction_queue_build_button"))).click()
            delay()
            for bld in building_queue[present_city]:
                if bld == "académie":
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR("div[class='city_overview_overlay academy']")))).click()
                        print("Académie améliorée à ", str(present_city, "!"))
                        delay()
                    except:
                        pass
                if bld == "port":
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR("div[class='city_overview_overlay docks']")))).click()
                        delay()
                    except:
                        pass
                if bld == "sénat":
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR("div[class='city_overview_overlay main']")))).click()
                        delay()
                    except:
                        pass
                if bld == "ferme":
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR("div[class='city_overview_overlay farm']")))).click()
                        delay()
                    except:
                        pass
                if bld == "entrepôt":
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR("div[class='city_overview_overlay storage']")))).click()
                        delay()
                    except:
                        pass
                if bld == "remparts":
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR("[data_building_id='wall']")))).click()
                        delay()
                    except:
                        pass
        next_city()
        if start_city == selected_city():
            island_view()
            break



# à modifier (?): doit supporter la mise en veille de l'ordi
def reconnect():
    print('Waiting to reconnect')
    if 'fr0' in driver.current_url:
        print('Bot disconnected at {}, reconnecting in {} minutes...'.format(datetime.now().time(), reconnexion))
        time.sleep(reconnexion * 60) 
        driver.find_element(By.XPATH, "//*[contains(text(), server)]").click()
        print('Reconnected')


def next_city():
    try :
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(((By.XPATH, "//div[@class='btn_next_town button_arrow right']")))).click()
        delay()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(((By.XPATH, "//div[@class='btn_jump_to_town circle_button jump_to_town']//div[@class='icon js-caption']")))).click()
        delay()
    except :
        pass


