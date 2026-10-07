import selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime 
from selenium.webdriver.chrome.options import Options as ChromeOptions 
from random import expovariate
import asyncio
import time
import pprint


minutos_reconexion = 2  # Minutos que espera el bot para conectarse de nuevo una vez tu lo echas iniciando sesion
minutos_frecuencia_comercio = 30 # Minutos que farme antes de intentar traspasar materias entre ciudades
ciudad_evento = [] # ciudad donde vas a sacar hoplitas a saco para el evento
no_farm_cities = [] # Lista de las ciudades que NO quieres que cojan recursos de las aldeas(Al compartir isla es normal)


# La ciudad y al lado el numero de unidad que quieres que recoja de las aldeas una vez no quedan mas materias.
# 0 infante, 1 hondero, 2 arquero, 3 hoplita
troops_cities = {
  "Familja": 3
  }

ciudades = {}


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.add_argument("window-size=1920,1000")
    chrome_options.add_argument("--log-level=3")
    #chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def Login():
    """Connects to grepolis and login"""
    driver.get("https://es.grepolis.com/")

    with open('c:/Users/Mikel/Desktop/Grepo/data.txt') as json_file:
        data = json.load(json_file)
        name = data['name']
        passw = data['pass']

        username = driver.find_element(By.ID, "login_userid").send_keys(name)
        password = driver.find_element(By.ID, "login_password").send_keys(passw)

        time.sleep(4)

        driver.find_element(By.ID, "login_Login").click()
        time.sleep(4)
        
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'DORILEA')]"))).click()


async def recogida_aldeas(duration):

    print('COMIENZO FARMEO A LAS  {}'.format(datetime.now().time()))
    close_time = time.time() + duration
    while True:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(((By.NAME, "island_view")))).click()

            try:
                driver.find_element(By.CLASS_NAME,'close_all').click()
            except Exception:
                pass
            time.sleep(2.5)

            while True:
                if time.time() > close_time:
                    break
                ciudad = driver.find_element(By.XPATH,"/html/body/div[1]/div[17]/div[3]/div[1]/div").text
                if ciudad not in no_farm_cities:
                    time.sleep(0.4)
                    try:
                        driver.find_element(By.CLASS_NAME,'claim').click()
                        time.sleep(0.4)
                        recursos_aldea = driver.find_element(By.CLASS_NAME,'resources_pb').text
                        recursos_aldea = recursos_aldea.split('/')[0]
                        time.sleep(0.4)
                        #breakpoint()
                        if int(recursos_aldea) > 114 or len(driver.find_elements(By.CLASS_NAME,'limit_reached')) > 0:  
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Recoger')]").click()
                        else:
                            poblacion_displonible = driver.find_element(By.CLASS_NAME,'population').text
                            if int(poblacion_displonible) < 8:
                                no_farm_cities.append(ciudad)
                                print('La ciudad {} requiere de atención'.format(ciudad))
                            elif ciudad in troops_cities:
                                time.sleep(0.8)
                                driver.find_element(By.CLASS_NAME,'units').click()
                                time.sleep(0.5)
                                driver.find_elements(By.CLASS_NAME,'action_card')[troops_cities[ciudad]].click()
                            else:
                                next_city()
                        time.sleep(0.4)
                        driver.find_element(By.CLASS_NAME,'close_all').click()
                        time.sleep(0.4)
                    except Exception as e:
                        #print(e.msg)
                        #print('No hay aldeas disponibles a las  {} en {}'.format(datetime.now().time(), ciudad))
                        next_city()
                else:
                    next_city()
            break
        except Exception as e:
            #print(e.msg)
            reconnect()

    #await asyncio.sleep(0)

async def comerciar():
    print('COMIENZO COMERCIO A LAS  {}'.format(datetime.now().time()))
    while True:
        ciudad = driver.find_element(By.XPATH,"/html/body/div[1]/div[17]/div[3]/div[1]/div").text
            
        ciudades[ciudad] = {}
        ciudades[ciudad]['madera'] = driver.find_element(By.XPATH, "//*[@id='ui_box']/div[6]/div[1]/div[1]/div[2]").text
        ciudades[ciudad]['piedra'] = driver.find_element(By.XPATH, "//*[@id='ui_box']/div[6]/div[2]/div[1]/div[2]").text
        ciudades[ciudad]['plata'] = driver.find_element(By.XPATH, "//*[@id='ui_box']/div[6]/div[3]/div[1]/div[2]").text
        ciudades[ciudad]['media'] = (int(ciudades[ciudad]['madera']) + int(ciudades[ciudad]['piedra']) + int(ciudades[ciudad]['plata']))/3

        if int(ciudades[ciudad]['piedra']) > int(ciudades[ciudad]['media']) and int(ciudades[ciudad]['piedra']) > 8000:
            print('En {}, la piedra sobra. Hay {} y la media es {}'.format(ciudad, ciudades[ciudad]['piedra'], ciudades[ciudad]['media']))
            ciudad_origen = ciudad
            for ciudad in ciudades:
                if int(ciudades[ciudad]['piedra']) < int(ciudades[ciudad]['media']):
                    print('TENEMOS MATCH')
                    ciudad_destino = ciudad
                    print('Ciudad origen: {}. Ciudad destino: {}'.format(ciudad_origen, ciudad_destino))
                    enviado = False
                    while enviado == False:
                        driver.find_element(By.XPATH, "//*[@id='ui_box']/div[17]/div[2]").click()
                        ciudad = driver.find_element(By.XPATH,"/html/body/div[1]/div[17]/div[3]/div[1]/div").text

                        if ciudad == ciudad_origen:
                            print('inicio comercio interno')
                            action = ActionChains(driver)
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Perfil')]").click()
                            time.sleep(2)
                            try:
                                driver.find_element(By.XPATH,"//*[contains(text(), '" + ciudad_destino + "')]").click()

                            except Exception:
                                source = driver.find_element(By.XPATH, "//*[@id='player_towns']/div/ul/li[2]")
                                action.move_to_element(source).perform()
                                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                                driver.execute_script("window.scrollBy(0,3000)","")
                            time.sleep(2)
                            source = driver.find_element(By.XPATH, "//*[@id='ui_box']/div[6]/div[3]/div[1]/div[2]")
                            time.sleep(2)
                            action.move_to_element(source).perform()
                            time.sleep(2)
                            driver.find_element(By.XPATH, "//*[@id='trading']").click()
                            #driver.find_element(By.XPATH,"//*[contains(text(), 'Comerciar')]").click()
                            time.sleep(2)
                            ciudad = driver.find_element(By.XPATH,"//*[@id='trade_type_stone']/div[3]/input").send_keys(2000)
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Enviar recursos')]").click()
                            time.sleep(2)
                            print('COMERCIO COMPLETADO')
                            enviado = True


        if int(ciudades[ciudad]['plata']) > int(ciudades[ciudad]['media']) and int(ciudades[ciudad]['plata']) > 5000:
            print('En {}, la plata sobra. Hay {} y la media es {}'.format(ciudad, ciudades[ciudad]['plata'], ciudades[ciudad]['media']))
            ciudad_origen = ciudad
            for ciudad in ciudades:
                if int(ciudades[ciudad]['plata']) < int(ciudades[ciudad]['media']):
                    print('TENEMOS MATCH')
                    ciudad_destino = ciudad
                    print('Ciudad origen: {}. Ciudad destino: {}'.format(ciudad_origen, ciudad_destino))
                    enviado = False
                    while enviado == False:
                        driver.find_element(By.XPATH, "//*[@id='ui_box']/div[17]/div[2]").click()
                        ciudad = driver.find_element(By.XPATH,"/html/body/div[1]/div[17]/div[3]/div[1]/div").text

                        if ciudad == ciudad_origen:
                            print('inicio comercio interno')
                            action = ActionChains(driver)
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Perfil')]").click()
                            time.sleep(2)
                            try:
                                driver.find_element(By.XPATH,"//*[contains(text(), '" + ciudad_destino + "')]").click()
                            except Exception:
                                #breakpoint()
                                source = driver.find_element(By.XPATH, "//*[@id='player_towns']/div/ul/li[2]")
                                action.move_to_element(source).perform()
                                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                            time.sleep(2)
                            source = driver.find_element(By.XPATH, "//*[@id='ui_box']/div[6]/div[3]/div[1]/div[2]")
                            time.sleep(2)
                            action.move_to_element(source).perform()
                            time.sleep(2)
                            driver.find_element(By.XPATH, "//*[@id='trading']").click()
                            #driver.find_element(By.XPATH,"//*[contains(text(), 'Comerciar')]").click()
                            time.sleep(2)
                            ciudad = driver.find_element(By.XPATH,"//*[@id='trade_type_iron']/div[3]/input").send_keys(2000)
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Enviar recursos')]").click()
                            time.sleep(2)
                            close = driver.find_element(By.CLASS_NAME,'close_all').click()
                            time.sleep(2)
                            print('COMERCIO COMPLETADO')
                            enviado = True

        if int(ciudades[ciudad]['madera']) > int(ciudades[ciudad]['media']) and int(ciudades[ciudad]['madera']) > 5000:
            print('En {}, la madera sobra. Hay {} y la media es {}'.format(ciudad, ciudades[ciudad]['madera'], ciudades[ciudad]['media']))
            ciudad_origen = ciudad
            for ciudad in ciudades:
                if int(ciudades[ciudad]['madera']) < int(ciudades[ciudad]['media']):
                    print('TENEMOS MATCH')
                    ciudad_destino = ciudad
                    print('Ciudad origen: {}. Ciudad destino: {}'.format(ciudad_origen, ciudad_destino))
                    enviado = False
                    while enviado == False:
                        driver.find_element(By.XPATH, "//*[@id='ui_box']/div[17]/div[2]").click()
                        ciudad = driver.find_element(By.XPATH,"/html/body/div[1]/div[17]/div[3]/div[1]/div").text

                        if ciudad == ciudad_origen:
                            print('inicio comercio interno')
                            action = ActionChains(driver)
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Perfil')]").click()
                            time.sleep(2)
                            try:
                                driver.find_element(By.XPATH,"//*[contains(text(), '" + ciudad_destino + "')]").click()
                            except Exception:
                                #breakpoint()
                                source = driver.find_element(By.XPATH, "//*[@id='player_towns']/div/ul/li[2]")
                                action.move_to_element(source).perform()
                                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                            time.sleep(2)
                            source = driver.find_element(By.XPATH, "//*[@id='ui_box']/div[6]/div[3]/div[1]/div[2]")
                            time.sleep(2)
                            action.move_to_element(source).perform()
                            time.sleep(2)
                            driver.find_element(By.XPATH, "//*[@id='trading']").click()
                            #driver.find_element(By.XPATH,"//*[contains(text(), 'Comerciar')]").click()
                            time.sleep(2)
                            ciudad = driver.find_element(By.XPATH,"//*[@id='trade_type_wood']/div[3]/input").send_keys(2000)
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Enviar recursos')]").click()
                            time.sleep(2)
                            close = driver.find_element(By.CLASS_NAME,'close_all').click()
                            time.sleep(2)
                            print('COMERCIO COMPLETADO')
                            enviado = True
                        

        await asyncio.sleep(1)

def reconnect():
    print('Waiting to reconnect')
    if 'es0' in driver.current_url:
        print('Bot disconnected at {}, reconnecting in {} ...'.format(datetime.now().time(), minutos_reconexion))
        time.sleep(minutos_reconexion * 60) 
        driver.find_element(By.XPATH, "//*[contains(text(), 'DORILEA')]").click()
        print('Reconnected')


def next_city():
        driver.find_element(By.XPATH, "//*[@id='ui_box']/div[17]/div[2]").click()
        driver.find_element(By.CSS_SELECTOR, 'div.btn_jump_to_town.circle_button.jump_to_town').click()


async def recursos_maras():
    print('SENDING RESOURCES TO WORLD WONDERS  {}'.format(datetime.now().time()))
    # Entrar en alianza
    driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[3]/div[1]/ul/li[3]/span/span[2]/span').click()
    print('Alianza button')
    time.sleep(2)
    # Entrar en maravillas
    driver.find_element(By.LINK_TEXT,'Maravillas del mundo').click()
    print('World wonders button')
    # Elegir primera maravilla
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,'El templo de Artemisa en Éfeso').click()
    # Entrar en info manuel mamahuevo
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="info"]').click()
    print('Dentro de info')
    time.sleep(5)
    # Seleccionar recurso a enviar
    driver.find_element(By.XPATH,"//*[contains(text(), 'wood')]").click()
    time.sleep(5)

    try:
        driver.find_element(By.XPATH,"//*[contains(text(), 'Enviar recursos')]").click()
    except:
        print("whatever")
        
    print('Recursos enviados')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME,'btn_next_town button_arrow right').click()
    print('Siguiente ciudad')
    time.sleep(2)
    

driver = init_driver()
Login()

async def main():

    recogida_aldeas_task = asyncio.create_task(recogida_aldeas(minutos_frecuencia_comercio * 60))
    await recogida_aldeas_task
    #asyncio.create_task(recursos_maras())
    #await recursos_maras
    asyncio.create_task(comerciar())
    #asyncio.create_task(evento())

while True:
    asyncio.run(main())
