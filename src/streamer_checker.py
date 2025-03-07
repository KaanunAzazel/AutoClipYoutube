import requests
from config import API_KEY, STREAMERS


def verificar_streamer_online(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&eventType=live&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        return True  # O streamer está online
    return False  # O streamer não está online


def get_live_chatID(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={video_id}&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data["items"][0]["liveStreamingDetails"]:
        return (data["items"][0]["liveStreamingDetails"]["activeLiveChatId"])


def get_live_videoID(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?part=id&channelId={channel_id}&type=video&eventType=live&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data["items"][0]["id"]["videoId"]:   # Percusso no Json
        # LiveID da transmissão online
        return (data["items"][0]["id"]["videoId"])

    return "No VideoID Founded"


def listar_streamers_online():
    online_streamers = []
    for nome, channel_id in STREAMERS.items():
        if verificar_streamer_online(channel_id):
            online_streamers.append(nome)

    return online_streamers


# Teste: Listar quais streamers estão ao vivo

videoID = get_live_videoID(STREAMERS["Hina"])
get_live_chatID(videoID)
# streamers_online = listar_streamers_online()
# if streamers_online:
#     print("Streamers online:", streamers_online)
# else:
#     print("Nenhum streamer está ao vivo no momento.")
