# Ventilator Scraper
- Scraps online simulation data (volume, flow, pressure) from ventsim.cc and xlung.net
- Save the data as .csv file and .png (for visualization)
- Used for lung-ventilation related projects that requires patient ventilator interaction

# Prerequisites
1. Require an account access at https://ventsim.cc/#/
2. Firefox browser
3. Python, selenium, webdriver installed 


# File breakdown
1. Parameter JSON files: consists of the parameters for simulation
2. template.py: used to generate (--gen) or add (--add) default templates for different types of xlung simulation <br />
  - Needs to specify patient type (--type) and ventilator mode (--mode)
<img width="340" alt="image" src="https://user-images.githubusercontent.com/59846636/176464743-409df87d-f69f-4bcb-92e2-5bf078185dca.png">
<img width="320" alt="image" src="https://user-images.githubusercontent.com/59846636/176464798-8054d4a8-bfb0-485b-a756-b447c934cfc3.png">
3. xlung.py: scraps xlung.net <br />
  - Needs to specify patient type (--type) and ventilator mode (--mode) <br />
4. ventsim.py: scraps https://ventsim.cc/#/ps <br />
  - Needs to specify whether to save a graph (--save) <br />

# TODO
1. Change the Firefox profile path according to your own laptop in xlung.py, template.py & ventsim.py
