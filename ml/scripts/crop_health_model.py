#crop health model training 
#dataset will be added after the team confirms the dataset
import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

# -----------------------------
# Settings
# -----------------------------

DATASET_DIR = "data/raw/cornmaize"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "crop_health_model.keras")

os.makedirs(MODEL_DIR, exist_ok=True)

print("🌱 KrishiRakshak Crop Health AI")
print("TensorFlow:", tf.__version__)

# -----------------------------
# Load dataset
# -----------------------------

print("\nLoading dataset...")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_dataset.class_names
num_classes = len(class_names)

print("\nClasses:")
for i, name in enumerate(class_names):
    print(i, name)

print("\nNumber of classes:", num_classes)

# -----------------------------
# Improve performance
# -----------------------------

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(AUTOTUNE)
validation_dataset = validation_dataset.prefetch(AUTOTUNE)

# -----------------------------
# Build MobileNetV2
# -----------------------------

print("\nBuilding model...")

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Rescaling(1./127.5, offset=-1),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# -----------------------------
# Train
# -----------------------------

print("\n🚀 Training started...")

model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)

# -----------------------------
# Save model
# -----------------------------

model.save(MODEL_PATH)

print("\n✅ MODEL TRAINING COMPLETE!")
print("Model saved to:", MODEL_PATH)

