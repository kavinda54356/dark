import tkinter as tk
import os

def clean_temp_files():
    temp_folder = os.path.join(os.environ["TEMP"])

    files_deleted = 0
    total_size_freed = 0

    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                files_deleted += 1
                total_size_freed += file_size
            except:
                pass

    print(f"Deleted {files_deleted} files, Freed {total_size_freed} bytes.")

def clean_cache():
    cache_folder = os.path.join(os.environ["LOCALAPPDATA"], "Cache")

    files_deleted = 0
    total_size_freed = 0

    for root, dirs, files in os.walk(cache_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                files_deleted += 1
                total_size_freed += file_size
            except:
                pass

    print(f"Deleted {files_deleted} files, Freed {total_size_freed} bytes.")

def clean_memory():
    clean_temp_files()
    clean_cache()

def temporary_file_cleanup():
    root = tk.Tk()
    root.title("Temporary File Cleanup")
    root.geometry("300x200")

    cleanup_btn = tk.Button(root, text="Clean Up", command=clean_memory)
    cleanup_btn.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()