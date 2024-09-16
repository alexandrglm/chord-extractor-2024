import yt_dlp as youtube_dl
from pydub import AudioSegment

def download_audio_from_youtube(youtube_url, output_path='downloaded_audio.mp3'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': output_path,
        'noplaylist': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        return output_path
