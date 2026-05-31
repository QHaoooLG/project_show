import tkinter as tk
from PIL import Image, ImageTk
import os

class DesktopPet:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("海绵宝宝桌面宠物")
        
        # 设置窗口属性：无边框、透明背景、始终置顶
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.wm_attributes("-topmost", True)
        
        # 初始化位置
        self.x = 0
        self.y = 0
        
        # 加载图片
        self.load_image()
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, width=self.image_width, height=self.image_height, highlightthickness=0)
        self.canvas.pack()
        
        # 在画布上显示图片
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        # 绑定事件
        self.bind_events()
        
        # 创建右键菜单
        self.create_context_menu()
        
        # 启动主循环
        self.root.mainloop()
    
    def load_image(self):
        # 检查图片文件是否存在，如果不存在则创建一个简单的海绵宝宝图像
        image_path = os.path.join(os.path.dirname(__file__), "spongebob.png")
        
        if os.path.exists(image_path):
            # 加载现有图片
            self.image = Image.open(image_path)
        else:
            # 创建一个简单的海绵宝宝图像（黄色背景，黑色轮廓）
            self.image = Image.new("RGBA", (100, 100), "white")
            # 这里可以添加简单的绘制逻辑，但为了简化，我们使用一个纯色图像
            # 实际使用时，应该替换为真实的海绵宝宝图片
            from PIL import ImageDraw
            draw = ImageDraw.Draw(self.image)
            draw.rectangle([10, 10, 90, 90], fill="yellow")
            draw.ellipse([20, 20, 40, 40], fill="black")  # 左眼
            draw.ellipse([60, 20, 80, 40], fill="black")  # 右眼
            draw.arc([30, 50, 70, 70], 0, 180, fill="black", width=2)  # 微笑
            # 保存图片
            self.image.save(image_path)
        
        # 调整图片大小
        self.image = self.image.resize((150, 150), Image.Resampling.LANCZOS)
        self.image_width, self.image_height = self.image.size
        self.tk_image = ImageTk.PhotoImage(self.image)
    
    def bind_events(self):
        # 绑定左键拖动事件
        self.canvas.bind("<Button-1>", self.on_left_button_down)
        self.canvas.bind("<B1-Motion>", self.on_left_button_drag)
        
        # 绑定右键菜单事件
        self.canvas.bind("<Button-3>", self.show_context_menu)
    
    def on_left_button_down(self, event):
        # 记录鼠标按下时的位置
        self.x = event.x_root
        self.y = event.y_root
        self.window_x = self.root.winfo_x()
        self.window_y = self.root.winfo_y()
    
    def on_left_button_drag(self, event):
        # 计算拖动距离
        delta_x = event.x_root - self.x
        delta_y = event.y_root - self.y
        
        # 更新窗口位置
        new_x = self.window_x + delta_x
        new_y = self.window_y + delta_y
        self.root.geometry(f"+{new_x}+{new_y}")
        
        # 更新记录的位置
        self.x = event.x_root
        self.y = event.y_root
        self.window_x = new_x
        self.window_y = new_y
    
    def create_context_menu(self):
        # 创建右键菜单
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="关闭", command=self.close_pet)
    
    def show_context_menu(self, event):
        # 显示右键菜单
        self.context_menu.post(event.x_root, event.y_root)
    
    def close_pet(self):
        # 关闭应用
        self.root.destroy()

if __name__ == "__main__":
    # 安装必要的依赖
    try:
        import PIL
    except ImportError:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageTk
    
    # 启动桌面宠物
    DesktopPet()