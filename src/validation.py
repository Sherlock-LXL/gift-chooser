import numpy as np

from .config import (
    SEED,
    LEARNING_RATE,
    TRAIN_STEPS,
    NUM_FOLDS,
)
from .model import (
    train,
    predict,
    mse_loss,
)

def make_folds(
    sample_count: int,
    num_folds: int = NUM_FOLDS,
    seed: int = SEED,
) -> list[np.ndarray]:
    if num_folds < 2:
        raise ValueError(
            f"num_folds must be at least 2, got {num_folds}."
        )
    if sample_count < num_folds:
        raise ValueError(
            f"Five-fold cross-validation requires at least "
            f"{num_folds} samples, but only {sample_count} were provided."
        )
    index = np.arange(sample_count)
    rng = np.random.default_rng(seed)
    rng.shuffle(index)
    folds = np.array_split(index, num_folds)
    return folds

def mae_loss(
    prediction: np.ndarray,
    target: np.ndarray,
) -> float:
    if prediction.shape != target.shape:
        raise ValueError(f"Shape mismatch: {prediction.shape} != {target.shape}")
    total_loss = 0.0
    rows, cols = prediction.shape
    for i in range(rows):
        for j in range(cols):
            total_loss += np.abs(prediction[i, j] - target[i, j])
    return total_loss / prediction.size

def baseline_mae(
    y_train: np.ndarray,
    y_val: np.ndarray,
) -> float:
    mean_score = np.mean(y_train)
    y_mean = np.full_like(y_val, mean_score)
    loss_mean = mae_loss(y_mean, y_val)
    return loss_mean

def evaluate_one_fold(
    X: np.ndarray,
    y: np.ndarray,
    folds: list[np.ndarray],
    fold_number: int,
    steps: int,
    learning_rate: float=LEARNING_RATE,
    seed: int=SEED,
) -> dict[str, float | int]:
    if not 0 <= fold_number < len(folds):
        raise ValueError(
            f"fold_number must be between 0 and {len(folds) - 1}."
        )
    train_index = np.concatenate([
        fold
        for i, fold in enumerate(folds)
        if i != fold_number
    ])
    val_index = folds[fold_number]
    X_train = X[train_index, :]
    y_train = y[train_index, :]
    X_val = X[val_index, :]
    y_val = y[val_index, :]
    parameters, _ = train(
        X_train,
        y_train,
        steps=steps,
        learning_rate=learning_rate,
        seed=seed,
    )
    train_prediction = predict(X_train, parameters)
    val_prediction = predict(X_val, parameters)
    train_mse = mse_loss(train_prediction, y_train)
    val_mse = mse_loss(val_prediction, y_val)
    val_mae = mae_loss(val_prediction, y_val)
    baseline_val_mae = baseline_mae(y_train, y_val)
    return {
        "fold": fold_number + 1,
        "train_mse": train_mse,
        "val_mse": val_mse,
        "val_mae": val_mae,
        "baseline_val_mae": baseline_val_mae,
    }

def cross_validate(
    X: np.ndarray,
    y: np.ndarray,
    num_folds: int = NUM_FOLDS,
    steps: int = TRAIN_STEPS,
    learning_rate: float = LEARNING_RATE,
    seed: int = SEED,
) -> dict:
    folds = make_folds(
        sample_count=len(X),
        num_folds=num_folds,
        seed=seed,
    )
    fold_results = []
    for fold_number in range(num_folds):
        result = evaluate_one_fold(
            X=X,
            y=y,
            folds=folds,
            fold_number=fold_number,
            steps=steps,
            learning_rate=learning_rate,
            seed=seed,
        )
        fold_results.append(result)
    train_mse_values = np.array([
        result["train_mse"]
        for result in fold_results
    ])
    mean_train_mse = np.mean(train_mse_values)
    std_train_mse = np.std(train_mse_values)
    val_mse_values = np.array([
        result["val_mse"]
        for result in fold_results
    ])
    mean_val_mse = np.mean(val_mse_values)
    std_val_mse = np.std(val_mse_values)
    val_mae_values = np.array([
        result["val_mae"]
        for result in fold_results
    ])
    mean_val_mae = np.mean(val_mae_values)
    std_val_mae = np.std(val_mae_values)
    baseline_val_mae_values = np.array([
        result["baseline_val_mae"]
        for result in fold_results
    ])
    mean_baseline_val_mae = np.mean(baseline_val_mae_values)
    std_baseline_val_mae = np.std(baseline_val_mae_values)
    return {
        "fold_results": fold_results,
        "mean_train_mse": mean_train_mse,
        "std_train_mse": std_train_mse,
        "mean_val_mse": mean_val_mse,
        "std_val_mse": std_val_mse,
        "mean_val_mae": mean_val_mae,
        "std_val_mae": std_val_mae,
        "mean_baseline_val_mae": mean_baseline_val_mae,
        "std_baseline_val_mae": std_baseline_val_mae,
    }