# -*- coding: utf-8 -*-
import sys
from PIL import Image
import cv2
import numpy as np
import os


def convert_16bit_png_to_8bit_tga(input_path, output_path_combined):
    print("Starting to process file: %s" % input_path)
    # Check if the file exists
    if not os.path.exists(input_path):
        print("File does not exist: %s" % input_path)
        return
    # Read the 16-bit PNG image
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print("Failed to read the image from %s" % input_path)
        return

    height, width = image.shape[:2]
    num_channels = image.shape[2]  # Get the number of channels
    bit_depth = np.dtype(image.dtype).itemsize * 8  # Get the bit depth of the image
    image_min = np.min(image)
    image_max = np.max(image)
    print("Original image: size %d x %d, bit depth %d, channels %s, format PNG 16-bit, data range: min = %d, max = %d" % (width, height, bit_depth, "RGBA", image_min, image_max))

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

    # Separate high 8 bits and low 8 bits
    image_8bit_high = np.zeros((height, width, num_channels), dtype=np.uint8)
    image_8bit_low = np.zeros((height, width, num_channels), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            for c in range(num_channels):  # Consider all channels, including RGBA
                pixel_value = image[i, j, c]
                high_byte = (pixel_value >> 8) & 0xFF
                low_byte = pixel_value & 0xFF
                image_8bit_high[i, j, c] = high_byte
                image_8bit_low[i, j, c] = low_byte

    # Horizontally concatenate the high 8-bit and low 8-bit images
    combined_image = Image.new('RGBA', (width * 2, height))
    combined_image.paste(Image.fromarray(image_8bit_high), (0, 0))
    combined_image.paste(Image.fromarray(image_8bit_low), (width, 0))
    try:
        combined_image.save(output_path_combined)
        print("Combined image saved successfully, save location: %s" % output_path_combined)
        # Get the information of the output image
        output_image = Image.open(output_path_combined)
        output_width, output_height = output_image.size
        output_num_channels = output_image.getbands()
        output_bit_depth = 8  # The output image is 8-bit
        output_image_data = np.array(output_image)
        output_min = np.min(output_image_data)
        output_max = np.max(output_image_data)
        print("Output image: size %d x %d, bit depth %d, channels %s, format %s, data range: min = %d, max = %d" % (
            output_width, output_height, output_bit_depth, "".join(output_num_channels), output_image.format, output_min, output_max))
    except Exception as e:
        print("Failed to save the combined image, error message: %s" % str(e))


def batch_convert_16bit_png_to_8bit_tga():
    try:
        # Get the input directory where the Python file is located
        input_dir = os.path.dirname(sys.argv[0])  # 使用 sys.argv[0] 获取 exe 文件的目录
        print("Input directory: %s" % input_dir)
        # Traverse all files in the input directory
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.png') or file.endswith('.PNG'):  # Match.png and.PNG suffixes
                    input_path = os.path.join(root, file)  # Use os.path.join to concatenate file paths
                    # Generate the name of the output file
                    base_name = os.path.splitext(file)[0]
                    output_path_combined = os.path.join(root, base_name + "_8bit.tga")
                    convert_16bit_png_to_8bit_tga(input_path, output_path_combined)
                    print("\n\n")  # Use two newlines to separate different textures
    except Exception as e:
        print("An exception occurred during batch conversion: %s" % str(e))
    finally:
        raw_input("Press Enter to exit the program...")


if __name__ == "__main__":
    print("Starting batch conversion operation")
    batch_convert_16bit_png_to_8bit_tga()