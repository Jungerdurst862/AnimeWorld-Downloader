
import Libary
from selenium.webdriver.common.by import By
import Discord_Interaction as discord

Discord_Message = discord.Discord_Message

def get_popular_animes(browser,limit=100):
    popular_animes = []
    animes_href = []
    browser.get("https://aniworld.to/beliebte-animes")
    
    try:
        # Wait for the anime list to load
        Libary.WebDriverWait(browser, 10).until(
            Libary.EC.presence_of_element_located((By.CLASS_NAME, "paragraph-end"))
        )

        # Find all anime elements
        anime_elements = browser.find_elements(By.XPATH, "/html/body/div/div[3]/div[2]/*")##wrapper > div.container.marginBottom > div.seriesListContainer.row > div:nth-child(2)   /html/body/div/div[3]/div[2]/div[2]   children

        for index, anime in enumerate(anime_elements[:limit]):
            try:
                href_elements = browser.find_element(By.XPATH,f"/html/body/div/div[3]/div[2]/div[{index + 1}]/a")
                title_element = anime.find_element(By.XPATH,f"/html/body/div/div[3]/div[2]/div[{index + 1}]/a/h3" )#  /html/body/div/div[3]/div[2]/div[1]/a
                href = href_elements.get_attribute('href')
                title = title_element.text
                popular_animes.append(title)
                animes_href.append(href)
            except Exception as e:
                print(f"Error processing anime {index + 1}: {str(e)}")
                continue

    except Libary.TimeoutException:
        print("Timeout while loading the popular animes page")
        Discord_Message("Failed to load popular animes list")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        Discord_Message(f"An error occurred while fetching popular animes: {str(e)}")

    # Print the page source if no animes were found
    if not popular_animes:
        print("No animes found. Printing page source:")

    return popular_animes,animes_href
