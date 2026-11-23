# 送礼选择器 · Gift Chooser

[中文](#中文) · [English](#english) · [下载](https://github.com/Sherlock-LXL/gift-chooser/releases)

## 中文

使用 NumPy 手写两层神经网络，根据七项连续评分和七种礼物类别预测喜欢程度，提供中英文命令行、10 分制结果与规则建议。

### 运行

建议 Python 3.10+，已在 Python 3.12 运行：

```bash
python -m pip install -r requirements.txt
python app.py
python evaluate.py
python train_final.py
```

最终模型为 `models/final_model.npz`。五折验证至少需要 5 条样本。Windows 用户也可下载 `GiftChooser-1.0.0.exe`，无需安装 Python 或 NumPy。

### 输入与模型

| 连续特征（固定顺序，0–1，越高越好） | One-hot 类别（固定顺序） |
|---|---|
| 明确兴趣匹配 `interest_match` | 首饰配饰 `cat_jewelry_accessories` |
| 需求与实用性 `need_utility` | 周边收藏 `cat_fandom_collectibles` |
| 情感个性化 `emotional_personalization` | 书籍文创 `cat_books_stationery` |
| 审美命中把握 `aesthetic_confidence` | 电子影像 `cat_electronics_imaging` |
| 选择安全度 `selection_safety` | 美妆香氛 `cat_beauty_fragrance` |
| 收纳友好度 `storage_friendliness` | 包袋服饰 `cat_bags_clothing` |
| 价值匹配 `value_fit` | 生活日用 `cat_daily_life` |

前七维为连续特征，后七维类别恰有一个为 1。网络为 `14 → 8 ReLU → 1`；MSE 损失、学习率 0.01、4,000 步训练。线性输出只在界面显示时裁剪。

原始 61 条样本的一次五折结果：MSE **0.00886**、MAE **0.0631**、均值 baseline MAE **0.1645**，对应十分制平均误差约 **0.63**。小样本与相似礼物跨折会影响泛化，结果反映当前标签和评分规则。

### 数据与项目结构

- `src/`：配置、JSON 校验、模型、交叉验证与双语界面。
- `data/training_data.json`：默认数据；可修改 `src/config.py` 的 `DATA_PATH`。
- [双语数据提示词与评分细则](prompts/generate_training_data_prompt.md)：生成或整理自己的训练样本，默认预算为学生情侣通常不超过人民币 1,000 元。

数据要求唯一 `sample_id`、准确的 14 维特征、合法 one-hot 与 0–1 的 `target_liking`；提供 `feature_order` 时必须与固定顺序一致。AI 生成标签主要用于学习评分规则，应结合人工审阅与真实反馈。

发布模型源于特定收礼人的偏好，仅用于展示、个人实验与流程演示；原使用范围不适用于其他个人、群体或商业用途。详见 [MODEL_AND_DATA_NOTICE.md](MODEL_AND_DATA_NOTICE.md)。

李湘伦（Sherlock Lee）负责项目方向、架构、主要实现、验证与发布；ChatGPT（OpenAI）协助数据整理、评分细则、编程、调试与文档。

## English

A two-layer neural network implemented directly with NumPy predicts gift preferences from seven continuous ratings and seven categories. It includes a bilingual CLI, scores out of ten and rule-based suggestions.

### Run

Python 3.10+ is recommended; the project has run on Python 3.12:

```bash
python -m pip install -r requirements.txt
python app.py
python evaluate.py
python train_final.py
```

The final model is `models/final_model.npz`. Five-fold validation requires at least five samples. Windows users can download `GiftChooser-1.0.0.exe` without Python or NumPy.

### Inputs and model

| Continuous feature (fixed order, 0–1, higher is better) | One-hot category (fixed order) |
|---|---|
| Interest match `interest_match` | Jewelry/accessories `cat_jewelry_accessories` |
| Need/utility `need_utility` | Fandom/collectibles `cat_fandom_collectibles` |
| Emotional personalization `emotional_personalization` | Books/stationery `cat_books_stationery` |
| Aesthetic confidence `aesthetic_confidence` | Electronics/imaging `cat_electronics_imaging` |
| Selection safety `selection_safety` | Beauty/fragrance `cat_beauty_fragrance` |
| Storage friendliness `storage_friendliness` | Bags/clothing `cat_bags_clothing` |
| Value fit `value_fit` | Daily-life items `cat_daily_life` |

The first seven dimensions are continuous; exactly one of the last seven equals 1. The network is `14 → 8 ReLU → 1`, trained with MSE, learning rate 0.01 and 4,000 steps. Only the displayed linear output is clipped.

One five-fold run on the original 61 samples produced MSE **0.00886**, MAE **0.0631**, mean-prediction baseline MAE **0.1645**, and an average error of **0.63** on a ten-point scale. Small samples and similar gifts across folds affect generalization; results reflect the current labels and rubric.

### Data and structure

- `src/`: configuration, JSON validation, model, cross-validation and bilingual UI.
- `data/training_data.json`: default dataset; set `DATA_PATH` in `src/config.py` to change it.
- [Bilingual data prompt and scoring rubric](prompts/generate_training_data_prompt.md): prepare your own samples, with a default student-couple budget usually below RMB 1,000.

Samples require unique `sample_id` values, exactly 14 features, valid one-hot categories and `target_liking` within 0–1. Optional `feature_order` must match the fixed order. AI-generated labels mainly teach a scoring rubric; human review and real feedback help improve it.

The released model reflects one specific recipient and is intended for demonstration, personal experiments and workflow illustration. Its original scope excludes use for other people, groups or commercial purposes. See [MODEL_AND_DATA_NOTICE.md](MODEL_AND_DATA_NOTICE.md).

Sherlock Lee leads project direction, architecture, primary implementation, validation and release. ChatGPT (OpenAI) assisted with data structuring, rubrics, programming, debugging and documentation.
