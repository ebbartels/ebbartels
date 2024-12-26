# python imports
import os
from tqdm import tqdm
import numpy as np
# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__()
        # certain definitions
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5, stride=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.flat = nn.Flatten()

        self.l1 = nn.Linear(16 * 5 * 5, 256)
        self.relu3 = nn.ReLU()

        self.l2 = nn.Linear(256, 128)
        self.relu4 = nn.ReLU()

        self.o = nn.Linear(128, num_classes)


    def forward(self, x):
        shape_dict = {}
        # certain operations
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        shape_dict[1] = list(x.shape)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        shape_dict[2] = list(x.shape)

        x = self.flat(x)
        shape_dict[3] = list(x.shape)

        x = self.l1(x)
        x = self.relu3(x)
        shape_dict[4] = list(x.shape)

        x = self.l2(x)
        x = self.relu4(x)
        shape_dict[5] = list(x.shape)

        out = self.o(x)
        shape_dict[6] = list(x.shape)

        return out, shape_dict


def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    model = LeNet()
    model_params = 0.0

    for p in model.named_parameters():
        name, size = p
        model_params += np.prod(size.size())   

    return model_params / 1e6


def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc


print(count_model_params())
