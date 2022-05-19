import os
import cv2
import numpy as np
from PIL import Image
from noise import pnoise3

np.set_printoptions(threshold=np.inf)
np.errstate(invalid='ignore', divide='ignore')


def gen_noise(img, depth):
    p1 = Image.new('L', (img.shape[1], img.shape[0]))
    p2 = Image.new('L', (img.shape[1], img.shape[0]))
    p3 = Image.new('L', (img.shape[1], img.shape[0]))

    scale = 1 / 800.0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            v = pnoise3(x * scale, y * scale, depth[y, x] * scale, octaves=1, persistence=0.5, lacunarity=2.0)
            color = int((v + 1) * 128.0)
            p1.putpixel((x, y), color)

    scale = 1 / 500.0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            v = pnoise3(x * scale, y * scale, depth[y, x] * scale, octaves=1, persistence=0.5, lacunarity=2.0)
            color = int((v + 0.5) * 128)
            p2.putpixel((x, y), color)

    scale = 1 / 300.0
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            v = pnoise3(x * scale, y * scale, depth[y, x] * scale, octaves=1, persistence=0.5, lacunarity=2.0)
            color = int((v + 1.2) * 128)
            p3.putpixel((x, y), color)

    perlin = (np.array(p1) + np.array(p2) / 2 + np.array(p3) / 4) / 3

    return perlin


def add_fog(image_path, image_name, fog_path, parameter_set, j):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    condition_dict = {0: 'heavy', 1: 'medium', 2: 'light'}

    shader = np.empty_like(img)
    result = np.empty_like(img)
    camera_height = parameter_set[0]
    fog_height = parameter_set[1]
    haze_height = parameter_set[2]
    temp_ecm = 3.912 / parameter_set[3]
    temp_eca = 3.912 / parameter_set[4]

    elevation = np.ones((height, width))
    elevation *= camera_height

    if fog_height != 0:
        perlin = gen_noise(img, elevation)
        eca = temp_eca
        c = (1 - elevation / (fog_height + 0.00001))
        c[c < 0] = 0

        if fog_height > haze_height:
            ecm = (temp_ecm * c + (1 - c) * temp_eca) * (perlin / 255)
        else:
            ecm = (temp_eca * c + (1 - c) * temp_ecm) * (perlin / 255)

    else:
        eca = temp_eca
        ecm = temp_ecm

    distance_through_fog = np.ones_like(elevation)
    distance_through_haze = np.ones_like(elevation)
    distance_through_fog *= fog_height
    distance_through_haze *= haze_height

    shader[:, :, 0] = img[:, :, 0] * np.exp(-eca * distance_through_haze - ecm * distance_through_fog)
    shader[:, :, 1] = img[:, :, 1] * np.exp(-eca * distance_through_haze - ecm * distance_through_fog)
    shader[:, :, 2] = img[:, :, 2] * np.exp(-eca * distance_through_haze - ecm * distance_through_fog)
    omit = 1 - np.exp(-eca * distance_through_haze - ecm * distance_through_fog)

    fog_color = np.empty_like(img)

    result_path = os.path.join(fog_path, image_name)

    if j != 100:
        result_path += '_{}_fog.jpg'.format(condition_dict[j])
        fog_color[:, :, 0] = 240
        fog_color[:, :, 1] = 240
        fog_color[:, :, 2] = 240
    else:
        result_path += '_rain.jpg'
        fog_color[:, :, 0] = 225
        fog_color[:, :, 1] = 225
        fog_color[:, :, 2] = 201

    result[:, :, 0] = shader[:, :, 0] + omit * fog_color[:, :, 0]
    result[:, :, 1] = shader[:, :, 1] + omit * fog_color[:, :, 1]
    result[:, :, 2] = shader[:, :, 2] + omit * fog_color[:, :, 2]

    cv2.imwrite(result_path, result)
