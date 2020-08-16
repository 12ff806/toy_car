#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyzbar import pyzbar
import argparse
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
barcodes = pyzbar.decode(image)

for barcode in barcodes:
    barcode_data = barcode.data.decode("utf-8")
    barcode_type = barcode.type

    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    text = "{} ({})".format(barcode_data, barcode_type)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    print("[INFO] Found {} barcode: {}".format(barcode_type, barcode_data))

    cv2.imshow("Image", image)
    cv2.waitKey(0)
