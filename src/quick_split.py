#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速一句话脚本：把参考图片文件夹里的所有PNG都去透明边 + 分割元素
直接在终端跑：python quick_split.py
"""

from PIL import Image
import numpy as np
from scipy import ndimage
import os
from pathlib import Path
from datetime import datetime

def process_image(image_path):
    """处理单个图片"""
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 去透明边
    alpha = np.array(img.split()[-1])
    bbox = Image.new('RGBA', img.size).split()[-1].getbbox()
    try:
        bbox = alpha.getbbox() if hasattr(alpha, 'getbbox') else None
    except:
        alpha_img = Image.fromarray(alpha, 'L')
        bbox = alpha_img.getbbox()
    
    if bbox is None:
        coords = np.where(alpha > 128)
        if len(coords[0]) == 0:
            return None
        y_min, y_max = coords[0].min(), coords[0].max()
        x_min, x_max = coords[1].min(), coords[1].max()
        bbox = (x_min, y_min, x_max+1, y_max+1)
    
    img = img.crop(bbox)
    
    # 分割元素
    alpha = np.array(img.split()[-1])
    binary = alpha > 128
    labeled, num = ndimage.label(binary)
    
    return img, labeled, num, np.array(img)

def main():
    folder = r"D:\游戏开发\参考图片"
    os.makedirs(folder, exist_ok=True)
    
    pngs = sorted(Path(folder).glob("*.png")) + sorted(Path(folder).glob("*.PNG"))
    
    if not pngs:
        print(f"❌ {folder} 中没有PNG文件")
        print("请将截图PNG放入此文件夹，然后再运行脚本")
        return
    
    print(f"🎨 处理 {len(pngs)} 个图片...\n")
    
    for idx, png_path in enumerate(pngs, 1):
        png_path = str(png_path)
        name = Path(png_path).stem
        result = process_image(png_path)
        
        if result is None:
            print(f"{idx}. ❌ {name} 无法处理")
            continue
        
        img, labeled, num_elements, img_arr = result
        
        # 创建输出文件夹
        out_folder = os.path.join(folder, f"{name}_分割")
        os.makedirs(out_folder, exist_ok=True)
        
        # 保存完整图
        img.save(os.path.join(out_folder, "00_完整.png"))
        
        # 保存各个元素
        count = 0
        for i in range(1, num_elements + 1):
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
                os.path.join(out_folder, f"{i:03d}.png"),
                'PNG'
            )
            count += 1
        
        print(f"{idx}. ✓ {name} → 找到 {count} 个元素，保存到 {name}_分割/")
    
    print(f"\n✅ 全部完成！")

if __name__ == "__main__":
    main()
