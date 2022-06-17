import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
from bs4 import BeautifulSoup

SAVE_DIR = './data/'
DURATION = 10
RESOLUTION = 0.01


DICT = [
    {
        'Lung-Compliance': 0.1,
        'Lung-Resistance': 10,
        'Lung-V0': 0,
        'Lung-Shift': -0.1,
        'Lung-RR': 12,
        'lung-Pmus': 5,
        'Lung-Ti': 1,
        'Vent-PS': 5,
        'vent-PEEP': 5,
        'Vent-InspCycleOff': 30
    },
]


def main():
    geckodriver_autoinstaller.install()

    profile = webdriver.FirefoxProfile(
        '/Users/wujiaqi/Library/Application Support/Firefox/Profiles/756agzw0.default-release')

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX

    driver = webdriver.Firefox(firefox_profile=profile,
                            desired_capabilities=desired)
    url = 'https://ventsim.cc/#/ps'
    driver.get(url)
    frame = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(frame)

    labels = driver.find_elements(By.XPATH, '//label[@class="netlogo-widget netlogo-slider netlogo-input"]')
    for label in labels:
        name = label.find_element(By.XPATH, './/span[@class="netlogo-label"]').text
        print(name)
        input = label.find_element(By.XPATH, './/input[@type="number"]')
        input.clear()
        val = DICT[0][name]
        print(str(val))
        input.send_keys(str(val))

    outputs = driver.find_elements(By.XPATH, '//div[@class="netlogo-widget netlogo-monitor netlogo-output"]')
    locator = {}
    for output in outputs:
        lab = output.find_element(By.TAG_NAME, 'label').text
        locator[lab] = output.find_element(By.TAG_NAME, 'output')
    print(locator)
    print(locator['Airway Pressure'].text)
    print(locator['Flow'].text)
    pressures = []
    flows = []
    start = driver.find_element(By.ID, 'netlogo-button-14')
    start.click()

    start_time = time.time()

    while time.time() - start_time < DURATION:
        curr_pressure = locator['Airway Pressure'].text
        curr_flow = locator['Flow'].text
        pressures.append(float(curr_pressure))
        flows.append(float(curr_flow)) 
        time.sleep(RESOLUTION)
        
    start.click()

    
    # driver.execute_script("arguments[0].setAttribute('value', arguments[1])", compliance, '0.3')





if __name__ == '__main__':
    main()