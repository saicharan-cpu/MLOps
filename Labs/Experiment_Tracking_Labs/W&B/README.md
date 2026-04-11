# Lab 2 — Fashion MNIST CNN with W&B Experiment Tracking

## Overview

This lab trains a Convolutional Neural Network (CNN) on the **Fashion MNIST** dataset and tracks all experiments using **Weights & Biases (wandb)**. Building on the baseline from Lab 1, this version explores architectural improvements and training optimizations to push validation accuracy higher.

---

## What Changed from the Baseline

| Component | Baseline (Lab 1) | This Lab |
|---|---|---|
| Conv blocks | 1 (32 filters, 5×5) | 2 (64 → 128 filters, 3×3) |
| Batch Normalization | No | Yes (after each conv block) |
| Dense hidden layer | No | Yes (256 units) |
| Dropout | 0.2 | 0.3 |
| Optimizer | SGD + Nesterov | Adam |
| Learning rate | Fixed 0.01 | 0.001 with ExponentialDecay |
| Training samples | 10,000 | 60,000 (full dataset) |
| Epochs | 5 | 10 (with EarlyStopping) |

---

## Architecture

```
Input (28×28×1)
    │
    ▼
Conv2D(64, 3×3, relu, same) → BatchNorm → MaxPool(2×2) → Dropout(0.3)
    │
    ▼
Conv2D(128, 3×3, relu, same) → BatchNorm → MaxPool(2×2) → Dropout(0.3)
    │
    ▼
Flatten → Dense(256, relu) → Dropout(0.3)
    │
    ▼
Dense(10, softmax)
```

---

## Key Design Choices

**Why Adam instead of SGD?**  
Adam adapts the learning rate per parameter and generally converges faster on image classification tasks. With a fixed LR schedule, SGD can overshoot — Adam handles this better out of the box.

**Why ExponentialDecay?**  
Starting at 0.001 and decaying slowly allows the model to make big updates early and refine weights more carefully in later epochs, avoiding getting stuck in local minima.

**Why BatchNormalization?**  
Normalizing activations between layers stabilizes training and lets us use higher learning rates without diverging.

**Why EarlyStopping?**  
With 10 epochs set, training will stop if `val_loss` doesn't improve for 3 consecutive epochs, and automatically restores the best weights. This prevents wasting compute on overfit epochs.

---

## W&B Logging

The following are tracked per run:

- **Metrics**: `train_loss`, `train_accuracy`, `val_loss`, `val_accuracy` every 10 steps
- **Learning rate**: logged each epoch via `LogLRCallback`
- **Prediction table**: 32 sample images with true label, predicted label, confidence (`LogSamplesCallback`)
- **Confusion matrix**: full validation set every epoch (`ConfusionMatrixCallback`)
- **Model artifact**: saved `.h5` + summary text uploaded as `fashion_mnist_model_v2`
- **Checkpoints**: saved each epoch to `checkpoints/`

---

## How to Run

**1. Install dependencies**
```bash
pip install wandb tensorflow
```

**2. Login to wandb**
```bash
wandb login
```

**3. Run the notebook**
Open `Lab2.ipynb` and run all cells. Results will stream to your wandb project `Lab2-deeper-cnn`.

---

## Dataset

**Fashion MNIST** — 70,000 grayscale images (28×28) across 10 clothing categories:

| Label | Class |
|---|---|
| 0 | T-shirt/top |
| 1 | Trouser |
| 2 | Pullover |
| 3 | Dress |
| 4 | Coat |
| 5 | Sandal |
| 6 | Shirt |
| 7 | Sneaker |
| 8 | Bag |
| 9 | Ankle boot |

60,000 images used for training, full 10,000 test set for validation.

---

## Configuration Reference

```python
cfg = dict(
    dropout       = 0.3,
    layer_1_size  = 64,
    layer_2_size  = 128,
    dense_units   = 256,
    learn_rate    = 0.001,
    decay_steps   = 1000,
    decay_rate    = 0.9,
    epochs        = 10,
    batch_size    = 64,
    sample        = 60000,
    optimizer     = "adam",
)
```

All config values are passed to `wandb.config` and visible in the W&B dashboard, making it easy to sweep over hyperparameters in future experiments.

---

## Dependencies

- Python 3.10+
- TensorFlow / Keras
- wandb
- numpy
