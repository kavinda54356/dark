import os

def clear_cache():
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

    print(f"Cache Cleanup Complete!")
    print(f"Deleted {files_deleted} files, Freed {total_size_freed} bytes.")

clear_cache()