from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=D:\OnePiece")
baseurl = "https://aniworld.to/anime/stream/one-piece/staffel-{staffel}/episode-{episode}"
browser = webdriver.Chrome()
def changeurl(x,y):
    browser.get(baseurl.format(staffel = x,episode = y))
    if browser.current_url != baseurl.format(staffel = x,episode = y):
        return True
    time.sleep(1)
    elem = browser.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/div[5]/ul/li[2]/div/a")
    redirectlink = elem.get_attribute("href")
    browser.get("https://aniworld.to/"+redirectlink)
    time.sleep(2)
    doodlelink = browser.current_url
    print(doodlelink)
    baseurl9 = "https://9xbuddy.com/process?url={x}".format(x = doodlelink)
    browser.get(baseurl9)
    time.sleep(1)
    elem2 = browser.find_element(By.XPATH,"/html/body/main/section/section[3]/section[2]/div[2]/div[4]/div[2]/a")
    downloadlink = elem2.get_attribute("href")
    browser.get(downloadlink)
    return False

staffel = 1
episode = 2

while True:
    ende = changeurl(staffel,episode)
    episode += 1
    if ende == True:
        print("Ende der Staffel")
        episode = 1
        staffel += 1
        print("Staffel",staffel)
        if staffel == 22:
            print("Fertig")
            break
        
    
    
browser.quit()