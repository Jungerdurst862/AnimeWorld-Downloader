import Libary
By = Libary.By

Last_news = []

def Test_Download(newest_animes):
    if Last_news != [newest_animes]:
        return True
    return False
    
def check_right_language(flag_src : str,onlygerman : bool = True, withgermanSubtitle : bool = False):
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
def get_newest_animes(browser,limit = 150,onlygerman : bool = True, withgermanSubtitle : bool = False ):

    try:
        # Navigate to the aniworld.to homepage
        browser.get("https://aniworld.to/neue-episoden")
        base_XPATH = "/html/body/div/div[2]/div[2]/div[1]"

        # Wait for the anime list to load
        Libary.WebDriverWait(browser, 10).until(
            Libary.EC.presence_of_element_located((By.XPATH, f"{base_XPATH}/div[last()]"))
        )
        #scroll down to load more anime elements
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #time.sleep(1)
        # Find all anime elements
        anime_elements = browser.find_elements(By.XPATH, f"{base_XPATH}/*")
        
        
        if limit > len(anime_elements):
            limit = len(anime_elements) 
            
        newest_animes = []
        anime_href = []
        for index,anime in enumerate(anime_elements[:limit]):
            try:
                element_count = anime.get_attribute("childElementCount")
                if element_count != str(0):
                    flag_load = anime.find_element(By.XPATH,f"{base_XPATH}/div[{index+1}]/div/div/img")#/html/body/div/div[2]/div[2]/div[1]/div[1]/div/div/img
                    language_result = check_right_language(flag_load.get_attribute("src"),onlygerman=onlygerman,withgermanSubtitle=withgermanSubtitle)
                    if language_result == True:
                        title_element = anime.find_element(By.XPATH, f"{base_XPATH}/div[{index+1}]/div/div/a/strong")#/html/body/div/div[2]/div[2]/div[1]/div[1]/div/div/a/strong
                        title = title_element.get_attribute("outerText")
                        href_element = anime.find_element(By.XPATH, f"{base_XPATH}/div[{index+1}]/div/div/a")
                        href = href_element.get_attribute('href')
                        newest_animes.append(title)
                        anime_href.append(href)
            except Exception as e:
                print(f"Error processing anime: {str(e)}")
                continue
            
        
    except Libary.TimeoutException:
        print("Timeout while loading the newest animes page")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    Download_succes = Test_Download(newest_animes)
    if Download_succes == True:
        Last_news.clear()
        Last_news.append(newest_animes)
    return newest_animes,Download_succes,anime_href