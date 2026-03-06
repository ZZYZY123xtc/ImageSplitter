#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片选择器 + 分割工具
使用tkinter GUI选择图片，然后自动去透明边+分割元素
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from scipy import ndimage
import os
from pathlib import Path

class ImageSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 图片元素分割工具")
        self.root.geometry("600x300")
        
        # 设置输出文件夹
        self.output_folder = r"D:\游戏开发\参考图片"
        os.makedirs(self.output_folder, exist_ok=True)
        
        # UI
        self.label = tk.Label(
            root, 
            text="📊 图片元素分割工具\n\n点击下方按钮选择PNG图片",
            font=("Arial", 12),
            justify=tk.CENTER
        )
        self.label.pack(pady=20)
        
        self.select_btn = tk.Button(
            root,
            text="🖼️  选择图片",
            font=("Arial", 14),
            command=self.select_image,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.select_btn.pack(pady=10)
        
        self.batch_btn = tk.Button(
            root,
            text="📁 批量处理文件夹",
            font=("Arial", 14),
            command=self.batch_process,
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10
        )
        self.batch_btn.pack(pady=10)
        
        self.info_label = tk.Label(
            root,
            text=f"输出位置: {self.output_folder}",
            font=("Arial", 9),
            fg="gray"
        )
        self.info_label.pack(pady=10)
    
    def process_image(self, image_path):
        """处理单个图片"""
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 去透明边
        alpha = np.array(img.split()[-1])
        coords = np.where(alpha > 128)
        
        if len(coords[0]) == 0:
            return None, "无法检测到内容"
        
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
        
        return out_folder, f"找到 {element_count} 个元素"
    
    def select_image(self):
        """选择单个图片"""
        file_path = filedialog.askopenfilename(
            title="选择PNG图片",
            filetypes=[("PNG 文件", "*.png"), ("所有文件", "*.*")],
            initialdir=self.output_folder
        )
        
        if not file_path:
            return
        
        out_folder, msg = self.process_image(file_path)
        
        if out_folder is None:
            messagebox.showerror("错误", msg)
        else:
            messagebox.showinfo(
                "成功",
                f"处理完成！\n\n{msg}\n\n输出文件夹：\n{out_folder}"
            )
            os.startfile(out_folder)  # 打开文件夹
    
    def batch_process(self):
        """批量处理文件夹中的所有PNG"""
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
        
        success = 0
        for idx, png_path in enumerate(pngs, 1):
            out_folder, msg = self.process_image(str(png_path))
            if out_folder:
                success += 1
            self.label.config(text=f"处理中... {idx}/{len(pngs)}")
            self.root.update()
        
        messagebox.showinfo(
            "完成",
            f"批量处理完成！\n成功: {success}/{len(pngs)}"
        )
        self.label.config(text="📊 处理完成！")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSplitterApp(root)
    root.mainloop()
