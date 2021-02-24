import numpy as np
import cv2
import sys
TYPE_ABSOLUTE = 'absolute_to_ratio'
TYPE_RATIO = 'ratio_to_absolute'

coordinates = TYPE_RATIO
def on_set(key, val):
    if key == 'coordinates':
        global coordinates
        coordinates = val

def on_get(key):
    if key == 'coordinates':
        return coordinates

def on_run(image : np.ndarray, bbox:np.ndarray):
    assert len(image.shape) == 3
    assert image.shape[0] >= 1
    assert image.shape[1] >= 1
    assert image.shape[2] >= 1
    
    if bbox.size <3 :
        return {'box': None}
    h,w,c = image.shape
    pts = []
    for bb in bbox:
        if coordinates == TYPE_RATIO :
            br = to_absolute(bb, w, h)
            pts.append(np.array(br, np.float32))
        elif coordinates == TYPE_ABSOLUTE:
            br = to_ratio(bb,w,h)
            pts.append(np.array(br, np.float32))
    if not pts:
        return {'box':None}
    arr = np.array(pts, np.float32)
    return {'box' : arr}


def to_absolute(bbox,width,height):
    return [b * width if idx % 2 == 0 else b * height for idx,b in enumerate(bbox)]

def to_ratio(bbox,width,height):
    return [b / width if idx % 2 == 0 else b / height for idx,b in enumerate(bbox)]



