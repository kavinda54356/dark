import psutil
import tkinter as tk

def monitor_system():
    root = tk.Tk()
    root.title("System Monitoring")
    root.geometry("300x200")

    cpu_label = tk.Label(root, text="CPU Usage:")
    cpu_label.pack()

    mem_label = tk.Label(root, text="Memory Usage:")
    mem_label.pack()

    disk_label = tk.Label(root, text="Disk Usage:")
    disk_label.pack()

    net_label = tk.Label(root, text="Network Usage:")
    net_label.pack()

    def update_stats():
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_label.config(text=f"CPU Usage: {cpu_percent}%")

        # Get memory usage
        mem_info = psutil.virtual_memory()
        mem_percent = mem_info.percent
        mem_label.config(text=f"Memory Usage: {mem_percent}%")

        # Get disk usage
        disk_usage = psutil.disk_usage('/')
        disk_percent = disk_usage.percent
        disk_label.config(text=f"Disk Usage: {disk_percent}%")

        # Get network usage
        net_info = psutil.net_io_counters()
        net_bytes_sent = net_info.bytes_sent
        net_bytes_recv = net_info.bytes_recv
        net_label.config(text=f"Network Usage: Sent: {net_bytes_sent} bytes, Received: {net_bytes_recv} bytes")

        # Schedule the next update
        root.after(1000, update_stats)

    # Schedule the initial update
    root.after(1000, update_stats)

    # Start the GUI event loop
    root.mainloop()