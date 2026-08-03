from __future__ import annotations
import json
from pathlib import Path
import numpy as np

from .config import DATA_PATH

FEATURE_ORDER: tuple[str, ...] = (
    "interest_match",
    "need_utility",
    "emotional_personalization",
    "aesthetic_confidence",
    "selection_safety",
    "storage_friendliness",
    "value_fit",
    "cat_jewelry_accessories",
    "cat_fandom_collectibles",
    "cat_books_stationery",
    "cat_electronics_imaging",
    "cat_beauty_fragrance",
    "cat_bags_clothing",
    "cat_daily_life",
)

CONTINUOUS_FEATURES = FEATURE_ORDER[:7]
CATEGORY_FEATURES = FEATURE_ORDER[7:]

def _read_finite_number(value: object, *, field: str, sample_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{sample_id}: {field} must be a JSON number.")
    number = float(value)
    if not np.isfinite(number):
        raise ValueError(f"{sample_id}: {field} must be finite.")
    return number

def load_dataset(
    json_path: str | Path,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    path = Path(json_path)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(payload, dict):
        raise ValueError("The top-level JSON value must be an object.")
    declared_order = payload.get("feature_order")
    if declared_order is not None and tuple(declared_order) != FEATURE_ORDER:
        raise ValueError("feature_order does not match the model's required 14-feature order.")
    samples = payload.get("samples")
    if not isinstance(samples, list) or not samples:
        raise ValueError("'samples' must be a non-empty list.")
    rows: list[list[float]] = []
    targets: list[float] = []
    sample_ids: list[str] = []
    seen_ids: set[str] = set()
    for position, sample in enumerate(samples, start=1):
        if not isinstance(sample, dict):
            raise ValueError(f"Sample {position} must be an object.")
        sample_id = sample.get("sample_id")
        if not isinstance(sample_id, str) or not sample_id.strip():
            raise ValueError(f"Sample {position} has an invalid sample_id.")
        if sample_id in seen_ids:
            raise ValueError(f"Duplicate sample_id: {sample_id}")
        seen_ids.add(sample_id)
        features = sample.get("features")
        if not isinstance(features, dict):
            raise ValueError(f"{sample_id}: 'features' must be an object.")
        missing = [name for name in FEATURE_ORDER if name not in features]
        extra = [name for name in features if name not in FEATURE_ORDER]
        if missing or extra:
            raise ValueError(
                f"{sample_id}: feature keys mismatch; "
                f"missing={missing}, extra={extra}"
            )
        row: list[float] = []
        for name in CONTINUOUS_FEATURES:
            value = _read_finite_number(
                features[name], field=name, sample_id=sample_id
            )
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{sample_id}: {name}={value} is outside [0, 1]."
                )
            row.append(value)
        category_values: list[int] = []
        for name in CATEGORY_FEATURES:
            raw_value = features[name]
            if isinstance(raw_value, bool) or raw_value not in (0, 1):
                raise ValueError(
                    f"{sample_id}: {name} must be exactly 0 or 1."
                )
            category_values.append(int(raw_value))
        if sum(category_values) != 1:
            raise ValueError(
                f"{sample_id}: category features must be one-hot; "
                f"found sum={sum(category_values)}."
            )
        row.extend(float(value) for value in category_values)
        target = _read_finite_number(
            sample.get("target_liking"),
            field="target_liking",
            sample_id=sample_id,
        )
        if not 0.0 <= target <= 1.0:
            raise ValueError(
                f"{sample_id}: target_liking={target} is outside [0, 1]."
            )
        rows.append(row)
        targets.append(target)
        sample_ids.append(sample_id)
    X = np.asarray(rows, dtype=float)
    y = np.asarray(targets, dtype=float).reshape(-1, 1)
    expected_x_shape = (len(samples), len(FEATURE_ORDER))
    expected_y_shape = (len(samples), 1)
    if X.shape != expected_x_shape:
        raise RuntimeError(
            f"Unexpected X shape: {X.shape}; expected {expected_x_shape}."
        )
    if y.shape != expected_y_shape:
        raise RuntimeError(
            f"Unexpected y shape: {y.shape}; expected {expected_y_shape}."
        )
    return X, y, sample_ids

X, y, sample_ids = load_dataset(DATA_PATH)