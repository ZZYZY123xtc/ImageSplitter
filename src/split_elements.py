#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片元素分割脚本
功能：去透明边 + 分割图片中的各个元素成独立文件
"""

from PIL import Image, ImageOps
import numpy as np
from scipy import ndimage
import os
from pathlib import Path
from collections import defaultdict

def crop_transparent_edges(image):
    """移除透明边"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    alpha = image.split()[-1]
    bbox = alpha.getbbox()
    
    if bbox is None:
        return image
    
    return image.crop(bbox)


def split_elements(image_path, output_folder=None):
    """
    分割图片中的所有元素
    
    Args:
        image_path: 输入图片路径
        output_folder: 输出文件夹（不指定则自动创建）
    """
    try:
        # 打开并转换图片
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        print(f"\n📸 处理: {os.path.basename(image_path)}")
        print(f"   原始尺寸: {img.size}")
        
        # 第一步：去透明边
        img_cropped = crop_transparent_edges(img)
        print(f"   裁剪后: {img_cropped.size}")
        
        # 第二步：创建输出文件夹
        if output_folder is None:
            base_name = Path(image_path).stem
            output_folder = os.path.join(
                os.path.dirname(image_path), 
                f"{base_name}_elements"
            )
        
        os.makedirs(output_folder, exist_ok=True)
        
        # 第三步：提取Alpha通道用于分割
        alpha = np.array(img_cropped.split()[-1])
        
        # 通过Alpha通道识别非透明区域
        binary = alpha > 128  # 设置透明度阈值
        
        # 使用连通区域标记来识别独立的元素
        labeled_array, num_features = ndimage.label(binary)
        
        print(f"   找到 {num_features} 个独立元素")
        
        # 第四步：逐个提取和保存元素
        img_array = np.array(img_cropped)
        
        for i in range(1, num_features + 1):
            # 获取当前元素的掩膜
            mask = (labeled_array == i)
            
            # 获取元素的边界框
            coords = np.where(mask)
            if len(coords[0]) == 0:
                continue
            
            y_min, y_max = coords[0].min(), coords[0].max()
            x_min, x_max = coords[1].min(), coords[1].max()
            
            # 添加一点边距，避免完全贴边
            padding = 2
            y_min = max(0, y_min - padding)
            y_max = min(img_array.shape[0], y_max + padding)
            x_min = max(0, x_min - padding)
            x_max = min(img_array.shape[1], x_max + padding)
            
            # 提取元素区域
            element_array = img_array[y_min:y_max+1, x_min:x_max+1].copy()
            
            # 创建掩膜并应用
            element_mask = mask[y_min:y_max+1, x_min:x_max+1]
            
            # 确保透明度正确
            if element_array.shape[2] == 4:  # 有Alpha通道
                alpha_channel = element_array[:, :, 3].astype(float)
                alpha_channel[~element_mask] = 0
                element_array[:, :, 3] = alpha_channel.astype(np.uint8)
            
            # 转为PIL图像并保存
            element_img = Image.fromarray(element_array, 'RGBA')
            
            # 计算元素的大小（用于排序）
            element_size = (x_max - x_min) * (y_max - y_min)
            
            output_path = os.path.join(
                output_folder,
                f"element_{i:03d}.png"
            )
            
            element_img.save(output_path, 'PNG')
            print(f"   ✓ element_{i:03d}.png | 尺寸: {element_img.size}")
        
        # 也保存裁剪后的完整图
        img_cropped.save(os.path.join(output_folder, "00_full_cropped.png"), 'PNG')
        print(f"   ✓ 00_full_cropped.png | 完整图片（已去透明边）")
        
        print(f"\n✅ 输出文件夹: {output_folder}")
        return True
        
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    input_folder = r"D:\游戏开发\参考图片"
    
    # 检查文件夹
    if not os.path.exists(input_folder):
        print(f"❌ 文件夹不存在: {input_folder}")
        return
    
    # 获取所有PNG文件
    png_files = list(Path(input_folder).glob("*.png")) + list(Path(input_folder).glob("*.PNG"))
    
    if not png_files:
        print(f"❌ 在 {input_folder} 中未找到PNG文件")
        return
    
    print(f"{'='*60}")
    print(f"🎨 图片元素分割工具")
    print(f"{'='*60}")
    print(f"📁 找到 {len(png_files)} 个PNG文件，开始处理...\n")
    
    success_count = 0
    
    for png_file in sorted(png_files):
        if split_elements(str(png_file)):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 处理完成！共成功处理 {success_count} 个文件")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
    input("按 Enter 键退出...")
