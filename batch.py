# -*- coding: utf-8 -*-
from PIL import Image
import cv2
import numpy as np
import os


def convert_16bit_png_to_8bit_tga(input_path, output_path_high, output_path_low, output_path_combined):
    # 读取 16 位 PNG 图像
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print("Failed to read the image from %s" % input_path)
        return

    print("Original Image data range: min = %d, max = %d" % (np.min(image), np.max(image)))

    # 将 BGR 转换为 RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

    # 获取图像尺寸
    height, width = image.shape[:2]
    num_channels = image.shape[2]  # 获取通道数

    # 创建四个 8 位图像
    image_8bit_high = np.zeros((height, width, num_channels), dtype=np.uint8)
    image_8bit_low = np.zeros((height, width, num_channels), dtype=np.uint8)

    # 分离高 8 位和低 8 位
    for i in range(height):
        for j in range(width):
            for c in range(num_channels):  # 考虑所有通道，包括 RGBA
                pixel_value = image[i, j, c]
                high_byte = (pixel_value >> 8) & 0xFF
                low_byte = pixel_value & 0xFF
                image_8bit_high[i, j, c] = high_byte
                image_8bit_low[i, j, c] = low_byte

    # 使用 PIL 保存高 8 位图像
    pil_image_high = Image.fromarray(image_8bit_high)
    pil_image_high.save(output_path_high)
    print("Successfully saved high 8-bit image to %s" % output_path_high)

    # 使用 PIL 保存低 8 位图像
    pil_image_low = Image.fromarray(image_8bit_low)
    pil_image_low.save(output_path_low)
    print("Successfully saved low 8-bit image to %s" % output_path_low)

    # 将高 8 位和低 8 位图像横向拼接
    combined_image = Image.new('RGBA', (width * 2, height))
    combined_image.paste(pil_image_high, (0, 0))
    combined_image.paste(pil_image_low, (width, 0))
    combined_image.save(output_path_combined)
    print("Successfully saved combined image to %s" % output_path_combined)


def batch_convert_16bit_png_to_8bit_tga(input_dir):
    # 遍历输入目录中的所有文件
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.png'):
                input_path = os.path.join(root, file)
                # 生成输出文件的名称
                base_name = os.path.splitext(file)[0]
                output_path_high = os.path.join(root, base_name + "_high.tga")
                output_path_low = os.path.join(root, base_name + "_low.tga")
                output_path_combined = os.path.join(root, base_name + "_combined.tga")
                # 调用转换函数
                convert_16bit_png_to_8bit_tga(input_path, output_path_high, output_path_low, output_path_combined)


if __name__ == "__main__":
    input_dir = 'your_input_directory'  # 这里输入存放 16 位 PNG 图像的目录
    batch_convert_16bit_png_to_8bit_tga(input_dir)
