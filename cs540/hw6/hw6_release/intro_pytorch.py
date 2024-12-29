import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# !pip show torch

torch.__version__ 


def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
        
    """
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    if training:
        train_set=datasets.FashionMNIST('./data',train=True, download=True,transform=custom_transform)
        loader = torch.utils.data.DataLoader(train_set, batch_size = 64, persistent_workers=False)
        return loader

    else:
        test_set=datasets.FashionMNIST('./data', train=False, transform=custom_transform)
        loader = torch.utils.data.DataLoader(test_set, batch_size = 64, persistent_workers=False)

        return loader


train_set = get_data_loader()


test_set = get_data_loader(False)


def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
                          nn.Flatten(),
                          nn.Linear(784, 128),
                          nn.ReLU(),
                          nn.Linear(128, 64),
                          nn.ReLU(),
                          nn.Linear(64, 10),
                         )
    return model


model = build_model()
print(model)


def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    model.train()
    opt = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    for epoch in range(T):
        correct = 0
        total = 0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            opt.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()
            
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        print(f"Train Epoch: {epoch} Accuracy: {correct}/{total}({correct/total*100:.2f}%) Loss: {loss:.3f}") 


criterion = nn.CrossEntropyLoss()
train_model(model, train_set, criterion, 5)


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    
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
    
    if show_loss:
        print(f"Average loss: {running_loss / len(test_loader):.4f}")
        
    print(f"Accuracy: {correct/total*100:.2f}%")
    


evaluate_model(model, test_set, criterion, True)


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']
    model.eval()
    with torch.no_grad():
        outputs = model(test_images)
        
        probabilities = F.softmax(outputs, dim=1)
        
        top3_probabilities, top3_indices = torch.topk(probabilities, 3)

        for i in top3_indices[index]:
            print(f"{class_names[i.item()]}: {probabilities[index][i.item()] * 100:.2f}%")


test_images = next(iter(test_set))[0]
predict_label(model, test_images, 13)

if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
