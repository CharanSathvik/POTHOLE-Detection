import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score
import joblib
# Set the path to your finger vein image dataset
data_dir = "./Dataset"


# Define the image size
img_size = 64

# Load the images and labels into arrays
images = []
labels = []
for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)
    for img_file in os.listdir(label_dir):
        img_path = os.path.join(label_dir, img_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (img_size, img_size))
        images.append(img)
        labels.append(int(label))

# Convert the images and labels to numpy arrays
X = np.array(images)
y = np.array(labels)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape the training and testing data to be compatible with SVM
X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

# Define the SVM classifier with a linear kernel
clf = svm.SVC(kernel='linear')

# Train the SVM classifier
clf.fit(X_train, y_train)

# Save the SVM model
joblib.dump(clf, "finger_vein_svm_model.joblib")

# Test the SVM classifier
y_pred = clf.predict(X_test)

# Calculate the confusion matrix, precision, recall, and F1-score
cm = confusion_matrix(y_test, y_pred)
precision, recall, f1_score, _ = precision_recall_fscore_support(y_test, y_pred, average='macro')
accuracy = accuracy_score(y_test, y_pred)

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(len(np.unique(y)))
plt.xticks(tick_marks, np.unique(y), rotation=45)
plt.yticks(tick_marks, np.unique(y))
plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()

# Plot the accuracy, precision, and recall
plt.figure(figsize=(8, 6))
x_labels = ['Accuracy', 'Precision', 'Recall']
y_values = [accuracy, precision, recall]
plt.bar(x_labels, y_values)
plt.ylim(0, 1)
plt.title('Accuracy, Precision, and Recall')
plt.show()

# Print the precision, recall, and F1-score
print("Precision: ", precision)
print("Recall: ", recall)
print("F1-score: ", f1_score)
print("Accuracy: ", accuracy)
