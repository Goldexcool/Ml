# 🎓 Model Training Guide

## ⏱️ Training Time Estimates

### With CPU Only:
- **Per epoch**: ~2-3 minutes
- **50 epochs**: ~2-2.5 hours
- **100 epochs**: ~4-5 hours

### With GPU (NVIDIA):
- **Per epoch**: ~20-40 seconds
- **50 epochs**: ~30-40 minutes
- **100 epochs**: ~1-1.5 hours

*Note: Early stopping may finish training sooner if validation accuracy stops improving!*

---

## 🚀 How to Train

### Step 1: Prepare Your Data

Ensure your data is organized like this:
```
C:\Users\golde\Downloads\tomato\
├── train\
│   ├── Tomato___Bacterial_spot\
│   ├── Tomato___Early_blight\
│   ├── Tomato___healthy\
│   ├── Tomato___Late_blight\
│   └── ... (other disease folders)
└── val\
    ├── Tomato___Bacterial_spot\
    ├── Tomato___Early_blight\
    └── ... (same structure)
```

### Step 2: Install Training Dependencies

```powershell
cd c:\Users\golde\OneDrive\Desktop\model
.\.venv\Scripts\Activate.ps1
pip install matplotlib
```

### Step 3: Configure Training (Optional)

Edit `train_model.py` if needed:
```python
CONFIG = {
    'data_dir': r'C:\Users\golde\Downloads\tomato',
    'img_height': 128,
    'img_width': 128,
    'batch_size': 32,
    'epochs': 50,  # Adjust this
    'learning_rate': 0.001,
}
```

### Step 4: Start Training

```powershell
cd c:\Users\golde\OneDrive\Desktop\model
.\.venv\Scripts\Activate.ps1
python train_model.py
```

### Step 5: Monitor Progress

You'll see output like:
```
Epoch 1/50
45/45 [==============================] - 3s 67ms/step - loss: 2.1234 - accuracy: 0.3456 - val_loss: 1.9876 - val_accuracy: 0.4123
Epoch 2/50
45/45 [==============================] - 2s 44ms/step - loss: 1.8765 - accuracy: 0.4567 - val_loss: 1.7654 - val_accuracy: 0.5234
...
```

---

## 📊 What to Expect

### Training Progress:
- **Epochs 1-10**: Model learns basic patterns (~40-60% accuracy)
- **Epochs 10-30**: Accuracy improves significantly (~70-85%)
- **Epochs 30-50**: Fine-tuning (85-95%+ accuracy)
- **Early stopping**: May stop if no improvement for 10 epochs

### Output Files:
1. **`best_tomato_model.h5`** - Best model (highest validation accuracy)
2. **`tomato_disease_classifier_final.h5`** - Final model after all epochs
3. **`tomato_disease_classifier_weights.h5`** - Weights only
4. **`training_info.json`** - Training statistics
5. **`training_history.png`** - Accuracy/loss graphs

---

## 🎯 Recommended Settings

### For Quick Testing (30 minutes):
```python
'epochs': 20,
'batch_size': 32,
```

### For Good Results (2-3 hours):
```python
'epochs': 50,
'batch_size': 32,
```

### For Best Results (5-8 hours):
```python
'epochs': 100,
'batch_size': 16,
```

---

## 💡 Training Tips

### 1. Use GPU if Available
- Training is **5-10x faster** with a NVIDIA GPU
- Check if GPU is available: `python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"`

### 2. Monitor Validation Accuracy
- If validation accuracy plateaus, training may finish early
- Early stopping prevents overfitting

### 3. Adjust Batch Size
- Larger batch size = faster but uses more memory
- If you get memory errors, reduce batch size to 16 or 8

### 4. Data Augmentation
- Already included (rotation, flip, zoom)
- Helps model generalize better

---

## 🐛 Troubleshooting

### Memory Error (OOM)
**Solution**: Reduce batch size
```python
'batch_size': 16,  # or even 8
```

### Very Slow Training
**Solution**: 
- Use GPU if available
- Increase batch size: `'batch_size': 64`
- Reduce epochs: `'epochs': 20`

### Low Accuracy (<70%)
**Solution**:
- Train longer (more epochs)
- Check if data is balanced
- Ensure images are in correct folders

### Model Overfitting (train acc >> val acc)
**Solution**:
- Already has dropout (0.5, 0.3)
- Increase data augmentation
- Add more training data

---

## 📈 After Training

### 1. Check Results
```powershell
# View training info
Get-Content training_info.json

# Open accuracy plot
start training_history.png
```

### 2. Test New Model
Update `main.py` to use the new model:
```python
h5_path = "best_tomato_model.h5"
```

### 3. Deploy Updated Model
```powershell
# Commit changes
git add best_tomato_model.h5
git commit -m "Updated model with improved accuracy"
git push
```

---

## ⚡ Quick Start Command

```powershell
cd c:\Users\golde\OneDrive\Desktop\model
.\.venv\Scripts\Activate.ps1
python train_model.py
```

**Then wait 2-3 hours (CPU) or 30-40 minutes (GPU)!**

---

## 📞 Need Help?

Common questions:
- **How long?** 2-3 hours on CPU, 30-40 min on GPU
- **When to stop?** Early stopping will handle this automatically
- **How to improve?** More epochs, more data, or fine-tune hyperparameters

---

**Good luck with training! 🍅🚀**
