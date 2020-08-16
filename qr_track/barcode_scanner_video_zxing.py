#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from imutils.video import VideoStream
#from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import zxing
from PIL import Image
#from io import BytesIO


def barcode_scanner(csv_file):
    print("[INFO] Starting video stream ....")
    vs = VideoStream(src=0).start()
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    
    csv = open(csv_file, "a")
    found = set()
    reader = zxing.BarCodeReader()
    
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        
        #barcodes = pyzbar.decode(frame)
        
        #f = BytesIO()
        
        im = Image.fromarray(frame)
        
        im.save("./tmp/a.jpeg")
        barcodes = reader.decode("./tmp/a.jpeg")
        
        #im.save(f, "JPEG")
        #barcodes = reader.decode(f.read())
        #f.close()
        
        if barcodes:
            print(barcodes)

        if barcodes and (barcodes.format == "CODE_39" or barcodes.format == "QR_CODE"):
            print(dir(barcodes))
            print("raw: {}".format(barcodes.raw))
            print("type: {}".format(barcodes.type))
            print("format: {}".format(barcodes.format))
            print("parse: {}".format(barcodes.parse))
            print("parsed: {}".format(barcodes.parsed))
            print("points: {}".format(barcodes.points))
            print(barcodes)

            barcode_data = barcodes.raw
            barcode_type = barcodes.format
            
            (x1, y1) = (int(barcodes.points[0][0]), int(barcodes.points[0][1]))
            (x2, y2) = (int(barcodes.points[1][0]), int(barcodes.points[1][1]))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            text = "{} ({})".format(barcode_data, barcode_type)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            

            #for barcode in barcodes:
            #    barcode_data = barcode.data.decode("utf-8")
            #    barcode_type = barcode.type
    
            #    (x, y, w, h) = barcode.rect
            #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #    
            #    text = "{} ({})".format(barcode_data, barcode_type)
            #    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
            #    if barcode_data not in found:
            #        csv.write("{},{},{}\n".format(datetime.datetime.now(), barcode_data, barcode_type))
            #        csv.flush()
            #        found.add(barcode_data)
    
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
