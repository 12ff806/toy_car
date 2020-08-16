#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
from PIL import Image
import re


def barcode_scanner(csv_file):
    print("[INFO] Starting video stream ....")
    vs = VideoStream(src=0).start()    # web cam
    #vs = VideoStream(usePiCamera=True).start()    # camera of raspberry pi
    time.sleep(2.0)
    
    csv = open(csv_file, "a")
    found = set()
    
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        barcodes = pyzbar.decode(frame)

        if not barcodes:
            im = Image.fromarray(frame)
            for i in range(5):
                im_copy = im.rotate(18+18*i)
                barcodes = pyzbar.decode(im_copy)
                if barcodes:
                    break
    
        for barcode in barcodes:
            #print("barcodes: {}".format(barcodes))
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type

            if barcode_type != "CODE39":
                continue

            pattern = r"^\d-\d$"
            if not re.match(pattern, barcode_data):
                continue
            
            print("barcode: {}".format(barcode_data))
    
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            text = "{} ({})".format(barcode_data, barcode_type)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
            if barcode_data not in found:
                csv.write("{},{},{}\n".format(datetime.datetime.now(), barcode_data, barcode_type))
                csv.flush()
                found.add(barcode_data)
    
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    
    print("[INFO] Cleaning up....")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    barcode_scanner(args["output"])
