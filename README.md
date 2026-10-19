# 送礼选择器 / Gift Chooser

一个小型、可解释的神经网络项目：根据七项连续评分和一个礼物类别，估计收礼人对某件礼物的喜欢程度。

A small, explainable neural-network project that estimates how much a recipient may like a gift from seven continuous ratings and one gift category.

---

## 中文说明

### 1. 项目简介

**送礼选择器**是一个用于学习完整机器学习流程的小型项目。它将候选礼物表示为 14 维输入，并通过一个使用 NumPy 手写的两层神经网络输出喜欢程度预测，再在界面中换算为 10 分制结果。

项目包含：

- 数据读取与格式验证
- 参数初始化、前向传播与反向传播
- 均方误差损失和梯度下降训练
- 五折交叉验证与 baseline 对比
- 模型保存与读取
- 中英文命令行界面
- 分数段评语与规则驱动的个性化建议

模型结构：

```text
14 维输入
-> Linear
-> ReLU
-> Linear
-> 1 个喜欢程度预测值
```

默认配置：

```text
Input dimension: 14
Hidden dimension: 8
Output dimension: 1
Learning rate: 0.01
Training steps: 4000
Cross-validation folds: 5
Loss: Mean Squared Error
```

原始 61 条样本的一次验证结果约为：

```text
Mean validation MSE: 0.00886
Mean validation MAE: 0.0631
Mean baseline MAE: 0.1645
10-point average error: 0.63
```

在当前数据和评分规则下，模型明显优于“所有礼物都预测为训练集平均分”的 baseline。

> 重要说明：模型首先学习的是训练数据中的评分规则，而不是直接读取某个人的真实心理。AI 生成标签、人工判断和真实反馈是三种不同的信息来源。若要让模型更接近真实偏好，应持续加入本人确认、实际使用频率、主动提及、长期保留和退换情况等真实反馈。

---

### 2. 输入特征

每件礼物由 7 个连续特征和 7 个 one-hot 类别组成。

七个连续特征：

1. 明确兴趣匹配
2. 需求与实用性
3. 情感个性化
4. 审美命中把握
5. 选择安全度
6. 收纳友好度
7. 价值匹配

七个礼物类别：

1. 首饰配饰
2. 周边收藏
3. 书籍文创
4. 电子影像
5. 美妆香氛
6. 包袋服饰
7. 生活日用

所有连续特征均为“越高越好”，范围为 `0.0-1.0`。类别采用 one-hot 编码，因此七个类别值中必须恰好有一个为 `1`，其余为 `0`。

完整特征顺序：

```text
0  interest_match
1  need_utility
2  emotional_personalization
3  aesthetic_confidence
4  selection_safety
5  storage_friendliness
6  value_fit
7  cat_jewelry_accessories
8  cat_fandom_collectibles
9  cat_books_stationery
10 cat_electronics_imaging
11 cat_beauty_fragrance
12 cat_bags_clothing
13 cat_daily_life
```

---

### 3. 项目结构

```text
gift-chooser/
├─ app.py
├─ evaluate.py
├─ train_final.py
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ models/
│  └─ final_model.npz
├─ prompts/
│  └─ generate_training_data_prompt.md
├─ data/
│  └─ training_data.json
└─ gift_chooser/
   ├─ __init__.py
   ├─ config.py
   ├─ data.py
   ├─ model.py
   ├─ ui.py
   └─ validation.py
```

各文件职责：

- `config.py`: 保存随机种子、网络维度、学习率、训练步数、折数和数据路径。
- `data.py`: 读取并验证 JSON，生成 `X`、`y` 和样本编号。
- `model.py`: 参数初始化、前向传播、损失、反向传播、训练、预测、保存与读取模型。
- `validation.py`: 五折划分、MAE、baseline 和交叉验证。
- `evaluate.py`: 运行五折验证并打印指标。
- `train_final.py`: 使用全部数据训练最终模型并保存为 `.npz`。
- `ui.py`: 中英文文字、评分引导、输入检查、14 维输入、评语和建议。
- `app.py`: 加载模型、调用界面、执行预测并显示结果。

默认数据文件名为：

```text
data/training_data.json
```

其他用户可以替换同名文件，也可以使用其他文件名并在 `config.py` 中修改 `DATA_PATH`：

```python
DATA_PATH = PROJECT_ROOT / "data" / "my_training_data.json"
```

---

### 4. 安装与运行

建议使用 Python 3.10 或更高版本。项目已在 Python 3.12 环境中运行。

安装依赖：

```powershell
py -m pip install -r requirements.txt
```

可选虚拟环境：

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

运行五折交叉验证：

```powershell
py evaluate.py
```

默认使用五折交叉验证，因此数据集至少需要 5 条样本。样本很少时，即使程序能够运行，结果也可能非常不稳定。

训练最终模型：

```powershell
py train_final.py
```

模型会保存为：

```text
models/final_model.npz
```

运行应用：

```powershell
py app.py
```

实际流程：

1. 显示项目标题和 credits。
2. 加载最终模型。
3. 选择中文或英文。
4. 输入七项评分。
5. 选择礼物类别。
6. 构建 `(1, 14)` 输入。
7. 预测十分制喜欢指数。
8. 显示分数段评语和个性化建议。
9. 等待用户退出。

---

### 5. 如何让 AI 生成自己的训练数据

#### 步骤 1：准备可靠的偏好材料

整理与收礼人有关的可靠信息，例如：

- 明确说过喜欢或不喜欢的礼物
- 喜欢的品牌、作品、角色、材质、颜色和风格
- 当前真正需要的物品
- 已经拥有很多、容易重复或会造成收纳负担的物品
- 对尺寸、色号、香味、肤质、兼容性等条件的要求
- 常见预算范围
- 收到过往礼物后的真实反馈

不要为了增加样本数量而凭空编造。不要输入真实姓名、地址、电话或账号等不必要的身份信息。

#### 步骤 2：把项目提示词交给 AI

打开：

```text
prompts/generate_training_data_prompt.md
```

文件内提供中文和英文两个版本。只复制其中一个完整版本，并把自己的偏好资料和候选礼物清单放入对应输入区。

#### 步骤 3：检查 AI 输出

期望结构：

```json
{
  "feature_order": [
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
    "cat_daily_life"
  ],
  "samples": [
    {
      "sample_id": "sample_001",
      "features": {
        "interest_match": 0.90,
        "need_utility": 0.70,
        "emotional_personalization": 0.80,
        "aesthetic_confidence": 0.75,
        "selection_safety": 0.60,
        "storage_friendliness": 0.90,
        "value_fit": 0.80,
        "cat_jewelry_accessories": 0,
        "cat_fandom_collectibles": 0,
        "cat_books_stationery": 1,
        "cat_electronics_imaging": 0,
        "cat_beauty_fragrance": 0,
        "cat_bags_clothing": 0,
        "cat_daily_life": 0
      },
      "target_liking": 0.86
    }
  ]
}
```

重点检查：

1. 每个 `sample_id` 唯一。
2. 每个样本正好包含 14 个特征。
3. 前 7 个特征均在 `0-1`。
4. 后 7 个类别值只能是 `0` 或 `1`。
5. 后 7 个类别之和必须等于 `1`。
6. `target_liking` 在 `0-1`。
7. JSON 中没有注释、尾逗号或额外说明。
8. 不把目标分、来源颜色、标签置信度、礼物名称等泄漏信息放入模型输入。

`feature_order` 用于明确固定输入顺序。当前加载器会在该字段存在时检查顺序，同时验证样本特征键、值域、one-hot 类别、样本编号和输出 shape。

> 若 AI 同时生成特征和目标标签，训练出的模型主要是在蒸馏这套 AI 评分规则。正式使用前，最好由人审阅标签，并逐步用真实反馈替换或补充 AI 标签。

#### 步骤 4：保存 JSON

默认保存路径：

```text
data/training_data.json
```

使用其他文件名时，必须同步修改 `config.py` 中的 `DATA_PATH`。文件开头应直接是 `{`，结尾应为 `}`，不要包含 Markdown 代码块标记。

#### 步骤 5：运行验证、训练和应用

```powershell
py evaluate.py
py train_final.py
py app.py
```

正常训练完成后应看到：

```text
Reloaded predictions match: True
```

根据新的真实反馈更新数据时，应新增样本而不是覆盖旧样本，并重新运行验证和最终训练。

---

### 6. 七项评分原则

所有连续特征均为“越高越好”。

```text
明确兴趣匹配
9-10: 明确提过具体物品、品牌、作品、风格或材质
7-8: 明确喜欢相关品牌、系列、风格或类别
5-6: 只知道喜欢这一大类
3-4: 关联较弱，主要依靠猜测
0-2: 明确不喜欢、不需要或与偏好冲突

需求与实用性
9-10: 当前明确需要，几乎每天使用
7-8: 有清晰需求，每周频繁使用
5-6: 有一定用途，但不紧急
3-4: 用途有限或已有类似物品
0-2: 明确不需要、已有很多或很可能闲置

情感个性化
9-10: 对应共同记忆、私人含义或长期愿望
7-8: 明显体现对对方和关系的了解
5-6: 与兴趣相关，但比较常见
3-4: 有一点心意，但较通用
0-2: 几乎没有个性化

审美命中把握
9-10: 对方明确选中过该物品或高度相似款式
7-8: 已知稳定喜欢相应品牌、颜色、材质或风格
5-6: 中性、安全，但直接证据有限
3-4: 主要依靠猜测
0-2: 与已知审美偏好冲突

选择安全度
9-10: 型号、尺寸、版本、色号或款式已经确认
7-8: 大多数关键条件已知
5-6: 有一定不确定性，但风险可以接受
3-4: 高度依赖尺寸、色号、肤质、香味或兼容性
0-2: 关键条件未知，容易选错且难以退换

收纳友好度
9-10: 小巧、易存放、可消耗、几乎不会重复
7-8: 只有轻微收纳负担
5-6: 需要一定空间或可能重复
3-4: 类似物品较多、体积较大或可能闲置
0-2: 会造成明显杂物、重复或收纳压力

价值匹配
9-10: 舒适预算内，质量和用途明显值得
7-8: 价格与质量、设计和使用价值较匹配
5-6: 可以接受，但整体价值普通
3-4: 偏贵、品牌溢价明显或与使用频率不匹配
0-2: 明显超预算、性价比低或极可能闲置
```

默认预算假设为学生情侣，通常不超过人民币 1000 元；接近 1000 元已经较贵。

---

### 7. Credits / 致谢与贡献

#### 李湘伦 (Sherlock Lee)

项目作者与主要开发者。

- 提出“送礼选择器”的项目目标和使用场景。
- 负责核心架构设计与大部分代码实现。
- 使用 NumPy 手写两层神经网络的前向传播、反向传播和训练循环。
- 完成模型参数、损失函数、训练接口和预测接口。
- 实现五折交叉验证、baseline 对比和指标汇总。
- 负责项目调试、运行方式、目录组织和最终集成。
- 设计并实现中英文交互流程。
- 决定 14 维特征结构、模型用途和最终展示方式。
- 对 AI 辅助生成的内容进行审阅、修改、测试和最终取舍。

#### ChatGPT (OpenAI)

AI 开发辅助、数据整理与文档支持。

- 协助把原始偏好材料整理为七项连续特征、七项类别和目标喜欢程度。
- 协助设计评分标准、标签区间、预算假设和数据匿名化规则。
- 生成并整理用于 AI 产生训练样本的提示词。
- 协助生成、检查和打包匿名训练 JSON 及读取模块。
- 提供模块划分建议、逐步编程指导、错误定位和调试建议。
- 协助完成模型保存与读取、最终训练脚本、双语界面文字、评分说明、分数段评语和个性化建议规则。
- 协助生成 README、requirements 和辅助项目文件。
- 执行部分文件生成、格式整理、数据验证和后端打包操作。

ChatGPT 的角色是辅助设计、整理、生成和调试。项目方向、架构决策、主要代码实现、测试和最终发布决定由 Sherlock Lee 负责。

---

### 8. 局限性与使用范围

- 数据量较小，结果不应视为普遍规律。
- 初始标签包含人工判断和 AI 辅助整理，可能存在主观偏差。
- 随机五折划分可能让相似礼物同时出现在训练集和验证集中。
- 相同的 14 维输入若对应不同标签，模型只能学习折中结果。
- 线性输出层可能产生低于 0 或高于 1 的原始预测，界面只在显示时裁剪。
- 模型不能替代沟通，也不能保证某件礼物一定会被喜欢。
- 对真实个人使用时，应尊重隐私、知情和数据使用边界。
- 本项目主要用于学习、实验和个人送礼决策辅助。
- 公开数据前，请删除可识别个人身份的信息，并取得适当同意。

---

## English

### 1. Overview

**Gift Chooser** is a small educational machine-learning project that represents each candidate gift as a 14-dimensional input and uses a two-layer neural network implemented directly with NumPy to estimate a liking score.

The project includes data validation, forward and backward propagation, gradient-descent training, five-fold cross-validation, baseline comparison, model persistence, a bilingual command-line interface, score-band comments, and rule-based personalized suggestions.

Network structure:

```text
14-dimensional input
-> Linear
-> ReLU
-> Linear
-> One liking-score prediction
```

Default configuration:

```text
Input dimension: 14
Hidden dimension: 8
Output dimension: 1
Learning rate: 0.01
Training steps: 4000
Cross-validation folds: 5
Loss: Mean Squared Error
```

One run on the original 61-sample dataset produced approximately:

```text
Mean validation MSE: 0.00886
Mean validation MAE: 0.0631
Mean baseline MAE: 0.1645
Average error on a 10-point scale: 0.63
```

The model initially learns the scoring rules embedded in the dataset. It does not directly read a person's mind. Human review and real-world feedback remain important.

---

### 2. Input Features

Each gift uses seven continuous features and seven one-hot category values.

Continuous features:

1. Explicit interest match
2. Need and utility
3. Emotional personalization
4. Aesthetic confidence
5. Selection safety
6. Storage friendliness
7. Value fit

Categories:

1. Jewelry and accessories
2. Fandom and collectibles
3. Books and stationery
4. Electronics and imaging
5. Beauty and fragrance
6. Bags and clothing
7. Daily-life items

All continuous features are higher-is-better and must be within `0.0-1.0`. Exactly one category value must equal `1`.

The complete feature order is identical to the Chinese section above.

---

### 3. Project Structure

```text
gift-chooser/
├─ app.py
├─ evaluate.py
├─ train_final.py
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ models/
│  └─ final_model.npz
├─ prompts/
│  └─ generate_training_data_prompt.md
├─ data/
│  └─ training_data.json
└─ gift_chooser/
   ├─ __init__.py
   ├─ config.py
   ├─ data.py
   ├─ model.py
   ├─ ui.py
   └─ validation.py
```

The default dataset path is:

```text
data/training_data.json
```

Users may replace that file or update `DATA_PATH` in `config.py`.

---

### 4. Installation and Usage

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

Run five-fold cross-validation:

```powershell
py evaluate.py
```

The default five-fold workflow requires at least five samples. Very small datasets may produce unstable results.

Train the final model:

```powershell
py train_final.py
```

Run the application:

```powershell
py app.py
```

Actual application order:

1. Displays the project title and credits.
2. Loads the final model.
3. Lets the user choose Chinese or English.
4. Collects seven feature scores.
5. Collects one gift category.
6. Builds a `(1, 14)` input.
7. Predicts a score on a 10-point scale.
8. Displays a score-band assessment and personalized suggestions.
9. Waits for the user to exit.

---

### 5. Generating Your Own Training Data with AI

1. Prepare reliable preference material and candidate gifts.
2. Open `prompts/generate_training_data_prompt.md`.
3. Copy one complete language version only.
4. Require valid JSON with the exact 14-feature order.
5. Confirm that continuous features and `target_liking` are within `0-1`.
6. Confirm that exactly one category equals `1`.
7. Save the file as `data/training_data.json`, or update `DATA_PATH`.
8. Run `py evaluate.py`.
9. Run `py train_final.py`.
10. Run `py app.py`.

The loader validates JSON parsing, non-empty samples, unique IDs, feature keys, value ranges, one-hot categories, and output shapes. It checks `feature_order` when that field is present.

If the AI generates both features and target labels, the model mainly distills the AI scoring rubric. Human review and real feedback should gradually replace or supplement generated labels.

---

### 6. Scoring Rubric

All continuous features use a higher-is-better convention. The detailed English rubric is included in `prompts/generate_training_data_prompt.md` and mirrors the Chinese scoring standards in this README.

---

### 7. Credits

#### Sherlock Lee

Creator and primary developer.

- Conceived the project and its intended use.
- Designed the core architecture and implemented most of the code.
- Implemented the NumPy neural network, backpropagation, training loop, validation workflow, baseline comparison, project integration, and bilingual interaction flow.
- Reviewed, modified, tested, and approved AI-assisted content.

#### ChatGPT (OpenAI)

AI development assistant, data-structuring assistant, and documentation contributor.

- Helped structure source material into features, categories, and target labels.
- Helped design scoring rubrics, target bands, budget assumptions, and anonymization rules.
- Generated and refined the training-data prompt.
- Assisted with JSON generation and validation, modular design, debugging, model persistence, bilingual UI text, score-band comments, personalized suggestion rules, and documentation.
- Performed selected file-generation, formatting, data-validation, and backend packaging operations.

The project's direction, architecture, primary implementation, testing, and release decisions were led by Sherlock Lee.

---

### 8. Limitations and Intended Use

- The dataset is small and is not a universal model of gift preferences.
- Labels include human judgment and AI-assisted structuring.
- Random cross-validation may place similar gift types in both training and validation folds.
- Identical inputs with different labels can only be learned as a compromise.
- The UI clips only the displayed score when the linear output falls outside `0-1`.
- The model cannot replace communication or guarantee that a gift will be liked.
- Use with real people should respect privacy and consent.
- The project is intended for learning, experimentation, and personal gift-planning assistance.
