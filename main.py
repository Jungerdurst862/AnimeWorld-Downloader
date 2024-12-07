import Libary
import GetPopular
import JD
import configuration
import NewestAnimes
import Discord_Interaction
from selenium.webdriver.common.by import By
import os

time = Libary.time

#configuration for selenium
options = Libary.webdriver.ChromeOptions() 
options.add_argument("download.default_directory=D:\OnePiece")

#Configuration
DiscordUse = configuration.Use_Discord
Set_Stop = configuration.Set_Stop
Stop_episode = configuration.Stop_episode
Stop_Season = configuration.Stop_Season
Amount_of_new_Anime_Download_popular = configuration.Amount_of_new_Anime_Download_popular
Amount_of_new_Anime_Download_new = configuration.Amount_of_new_Anime_Download_new
scratch_popular = configuration.scratch_popular
scratch_newest = configuration.scratch_newest
namelist = configuration.namelist
only_download_links = configuration.only_download_links
onlygerman = configuration.onlygerman
withgermanSubtitle = configuration.withgermanSubtitle
Webhock = configuration.Webhock
staffel = configuration.staffel
episode = configuration.episode
wait_time = configuration.wait_time
Hallo  = True
finsihedepisodes = episode - 1
first_run = True
url_list = ["dood.li","vidmoly.to"]

baseurl = "https://aniworld.to/anime/stream/{animename}/staffel-{staffel}/episode-{episode}"

browser = Libary.webdriver.Chrome()

def Discord_Message(message):
    if DiscordUse:
        Libary.requests.post(Webhock, json={"content": message})

def check_right_language(flag_src):
    if onlygerman == True:
        if flag_src == "https://aniworld.to/public/img/german.svg":
            return True
        else:
            return False
    if withgermanSubtitle == True:
        if flag_src == "https://aniworld.to/public/img/japanese-german.svg":
            return True
        else:
            return False

def language():
    germanlanguage = False
    germansub = False
    
    language = browser.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/div[5]/div[1]/div/img[1]") #language
    
    if onlygerman:
        if language.get_attribute("data-lang-key") == "1" or language.get_attribute("src") == "https://aniworld.to/public/img/german.svg":
            germanlanguage = True
        else:
            print(f"Staffel {staffel}, Episode {episode}: wrong language")
            return False
    
    if withgermanSubtitle:
        if language.get_attribute("data-lang-key") == "3" and language.get_attribute("src") == "https://aniworld.to/public/img/japanese-german.svg":
            germansub = True
        elif not germanlanguage:
            return False
    
    return True

def change_to_voe(url):
    beginchange = str.find(url, '//')
    endchange = str.find(url, '/', beginchange + 2)
    if url[beginchange+2:endchange] in url_list:
        print("doodle link")
        return url
    else:
        return url[:beginchange+2] + 'voe.sx' + url[endchange:]
    

def changeurl(x,y,name,single : bool = False,seperate_name : str = ""):
    browser.get(baseurl.format(staffel = x,episode = y,animename = name))
    if browser.current_url != baseurl.format(staffel = x,episode = y,animename = name):
        return True
    time.sleep(1)
    
    language_result = language()  
    if language_result == False:
        Discord_Message(f"Staffel {x}, Episode {y}: No suitable Language stream found")
    
    elem = browser.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/div[5]/ul/li[1]/div/a")   #VOE
    #elem = browser.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[3]/div[5]/ul/li[2]/div/a")  #doodstream
    redirectlink = elem.get_attribute("href")
    browser.get("https://aniworld.to/"+redirectlink)
    Libary.time.sleep(2)
    doodlelink = browser.current_url
    voelink = change_to_voe(str(doodlelink))
    link_paste = "new" if single else "Serie"
    past_name = seperate_name if seperate_name != "" else name
    File = open(f"{link_paste}Links/"+past_name,"a")
    File.write(voelink+'\n')
    File.close()
    
    JD.add_links(voelink,packagename=f"{name} Staffel:{staffel}",destinationFolder=f"D:/OnePiece/{name}/Staffel{staffel}")
  
  
def CheckIfEnded(staffel2,episode2,name):
    browser.get(baseurl.format(staffel = staffel2,episode = episode2 + 1,animename = name))
    
    time.sleep(1)
    
    if browser.current_url == baseurl.format(staffel = staffel2,episode = episode2 + 1,animename = name):
        return True
    else:
        return False

def Continue_download():
    if scratch_popular:
        popular_animes,href = GetPopular.get_popular_animes(browser=browser,limit = Amount_of_new_Anime_Download_popular)
        for index, x in enumerate(popular_animes):
            name_begin = href[index].find("stream/")
            if href[index][name_begin + 7:] not in os.listdir("SerieLinks"):
                Discord_Message(f"Appended new Anime to the list:{x} link:{href[index][name_begin + 7:]}")
                namelist.append(href[index][name_begin + 7:])
    if scratch_newest:
        newest_animes,Download_succes,href = NewestAnimes.get_newest_animes(browser=browser,limit = Amount_of_new_Anime_Download_new,onlygerman=onlygerman,withgermanSubtitle=withgermanSubtitle)
        if Download_succes:
            for index, x in enumerate(newest_animes):
                name_begin = href[index].find("stream/")
                noslashes = href[index][name_begin + 7:].replace("/","-!-")
                if noslashes not in os.listdir("newlinks"):
                    Discord_Message(f"Appended new Anime episode to the list:{x} link:{href[index][name_begin + 7:]}")
                    end_link = href[index][name_begin + 7:]
                    anime_name = end_link[:end_link.rfind("staffel")-1]
                    staffel = end_link[end_link.rfind("/staffel-")+9:end_link.rfind("/staffel-")+10]
                    episode = end_link[end_link.rfind("/episode-")+9:]
                    changeurl(int(staffel), int(episode), anime_name, single=True,seperate_name=noslashes)
                    #namelist.append(href[index][name_begin + 7:])
    
def get_anime_info(anime_name):
    # Navigate to the anime page
    browser.get(f"https://aniworld.to/anime/stream/{anime_name}")
    time.sleep(2)  # Wait for the page to load

    total_episodes = 0
    total_seasons = 0

    # Find all season elements
    seasons = browser.find_elements(By.XPATH,"/html/body/div/div[2]/div[2]/div[2]/ul[1]/*")
    seasonlist = []
    for x in seasons:
        seasonlist.append("dw")
    for index,shit in enumerate(seasonlist):
        try:
            season = browser.find_element(By.XPATH, f"/html/body/div/div[2]/div[2]/div[2]/ul[1]/li[{index+1}]")
            if season.get_attribute("innerText") == "Staffeln:" or season.get_attribute("innerText") == "Filme":
                continue
            season_number = int(season.get_attribute("innerText"))
            browser.get(baseurl.format(staffel = season.get_attribute("innerText"), episode = 0, animename = anime_name))
            # Wait for episodes to load
            time.sleep(1)
            # Find all episode elements for this season
            episodes = browser.find_elements(By.XPATH, f"/html/body/div/div[2]/div[2]/div[2]/ul[2]/*")
            episode_num = len(episodes) - 1
            total_episodes += episode_num
        except Exception as e:
            print(f"Error processing anime {index - 2}: {str(e)}")
            continue
        total_seasons += 1
    return total_episodes, total_seasons

while Hallo == True:
    if namelist == []:
        if only_download_links:
            Discord_Message(f"Finished getting all Links")
            break
        else:
            Continue_download()
            continue
        
    if first_run:
        total_episodes , total_seasons = get_anime_info(namelist[0])
        message_id = Discord_Interaction.Create_Progress_Message(anime_name=namelist[0],finished=0, total=total_episodes)
        first_run = False
        
    ende = changeurl(staffel,episode,namelist[0])
    
    finsihedepisodes += 1
    episode += 1
        
    if ende == True:
        episode = 1
        staffel += 1
        
        Continue = CheckIfEnded(staffel,episode,namelist[0])
        
        if Continue == True:
            print("Next Staffel:",staffel)
            
        else:
            Discord_Message(f"Finished downloading all episodes for {namelist[0]}")
            namelist.pop(0)
            staffel = 1
            episode = 1
            finsihedepisodes = 0
            
            #JD.send_download()
            total_episodes , total_seasons = get_anime_info(namelist[0])
            message_id = Discord_Interaction.Create_Progress_Message(anime_name=namelist[0],finished=0, total=total_episodes)
    if finsihedepisodes <= total_episodes: 
        Discord_Interaction.Update_Progress_Message(message_id, finsihed=finsihedepisodes, total=total_episodes,anime_name=namelist[0])
     
     
            


browser.quit()