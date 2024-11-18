# +
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image, ImageEnhance
import random

# +
import kagglehub

# Download latest version
path = kagglehub.dataset_download("masoudnickparvar/brain-tumor-mri-dataset")

print("Path to dataset files:", path)


# -

def get_class_paths(path):
    classes = []
    class_paths = []

    # Iterate through directories in the training path
    for label in os.listdir(path):
        label_path = os.path.join(path, label)

        # Check if it's a directory
        if os.path.isdir(label_path):
            # Iterate through images in the label directory
            for image in os.listdir(label_path):
                image_path = os.path.join(label_path, image)

                # Add class and path to respective lists
                classes.append(label)
                class_paths.append(image_path)

    # Create a DataFrame with the collected data
    df = pd.DataFrame({
        'Class Path': class_paths,
        'Class': classes
    })

    return df


test_df = get_class_paths(os.path.join(path, "Testing"))
train_df = get_class_paths(os.path.join(path, "Training"))

print(train_df["Class"].unique())

print(test_df["Class"].unique())

train_df.Class.value_counts()

test_df.Class.value_counts()

# +
batch_size = 32

img_size = (244, 244)


# -

class RandomBrightness(object):
    def __init__(self, brightness_range=(0.8, 1.2)):
        self.brightness_range = brightness_range

    def __call__(self, img):
        brightness_factor = random.uniform(self.brightness_range[0], self.brightness_range[1])
        enhancer = ImageEnhance.Brightness(img)  # Create enhancer for brightness
        return enhancer.enhance(brightness_factor)  # Adjust brightness


# +
transform = transforms.Compose([
    transforms.Resize(img_size),           # Resize images (optional)
    #RandomBrightness(brightness_range=(0.8, 1.2)),  # Random brightness adjustment
    transforms.ToTensor(),                   # Convert image to tensor
    #transforms.Lambda(lambda x: x / 255.0),  # Rescale pixel values to [0, 1]
    #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalization for pre-trained models (optional)
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])  # Normalization

])



# Create a dataset object
train_set = datasets.ImageFolder(root=os.path.join(path, "Training"), transform=transform)

test_set = datasets.ImageFolder(root=os.path.join(path, "Testing"), transform=transform)

# Create a DataLoader for batching and shuffling
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

test_loader = DataLoader(test_set, batch_size=16, shuffle=False)


# -
class Net(nn.Module):
    # input shape is 244X244
    #output is 4 classes
    def __init__(self, num_classes = 4):
        super(Net, self).__init__()
        
        # Convolutional Layer 1
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)  # Input: 3x244x244, Output: 16x244x244
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)  # Output: 16x122x122
        
        # Convolutional Layer 2
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)  # Output: 32x122x122
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)  # Output: 32x61x61
        
        self.flat = nn.Flatten()
        self.l1 = nn.Linear(32*61*61, 128)
        self.relu3 = nn.ReLU()
        self.l2 = nn.Linear(128,64)
        self.relu4 = nn.ReLU()
        self.l3 = nn.Linear(64, num_classes)
        
    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))  # Apply conv1 + relu + pool1
        x = self.pool2(self.relu2(self.conv2(x)))  # Apply conv2 + relu + pool2
        x = self.flat(x)
        x = self.relu3(self.l1(x))
        x = self.relu4(self.l2(x))
        x = self.l3(x)
        return x


model = Net()

criterion = nn.CrossEntropyLoss()
opt = optim.SGD(model.parameters(), lr=0.005, momentum=0.9)

for epoch in range(10):
    correct = 0
    total = 0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        opt.zero_grad()

        #print(inputs.shape)
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        opt.step()

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f"Train Epoch: {epoch} Accuracy: {correct}/{total}({correct/total*100:.2f}%) Loss: {loss:.3f}") 

# +
model.eval()
running_loss = 0.0
correct = 0
total = 0

with torch.no_grad():
    for data, labels in test_loader:
        outputs = model(data)

        _, predicted = torch.max(outputs.data, 1)

        loss = criterion(outputs, labels)
        running_loss += loss.item()
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Average loss: {running_loss / len(test_loader):.4f}")

print(f"Accuracy: {correct/total*100:.2f}%")
# -
# batch size 32, lr 0.001, 2 conv layers = 90.3%
# batch size 64, lr 0.001, 2 conv layers = 89.7%
# batch size 32, lr 0.005, 2 conv layers = 95.27%


