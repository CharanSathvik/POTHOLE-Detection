import tkinter as tk
import tkinter.filedialog
import cv2
import numpy as np
import joblib
import time
import telepot
import serial
import time
import string
import pynmea2

# Set the path to the SVM model file
model_path = "finger_vein_svm_model.joblib"

# Define the image size
img_size = 64

# Load the SVM model
clf = joblib.load(model_path)



# Create a function to browse for an image file and predict its label
def predict_label():
    # Ask the user to select an image file
    file_path = tk.filedialog.askopenfilename()
    
    # Load the image and resize it
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (img_size, img_size))
    
    # Convert the image to a numpy array
    X = np.array([img])
    
    # Reshape the data to be compatible with SVM
    X = X.reshape(X.shape[0], -1)
    
    # Predict the label of the image
    y_pred = clf.predict(X)
    
    # Print the predicted label
    label.config(text="Predicted label: " + str(y_pred[0]))
 

# Create a GUI window
root = tk.Tk()
root.title("Finger Vein Image Prediction")

# Create a button to browse for an image file
browse_button = tk.Button(root, text="Browse", command=predict_label)
browse_button.pack(pady=10)

# Create a label to display the predicted label
label = tk.Label(root, text="")
label.pack(pady=10)

# Start the GUI event loop
root.mainloop()
