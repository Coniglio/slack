# -*- coding:utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Slackのピン留めを画像化したファイルに対して、それぞれのコメントを画像として出力する。
"""

INPUT_IMAGE_PATH = ''

OUTPUT_IMAGE_PATH =''
OUTPUT_IMAGE_EXTENSION = '.png'

def scanning(thresh):
    """
    1枚のピン留め画像のコメント開始・終了Y座標を走査します。
    @param thresh 2値化したピン留め画像
    @return コメントの開始・終了Y座標リスト
    """
    comments_point_y_list = [] # 各コメントのY座標
    for i, line in enumerate(thresh):
        for j, rgb in enumerate(line):
            if rgb != 255:
                comments_point_y_list.append(i)
                break
    return comments_point_y_list

def format(comments_point_y_list):
    """
    コメントの開始・終了座標を整形します。
    @param comments_point_y_list コメントの開始・終了Y座標リスト
    @return 整形済みのY座標リスト
    """
    formatted_point_y_list = []
    num = len(comments_point_y_list)
    for i, x in enumerate(comments_point_y_list):
        # 1要素目、最終要素
        # 現在座標 + 1 != 次の要素の座標(次のコメントの判定。コメントとコメントの間は数ピクセル間違があるため) ←コメントの終了
        # 現在座標 - 1 != 前の要素の座標←コメントの開始
        if i == 0 or i == num - 1 or (x + 1 != comments_point_y_list[i + 1]) or (x - 1 != comments_point_y_list[i - 1]):
            formatted_point_y_list.append(x)
    return formatted_point_y_list

def output(formatted_point_y_list, image):
    """
    ピン留め画像を出力します。
    @param formatted_point_y_list 整形済みのY座標リスト
    @param image 1枚のピン留め画像
    """
    it = formatted_point_y_list
    itit = iter(it)
    count = 1
    for start_point_y, end_point_y in zip(itit, itit):
        output_path = OUTPUT_IMAGE_PATH + str(count) + OUTPUT_IMAGE_EXTENSION
        # image[Y始点:Y終点, X始点:X終点]
        cv2.imwrite(output_path, image[start_point_y - 1:end_point_y + 2, 2:548 + 8])
        count = count + 1

if __name__ == '__main__':

    # ピン留め画像読み込み
    image = cv2.imread(INPUT_IMAGE_PATH)

    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    #2値化
    threshold = 240 # 枠線は残す
    max_value = 255 # 閾値以上の値を白色にする
    ret, thresh = cv2.threshold(gray, threshold, max_value, cv2.THRESH_BINARY)

    # 1枚のピン留め画像のコメント開始・終了Y座標を走査
    comments_point_y_list = scanning(thresh)

    # コメントの開始・終了座標の整形
    formatted_point_y_list = format(comments_point_y_list)

    # ピン留め画像を出力
    output(formatted_point_y_list, image)
