import requests

# Configurações
API_KEY = "AIzaSyCtQOZbR1SwjZwqzcLOGnzW-aNVIJbwEGM"
STREAMERS = {
    "Hina": "UCQQfneexNE9cX88ZLyD-bQA",  # ID do canal do YouTube
}


def verificar_streamer_online(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&eventType=live&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        return True  # O streamer está online
    return False  # O streamer não está online


def listar_streamers_online():
    online_streamers = []
    for nome, channel_id in STREAMERS.items():
        if verificar_streamer_online(channel_id):
            online_streamers.append(nome)

    return online_streamers


# Teste: Listar quais streamers estão ao vivo
streamers_online = listar_streamers_online()
if streamers_online:
    print("Streamers online:", streamers_online)
else:
    print("Nenhum streamer está ao vivo no momento.")
