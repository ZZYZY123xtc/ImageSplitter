#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 图片元素分割工具 - 启动中心
一个exe搞定所有操作
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageGrab
import numpy as np
from scipy import ndimage
import os
from pathlib import Path
import threading
from datetime import datetime

class ImageSplitterHub:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 图片元素分割工具")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # 设置输出文件夹
        self.output_folder = r"D:\游戏开发\参考图片"
        os.makedirs(self.output_folder, exist_ok=True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 标题
        title = tk.Label(
            root,
            text="🎨 图片元素分割工具",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        # 副标题
        subtitle = tk.Label(
            root,
            text="一键去透明边 + 自动分割元素",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        subtitle.pack(pady=0)
        
        # 功能区域
        button_frame = tk.Frame(root)
        button_frame.pack(pady=30)
        
        # 按钮1：快速粘贴
        self.btn1 = tk.Button(
            button_frame,
            text="📋 快速粘贴分割",
            font=("Arial", 12, "bold"),
            command=self.quick_paste,
            bg="#27ae60",
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        self.btn1.pack(pady=10, padx=20)
        label1 = tk.Label(
            button_frame,
            text="Ctrl+C 复制 → 点此运行 → 自动完成",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        label1.pack()
        
        # 按钮2：选择图片
        self.btn2 = tk.Button(
            button_frame,
            text="🖼️  选择单个图片",
            font=("Arial", 12, "bold"),
            command=self.select_image,
            bg="#3498db",
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        self.btn2.pack(pady=10, padx=20)
        label2 = tk.Label(
            button_frame,
            text="浏览选择一张PNG → 处理 → 打开结果",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        label2.pack()
        
        # 按钮3：批量处理
        self.btn3 = tk.Button(
            button_frame,
            text="📁 批量处理文件夹",
            font=("Arial", 12, "bold"),
            command=self.batch_process,
            bg="#9b59b6",
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        self.btn3.pack(pady=10, padx=20)
        label3 = tk.Label(
            button_frame,
            text="选择文件夹 → 一键处理全部PNG",
            font=("Arial", 9),
            fg="#95a5a6"
        )
        label3.pack()
        
        # 底部信息
        info_frame = tk.Frame(root, bg="#ecf0f1", height=80)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        info_text = tk.Label(
            info_frame,
            text=f"📁 输出位置: {self.output_folder}\n\n"
                 "✨ 功能：去透明边 + 连通区域分割\n"
                 "💻 快速处理，无需其他工具",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#34495e",
            justify=tk.LEFT
        )
        info_text.pack(padx=20, pady=15, anchor="w")
        
        # 禁用按钮的初始状态
        self.processing = False
    
    def set_button_state(self, state):
        """设置按钮状态"""
        for btn in [self.btn1, self.btn2, self.btn3]:
            btn.config(state=state)
    
    def process_image(self, image_path):
        """处理单个图片"""
        try:
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 去透明边
            alpha = np.array(img.split()[-1])
            coords = np.where(alpha > 128)
            
            if len(coords[0]) == 0:
                return None, "无法检测到内容（全透明？）"
            
            y_min, y_max = coords[0].min(), coords[0].max()
            x_min, x_max = coords[1].min(), coords[1].max()
            img = img.crop((x_min, y_min, x_max+1, y_max+1))
            
            # 分割元素
            alpha = np.array(img.split()[-1])
            binary = alpha > 128
            labeled, num = ndimage.label(binary)
            img_arr = np.array(img)
            
            # 创建输出文件夹
            base_name = Path(image_path).stem
            out_folder = os.path.join(self.output_folder, f"{base_name}_elements")
            os.makedirs(out_folder, exist_ok=True)
            
            # 保存完整图
            img.save(os.path.join(out_folder, "00_full.png"))
            
            # 保存元素
            element_count = 0
            for i in range(1, num + 1):
                mask = (labeled == i)
                coords = np.where(mask)
                
                if len(coords[0]) == 0:
                    continue
                
                y_min, y_max = coords[0].min(), coords[0].max()
                x_min, x_max = coords[1].min(), coords[1].max()
                
                pad = 2
                y_min = max(0, y_min - pad)
                y_max = min(img_arr.shape[0] - 1, y_max + pad)
                x_min = max(0, x_min - pad)
                x_max = min(img_arr.shape[1] - 1, x_max + pad)
                
                elem_arr = img_arr[y_min:y_max+1, x_min:x_max+1].copy()
                elem_mask = mask[y_min:y_max+1, x_min:x_max+1]
                
                if elem_arr.shape[2] == 4:
                    alpha_ch = elem_arr[:, :, 3].astype(float)
                    alpha_ch[~elem_mask] = 0
                    elem_arr[:, :, 3] = alpha_ch.astype(np.uint8)
                
                elem_img = Image.fromarray(elem_arr, 'RGBA')
                elem_img.save(
                    os.path.join(out_folder, f"element_{i:03d}.png"),
                    'PNG'
                )
                element_count += 1
            
            return out_folder, element_count
        
        except Exception as e:
            return None, str(e)
    
    def quick_paste(self):
        """快速粘贴分割"""
        if self.processing:
            messagebox.showwarning("提示", "正在处理中，请稍候...")
            return
        
        try:
            img = ImageGrab.grabclipboard()
            
            if img is None or not isinstance(img, Image.Image):
                messagebox.showerror(
                    "错误",
                    "剪贴板中没有图片！\n\n"
                    "步骤：\n"
                    "1. Win + Shift + S 截图\n"
                    "2. Ctrl + C 复制\n"
                    "3. 再点这个按钮"
                )
                return
            
            self.set_button_state(tk.DISABLED)
            self.processing = True
            
            # 时间戳生成名字
            time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = os.path.join(self.output_folder, f"temp_{time_str}.png")
            img.save(temp_file)
            
            out_folder, result = self.process_image(temp_file)
            os.remove(temp_file)
            
            if out_folder is None:
                messagebox.showerror("错误", f"处理失败：{result}")
            else:
                os.startfile(out_folder)
                messagebox.showinfo(
                    "✅ 成功!",
                    f"找到 {result} 个元素\n\n"
                    f"文件夹已打开：\n{os.path.basename(out_folder)}"
                )
            
            self.set_button_state(tk.NORMAL)
            self.processing = False
        
        except Exception as e:
            messagebox.showerror("错误", f"处理失败：{str(e)}")
            self.set_button_state(tk.NORMAL)
            self.processing = False
    
    def select_image(self):
        """选择单个图片"""
        if self.processing:
            messagebox.showwarning("提示", "正在处理中，请稍候...")
            return
        
        file_path = filedialog.askopenfilename(
            title="选择PNG图片",
            filetypes=[("PNG 文件", "*.png"), ("所有文件", "*.*")],
            initialdir=self.output_folder
        )
        
        if not file_path:
            return
        
        self.set_button_state(tk.DISABLED)
        self.processing = True
        self.root.update()
        
        out_folder, result = self.process_image(file_path)
        
        if out_folder is None:
            messagebox.showerror("错误", f"处理失败：{result}")
        else:
            os.startfile(out_folder)
            messagebox.showinfo(
                "✅ 成功！",
                f"找到 {result} 个元素\n\n"
                f"输出文件夹：\n{os.path.basename(out_folder)}"
            )
        
        self.set_button_state(tk.NORMAL)
        self.processing = False
    
    def batch_process(self):
        """批量处理文件夹"""
        if self.processing:
            messagebox.showwarning("提示", "正在处理中，请稍候...")
            return
        
        folder = filedialog.askdirectory(
            title="选择包含PNG文件的文件夹",
            initialdir=self.output_folder
        )
        
        if not folder:
            return
        
        pngs = sorted(Path(folder).glob("*.png")) + sorted(Path(folder).glob("*.PNG"))
        
        if not pngs:
            messagebox.showwarning("提示", "该文件夹中没有PNG文件")
            return
        
        self.set_button_state(tk.DISABLED)
        self.processing = True
        
        # 创建进度窗口
        progress_window = tk.Toplevel(self.root)
        progress_window.title("处理中...")
        progress_window.geometry("400x150")
        
        label = tk.Label(progress_window, text="正在处理...", font=("Arial", 11))
        label.pack(pady=20)
        
        progress = ttk.Progressbar(
            progress_window,
            length=350,
            mode='determinate',
            maximum=len(pngs)
        )
        progress.pack(pady=10, padx=25)
        
        info = tk.Label(progress_window, text="", font=("Arial", 9), fg="#7f8c8d")
        info.pack(pady=10)
        
        success = 0
        
        for idx, png_path in enumerate(pngs, 1):
            out_folder, result = self.process_image(str(png_path))
            if out_folder:
                success += 1
            
            progress['value'] = idx
            info.config(text=f"{idx}/{len(pngs)}")
            progress_window.update()
        
        progress_window.destroy()
        
        os.startfile(self.output_folder)
        messagebox.showinfo(
            "✅ 完成！",
            f"批量处理完成\n\n"
            f"成功: {success}/{len(pngs)}\n\n"
            f"文件夹已打开：参考图片"
        )
        
        self.set_button_state(tk.NORMAL)
        self.processing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSplitterHub(root)
    root.mainloop()
