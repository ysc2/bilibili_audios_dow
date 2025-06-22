import os
import yt_dlp
from bilibili_api import user, sync
import time

def get_all_up_videos(mid, output_file="bilibili_videos.txt"):
    u = user.User(mid)
    all_videos = []
    page = 1

    with open(output_file, "w", encoding="utf-8") as f:
        while True:
            try:
                videos = sync(u.get_videos(pn=page))
                vlist = videos["list"]["vlist"]
                if not vlist:
                    break
                for video in vlist:
                    video_url = f"https://www.bilibili.com/video/{video['bvid']}"
                    all_videos.append(video_url)
                    f.write(video_url + "\n")
                page += 1
                time.sleep(1)
            except Exception as e:
                print(f"获取第 {page} 页失败: {e}")
                break
    return all_videos


def download_audio_from_txt(txt_file, output_dir="audio_downloads"):
    os.makedirs(output_dir, exist_ok=True)

    with open(txt_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "ffmpeg_location": "D:/work/ffmpeg-7.1.1-full_build-shared/bin/ffmpeg.exe",  # 替换为你的 FFmpeg 路径
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"正在下载: {url}")
                ydl.download([url])
            except Exception as e:
                print(f"❌ 下载失败: {e}")


if __name__ == "__main__":
    up_mid = 25660822  # 替换为目标 UP 主的 UID
    video_txt = "vedio.txt"
    audio_dir = "audios"

    #get_all_up_videos(up_mid, video_txt)
    download_audio_from_txt(video_txt, audio_dir)
