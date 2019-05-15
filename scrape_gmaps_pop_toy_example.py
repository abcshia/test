import matplotlib.pyplot as plt

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# Chrome
from selenium.webdriver.chrome.options import Options
driverPath = r'C:\Users\James\OneDrive\PythonFiles\packages\selenium\WebDrivers\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path = driverPath)

## fetch popularity data

# search key words
search_words = 'daimo'#'Asian Pearl Seafood Restaurant'

# get search results from google maps
html_url = 'https://maps.google.com'
driver.get(html_url)
WebDriverWait(driver,60).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))

searchbox = driver.find_element_by_id('searchboxinput')
searchbox.send_keys(search_words)
searchbutton = driver.find_element_by_id('searchbox-searchbutton')
searchbutton.click()


# wait to load page
WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-popular-times')))

# CSS Selector
s_hour = 3
e_hour = 27
labels = []
for hour in range(s_hour,e_hour):
    css = '.section-popular-times-graph-visible > div:nth-child(' + str(hour) + ')'
    elements = driver.find_elements_by_css_selector(css)
    if len(elements) > 0:
        element = elements[0]
        label = element.get_attribute('aria-label')
        labels.append(label)
    else:
        e_hour = hour
        break


# Regular expression: extract percentage. See https://docs.python.org/3/library/re.html
import re
re_percentage = re.compile('\d+\%') # re_percentage.search(label).group() gives the percentage. e.g. '40%'
re_hour = re.compile('\d+(?= AM)|\d+(?= PM)|\d+(?=時)') # exclude %, (?!...) excludes, (?=...) is like AND

matches = ['Currently',
           '目前']
# check for words in list matches to see if current time info is available
def get_current(s,matches):
    for match in matches:
        if match in s:
            return(True)


pops = []
current = np.nan
for i,label in enumerate(labels):
    # c = label.find('Currently')
    # if c != -1:
    if get_current(label,matches):
        current = i
    else:
        print('hour:{}\tpercentage:{}'.format(re_hour.search(label).group(),re_percentage.search(label).group()))
    pop = np.int(re_percentage.search(label).group()[:-1])
    pops.append(pop)
    
    
plt.bar(np.arange(s_hour,e_hour),pops)
if ~np.isnan(current):
    plt.bar(np.arange(s_hour,e_hour)[current],pops[current],color='magenta')
# plt.plot(np.arange(s_hour,e_hour),pops)

plt.ylim(0,100)
plt.show()



driver.close()