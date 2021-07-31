import os
import unittest
from typing import Optional
import numpy as np
import argparse
import cv2
from project_py.vis import RoI, draw_roi, draw_segmentation, embed_subframe, render_heatmap


# global variables
GENERATE = os.getenv("GENERATE")
TESTDIR = os.path.dirname(os.path.realpath(__file__))
GOLDEN_DIR = os.path.join(TESTDIR, "golden")
os.makedirs(GOLDEN_DIR, exist_ok = True)
if GENERATE:
    print("GENERATING IMAGES. Make sure to check that they look alright before running the actual tests!")

class VisTest(unittest.TestCase):

    WHITE_IMAGE = np.full((500, 500, 3), 255, dtype=np.uint8)

    def make_white_image(self):
        return np.copy(self.WHITE_IMAGE)

    def save_image_or_check_against_golden(self, im : np.ndarray, golden_name : str):
        if GENERATE:
            golden_path = os.path.join(GOLDEN_DIR, golden_name + ".png")
            cv2.imwrite(golden_path, im)
        else:
            golden_path = os.path.join(GOLDEN_DIR, golden_name + ".png")
            if not os.path.exists(golden_path):
                self.skipTest("MISSING: %s. " % golden_path + \
                              "Make the test images with the [--generate] flag.")
            else:
                golden = cv2.imread(golden_path, cv2.IMREAD_COLOR)
                self.assertTrue(np.array_equal(im, golden))

    """
    Tests
    """

    def test_draw_roi(self):
        roi = RoI(top=200, bottom=300, left=200, right=300)
        target = draw_roi(self.make_white_image(), roi)
        self.save_image_or_check_against_golden(target, "roi")

    def test_draw_segmentation(self):
        segmap = np.zeros((500, 500), dtype=np.uint8)
        segmap[10:60,10:60] = 1
        segmap[100:150,100:150] = 2
        target = draw_segmentation(self.make_white_image(), segmap)
        self.save_image_or_check_against_golden(target, "segmentation")

    def test_render_heatmap(self):
        x = np.arange(-3.0,3.0)
        z_func = lambda x, y: ((1-(x**2+y**3))*np.exp(-(x**2+y**2)/2))**2
        x = np.arange(-3.0,3.0,0.1)
        y = np.arange(-3.0,3.0,0.1)
        X,Y = np.meshgrid(x, y)  # grid of point
        pixel_scoremap = z_func(X, Y)  # evaluation of the function on the grid
        target = render_heatmap(pixel_scoremap)
        self.save_image_or_check_against_golden(target, "heatmap")

    def test_embed_subframe(self):
        test_im = cv2.imread(os.path.join(TESTDIR, "input_images", "hand.png"), cv2.IMREAD_COLOR)
        target = embed_subframe(test_im, self.make_white_image())
        self.save_image_or_check_against_golden(target, "subframe")
