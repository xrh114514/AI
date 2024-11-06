import tkinter as tk
from tkinter import simpledialog, messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image
from datetime import datetime
import json
import threading
import os

class TimeWindow:
    def __init__(self):
        # 默认刷新率为60Hz
        self.refresh_rate = 60
        self.frame_interval = int(1000 / self.refresh_rate)
        
        # 创建Tkinter窗口
        self.window = tk.Tk()
        self.window.iconbitmap("icon.ico")  # 设置窗口图标为icon.ico
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"300x50+{self.screen_width - 300}+0")
        self.window.overrideredirect(True)
        self.window.attributes("-transparentcolor", "black")
        self.window.attributes("-topmost", True)
        self.window.wm_attributes("-disabled", True)
        
        # 创建标签用于显示时间
        self.label = tk.Label(self.window, font=("Helvetica", 18), fg="white", bg="black")
        self.label.pack(fill="both", expand=True)
        
        # 初始化时间更新
        self.update_time()

        # 启动系统托盘图标
        self.tray_thread = threading.Thread(target=self.setup_tray)
        self.tray_thread.daemon = True
        self.tray_thread.start()
    
    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.label.config(text=now)
        self.window.after(self.frame_interval, self.update_time)
    
    def setup_tray(self):
        # 加载自定义托盘图标
        icon_image = Image.open("icon.ico")  # 使用icon.ico文件作为托盘图标
        
        # 创建托盘菜单
        menu = Menu(
            MenuItem("关于", self.show_about),
            MenuItem("设置帧率", lambda: self.window.after(0, self.set_frame_rate)),
            MenuItem("退出", self.exit_app)
        )
        
        # 设置托盘图标和菜单
        self.icon = Icon("time_window", icon_image, menu=menu)
        self.icon.run()
    
    def set_frame_rate(self):
        # 弹出一个输入框来设置帧率
        self.window.attributes("-topmost", False)  # 暂时取消置顶
        new_rate = simpledialog.askinteger("设置帧率", "请输入刷新率 (Hz):", initialvalue=self.refresh_rate, parent=self.window)
        if new_rate:
            self.refresh_rate = new_rate
            self.frame_interval = int(1000 / self.refresh_rate)
        self.window.attributes("-topmost", True)  # 恢复置顶

    def show_about(self):
        # 显示关于窗口，读取 about.json 文件内容
        about_file = "about.json"
        if os.path.exists(about_file):
            with open(about_file, "r", encoding="utf-8") as f:
                about_content = json.load(f)
            about_text = "\n".join(f"{key}: {value}" for key, value in about_content.items())
            messagebox.showinfo("关于", about_text)
        else:
            messagebox.showerror("错误", "about.json 文件不存在！")

    def exit_app(self, icon=None, item=None):
        if icon:
            icon.stop()
        self.window.quit()

if __name__ == "__main__":
    app = TimeWindow()
    app.window.mainloop()
