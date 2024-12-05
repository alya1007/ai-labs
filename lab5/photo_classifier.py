import torch  # type: ignore
import torch.nn as nn  # type: ignore
import torch.optim as optim  # type: ignore
from torchvision import datasets, transforms  # type: ignore
from torch.utils.data import Dataset  # type: ignore
from PIL import Image

# Define the CNN Model


class PassportPhotoClassifier(nn.Module):
    def __init__(self):
        super(PassportPhotoClassifier, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        # Placeholder for the fully connected layers (we'll initialize it later)
        self.fc_layers = None

    def forward(self, x):
        x = self.conv_layers(x)
        if self.fc_layers is None:
            # Dynamically compute the flattened size
            flattened_size = x.view(x.size(0), -1).size(1)
            self.fc_layers = nn.Sequential(
                nn.Flatten(),
                nn.Linear(flattened_size, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 1),
                nn.Sigmoid()
            )
            # Move the FC layers to the same device as the convolutional layers
            self.fc_layers.to(x.device)
        x = self.fc_layers(x)
        return x


# Custom Dataset to Load Data from Labels CSV


class PassportPhotoDataset(Dataset):
    def __init__(self, dataset, transform=None):
        self.data = dataset
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.data.iloc[idx]['new_path']
        label = self.data.iloc[idx]['label']
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label, dtype=torch.float32)

# Training Function


def train_model(model, train_loader, val_loader, criterion, optimizer, device, num_epochs=10):
    model.to(device)
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device).unsqueeze(1)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        # Validation
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(
                    device), labels.to(device).unsqueeze(1)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

                # Accuracy
                predictions = (outputs > 0.5).float()
                correct += (predictions == labels).sum().item()
                total += labels.size(0)

        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}, "
              f"Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {correct/total:.4f}")
