"""
Simple training script using transfer learning (PyTorch + torchvision).

This is a starting point. It expects dataset organized as ImageFolder:

data/
  train/
    healthy/
    botrytis/
  val/
    healthy/
    botrytis/

Run example:

python train.py --data-dir ../data --epochs 5 --batch-size 16 --out ../model.pth

"""
import argparse
import os
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models


def get_dataloaders(data_dir, batch_size, img_size=224):
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')

    train_tfms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_tfms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    train_ds = datasets.ImageFolder(train_dir, transform=train_tfms)
    val_ds = datasets.ImageFolder(val_dir, transform=val_tfms)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=4)
    return train_loader, val_loader, train_ds.classes


def build_model(num_classes, base_model='resnet50', pretrained=True):
    if base_model == 'resnet50':
        model = models.resnet50(pretrained=pretrained)
        in_f = model.fc.in_features
        model.fc = nn.Linear(in_f, num_classes)
    else:
        model = models.mobilenet_v2(pretrained=pretrained)
        in_f = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_f, num_classes)
    return model


def train_loop(model, device, train_loader, optimizer, criterion):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, preds = outputs.max(1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
    return running_loss / total, correct / total


def eval_loop(model, device, val_loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item() * images.size(0)
            _, preds = outputs.max(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return running_loss / total, correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str, required=True)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch-size', type=int, default=16)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--out', type=str, default='../model.pth')
    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_loader, val_loader, classes = get_dataloaders(args.data_dir, args.batch_size)
    num_classes = len(classes)
    model = build_model(num_classes=num_classes, base_model='resnet50', pretrained=True)
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    best_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = train_loop(model, device, train_loader, optimizer, criterion)
        val_loss, val_acc = eval_loop(model, device, val_loader, criterion)
        print(f"Epoch {epoch}/{args.epochs} - train_loss: {train_loss:.4f} acc: {train_acc:.4f} | val_loss: {val_loss:.4f} acc: {val_acc:.4f}")

        if val_acc > best_acc:
            best_acc = val_acc
            out_path = os.path.abspath(args.out)
            torch.save(model.state_dict(), out_path)
            print(f"Saved best model to {out_path}")


if __name__ == '__main__':
    main()
