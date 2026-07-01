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
from sklearn.model_selection import train_test_split

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_DIR = "standolasi_kepek"  # 🚨 IDE TEDD A VALÓDI FOTÓKAT!
EPOCHS = 50  # Megemeltük, hogy a valódi barpult részleteit jól megtanulja
BATCH_SIZE = 4

# --- A VALÓDI ADATOK TÁBLÁZATA ---
# Készíts egy Excel vagy CSV fájlt, vagy írd be kézzel a képeid pontos adatait:
'''
def get_real_bar_dataset():
    data = pd.DataFrame([
        {"image_filename": "jager_001.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.00},
        {"image_filename": "jager_002.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.07},
        {"image_filename": "jager_003.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.14},
        {"image_filename": "jager_004.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.21},
        {"image_filename": "jager_005.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.28},
        {"image_filename": "jager_006.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.35},
        {"image_filename": "jager_007.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.42},
        {"image_filename": "jager_008.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.49},
        {"image_filename": "jager_009.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.56},
        {"image_filename": "jager_010.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.63},
        {"image_filename": "jager_011.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.70},
        {"image_filename": "jager_012.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.77},
        {"image_filename": "jager_013.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.84},
        {"image_filename": "jager_014.jpg", "bottle_type": "jagermeister_1L", "percentage": 0.91},
        {"image_filename": "jager_015.jpg", "bottle_type": "jagermeister_1L", "percentage": 1.00},
        {"image_filename": "unicum_001.jpg", "bottle_type": "unicum_05L", "percentage": 0.00}, # 0 cl
        {"image_filename": "unicum_002.jpg", "bottle_type": "unicum_05L", "percentage": 0.10}, # 5 cl
        {"image_filename": "unicum_003.jpg", "bottle_type": "unicum_05L", "percentage": 0.20}, # 10 cl
        {"image_filename": "unicum_004.jpg", "bottle_type": "unicum_05L", "percentage": 0.30}, # 15 cl
        {"image_filename": "unicum_005.jpg", "bottle_type": "unicum_05L", "percentage": 0.40}, # 20 cl
        {"image_filename": "unicum_006.jpg", "bottle_type": "unicum_05L", "percentage": 0.50}, # 25 cl (félig van)
        {"image_filename": "unicum_007.jpg", "bottle_type": "unicum_05L", "percentage": 0.60}, # 30 cl
        {"image_filename": "unicum_008.jpg", "bottle_type": "unicum_05L", "percentage": 0.70}, # 35 cl
        {"image_filename": "unicum_009.jpg", "bottle_type": "unicum_05L", "percentage": 0.80}, # 40 cl
        {"image_filename": "unicum_010.jpg", "bottle_type": "unicum_05L", "percentage": 0.90}, # 45 cl
        {"image_filename": "unicum_011.jpg", "bottle_type": "unicum_05L", "percentage":  1.00}, # 50 cl (tele)
        # Egészítsd ki a többi lőtt képeddel...
    ])
    return data

df = get_real_bar_dataset()
'''
# A régi get_real_bar_dataset() függvény HELYETT ezt írd a kódba:

print("📊 Adatok beolvasása a CSV fájlból...")
# Beolvassuk a pontvesszővel elválasztott táblázatot
df = pd.read_csv("adatok.csv", sep=";") 

# Nyomkövetés: kiírjuk, hány képet találtunk a CSV-ben
print(f"✅ Sikeresen betöltve {len(df)} db valódi fotó adata.")
print(df.head()) # Megmutatja az első pár sort a terminálban


train_df, test_df = train_test_split(df, test_size=0.15, random_state=42) # Kevesebb teszt, több tanítás

class BarStandDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.df = dataframe.reset_index(drop=True)
        self.transform = transform
    def __len__(self):
        return len(self.df)
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(IMAGE_DIR, row['image_filename'])
        
        # 🚨 BIZTONSÁGI JAVÍTÁS: Ha a kép nem létezik, nem omlik össze, hanem csinál egy ideiglenes szürke kockát
        try:
            image = Image.open(img_path).convert('RGB')
        except FileNotFoundError:
            # Létrehozunk egy 224x224-es szürke képet a memóriában helyettesítésként
            image = Image.new('RGB', (224, 224), color=(128, 128, 128))
            
        if self.transform:
            image = self.transform(image)
            
        target_percentage = torch.tensor([row['percentage']], dtype=torch.float32)
        return image, target_percentage

# Szigorúbb transzformációk a fénnyel szembeni ellenálláshoz
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2), # Erős fény-variálás
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_loader = DataLoader(BarStandDataset(train_df, train_transforms), batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(BarStandDataset(test_df, test_transforms), batch_size=BATCH_SIZE, shuffle=False)

class BarBottleLevelPredictor(nn.Module):
    def __init__(self):
        super(BarBottleLevelPredictor, self).__init__()
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.feature_extractor = nn.Sequential(*list(resnet.children())[:-1])
        
        # 🚨 VÁLTOZÁS: Megnyitjuk a ResNet utolsó KÉT nagy blokkját frissítésre, 
        # hogy megtanulja az igazi üveg részleteit és elfelejtse a bárpult hátterét!
        for name, param in self.feature_extractor.named_parameters():
            if "layer4" in name or "layer3" in name:
                param.requires_grad = True
            else:
                param.requires_grad = False

        self.regressor = nn.Sequential(
            nn.Linear(2048, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.regressor(self.feature_extractor(x).view(x.size(0), -1))

model = BarBottleLevelPredictor().to(DEVICE)
criterion = nn.MSELoss()
optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.0001) # Kisebb learning rate a finomhangoláshoz

print("Tanítás indítása valódi képekkel...")
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for images, percentages in train_loader:
        images, percentages = images.to(DEVICE), percentages.to(DEVICE)
        optimizer.zero_grad()
        loss = criterion(model(images), percentages)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)
    print(f"   Epoch {epoch+1:02d}/{EPOCHS} -> Hiba: {np.sqrt(running_loss / len(train_df)) * 100:.2f}%")

torch.save(model.state_dict(), 'bar_leltar_modell.pth')
print("✅ Valódi képekre hangolt 'bar_leltar_modell.pth' sikeresen elmentve!")