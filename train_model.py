"""
Tomato Disease Classification Model Training Script
Updated for TensorFlow 2.x with modern best practices
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import numpy as np
import time
from datetime import timedelta

print("="*60)
print("🍅 TOMATO DISEASE CLASSIFIER - TRAINING SCRIPT")
print("="*60)
print(f"TensorFlow version: {tf.__version__}")
print(f"GPU available: {tf.config.list_physical_devices('GPU')}")
print("="*60)

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# ============================================
# CONFIGURATION
# ============================================
CONFIG = {
    'data_dir': r'C:\Users\golde\Downloads\tomato',  # Your data directory
    'img_height': 128,
    'img_width': 128,
    'batch_size': 32,
    'epochs': 10,  # Reduced from 50 to 10 (~30 minutes)
    'learning_rate': 0.001,
    'validation_split': 0.2,
}

# ============================================
# BUILD MODEL
# ============================================
def build_model(num_classes):
    """Build CNN model architecture"""
    model = models.Sequential([
        # Input layer
        layers.InputLayer(input_shape=(CONFIG['img_height'], CONFIG['img_width'], 3)),
        
        # Conv Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Conv Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Conv Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Flatten and Dense layers
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax' if num_classes > 2 else 'sigmoid')
    ])
    
    return model

# ============================================
# DATA LOADING
# ============================================
print("\n📁 Loading dataset...")

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  # Use 20% for validation
)

# Only rescaling for validation
val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Load training data
train_generator = train_datagen.flow_from_directory(
    os.path.join(CONFIG['data_dir'], 'train'),
    target_size=(CONFIG['img_height'], CONFIG['img_width']),
    batch_size=CONFIG['batch_size'],
    class_mode='categorical',  # or 'binary' for 2 classes
    subset='training',
    shuffle=True
)

# Load validation data
validation_generator = val_datagen.flow_from_directory(
    os.path.join(CONFIG['data_dir'], 'train'),
    target_size=(CONFIG['img_height'], CONFIG['img_width']),
    batch_size=CONFIG['batch_size'],
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Get class information
num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())

print(f"\n✅ Dataset loaded successfully!")
print(f"   Classes found: {num_classes}")
print(f"   Class names: {class_names}")
print(f"   Training samples: {train_generator.samples}")
print(f"   Validation samples: {validation_generator.samples}")

# ============================================
# BUILD AND COMPILE MODEL
# ============================================
print("\n🏗️  Building model...")
model = build_model(num_classes)

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=CONFIG['learning_rate']),
    loss='categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy',
    metrics=['accuracy']
)

print("\n📊 Model Architecture:")
model.summary()

# Calculate total parameters
total_params = model.count_params()
print(f"\n   Total parameters: {total_params:,}")

# ============================================
# CALLBACKS
# ============================================
callbacks = [
    # Save best model
    ModelCheckpoint(
        'best_tomato_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    
    # Early stopping if no improvement
    EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ),
    
    # Reduce learning rate on plateau
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
]

# ============================================
# TIME ESTIMATION
# ============================================
print("\n⏱️  TIME ESTIMATION:")
print(f"   Batch size: {CONFIG['batch_size']}")
print(f"   Total epochs: {CONFIG['epochs']}")
print(f"   Steps per epoch: {train_generator.samples // CONFIG['batch_size']}")
print(f"   Validation steps: {validation_generator.samples // CONFIG['batch_size']}")

# Estimate time based on hardware
steps_per_epoch = train_generator.samples // CONFIG['batch_size']
if tf.config.list_physical_devices('GPU'):
    time_per_epoch = 30  # ~30 seconds with GPU
    print(f"\n   🚀 GPU DETECTED - Fast training!")
    print(f"   Estimated time per epoch: ~30 seconds")
    print(f"   Total estimated time: ~{(CONFIG['epochs'] * time_per_epoch) / 60:.0f} minutes")
else:
    time_per_epoch = 180  # ~3 minutes on CPU
    print(f"\n   💻 CPU ONLY - Slower training")
    print(f"   Estimated time per epoch: ~3 minutes")
    print(f"   Total estimated time: ~{(CONFIG['epochs'] * time_per_epoch) / 60:.0f} minutes")

print(f"\n   Note: Early stopping may finish training sooner!")

# ============================================
# TRAINING
# ============================================
print("\n" + "="*60)
print("🚀 STARTING TRAINING...")
print("="*60)

# Record start time
start_time = time.time()

# Train model
history = model.fit(
    train_generator,
    epochs=CONFIG['epochs'],
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Calculate training time
end_time = time.time()
training_time = end_time - start_time
training_time_str = str(timedelta(seconds=int(training_time)))

# ============================================
# SAVE MODEL
# ============================================
print("\n" + "="*60)
print("💾 SAVING MODEL...")
print("="*60)

# Save final model
model.save('tomato_disease_classifier_final.h5')
print(f"✅ Saved final model: tomato_disease_classifier_final.h5")

# Save model weights only
model.save_weights('tomato_disease_classifier_weights.h5')
print(f"✅ Saved weights: tomato_disease_classifier_weights.h5")

# ============================================
# TRAINING SUMMARY
# ============================================
print("\n" + "="*60)
print("📊 TRAINING SUMMARY")
print("="*60)

final_train_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
final_train_loss = history.history['loss'][-1]
final_val_loss = history.history['val_loss'][-1]

print(f"   Total training time: {training_time_str}")
print(f"   Epochs completed: {len(history.history['accuracy'])}")
print(f"   Final training accuracy: {final_train_acc*100:.2f}%")
print(f"   Final validation accuracy: {final_val_acc*100:.2f}%")
print(f"   Final training loss: {final_train_loss:.4f}")
print(f"   Final validation loss: {final_val_loss:.4f}")

# ============================================
# SAVE TRAINING HISTORY
# ============================================
import json

training_info = {
    'training_time': training_time_str,
    'epochs': len(history.history['accuracy']),
    'final_train_accuracy': float(final_train_acc),
    'final_val_accuracy': float(final_val_acc),
    'final_train_loss': float(final_train_loss),
    'final_val_loss': float(final_val_loss),
    'num_classes': num_classes,
    'class_names': class_names,
    'total_params': int(total_params),
    'config': CONFIG
}

with open('training_info.json', 'w') as f:
    json.dump(training_info, f, indent=2)

print(f"\n✅ Training info saved: training_info.json")

# ============================================
# PLOT TRAINING HISTORY
# ============================================
try:
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Train')
    ax1.plot(history.history['val_accuracy'], label='Validation')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Train')
    ax2.plot(history.history['val_loss'], label='Validation')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=150)
    print(f"✅ Training plots saved: training_history.png")
    
except ImportError:
    print("⚠️  Matplotlib not installed - skipping plots")

print("\n" + "="*60)
print("✅ TRAINING COMPLETE!")
print("="*60)
print("\n📁 Generated files:")
print("   1. best_tomato_model.h5 (best model during training)")
print("   2. tomato_disease_classifier_final.h5 (final model)")
print("   3. tomato_disease_classifier_weights.h5 (weights only)")
print("   4. training_info.json (training metrics)")
print("   5. training_history.png (accuracy/loss plots)")
print("\n🚀 Next step: Update your API to use the new model!")
print("="*60)
