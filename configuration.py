
#main Configuration--------------------------------------------------------------------------------------------------------------------------------
namelist = ["hunter-x-hunter"] #write the name of the anime you want to download
staffel = 1         #start at this staffel
episode = 1         #start at this episode
only_download_links = False #if enable it will only donwload the name list

#will only download links with are german or have a german subtitle
onlygerman = True
withgermanSubtitle = False

#Set a Stop for the anime downloader at a specific episode or season
Set_Stop = True 
Stop_episode = 1
Stop_Season = 0

#when finsihed downloading all animes from name list the download the newest or most popular animes
#the amount of new animes to download from popular or newest animes
scratch_popular = False
scratch_newest = True
Amount_of_new_Anime_Download_popular = 10
Amount_of_new_Anime_Download_new = 150


#JDownloader Configurations ---------------------------------------------------------------------------------------------------------------------------
JDownloader_device = ""#Write your device name from JDownloader
email = ""#wirte your JD email
password = ""#write your Jd Password


#Discord Configuration----------------------------------------------------------------------------------------------------------------------------------
Use_Discord = False #if enable it will send discord messages
Webhock = ""#Channel Webhook URL
autherization = ""#your authorization for discord.com
Channel_id = ""#channel id where you want to send the message
wait_time = 60  #wait time before stop waiting for a response from discord