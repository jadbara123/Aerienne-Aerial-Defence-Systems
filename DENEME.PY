import cv2 
import numpy as np
import os


def sort_files(file):
    file_dir =  os.listdir(file)
    sorted_file = []
    for i in file_dir:
        i = i.split(".txt")
        sorted_file.append(int(i[0]))
    return sorted_file

folder_name = "coordinate_file"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

camera = cv2.VideoCapture(0)
dists = []
prev_ex = 0
prev_ey = 0
file_name = 0

def calculate_distance_between_points(point1, point2=[320, 240]):
    # Calculate Euclidean distance between two points
    distance = np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    return (point1[0] - point2[0]), (point1[1] - point2[1]), distance

def mesafe_hesapla(image, point=[320,240]):
    cx, cy = yer_hesapla(image)
  
    if cx is not None:  
        distx, disty, dist = calculate_distance_between_points([cx,cy], point)
        return distx, disty, dist
    else:
        return None, None, None

def yer_hesapla(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_blue = np.array([90, 50, 50])
    high_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv_image, low_blue, high_blue)
    
    # Morfolojik işlem uygula
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    largest_contour = max(contours, key=cv2.contourArea)
    moments = cv2.moments(largest_contour)

    # Calculate the centroid of the largest contour
    cx = int(moments['m10'] / (moments['m00']+0.000000000000000004))
    cy = int(moments['m01'] / (moments['m00']+0.000000000000000004))

    return cx, cy

while True:
    file_name += 1
    ret, img = camera.read()
    img = cv2.resize(img, (640,480))
    errorx, errory, _ = mesafe_hesapla(img)
    if errorx is not None:
        dd = prev_ex - errorx
        if -5 < dd < 5:
            olcumx = int(prev_ex)
        else:
            olcumx = errorx
        dd = prev_ey - errory
        if -5 < dd < 5:
            olcumy = int(prev_ey)
        else: 
            olcumy = errory
        cx, cy = yer_hesapla(img)
        if cx is not None:
            with open(folder_name+"/"+str(file_name)+".txt", "w") as f:
                f.write(str(olcumx)+","+str(olcumy))
                f.close()
            if len(os.listdir(folder_name)) > 5:
                sorted_file = sort_files(folder_name)
                os.remove(folder_name+"/"+str(min(sorted_file))+".txt")
            cv2.circle(img, (int(cx), int(cy)), 20, (255,255,255), -1)
            cv2.circle(img, (int(cx), int(cy)), 5, (0,0,255), -1) # Merkezi işaretlemek için bir daire çiz
    else:
        pass
    cv2.imshow("kare", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
