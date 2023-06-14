import sympy
from numba import jit, cuda
import time
import copy
import cv2
from cv2 import *
import matplotlib.pyplot as plt
import scipy.signal
import numpy as np
import math


@jit(target_backend='cuda')
def data_manipulation(
    frame1=np.array([]),
    frame2=np.array([]),
    frame3=np.array([]),
    frame4=np.array([]),
    frame5=np.array([]),
    frame6=np.array([]),
    frame7=np.array([]),
    frame8=np.array([]),
    frame9=np.array([]),
    frame10=np.array([]),
):
    height = 21600
    width = 384

    frame1 = frame1.reshape((height, width*3))
    frame2 = frame2.reshape((height, width*3))
    frame3 = frame3.reshape((height, width*3))
    frame4 = frame4.reshape((height, width*3))
    frame5 = frame5.reshape((height, width*3))
    frame6 = frame6.reshape((height, width*3))
    frame7 = frame7.reshape((height, width*3))
    frame8 = frame8.reshape((height, width*3))
    frame9 = frame9.reshape((height, width*3))
    frame10 = frame10.reshape((height, width*3))

    frame1 = np.transpose(frame1)
    frame2 = np.transpose(frame2)
    frame3 = np.transpose(frame3)
    frame4 = np.transpose(frame4)
    frame5 = np.transpose(frame5)
    frame6 = np.transpose(frame6)
    frame7 = np.transpose(frame7)
    frame8 = np.transpose(frame8)
    frame9 = np.transpose(frame9)
    frame10 = np.transpose(frame10)

    frame1 = frame1.ravel()
    frame2 = frame2.ravel()
    frame3 = frame3.ravel()
    frame4 = frame4.ravel()
    frame5 = frame5.ravel()
    frame6 = frame6.ravel()
    frame7 = frame7.ravel()
    frame8 = frame8.ravel()
    frame9 = frame9.ravel()
    frame10 = frame10.ravel()

    frame_interweaved = np.empty(
        (frame1.size + frame2.size + frame3.size + frame4.size + frame5.size +
         frame6.size + frame7.size + frame8.size + frame9.size + frame10.size
         ), dtype=frame1.dtype)

    frame_interweaved[0::10] = frame1
    frame_interweaved[1::10] = frame2
    frame_interweaved[2::10] = frame3
    frame_interweaved[3::10] = frame4
    frame_interweaved[4::10] = frame5
    frame_interweaved[5::10] = frame6
    frame_interweaved[6::10] = frame7
    frame_interweaved[7::10] = frame8
    frame_interweaved[8::10] = frame9
    frame_interweaved[9::10] = frame10

    return frame_interweaved


@jit(target_backend='cuda')
def remove_and_cut_pixels_GPU(bit_array=[]):
    pixel_array_removed_pixel = np.empty(len(bit_array), dtype=np.uint8)
    i = 0
    for number in bit_array:
        if number >= 2 and number <= 253:
            pixel_array_removed_pixel[i] = (number) % 2
            i += 1
    return pixel_array_removed_pixel[:i]


@jit(target_backend='cuda', fastmath=True)
def equalize_bit_count(bit_array=np.array([])):
    pixel_array_removed_pixel = np.empty(len(bit_array), dtype=np.uint8)
    zeros = np.count_nonzero(bit_array == 0)
    ones = np.count_nonzero(bit_array == 1)
    difference = ones - zeros
    if difference > 0:
        factor = difference/ones
        one_count = 0
        i = 0
        for bit in bit_array:
            if bit == 1:
                if one_count > 1:
                    one_count -= 1
                else:
                    one_count += factor
                    pixel_array_removed_pixel[i] = bit
                    i += 1
            else:
                pixel_array_removed_pixel[i] = bit
                i += 1

    elif difference < 0:
        factor = (-1*difference)/zeros
        zero_count = 0
        i = 0
        for bit in bit_array:
            if bit == 0:
                if zero_count > 1:
                    zero_count -= 1
                else:
                    zero_count += factor
                    pixel_array_removed_pixel[i] = bit
                    i += 1
            else:
                pixel_array_removed_pixel[i] = bit
                i += 1
    return pixel_array_removed_pixel[:i]


@jit(target_backend='cuda')
def merge_bits_GPU(bit_array=np.array([])):
    bit_array_merged = np.empty(len(bit_array), dtype=np.uint64)
    i = 0
    for bit_pack in bit_array:
        random_value = 0
        for bit in bit_pack:
            random_value = (random_value << 1) | int(bit)
        bit_array_merged[i] = int(random_value)
        i += 1

    return bit_array_merged


video1 = cv2.VideoCapture("Pictures/rng_video_1.mp4")
video2 = cv2.VideoCapture("Pictures/rng_video_2.mp4")
video3 = cv2.VideoCapture("Pictures/rng_video_3.mp4")
video4 = cv2.VideoCapture("Pictures/rng_video_4.mp4")
video5 = cv2.VideoCapture("Pictures/rng_video_5.mp4")
video6 = cv2.VideoCapture("Pictures/rng_video_6.mp4")
video7 = cv2.VideoCapture("Pictures/rng_video_7.mp4")
video8 = cv2.VideoCapture("Pictures/rng_video_8.mp4")
video9 = cv2.VideoCapture("Pictures/rng_video_9.mp4")
video10 = cv2.VideoCapture("Pictures/rng_video_10.mp4")
ret1, frame1 = video1.read()
ret2, frame2 = video2.read()
ret3, frame3 = video3.read()
ret4, frame4 = video4.read()
ret5, frame5 = video5.read()
ret6, frame6 = video6.read()
ret7, frame7 = video7.read()
ret8, frame8 = video8.read()
ret9, frame9 = video9.read()
ret10, frame10 = video10.read()


random_numbers2 = np.empty(0, int)
how_many_numbers = 100000000
current_numbers_count = 0
while current_numbers_count < how_many_numbers:

    start = time.time()
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    ret3, frame3 = video3.read()
    ret4, frame4 = video4.read()
    ret5, frame5 = video5.read()
    ret6, frame6 = video6.read()
    ret7, frame7 = video7.read()
    ret8, frame8 = video8.read()
    ret9, frame9 = video9.read()
    ret10, frame10 = video10.read()
    
	# Sprawdź poprawność ramek
    if any(frame is None for frame in [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9, frame10]):
        continue  # Pomijaj tę iterację pętli

    # 0
    frame_all = np.concatenate((frame1.reshape(
        2160, 3840, 3), frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9, frame10))
    pixel_array = frame_all.ravel()

    # 1
    bit_array = data_manipulation(
        frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9, frame10)

    # 2
    bit_array = remove_and_cut_pixels_GPU(bit_array)

    # 4
    bit_array = equalize_bit_count(bit_array)

    # 5
    random_bit_length = 8
    random_in_image, extra_bits = divmod(len(bit_array), random_bit_length)
    if extra_bits > 0:
        bit_array = bit_array[:-extra_bits]

    bit_array = bit_array.reshape(random_in_image, random_bit_length)

    random_numbers = merge_bits_GPU(bit_array)

    random_numbers2 = np.concatenate((random_numbers2, random_numbers), axis=0)
    current_numbers_count = len(random_numbers2)


random_numbers2 = random_numbers2[:how_many_numbers]

del video1
del video2
del video3
del video4
del video5
del video6
del video7
del video8
del video9
del video10