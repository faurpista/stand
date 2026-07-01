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
IMAGE_DIR = "standolasi_kepek"  # A mappa, ahol az összes (eredeti + generált) kép van
CSV_PATH = "adatok_new.csv"  # Az új, generált CSV fájl elérése
EPOCHS = 50  
BATCH_SIZE = 4

print("📊 Adatok beolvasása a CSV fájlból...")
# Beolvassuk az új táblázatot (ha az előzőleg generált kódot használtad, az vesszővel választ el)
df = pd.read_csv(CSV_PATH, sep=",") 

print(f"✅ Sikeresen betöltve {len(df)} db fotó adata.")
print(df.head())

# --- OKOSABB ADATHALMAZ FELOSZTÁSA (TRAIN / TEST) ---
# Létrehozunk egy kombinált oszlopot a rétegzéshez, hogy a teszt halmazba is jusson dőlt/közeli kép
df["stratify_col"] = df["bottle_type"] + "_" + df["distance"] + "_" + df["angle"].astype(str)
counts = df["stratify_col"].value_counts()
df["stratify_col"] = df["stratify_col"].apply(lambda x: x if counts[x] > 1 else "other")

train_df, test_df = train_test_split(
    df, 
    test_size=0.15, 
    random_state=42, 
    stratify=None  # Kikapcsoljuk a rétegzést, mert túl kicsi az adathalmaz
)

# --- REFACTORÁLT DATASET OSZTÁLY ---
class BarStandDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.df = dataframe.reset_index(drop=True)
        self.transform = transform
        
    def __len__(self):
        return len(self.df)
        
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(IMAGE_DIR, row['image_filename'])
        
        # BIZTONSÁGI JAVÍTÁS: Ha egy generált vagy valódi kép hiányzik, szürke kocka helyettesíti
        try:
            image = Image.open(img_path).convert('RGB')
        except FileNotFoundError:
            image = Image.new('RGB', (224, 224), color=(128, 128, 128))
            
        if self.transform:
            image = self.transform(image)
            
        # MÓDOSÍTÁS: Mivel a Sigmoid 0 és 1 között jósol, a CSV-ben lévő 0-100 értéket elosztjuk 100-zal
        pct_scaled = float(row['percentage']) / 100.0
        target_percentage = torch.tensor([pct_scaled], dtype=torch.float32)
        
        return image, target_percentage

# Szigorú transzformációk a fénnyel és elforgatással szembeni ellenálláshoz
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2), 
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

# --- MODEL ARCHITEKTÚRA (RESNET50) ---
class BarBottleLevelPredictor(nn.Module):
    def __init__(self):
        super(BarBottleLevelPredictor, self).__init__()
        # Modern PyTorch weights beállítás
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.feature_extractor = nn.Sequential(*list(resnet.children())[:-1])
        
        # Layer 3 és Layer 4 tanítható marad az egyedi környezet (bárpult, dőlések) miatt
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
        features = self.feature_extractor(x)
        features = features.view(x.size(0), -1)
        return self.regressor(features)

model = BarBottleLevelPredictor().to(DEVICE)
criterion = nn.MSELoss()
optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.0001)

# --- TANÍTÁSI CIKLUS ---
print("Tanítás indítása az új, kibővített adathalmazzal...")
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for images, percentages in train_loader:
        images, percentages = images.to(DEVICE), percentages.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(images)
        
        loss = criterion(outputs, percentages)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        
    # Kiszámoljuk a hibát (mivel visszaszorozzuk 100-zal, a valódi %-os tévedést látjuk)
    epoch_error = np.sqrt(running_loss / len(train_df)) * 100.0
    print(f"   Epoch {epoch+1:02d}/{EPOCHS} -> Átlagos tévedés: {epoch_error:.2f}%")

# --- MODELL MENTÉSE ---
torch.save(model.state_dict(), 'bar_leltar_modell.pth')
print("✅ Az új adatokra hangolt 'bar_leltar_modell.pth' sikeresen elmentve!")
