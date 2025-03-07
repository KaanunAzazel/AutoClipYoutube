import datetime
from config import API_KEY, STREAMERS
from command_handler import COMMANDS
from main import generate_clip
from streamer_checker import get_live_chatID, get_live_videoID

import requests
import time


CHANNEL_ID = STREAMERS["Hina"]
NEXT_PAGE_TOKEN = None
VIDEOID = 0


def get_chat_messages(live_chat_id):
    """Captura mensagens do chat ao vivo com polling a cada 5 segundos"""
    global NEXT_PAGE_TOKEN  # Para continuar de onde parou

    url = f"https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={live_chat_id}&part=snippet,authorDetails&key={API_KEY}"

    # Se houver um token de paginação, adiciona para continuar de onde parou
    if NEXT_PAGE_TOKEN:
        url += f"&pageToken={NEXT_PAGE_TOKEN}"

    response = requests.get(url).json()

    messages = []
    try:
        if "items" in response:
            for item in response["items"]:
                user = item["authorDetails"]["displayName"]
                message = item["snippet"]["displayMessage"]
                messages.append((user, message))  # Retorna usuário e mensagem

        # Atualiza o token para pegar novas mensagens na próxima chamada
        NEXT_PAGE_TOKEN = response.get("nextPageToken", None)
    except:
        None

    return messages


def check_for_commands(messages, video_id):
    """Verifica se alguma mensagem contém um comando válido"""
    for user, message in messages:
        print(user, " - ", message)
        for command in COMMANDS:
            if message.startswith(command):
                print(f"🎯 Comando detectado: {command} de {user}")
                timestampMsg = datetime.datetime.utcnow()
                generate_clip(video_id, timestampMsg)


def monitor_chat():
    """Verifica se há uma live ativa e captura mensagens do chat"""
    VIDEOID = get_live_videoID(CHANNEL_ID)
    if not VIDEOID:
        print("❌ Nenhuma live encontrada no momento.")
        return

    live_chat_id = get_live_chatID(VIDEOID)
    if not live_chat_id:
        print("❌ Não foi possível obter o liveChatId.")
        return

    print("✅ Monitorando o chat... Pressione Ctrl + C para parar.")

    while True:
        messages = get_chat_messages(live_chat_id)
        # Verifica comandos nas mensagens
        check_for_commands(messages, VIDEOID)
        time.sleep(5)  # Aguarda 5 segundos antes de buscar novas mensagens


# Iniciar monitoramento do chat automaticamente
monitor_chat()
