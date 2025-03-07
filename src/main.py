from datetime import timedelta
import subprocess


def generate_clip(video_id, timestamp):
    """Baixa apenas o trecho desejado da live e gera um clipe"""
    video_url = f"https://www.youtube.com/watch?v=" + \
        str(video_id)  # link live
    clip_name = f"clip_{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"

    # Define o tempo de início do clipe (-30 segundos do timestamp)
    start_time = (timestamp - timedelta(seconds=30)).strftime("%H:%M:%S")
    init_time = timestamp.strftime("%H:%M:%S")

    print(f"📥 Baixando o trecho da live do YouTube...")

    # Baixa apenas os últimos 30 segundos diretamente da live
    subprocess.run([
        "yt-dlp", "-f", "best", "--download-sections", f"*{start_time}-{init_time}", "-o", clip_name, video_url
    ])

    print(f"✅ Clip salvo como: {clip_name}")
    return clip_name
