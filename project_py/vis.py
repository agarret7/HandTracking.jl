import io
import numpy as np
import cv2
from collections import namedtuple
import matplotlib.pyplot as plt
from matplotlib import cm


_RED = (0, 0, 255)
_GREEN = (0, 255, 0)
_BLACK = (0, 0, 0)
_CMAP = {
    1: _GREEN,
    2: _RED
}

RoI = namedtuple("RoI", ["top", "bottom", "left", "right"])

def _get_im_from_fig(fig, dpi=180):
    """
    define a function which returns an image as numpy array from figure
    found at: https://stackoverflow.com/questions/7821518/matplotlib-save-plot-to-numpy-array
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def draw_roi(im : np.ndarray, roi : RoI) -> np.ndarray:
    # roi box
    p1 = np.array([roi.top, roi.left])
    p2 = np.array([roi.bottom, roi.right])
    im = cv2.rectangle(im, p1, p2, _BLACK, 3)

    # reticle
    pcenter = (p2 + p1) // 2
    dx = np.array([5, 0])
    dy = np.array([0, 5])
    im = cv2.line(im, pcenter - dx, pcenter + dx, _BLACK, 1)
    im = cv2.line(im, pcenter - dy, pcenter + dy, _BLACK, 1)

    return im

def draw_segmentation(im : np.ndarray, segmap : np.ndarray) -> np.ndarray:
    segmap_im = np.zeros((*segmap.shape, 3), dtype=np.uint8)
    for (cls, color) in _CMAP.items():
        segmap_im[segmap == cls,:] = color
    return cv2.addWeighted(im, 0.7, segmap_im, 0.3, 0.0)

def embed_subframe(im : np.ndarray, subim : np.ndarray) -> np.ndarray:
    im = np.copy(im)
    h,w = im.shape[:2]
    sh,sw = h//3,h//3
    subframe = cv2.resize(subim, (sw,sh))
    im[:sh,w-sw:] = subframe
    return im

def render_heatmap(pixel_scoremap : np.ndarray) -> np.ndarray:
    fig, ax = plt.subplots()
    im = ax.imshow(pixel_scoremap, cmap="viridis")
    fig.colorbar(im)
    ax.set_title("Heatmap")
    return _get_im_from_fig(fig)

def imshow(im : np.ndarray) -> None:
    cv2.imshow("Image", im)
    while True:
        k = cv2.waitKey(1)
        if k == 27:
            break
