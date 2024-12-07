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
    #elem = browser.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/div[5]/ul/li[4]/div/a")#Stramtape
    elem = browser.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/div[5]/ul/li[2]/div/a")#Doodle
    redirectlink = elem.get_attribute("href")
    browser.get("https://aniworld.to/"+redirectlink)
    time.sleep(2)
    doodlelink = browser.current_url
    print(doodlelink)
    File = open("doodlelink","a")
    File.write(doodlelink+'\n')
    File.close()
    return False

staffel = 4
episode = 24

missing = []

def getEpisodeFromFile():
    File = open("ErrorHandle","r")
    ListOfStaffeln = File.readlines()
    staffel2 = 0
    for x in ListOfStaffeln:
        y = 0
        y2 = ""
        for x2 in x:
            if x2.isdigit() == True:
                y2 += str(x2)
            else:
                if y2 != "":
                    if y == 0:
                        staffel2 = int(y2)
                    if y == 1:
                        missing.append([staffel2,int(y2)])
                    y += 1
                y2 = "" 
    print(missing)
    
getEpisodeFromFile()
for x in missing:
    count = 0
    for x2 in x:
        if count == 0:
            staffel = x2
        else:
            episode = x2
        count += 1
    print(staffel,episode)
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