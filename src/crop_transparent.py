#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键去透明边脚本
用途：批量对PNG图片进行自动裁裁，移除四周的透明边
"""

from PIL import Image, ImageChops
import os
from pathlib import Path

def crop_transparent_edge(image_path, output_path=None):
    """
    裁剪图片的透明边
    
    Args:
        image_path: 输入图片路径
        output_path: 输出图片路径（不指定则覆盖原文件）
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 如果是RGB图片，先转RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 获取图片的通道分离
        # 最后一个通道是Alpha通道
        alpha = img.split()[-1]
        
        # 获取非透明的边界框
        bbox = alpha.getbbox()
        
        # 如果找不到非透明区域，直接返回
        if bbox is None:
            print(f"⚠️  {os.path.basename(image_path)} 是完全透明的，跳过")
            return False
        
        # 裁剪图片
        cropped_img = img.crop(bbox)
        
        # 确定输出路径
        if output_path is None:
            output_path = image_path
        
        # 保存图片，确保保留透明度
        cropped_img.save(output_path, 'PNG')
        
        print(f"✓ {os.path.basename(image_path)} | 原尺寸: {img.size} → 新尺寸: {cropped_img.size}")
        return True
        
    except Exception as e:
        print(f"✗ {os.path.basename(image_path)} 处理失败: {str(e)}")
        return False


def main():
    """主函数"""
    # 定义输入文件夹
    input_folder = r"D:\游戏开发\参考图片"
    
    # 检查文件夹是否存在
    if not os.path.exists(input_folder):
        print(f"❌ 文件夹不存在: {input_folder}")
        print(f"请先建立文件夹，并将PNG文件放入")
        return
    
    # 获取所有PNG文件
    png_files = list(Path(input_folder).glob("*.png")) + list(Path(input_folder).glob("*.PNG"))
    
    if not png_files:
        print(f"❌ 在 {input_folder} 中未找到PNG文件")
        return
    
    print(f"📁 找到 {len(png_files)} 个PNG文件，开始处理...\n")
    
    success_count = 0
    fail_count = 0
    
    # 处理每个PNG文件
    for png_file in sorted(png_files):
        if crop_transparent_edge(str(png_file)):
            success_count += 1
        else:
            fail_count += 1
    
    # 输出统计信息
    print(f"\n{'='*50}")
    print(f"处理完成！✓ 成功: {success_count} | ✗ 失败: {fail_count}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
    # 保持窗口显示，按任意键退出
    input("\n按 Enter 键退出...")
