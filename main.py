import cv2
import pickle
import numpy as np
import cvzone


cap = cv2.VideoCapture('D:/Parking/Parking-OpenCv/media/carPark.mp4')


if not cap.isOpened():
    print("Error: Could not open video file")
    exit()


with open('D:/Parking/Parking-OpenCv/CarParkPos', 'rb') as f:
    posList = pickle.load(f)


space_width, space_height = 107, 48

def checkParkingSpace(processed_img, img):
    
    free_spaces = 0  # Counter for free spaces

    for pos in posList:
        x, y = pos
        
       
        cropped_img = processed_img[y:y + space_height, x:x + space_width]
        
       
        pixel_count = cv2.countNonZero(cropped_img)

       
        if pixel_count < 900:  # Free space
            color = (0, 255, 0)  # Green for free
            thickness = 3
            free_spaces += 1
        else:  # Occupied space
            color = (0, 0, 255)  # Red for occupied
            thickness = 3

        cv2.rectangle(img, pos, (x + space_width, y + space_height), color, thickness)

    
    cvzone.putTextRect(img, f'Free: {free_spaces}/{len(posList)}', (50, 50), scale=2, thickness=3, offset=10, colorR=(0, 200, 0))

while True:
  
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    
    success, img = cap.read()

    # If the frame is not captured, exit the loop
    if not success:
        print("Error: Failed to capture frame")
        break

    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # Step 4: Apply median blur to remove small artifacts
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    # Step 5: Apply dilation to make parking lines thicker
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

   
    checkParkingSpace(imgDilate, img)

    
    cv2.imshow("Parking Lot", img)

    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()