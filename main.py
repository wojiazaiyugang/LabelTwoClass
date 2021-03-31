import os
import time
import shutil
import argparse

import cv2
import numpy


def process(args: argparse.Namespace):
    print(help_message)
    input_dir = args.input_dir or input("输入input_dir：")
    output_positive_dir = args.output_positive_dir or input("输入output_positive_dir：")
    output_negative_dir = args.output_negative_dir or input("输入output_negative_dir：")
    for d in [input_dir, output_positive_dir, output_negative_dir]:
        if not os.path.exists(d):
            print(f"目录{d}不存在，程序结束")
            time.sleep(5)
            exit()
    window_name = "label2class"
    cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO)
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        image_data = numpy.fromfile(item_path, dtype=numpy.uint8)
        if int(image_data.shape[0]) == 0:
            continue
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        if image is None:
            continue
        if image is not None:
            cv2.imshow(window_name, image)
            while True:
                key = cv2.waitKeyEx(0)
                if key == 27:
                    exit()
                elif key == 2490368:
                    target_path = os.path.join(output_positive_dir, item)
                    print(f"移动文件{item_path}->{target_path}")
                    shutil.move(item_path, target_path)
                    break
                elif key == 2621440:
                    target_path = os.path.join(output_negative_dir, item)
                    print(f"移动文件{item_path}->{target_path}")
                    shutil.move(item_path, target_path)
                    break
                else:
                    print("按键错误，只支持上下方向键")


if __name__ == '__main__':
    help_message = f"二分类图片标注程序 \n" \
                   f"输入一个文件夹，读取文件夹内所有的图片逐张显示 \n" \
                   f"输入方向键↑表示正样本，图片被移动到output_positive_dir文件夹 \n" \
                   f"输入方向键下表示负样本，图片被移动到output_negative_dir文件夹 \n" \
                   f"ESC结束"
    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument("--input_dir", type=str, help="待处理文件夹")
    parser.add_argument("--output_positive_dir", type=str, help="输出正样本文件夹")
    parser.add_argument("--output_negative_dir", type=str, help="输出负样本文件夹")
    process(parser.parse_args())
