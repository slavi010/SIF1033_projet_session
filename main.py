import numpy as np
import cv2 as cv2
from Fenetre import Fenetre

# cap = cv2.VideoCapture(0)
#
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()

fenetre = Fenetre()
while True:
    fenetre.root.update_idletasks()
    fenetre.root.update()
