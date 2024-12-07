#First of all you have to make an instance of the Myjdapi class and set your APPKey:
import myjdapi

jd=myjdapi.Myjdapi()
jd.set_app_key("EXAMPLE")

"""
After that you can connect.
Now you can only connect using username and password.
This is a problem because you can't remember the session between executions
for this reason i will add a way to "connect" which is actually not connecting,
but adding the old tokens you saved. This way you can use this between executions
as long as your tokens are still valid without saving the username and password.
"""

jd.connect("paul.lennard.kessel@icloud.com","PaLeKe6280!")

# When connecting it gets the devices also, so you can use them but if you want to
# gather the devices available in my.jdownloader later you can do it like this

jd.update_devices()

# Now you are ready to do actions with devices. To use a device you get it like this:
device=jd.get_device("JDownloader@paull")
lincs=myjdapi.myjdapi.Linkgrabber(device)
def add_links(links,packagename = "TestPackage",destinationFolder = "D:\OnePiece"):
    lincs.add_links([{
                          "autostart": True,
                          "links": links,  #Youtube account link (see examples below)
                          "packageName":packagename, #Name you want to call it, it will be used for the folder name
                          "extractPassword": None,
                          "priority": "DEFAULT",
                          "downloadPassword": None,
                          "destinationFolder": destinationFolder, 
                          "overwritePackagizerRules": True
                      }])

print('collecting...')
while(lincs.is_collecting()): #Wait while collecting links
    pass

linkList = lincs.query_links() #List of dictionaries with all links collected in Linkgrabber tab (you may want to clean it before collecting)
audios=[] #list of audio files
packageids=[]
linkids=[]
downloadfiles = [] #List of filenames in JD Downloads tab. It will be used to compare with Linkgrabber links, so you don't download files that you already have
downloads=device.downloads.query_links() #List of dictionaries of JD Downloads tab

for dic in downloads:
	downloadfiles.append(dic['name']) #Get filenames in JD Downloads tab

files=[] #List of files in Linkgrabber

for dic in linkList:
	files.append(dic['name']) #Get filenames in JD Linkgrabber tab                      
                    
for dic in linkList:
    file = dic['name'] #Single filename in Linkgrabber link
    if file.endswith('aac') or file.endswith('m4a') or file.endswith('ogg'): #if file is an audiofile...
        if file not in downloadfiles: #if file is it not already downloaded
            audios.append(file) #Add it to audiofile list, to be downloaded
            packageids.append(dic.get('packageUUID')) #Package ID of the audio file
            linkids.append(dic.get('uuid')) #Link ID of the audio file
            
def send_download():
    lincs.move_to_downloadlist(linkids, packageids) #Move the audio files to the Downloads list,pac


