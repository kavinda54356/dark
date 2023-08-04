
import tkinter as tk

def monitor_clipboard():
    def clipboard_monitor_thread():
        root = tk.Tk()
        root.withdraw()
        while True:
            clipboard_text = root.clipboard_get()
            if clipboard_text.startswith('http://') or clipboard_text.startswith('https://'):
                filename = clipboard_text.split('/')[-1]
                manager.download_file(clipboard_text, filename)

    thread = threading.Thread(target=clipboard_monitor_thread)
    thread.start()


