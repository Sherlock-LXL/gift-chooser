from pathlib import Path
import numpy as np

from gift_chooser.data import X, y
from gift_chooser.model import (
    train,
    predict,
    mse_loss,
    save_model,
    load_model,
)

MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "final_model.npz"
)

def main() -> None:
    print("Training final model...")
    parameters, loss_history = train(
        X,
        y,
        print_every=500,
    )
    prediction_before_save = predict(X, parameters)
    final_train_mse = mse_loss(
        prediction_before_save,
        y,
    )
    save_model(
        parameters,
        MODEL_PATH,
    )
    loaded_parameters = load_model(MODEL_PATH)
    prediction_after_load = predict(
        X,
        loaded_parameters,
    )
    predictions_match = np.allclose(
        prediction_before_save,
        prediction_after_load,
    )
    print()
    print("Training completed.")
    print(f"Number of samples: {len(X)}")
    print(f"Initial recorded loss: {loss_history[0]:.8f}")
    print(f"Final training MSE: {final_train_mse:.8f}")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Reloaded predictions match: {predictions_match}")
    if not predictions_match:
        raise RuntimeError(
            "Predictions changed after saving and loading the model."
        )

if __name__ == "__main__":
    main()