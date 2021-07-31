import os
import cv2


def gen_image():
    cap = cv2.VideoCapture(0)
    cap.set(5, 60)

    print(cap.get(5))

    while True:
        _, frame = cap.read()
        yield frame

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    DIR = os.path.dirname(os.path.realpath(__file__))

    for image in gen_image():
        cv2.imshow("Image", image)
        k = cv2.waitKey(1)
        if k == 27:
            break
        if k == 99:
            cv2.imwrite(os.path.join(DIR, "image.png"), image)
            break
