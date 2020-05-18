# coding:utf-8
#扩充人脸边界框，并对图像进行裁剪

import sys
import numpy as np
import cv2
import math
import fileinput


def increaseBbox(bbox, factor):
    tlx = bbox[0] 
    tly = bbox[1] 
    brx = bbox[2] 
    bry = bbox[3] 
    dx = factor
    dy = factor
    dw = 1 + factor
    dh = 1 + factor
    #Getting bbox height and width
    w = brx-tlx;
    h = bry-tly;
    tlx2 = tlx - w * dx
    tly2 = tly - h * dy
    brx2 = tlx + w * dw
    bry2 = tly + h * dh
    nbbox = np.zeros( (4,1), dtype=np.float32 )
    nbbox[0] = tlx2
    nbbox[1] = tly2
    nbbox[2] = brx2
    nbbox[3] = bry2 
    return nbbox

def image_bbox_processing_v2(img, bbox):
    img_h, img_w, img_c = img.shape
    lt_x = bbox[0]
    lt_y = bbox[1]
    rb_x = bbox[2]
    rb_y = bbox[3]

    fillings = np.zeros( (4,1), dtype=np.int32)
    if lt_x < 0: ## 0 for python
        fillings[0] = math.ceil(-lt_x)
    if lt_y < 0:
        fillings[1] = math.ceil(-lt_y)
    if rb_x > img_w-1:
        fillings[2] = math.ceil(rb_x - img_w + 1)
    if rb_y > img_h-1:
        fillings[3] = math.ceil(rb_y - img_h + 1)
    new_bbox = np.zeros( (4,1), dtype=np.float32 )
    imgc = img.copy()
    if fillings[0] > 0:
        img_h, img_w, img_c = imgc.shape
        imgc = np.hstack( [np.zeros( (img_h, fillings[0][0], img_c), dtype=np.uint8 ), imgc] )    
    if fillings[1] > 0:

        img_h, img_w, img_c = imgc.shape
        imgc = np.vstack( [np.zeros( (fillings[1][0], img_w, img_c), dtype=np.uint8 ), imgc] )
    if fillings[2] > 0:

        img_h, img_w, img_c = imgc.shape
        imgc = np.hstack( [ imgc, np.zeros( (img_h, fillings[2][0], img_c), dtype=np.uint8 ) ] )    
    if fillings[3] > 0:
        img_h, img_w, img_c = imgc.shape
        imgc = np.vstack( [ imgc, np.zeros( (fillings[3][0], img_w, img_c), dtype=np.uint8) ] )


    new_bbox[0] = lt_x + fillings[0]
    new_bbox[1] = lt_y + fillings[1]
    new_bbox[2] = rb_x + fillings[0]
    new_bbox[3] = rb_y + fillings[1]
    return imgc, new_bbox


def preProcessImage(_savingDir, data, factor, _alexNetSize):
    #### Formatting the images as needed
    filename = data['file']
    im = cv2.imread(filename)

    if im is not None:
        print ('Processing ' + filename)
        sys.stdout.flush()
        lt_x = data['x']
        lt_y = data['y']
        rb_x = lt_x + data['width']
        rb_y = lt_y + data['height']
        w = data['width']
        h = data['height']
        center = ((lt_x + rb_x) / 2, (lt_y + rb_y) / 2)
        side_length = max(w, h);
        bbox = np.zeros((4, 1), dtype=np.float32)
        bbox[0] = center[0] - side_length / 2
        bbox[1] = center[1] - side_length / 2
        bbox[2] = center[0] + side_length / 2
        bbox[3] = center[1] + side_length / 2
        # %% Get the expanded square bbox
        bbox_red = increaseBbox(bbox, factor)
        img_3, bbox_new = image_bbox_processing_v2(im, bbox_red)
        # %% Crop and resized
        bbox_new = np.ceil(bbox_new)
        side_length = max(bbox_new[2] - bbox_new[0], bbox_new[3] - bbox_new[1])
        bbox_new[2:4] = bbox_new[0:2] + side_length
        bbox_new = bbox_new.astype(int)

        crop_img = img_3[bbox_new[1][0]:bbox_new[3][0], bbox_new[0][0]:bbox_new[2][0], :];
        resized_crop_img = cv2.resize(crop_img, (_alexNetSize, _alexNetSize), interpolation=cv2.INTER_CUBIC)

        cv2.rectangle(im, (lt_x, lt_y), (rb_x , rb_y), (0, 255, 0), 8)
        cv2.imwrite(_savingDir + 'preprocess1.jpg', im)
        cv2.rectangle(im, (bbox_new[0], bbox_new[1]), (bbox_new[2], bbox_new[3]), (0, 255, 0), 8)
        cv2.imwrite(_savingDir + 'preprocess2.jpg', im)
        cv2.imwrite(_savingDir + 'preprocess3.jpg', resized_crop_img)

        return _savingDir + 'preprocess3.jpg'
    else:
        print ('Skipping image:', filename, 'Image is None')