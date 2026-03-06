#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从剪贴板粘贴图片到参考图片文件夹
支持：截图 → Ctrl+C → 运行脚本 → 自动保存 + 分割
"""

from PIL import Image, ImageGrab
import numpy as np
from scipy import ndimage
import os
from pathlib import Path
from datetime import datetime

def paste_from_clipboard():
    """从剪贴板粘贴图片"""
    try:
        img = ImageGrab.grabclipboard()
        if img is None:
            return None
        if not isinstance(img, Image.Image):
            return None
        return img
    except:
        return None

def crop_and_split(img, output_name="pasted_image"):
    """去透明边并分割"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 去透明边
    alpha = np.array(img.split()[-1])
    coords = np.where(alpha > 128)
    
    if len(coords[0]) == 0:
        return None
    
    y_min, y_max = coords[0].min(), coords[0].max()
    x_min, x_max = coords[1].min(), coords[1].max()
    img = img.crop((x_min, y_min, x_max+1, y_max+1))
    
    # 分割元素
    alpha = np.array(img.split()[-1])
    binary = alpha > 128
    labeled, num = ndimage.label(binary)
    img_arr = np.array(img)
    
    # 创建输出文件夹
    folder = r"D:\游戏开发\参考图片"
    os.makedirs(folder, exist_ok=True)
    
    # 按时间戳生成名字
    if output_name == "pasted_image":
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"img_{time_str}"
    
    out_folder = os.path.join(folder, f"{output_name}_elements")
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
        size = elem_img.size
        elem_img.save(
            os.path.join(out_folder, f"element_{i:03d}_{size[0]}x{size[1]}.png"),
            'PNG'
        )
        element_count += 1
    
    return out_folder, element_count, num

def main():
    folder = r"D:\游戏开发\参考图片"
    os.makedirs(folder, exist_ok=True)
    
    print("="*60)
    print("📋 从剪贴板粘贴图片工具")
    print("="*60)
    print("\n使用方法：")
    print("  1. 截图或复制图片（Ctrl+C）")
    print("  2. 运行本脚本")
    print("  3. 自动保存 + 分割元素")
    print("\n正在检查剪贴板...")
    
    img = paste_from_clipboard()
    
    if img is None:
        print("\n❌ 剪贴板中没有图片！")
        print("   • Windows 截图：Win + Shift + S")
        print("   • 复制图片：Ctrl + C")
        print("   • 再运行脚本")
        input("\n按 Enter 键退出...")
        return
    
    print(f"✓ 找到图片：{img.size}")
    print("\n🔄 处理中...")
    
    result = crop_and_split(img)
    
    if result is None:
        print("\n❌ 图片处理失败")
        return
    
    out_folder, elem_count, total_count = result
    
    print(f"\n✅ 完成！")
    print(f"   📁 输出文件夹：{os.path.basename(out_folder)}")
    print(f"   📊 统计：共找到 {total_count} 个连通区域，分割为 {elem_count} 个元素")
    print(f"\n   🗂️  完整路径：{out_folder}")
    
    # 列出生成的文件
    files = sorted(os.listdir(out_folder))
    print(f"\n   生成文件：")
    for f in files[:5]:
        print(f"     • {f}")
    if len(files) > 5:
        print(f"     ... 还有 {len(files)-5} 个文件")
    
    input("\n按 Enter 键退出...")

if __name__ == "__main__":
    main()
