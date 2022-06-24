# Scrapper for xlung.net
import time
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

SAVE_DIR = './data/xlung/'

JSON_FILE = 'xlung_params.json'

with open(JSON_FILE, 'r') as f:
    DICT = json.load(f)



def main():
    patient_type = 1
    if not os.path.isdir(SAVE_DIR):
        os.mkdir(SAVE_DIR)
    geckodriver_autoinstaller.install()

    profile = webdriver.FirefoxProfile(
        '/Users/wujiaqi/Library/Application Support/Firefox/Profiles/756agzw0.default-release')

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX

    driver = webdriver.Firefox(firefox_profile=profile,
                            desired_capabilities=desired)
    url = 'https://simulation.xlung.net/en/xlung/demo'
    driver.get(url)
    # time.sleep(2)
    try:
        WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME,  'loading')))
    except:
        print("Timed out..")
    # confirm = driver.find_element(By.CLASS_NAME, 'commit-button center-block')

    # inp = driver.find_element(By.ID, 'age')
    # inp.send_keys('20')
    locator = {}
    inputs = driver.find_elements(By.XPATH, '//input[@type="number"]')
    for inp in inputs:
        locator[inp.get_attribute('id')] = inp
    example = DICT['todo'][0]
    pause = driver.find_element(By.CLASS_NAME, 'pauseSimulation')
    pause.click()
    dest = driver.find_element(By.TAG_NAME, 'canvas')
    patient_category = driver.find_element(By.XPATH, '//a[@class="dropdown-toggle"][contains(text(), "Normal")]')
    #patient_category.click()
    # menu = driver.find_element(By.XPATH, '//li[@class="dropdown open"]')
    # menu_items = menu.find_element(By.XPATH, './/ul')
    # lis = menu_items.find_elements(By.XPATH, './/li')
    # lis[patient_type].click()
    metabolic_disorder = driver.find_element(By.XPATH, '//a[@class="dropdown-toggle"][contains(text(), "metabolic")]')
    #metabolic_disorder.click()
    mode = driver.find_element(By.XPATH, '//a[@class="dropdown-toggle"][contains(text(), "A/C")]')
    # confirm = driver.find_element(By.CLASS_NAME, 'commit-button center-block')
    #mode.click()
    # for key in example.keys():
    #     print(key)
    #     locator[key].clear()
    #     locator[key].send_keys(example[key])
    # confirm.click()
    pause.click()
    time.sleep(15)
    pause.click()
    loc = dest.location
    width = dest.size['width']
    # print(loc)
    # print(size)
  
    action = webdriver.ActionChains(driver)
    action.move_to_element_with_offset(dest, 50, 0).perform()
    position = 0

    vols = []
    flows = []
    pressures = []

    while position < width - 100:
        action.move_by_offset(1, 0).perform()
        volume = driver.find_element(By.ID, 'absoluteVolumeLabels')
        val_vol = volume.find_element(By.TAG_NAME, 'span')
        vols.append(float(val_vol.text.split(': ')[1]))
        pressure = driver.find_element(By.ID, 'pressureLabels')
        val_pres = pressure.find_element(By.TAG_NAME, 'span')
        pressures.append(float(val_pres.text.split(': ')[1]))
        flow = driver.find_element(By.ID, 'flowLabels')
        val_flow = flow.find_element(By.TAG_NAME, 'span') 
        flows.append(float(val_flow.text.split(': ')[1]))
        position += 1

    plt.plot(vols)
    plt.savefig('xlung_example.png')


if __name__ == '__main__':
    main()