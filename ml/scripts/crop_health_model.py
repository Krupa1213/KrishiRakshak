import os
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# =========================
# SETTINGS
# =========================

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "crop_health_model.keras")

os.makedirs(MODEL_DIR, exist_ok=True)

print("🌱 KrishiRakshak Crop Health AI")
print("TensorFlow:", tf.__version__)

# =========================
# LOAD PLANTVILLAGE DATASET
# =========================

print("\nDownloading/loading PlantVillage dataset...")

(ds_train, ds_val, ds_test), ds_info = tfds.load(
    "plant_village",
    split=[
        "train[:80%]",
        "train[80%:90%]",
        "train[90%:]"
    ],
    as_supervised=True,
    with_info=True
)

NUM_CLASSES = ds_info.features["label"].num_classes
CLASS_NAMES = ds_info.features["label"].names

print("Number of classes:", NUM_CLASSES)

for i, name in enumerate(CLASS_NAMES):
    print(i, name)

# =========================
# PREPROCESSING
# =========================

def preprocess(image, label):
    image = tf.image.resize(image, IMG_SIZE)
    image = preprocess_input(tf.cast(image, tf.float32))
    return image, label


ds_train = (
    ds_train
    .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    .shuffle(1000)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

ds_val = (
    ds_val
    .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

ds_test = (
    ds_test
    .map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    .batch(BATCH_SIZE)
    .prefetch(tf.data.AUTOTUNE)
)

# =========================
# BUILD MODEL
# =========================

print("\nBuilding MobileNetV2 model...")

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(NUM_CLASSES, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# TRAIN
# =========================

print("\n🚀 Training started...")

history = model.fit(
    ds_train,
    validation_data=ds_val,
    epochs=EPOCHS
)

# =========================
# EVALUATE
# =========================

print("\n📊 Evaluating model...")

test_loss, test_accuracy = model.evaluate(ds_test)

print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# =========================
# SAVE MODEL
# =========================

model.save(MODEL_PATH)

print("\n✅ Model saved successfully!")
print("Saved to:", MODEL_PATH)