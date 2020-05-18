# coding:utf-8
# 人脸检测，输出人脸边界框
from PIL import Image
from rustface import ImageData, Detector


def face_detection(image):
    image = Image.open(image)
    imagedata = ImageData.from_pillow_image(image)

    detector = Detector()
    detector.set_min_face_size(20)
    detector.set_score_thresh(2.0)
    detector.set_pyramid_scale_factor(0.8)
    detector.set_slide_window_step(4, 4)

    for face in detector.detect(imagedata):
        return face.x, face.y, face.width, face.height






