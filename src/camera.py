import os
import cv2
import requests


API_URL = "http://localhost:5000"

def gen_image():
    cap = cv2.VideoCapture(0)
    cap.set(5, 60)

    print(cap.get(5))

    while True:
        _, frame = cap.read()
        # cv2.imshow("Image", frame)
        yield frame

        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def post_image_to_vis_server(image):
    files = {"image": cv2.imencode(".jpg", image)[1]}
    r = requests.post(os.path.join(API_URL, "video_feed"), files=files)
    return r

if __name__ == "__main__":
    for image in gen_image():
        post_image_to_vis_server(image)
