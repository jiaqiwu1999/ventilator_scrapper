# Scrapper for ventsim.cc
import time
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


SAVE_DIR = './data/ventsim/'
JSON_FILE = 'ventsim_params.json'
DURATION = 10
RESOLUTION = 0.01
CYCLE = 3

with open('params.json', 'r') as f:
    DICT = json.load(f)


def simulate(info, driver, locator, start, save_graph):
    labels = driver.find_elements(By.XPATH, '//label[@class="netlogo-widget netlogo-slider netlogo-input"]')
    save_name = info['name']
    input_change_field = None
    rr = int(info['Lung-RR'])
    duration = (60 // rr) * 6
    buffer = []
    for label in labels:
        name = label.find_element(By.XPATH, './/span[@class="netlogo-label"]').text
        # print(name)
        input = label.find_element(By.XPATH, './/input[@type="number"]')
        input.clear()
        val = info[name]
        if isinstance(val, list):
            input_change_field = input
            buffer = val
            val = buffer[0]
            counter = 0
            interval = (60 // rr) * CYCLE
            duration =  interval * len(buffer)
            # change_param = name
        input.send_keys(str(val))

    pressures = []
    flows = []
    volumes = []

    start.click()

    start_time = time.time()

    while time.time() - start_time < duration:
        if (input_change_field != None and int(time.time() - start_time) % interval == 0 and  int(time.time() - start_time) > counter * interval):
            # print("%d seconds has passed" % (time.time() - start_time))
            print("Changing parameters...")
            counter += 1
            input_change_field.clear()
            # print("counter is %d" % counter)
            input_change_field.send_keys(str(buffer[counter]))
        curr_pressure = locator['Airway Pressure'].text
        curr_flow = locator['Flow'].text
        curr_vol = locator['Volume'].text
        pressures.append(float(curr_pressure))
        flows.append(float(curr_flow)) 
        volumes.append(float(curr_vol))
        time.sleep(RESOLUTION)
        
    start.click()
    print(f"Simulation of {save_name} is done")
    np.savetxt(f'{SAVE_DIR}{save_name}_pressure.csv', np.asarray(pressures), delimiter=',')
    np.savetxt(f'{SAVE_DIR}{save_name}_flow.csv', np.asarray(flows), delimiter=',')
    np.savetxt(f'{SAVE_DIR}{save_name}_volume.csv', np.asarray(volumes), delimiter=',')

    if save_graph:
        fig, axs = plt.subplots(nrows=3, ncols=1)
        axs[0].plot(pressures)
        axs[0].set_ylabel('Pressure')
        axs[1].plot(flows)
        axs[1].set_ylabel('Flow')
        axs[2].plot(volumes)
        axs[2].set_ylabel('Volume')
        plt.savefig(f'{SAVE_DIR}{save_name}.png')







def main():
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
    url = 'https://ventsim.cc/#/ps'
    driver.get(url)
    time.sleep(5)
    # try:
    #     element_present = EC.presence_of_element_located((By.ID, 'netlogo-button-14'))
    #     WebDriverWait(driver, 10).until(element_present)
    # except TimeoutException:
    #     print ("Timed out waiting for page to load, please start again")
    #     exit(1)
    frame = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(frame)

    start = driver.find_element(By.ID, 'netlogo-button-14')

    reset = driver.find_element(By.ID, 'netlogo-button-15')

    outputs = driver.find_elements(By.XPATH, '//div[@class="netlogo-widget netlogo-monitor netlogo-output"]')
    locator = {}
    for output in outputs:
        lab = output.find_element(By.TAG_NAME, 'label').text
        locator[lab] = output.find_element(By.TAG_NAME, 'output')

    for event_type in DICT['todo']:
        for i, event in enumerate(DICT['todo'][event_type]):
            try:
                simulate(event, driver, locator, start, True)
            except:
                print("Something went wrong in this simulation..")
                DICT['todo'][event_type] = DICT['todo'][event_type][i:]
                exit(1)
            reset.click()
            if not event_type in DICT['finished']:
                DICT['finished'][event_type] = []
            DICT['finished'][event_type].append(event)
    del DICT['todo'][event_type]

    print("finished simulating todo events ~ ")
    try:
        j = json.dumps(DICT, indent=4)
        with open(JSON_FILE, 'w') as f:
            f.write(j)
    except:
        print("Failed to update json file...")

    # plt.plot(pressures)
    # plt.show()

    
    # driver.execute_script("arguments[0].setAttribute('value', arguments[1])", compliance, '0.3')





if __name__ == '__main__':
    main()