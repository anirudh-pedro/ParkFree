import cv2
import pickle


img = cv2.imread('C:/Users/HP/Desktop/sem-project/carParkImg.png')


posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        # Right-click to remove the most recent point
        for i, pos in enumerate(posList):
            if pos[0] - 20 < x < pos[0] + 20 and pos[1] - 20 < y < pos[1] + 20:
                posList.pop(i)
    
   
    with open('D:/Parking/Parking-OpenCv/CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # Display the parking lot image
    imgCopy = img.copy()
    

    for pos in posList:
        cv2.rectangle(imgCopy, pos, (pos[0] + 107, pos[1] + 48), (255, 0, 0), 2)

    # Display instructions
    cv2.putText(imgCopy, "Click: Add (Left), Remove (Right)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the image window
    cv2.imshow("Select Parking Spaces", imgCopy)
    cv2.setMouseCallback("Select Parking Spaces", mouseClick)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
