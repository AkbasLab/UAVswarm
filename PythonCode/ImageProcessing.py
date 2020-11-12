import airsim
import cv2
import os
import numpy as np
from imutils import paths
import imutils
import matplotlib.pyplot as plt
import math

# Global testing variables
droneNum = 3
# initialPositions = np.array([[2,0,-2],[4,0,-2],[6,0,-2]])
VEHICLENAME = "UAV"


def connectToUnreal():
    # initializing AirSim Simulator
    tempClient = airsim.MultirotorClient()
    tempClient.confirmConnection()
    return tempClient


def initalizeDrone(client, droneNum, droneNames):
    # intializing drones

    for i in range(droneNum):
        droneName = "".join(map(str, droneNames[i]))
        client.enableApiControl(True, droneName)
        client.armDisarm(True, droneName)
        client.takeoffAsync(vehicle_name=droneName)

    # Get Image data (Initialization)
    for i in range(droneNum):
        name = "".join(map(str, droneNames[i]))
        imgs = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)], vehicle_name=name)
        # Scene vision image in uncompressed RGBA array
        img = imgs[0]

        if i == 0:
            imgArray = img.image_data_uint8
        else:
            imgArray = imgArray + img.image_data_uint8

    imgWidth = img.width
    imgHeight = img.height

    for i in range(droneNum):
        name = "".join(map(str, droneNames[i]))
        imgs = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)], vehicle_name=name)
        # Scene vision image in uncompressed RGBA array
        img = imgs[0]

        if i == 0:
            imgArray = img.image_data_uint8
        else:
            imgArray = imgArray + img.image_data_uint8


        response = imgs[0]

        # get numpy array
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

        # reshape array to 4 channel image array H X W X 4
        img_rgb = img1d.reshape(response.height, response.width, 3)

        # original image is fliped vertically
        back = os.curdir
        os.chdir(r"C:\Users\jmora\OneDrive\Pictures\Saved Pictures")
        # write to png
        airsim.write_png(os.path.normpath( 'img{}.png'.format(i)), img_rgb)

        image = img_rgb


        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)
        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key = cv2.contourArea)
        print(c)
        # compute the bounding box of the of the paper region and return it
        rresult = cv2.minAreaRect(c)

        (x, y, w, h) = cv2.boundingRect(cnts[0])  # assuming, there is

        pt = (x, y + h)  # bottom-left of the obj
        orig = (img_rgb.shape[1], img_rgb.shape[0]);  ## bottom-right of the img

        dist = math.sqrt((pt[0] - orig[0]) ** 2 + (pt[1] - orig[1]) ** 2)
        print(dist)

        cv2.imshow("edged",edged)
        cv2.imwrite("contoured.png",edged)
        cv2.waitKey(0)
         # assuming, there is



        inches = (18 * 571.4) / rresult[1][0]

        box = cv2.cv.BoxPoints(rresult) if imutils.is_cv2() else cv2.boxPoints(rresult)
        box = np.int0(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fft" % (inches/ 12),
                    (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    2.0, (0, 255, 0), 3)
        cv2.imshow("image", image)
        cv2.waitKey(0)




