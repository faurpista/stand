import os
import pandas as pd
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torchvision.models as models

# --- BEÁLLÍTÁSOK ---
IMAGE_DIR = "standolasi_kepek"      # A mappa, ahol a vodka és sörös képek vannak
CSV_PATH = "adatok_new.csv"          # Az előzőleg legenerált CSV fájl
EXISTING_MODEL_PATH = "regi_modell.pth"  # A meglévő ResNet50 .pth fájlod neve
NEW_MODEL_PATH = "frissitett_resnet50.pth" # Az új, kibővített modell neve

BATCH_SIZE = 16
EPOCHS = 10
LEARNING_RATE = 1e-5  # Alacsony érték a finomhangoláshoz (Fine-tuning)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- 1. PYTORCH DATASET OSZTÁLY ---
class BottleDataset(Dataset):
    def __init__(self, csv_file, img_dir, split="train", transform=None):
        df = pd.read_csv(csv_file)
        self.df = df[df["split"] == split].reset_index(drop=True)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        img_name = os.path.join(self.img_dir, self.df.iloc[idx]["image_filename"])
        image = Image.open(img_name).convert("RGB")
        
        # Százalék normalizálása 0.0 és 1.0 közé a regresszióhoz
        percentage = float(self.df.iloc[idx]["percentage"]) / 100.0
        label = torch.tensor(percentage, dtype=torch.float32)

        if self.transform:
            image = self.transform(image)

        return image, label

# --- 2. KÉP TRANSZFORMÁCIÓK (RESNET50 ELŐÍRÁSOK) ---
# A ResNet50 standard 224x224-es felbontást és ImageNet normalizációt vár
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    # Ha szeretnél szoftveres dőlésszöget (Data Augmentation), vedd ki a kommentet:
    # transforms.RandomRotation(degrees=(-15, 15)), 
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- 3. DATALOADEREK ---
train_dataset = BottleDataset(CSV_PATH, IMAGE_DIR, split="train", transform=train_transform)
val_dataset = BottleDataset(CSV_PATH, IMAGE_DIR, split="val", transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# --- 4. RESNET50 MODELL INICIALIZÁLÁSA ÉS SÚLYOK BETÖLTÉSE ---
# ResNet50 architektúra létrehozása (üresen, weights=None)
model = models.resnet50(weights=None) 

# Módosítjuk az utolsó réteget (fully connected layer) lineáris regresszióra (1 kimenet = százalék)
# ResNet50 esetén ez automatikusan 2048 bemeneti neuront fog jelenteni
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 1)

# Betöltjük a korábbi betanított ResNet50 .pth fájlt
if os.path.exists(EXISTING_MODEL_PATH):
    print(f"Létező ResNet50 modell súlyainak betöltése: {EXISTING_MODEL_PATH}")
    model.load_state_dict(torch.load(EXISTING_MODEL_PATH, map_location=DEVICE))
else:
    print(f"FIGYELEM: A megadott .pth fájl ({EXISTING_MODEL_PATH}) nem található! Alapállapotból indul a tanítás.")

model = model.to(DEVICE)

# --- 5. VESZTESÉGFÜGGVÉNY ÉS OPTIMALIZÁLÓ ---
criterion = nn.MSELoss() 
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# --- 6. TANÍTÁSI CIKLUS (FINE-TUNING) ---
print(f"ResNet50 finomhangolás elindítása {DEVICE} eszközön...")

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    
    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(images).squeeze() 
        
        # Ha a batch mérete 1-re csökkenne a végén, a squeeze törölheti a dimenziót, ezt kezeljük le
        if outputs.dim() == 0:
            outputs = outputs.unsqueeze(0)
            
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        
    epoch_loss = running_loss / len(train_loader.dataset)
    
    # Ellenőrzési fázis (Validation)
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images).squeeze()
            if outputs.dim() == 0:
                outputs = outputs.unsqueeze(0)
                
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            
    epoch_val_loss = val_loss / len(val_loader.dataset)
    
    print(f"Epoch {epoch+1}/{EPOCHS} -> Train MSE Loss: {epoch_loss:.5f} | Val MSE Loss: {epoch_val_loss:.5f}")

# --- 7. FRISSÍTETT RESNET50 MODELL MENTÉSE ---
torch.save(model.state_dict(), NEW_MODEL_PATH)
print(f"\nA kibővített ResNet50 modell sikeresen elmentve ide: {NEW_MODEL_PATH}")
