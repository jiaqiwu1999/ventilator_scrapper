import json
import argparse
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


GEN_TEMP = True

ADD_TEMP = False

def gen_template(keys, values, index, length=10):
    d = {'finished': [], 'todo': []}
    temp = dict(zip(keys, values))
    temp = [temp] * length
    d['todo'] = temp
    j = json.dumps(d, indent=4)
    with open(f'xlung_param_type_{index}.json', 'w') as f:
        f.write(j)

def main():
    parser = argparse.ArgumentParser(description='generate/add to json templates')
    parser.add_argument('--gen', default=True, action=argparse.BooleanOptionalAction, help='Generate new template?')
    parser.add_argument('--add', default=False, action=argparse.BooleanOptionalAction, help='Add to existing template?')
    parser.add_argument('--type', default=1, help='Type of patient [0-9]')
    args = parser.parse_args()
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
    # time.sleep(5)
    #pause = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,  'pauseSimulation')))
    # confirm = driver.find_element(By.CLASS_NAME, 'commit-button center-block')
    # pause = driver.find_element(By.CLASS_NAME, 'dropdown')
    #pause.click()
    # inp = driver.find_element(By.ID, 'age')
    # inp.send_keys('20')
    try:
        WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME,  'loading')))
    except:
        print("Timed out..")
    patient_category = driver.find_element(By.XPATH, '//a[@class="dropdown-toggle"][contains(text(), "Normal")]')
    patient_category.click()

    menu = driver.find_element(By.XPATH, '//li[@class="dropdown open"]')
    menu_items = menu.find_element(By.XPATH, './/ul')
    lis = menu_items.find_elements(By.XPATH, './/li')
    lis[args.type].click()

    inputs = driver.find_elements(By.XPATH, '//input[@type="number"]')
    names = []
    vals = []
    if args.gen:
        for inp in inputs:
            n = inp.get_attribute('id')
            val = inp.get_attribute('value')
            print(n)
            names.append(n)
            vals.append(val)
        gen_template(names, vals, args.type)
    with open(f'xlung_params_type_{args.type}', 'r') as f:
        params = json.load(f)
    if args.add:
        for inp in inputs:
            n = inp.get_attribute('id')
            val = inp.get_attribute('value')
            print(n)
            names.append(n)
            vals.append(val)
        p = dict(zip(names, vals))
        params['todo'].append([p] * 5)
        j = json.dumps(params, indent=4)
        with open(JSON_FILE, 'w') as f:
            f.write(j)


if __name__ == '__main__':
    main()