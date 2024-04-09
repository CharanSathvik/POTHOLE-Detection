import cv2
import urllib.request
import numpy as np
import requests
import joblib
import time

def nothing(x):
    pass
 
#change the IP address below according to the
#IP shown in the Serial monitor of Arduino code
url='http://192.168.29.186/cam-lo.jpg'
url1='http://192.168.29.186/'


# Set the path to the SVM model file
model_path = "finger_vein_svm_model.joblib"

# Define the image size
img_size = 64

# Load the SVM model
clf = joblib.load(model_path)


cnt=1
while True:
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    cv2.imwrite('test.jpg',frame)
    cv2.waitKey(1)
    img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (img_size, img_size))
    
    # Convert the image to a numpy array
    X = np.array([img])
    
    # Reshape the data to be compatible with SVM
    X = X.reshape(X.shape[0], -1)
    
    # Predict the label of the image
    y_pred = clf.predict(X)
    
    print("Predicted label: " + str(y_pred[0]))    
    
    cv2.imshow("live transmission", frame)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
    if key==ord('s'):
        cv2.imwrite('./data/2/'+ str(cnt)+'.jpg',frame)
        cv2.waitKey(1)
        cnt=cnt+1


    response = requests.get(url1)
    print(response.content)
    
cv2.destroyAllWindows()
