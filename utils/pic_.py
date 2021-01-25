# 裁剪指定坐标
from PIL import Image
import cv2 as cv
Image.MAX_IMAGE_PIXELS = 1000000000


def px_to_mm(i, dpi):
    return round(i / dpi * 25.4)


def slt(path, savepath,type='png'):
    im = Image.open(path)
    H, W, = im.size
    new_H, new_W = px_to_mm(H, 300), px_to_mm(W, 300)
    im.thumbnail((new_H, new_W))
    im.save(savepath, type)


def qiege(path, savepath, x0, y0, x1, y1):
    # 左上角为起点，横坐标为x,坐标为y
    img = img = Image.open(path)
    i = img.crop((x0, y0, x1, y1))
    i.save(savepath,dpi=img.info['dpi'])

def qiege2(path, savepath,  x0,x1,y0,y1,):
    # 左上角为起点，横坐标为x,坐标为y
    img = cv.imread(path, 1)
    cropped = img[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
    cv.imwrite(savepath, cropped)

# slt('./32.tif', './4.png',type='png')
# qiege2('./1.tif','./33.tif', 0, 14409,0, 14409,)
qiege('./1.tif','./34.tif', 0,0,5000, 14409)
