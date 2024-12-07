import requests
import Libary
import time

#write your webhook url here
Webhock = ""
autherization = ""#your authorization for discord.com
headers = {
    'authorization':autherization,
    'Content-Type': 'application/json'
    }
Channel_id = ""#channel id where you want to send the message

yes_list = ["ja", "yes","jo","yur","yurr"]
def Discord_Message(message):
    response = requests.post(Webhock, json={"content": message})
    
def get_last_message(limit = 1):
    response = requests.get(f"https://discord.com/api/v8/channels/{Channel_id}/messages?limit={limit}",headers=headers)
    return response.json()
    
def Create_Progress_Message(anime_name : str, finished : int, total : int):
    left = total - finished
    progress = (finished / total) * 100
    default_json = {
                    'embeds': [
                        {
                            'title': 'Anime Progress',
                            'description': f'Anime Name: {anime_name}\nProgress: {finished}/{total}',
                            'color': 0x00FF00,
                            'fields': [
                                {
                                    'name': 'Finsihed',
                                    'value': finished,
                                    'inline': True
                                },
                                {
                                    'name': 'Total',
                                    'value': total,
                                    'inline': True
                                },
                                {
                                    'name': 'Progress',
                                    'value': f'{progress:.2f}%',
                                    'inline': True
                                },
                                {
                                    'name': 'Left',
                                    'value': left,
                                    'inline': True
                                }
                            ]
                        
                        }
                    ]}
    requests.post(Webhock,json=default_json)
    response = get_last_message()
    return response[0]['id']

def wait_for_yes(wait_time:int):
    repeat_count = 0
    while repeat_count < wait_time:
        last_message = get_last_message()
        print(last_message[0]['content'].casefold())
        if last_message[0]['content'].casefold() in yes_list:
            return True
        repeat_count += 1
        Libary.time.sleep(1)

def Update_Progress_Message(message_id : int ,total : int , finsihed : int, anime_name : str):
    left = total - finsihed
    progress = (finsihed / total) * 100
    default_json = {
                    'embeds': [
                        {
                            'title': 'Anime Progress',
                            'description': f'Anime Name: {anime_name}\nProgress: {finsihed}/{total}',
                            'color': 0x00FF00,
                            'fields': [
                                {
                                    'name': 'Finsihed',
                                    'value': finsihed,
                                    'inline': True
                                },
                                {
                                    'name': 'Total',
                                    'value': total,
                                    'inline': True
                                },
                                {
                                    'name': 'Progress',
                                    'value': f'{progress:.2f}%',
                                    'inline': True
                                },
                                {
                                    'name': 'Left',
                                    'value': left,
                                    'inline': True
                                }
                            ]
                        
                        }
                    ]}
    response = requests.patch(f"{Webhock}/messages/{message_id}",json=default_json)
    

def Start_wait(wait_time : int): 
    wait_for_yes(wait_time = wait_time)
    return True


    


    
    