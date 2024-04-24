import cv2 
import numpy as np
import os

camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)
dists = []
prev_ex = 0
prev_ey = 0
file_name = 0
folder_name = "coordinate_file"

def calculate_distance_between_points(point1, point2=[320, 240]):
    # Calculate Euclidean distance between two points
    distance = np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    return (point1[0] - point2[0]), (point1[1] - point2[1]), distance

def find_largest_contour_center(binary_image):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    largest_contour = max(contours, key=cv2.contourArea)
    moments = cv2.moments(largest_contour)

    # Calculate the centroid of the largest contour
    cx = int(moments['m10'] / (moments['m00']+0.000000000000000004))
    cy = int(moments['m01'] / (moments['m00']+0.000000000000000004))

    return cx, cy

def mesafe_hesapla(image, point=[320,240]):
    cx, cy = yer_hesapla(image)
  
    if cx != None:  
        distx, disty, dist = calculate_distance_between_points([cx,cy], point)
        return distx, disty, dist
    else:
        return None, None, None


    
def yer_hesapla(image):
    low  = (0,70,50)
    high = (10,255,255)   
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(hsv_image, low, high)
    kernel = np.ones((10, 10), np.uint8) 

    # erode the image 
    erosion = cv2.erode(filtered, kernel, 
                        iterations=1) 
    cx, cy = find_largest_contour_center(erosion) 
    if cx != None:  
        return cx, cy
    else:
        return None, None

def sort_files(file):
    file_dir =  os.listdir(file)
    sorted_file = []
    for i in file_dir:
        i = i.split(".txt")
        sorted_file.append(int(i[0]))
    return sorted_file

def clear_history(file):
    file_list = os.listdir(file)
    for i in file_list:
        os.remove(file+'/'+i)

clear_history(folder_name)
while 1:

    file_name += 1
    ret, img = camera.read()
    img = cv2.resize(img, (640,480))
    errorx, errory, _ = mesafe_hesapla(img)
    print(str(errorx)+" "+str(errory))
    if errorx != None:
        yeni_cx , yeni_cy = yer_hesapla(img)
        if yeni_cy != None:
            cy = yeni_cy
            cx = yeni_cx
        with open(folder_name+"/"+str(file_name)+".txt", "w") as f:
            f.write(str(int(errorx))+","+str(int(errory)))
            f.close()
        if len(os.listdir(folder_name)) > 5:
            sorted_file = sort_files(folder_name)
            os.remove(folder_name+"/"+str(min(sorted_file))+".txt")
        cv2.circle(img, (int(cx), int(cy)), 20, (255,255,255), -1)
    else:
        pass
    cv2.imshow("kare", img)
    cv2.waitKey(1)
    