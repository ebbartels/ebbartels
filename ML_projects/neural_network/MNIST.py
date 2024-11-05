import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader


transform = transforms.Compose([
    transforms.ToTensor(),  # Converts PIL images to tensors
])

train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_set = datasets.MNIST(root='./data', train=False, download=True, transform=transform)


train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = DataLoader(test_set, batch_size=64, shuffle=False)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.flat = nn.Flatten()
        self.l1 = nn.Linear(784,128)
        self.relu1 = nn.ReLU()
        self.l2 = nn.Linear(128,64)
        self.relu2 = nn.ReLU()
        self.l3 = nn.Linear(64, 10)
        
    def forward(self, x):
        x = self.flat(x)
        x = self.relu1(self.l1(x))
        x = self.relu2(self.l2(x))
        x = self.l3(x)
        return x


model = Net()

criterion = nn.CrossEntropyLoss()
opt = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

for epoch in range(10):
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


