import cv2
import numpy as np

# Webcam
webcam_id = 0
cap = cv2.VideoCapture(webcam_id)

#template = cv2.imread('samples/data/blanco.png', 0)
#w, h = template.shape[::-1]

if cv2.__version__.startswith('2.4'):
    height_prop = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT 
else:
    height_prop = cv2.CAP_PROP_FRAME_HEIGHT

if cv2.__version__.startswith('2.4'):
    fps_prop = cv2.cv.CV_CAP_PROP_FPS
else:
    fps_prop = cv2.CAP_PROP_FPS

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (255,255,255)
thickness = 1

while True:
    _, frame = cap.read()


    # Define range in BGR
    lower_color = np.array([0, 0, 0])
    upper_color =  np.array([0, 0, 255])

    # Mask con color rojo
    mask = cv2.inRange(frame, lower_color, upper_color)

    
	
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    #Una vez este pulido se puede quitar el res y ganar rendimiento
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(mask)
    posicionTop = max_loc
    cv2.rectangle(res, posicionTop,posicionTop, 255, 2)

    #TM_CCORR_NORMED tiene un poco de lag (matar moscas a cagnonazos)
    #conTemplate = cv2.matchTemplate(mask,template,cv2.TM_CCORR_NORMED)
    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(conTemplate)
    #top_left = max_loc
    #bottom_right = (top_left[0] + w, top_left[1] + h)
    #cv2.rectangle(res, top_left, bottom_right, 255, 2)

    # Text position
    height = int(cap.get(height_prop))
    position = (50, height - 50)
        
    text = "X: " + str(posicionTop[0]) + " , Y: "+str(posicionTop[1])
        
    #Put text
    cv2.putText(res, text, position, font, font_scale, color, thickness)

    # Show
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Color', res)

    # Exit?
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
