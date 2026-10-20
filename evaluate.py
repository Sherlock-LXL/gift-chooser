from src.data import X, y
from src.validation import cross_validate

def main():
    results = cross_validate(X, y)
    for result in results["fold_results"]:
        print(f'Fold {result["fold"]}')
        print(f'  Train MSE: {result["train_mse"]:.6f}')
        print(f'  Val MSE: {result["val_mse"]:.6f}')
        print(f'  Val MAE: {result["val_mae"]:.6f}')
        print(f'  Baseline MAE: {result["baseline_val_mae"]:.6f}')
        print()
    print("Summary")
    print("Mean validation MSE:", results["mean_val_mse"])
    print("Mean validation MAE:", results["mean_val_mae"])
    print("Mean baseline MAE:", results["mean_baseline_val_mae"])
    print("10-point average error:", results["mean_val_mae"] * 10)

if __name__ == "__main__":
    main()
