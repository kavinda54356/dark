import os
import urllib.request
import threading
import datetime
import tkinter as tk
from tkinter import ttk
import sys
import socks
from new_file import detect_system_proxy, set_proxy

class DownloadManager:
    def __init__(self):
        self.url = ''
        self.filename = ''
        self.paused = False
        self.lock = threading.Lock()

    def download_file(self, url, filename, proxy=None):
        if proxy is not None:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename, reporthook=self._progress_hook)
        print('Download complete!')

    def _progress_hook(self, count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write('Downloading... %d%%' % percent)
        sys.stdout.flush()

    def pause_download(self):
        self.paused = True

    def resume_download(self):
        self.paused = False

    def _download(self):
        if os.path.exists(self.filename):
            file_size = os.path.getsize(self.filename)
            headers = urllib.request.urlopen(self.url).info()
            total_size = int(headers['Content-Length'])
            if file_size == total_size:
                print('File already downloaded')
                return
            elif file_size > total_size:
                print('File corrupted, deleting and restarting download')
                os.remove(self.filename)
            else:
                print('Resuming download from where it left off')
                headers['Range'] = f'bytes={file_size}-'
        urllib.request.urlretrieve(self.url, self.filename, reporthook=self._progress_hook)

        with self.lock:
            if self.paused:
                return

        print('Download complete!')

    def log_download(self, filename, size, speed):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'{timestamp} - File: {filename}, Size: {size}, Speed: {speed}'
        with open('download_history.txt', 'a') as file:
            file.write(log_entry + '
')

    def monitor_clipboard(self):
        root = tk.Tk()
        root.withdraw()
        while True:
            clipboard_text = root.clipboard_get()
            if clipboard_text.startswith('http://') or clipboard_text.startswith('https://'):
                filename = clipboard_text.split('/')[-1]
                self.download_file(clipboard_text, filename)
