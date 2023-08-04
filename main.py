import tkinter as tk
from tkinter import ttk
import urllib.request
import os
import threading
import datetime
import sys
import socks

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

def gui_code():
    root = tk.Tk()
    root.title(Download Manager)

    url_label = tk.Label(root, text=URL: )
    url_label.pack()
    url_entry = tk.Entry(root)
    url_entry.pack()

    filename_label = tk.Label(root, text=Filename: )
    filename_label.pack()
    filename_entry = tk.Entry(root)
    filename_entry.pack()

    download_button = tk.Button(root, text=Download, command=lambda: manager.download_file(url_entry.get(), filename_entry.get()))
    download_button.pack()

    pause_button = tk.Button(root, text=Pause, command=manager.pause_download)
    pause_button.pack()

    resume_button = tk.Button(root, text=Resume, command=manager.resume_download)
    resume_button.pack()

    clipboard_button = tk.Button(root, text=Monitor Clipboard, command=manager.monitor_clipboard)
    clipboard_button.pack()

    proxy_label = tk.Label(root, text=Proxy: )
    proxy_label.pack()
    proxy_entry = tk.Entry(root)
    proxy_entry.pack()

    set_proxy_button = tk.Button(root, text=Set Proxy, command=lambda: set_proxy(proxy_entry.get()))
    set_proxy_button.pack()

    progress_bar = ttk.Progressbar(root, mode=determinate)
    progress_bar.pack()

    percentage_label = tk.Label(root, text=0%)
    percentage_label.pack()

    def update_progress():
        downloaded_percentage = 0
        
        percentage_label.config(text=f{downloaded_percentage}%)
        progress_bar['value'] = downloaded_percentage

        root.after(100, update_progress)

    update_progress()

    root.mainloop()

def detect_system_proxy():
    proxy = urllib.request.getproxies().get('https')
    if proxy:
        proxy = proxy.split('://')[1]
        proxy = proxy.split(':')
        proxy = (proxy[0], int(proxy[1]))
        set_proxy(proxy)
        print('System proxy detected:', proxy)
    else:
        print('No system proxy detected')

def set_proxy(proxy):
    socks.set_default_proxy(socks.SOCKS5, proxy[0], proxy[1])
    socket.socket = socks.socksocket

if __name__ == __main__:
    manager = DownloadManager()
    gui_code()
