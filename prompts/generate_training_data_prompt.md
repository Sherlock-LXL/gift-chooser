# 礼物偏好训练数据标注 Prompt / Gift Preference Training-Data Prompt

本文件包含中文和英文两个版本。只复制其中一个完整版本交给 AI，不要同时复制两份。

This file contains Chinese and English versions. Copy only one complete version into the AI system.

---

# 中文版本

你是一名严格、保守、可复核的数据标注员。请根据我提供的“收礼人偏好资料”和“候选礼物清单”，为每个候选礼物生成一条用于回归模型训练的数据。

## 输入区

### 收礼人偏好资料

{{粘贴愿望清单、明确喜欢或不喜欢、品牌、IP、风格偏好、已有物品、近期需求、预算、关系背景和真实反馈等}}

### 候选礼物清单

{{逐条粘贴候选礼物，可包含名称、类别、价格、型号、尺寸、颜色、材质和用途等}}

## 总体规则

1. 只根据输入资料和合理常识评分。缺乏证据时必须保守，不得擅自补充偏好。
2. 证据优先级：明确说过的话 > 长期行为和习惯 > 已知品牌、类别或风格偏好 > 纯常识推断。
3. 前七个连续特征和 `target_liking` 均在 `0.00-1.00` 之间，最多保留两位小数。
4. 所有连续特征均采用“分数越高越有利”的方向。
5. 七个类别字段必须使用 one-hot 编码：必须且只能有一个为 `1`。
6. 不得把 `target_liking` 简单计算为七个连续特征的平均值。
7. 输出中不要包含具体礼物名称、品牌、人物、IP、私人称呼或其他可识别信息；只使用 `sample_001`、`sample_002` 等匿名编号。
8. 只输出合法 JSON，不要输出 Markdown 代码块，不要附加解释。
9. 默认五折交叉验证至少需要 5 条样本。不要为了凑数量而复制同一礼物。
10. 若两个候选礼物得到完全相同的 14 维输入，应重新检查它们是否真的需要作为两个独立样本。
11. 不得把目标标签、来源颜色、标签置信度、礼物名称或其他答案泄漏信息放入 `features`。

## 固定的 14 维特征顺序

1. `interest_match`: 明确兴趣匹配
2. `need_utility`: 需求实用综合
3. `emotional_personalization`: 情感个性化
4. `aesthetic_confidence`: 审美命中把握
5. `selection_safety`: 选择安全度
6. `storage_friendliness`: 收纳友好度
7. `value_fit`: 价值匹配
8. `cat_jewelry_accessories`: 首饰配饰
9. `cat_fandom_collectibles`: 周边收藏
10. `cat_books_stationery`: 书籍文创
11. `cat_electronics_imaging`: 电子影像
12. `cat_beauty_fragrance`: 美妆香氛
13. `cat_bags_clothing`: 包袋服饰
14. `cat_daily_life`: 生活日用

## 七个连续特征评分标准

### 1. interest_match | 明确兴趣匹配

- `0.90-1.00`: 明确点名想要、位于愿望清单，或精确命中指定品牌、IP、款式或材质。
- `0.70-0.89`: 明确喜欢该品牌、系列、风格或同类物品，但没有点名具体商品。
- `0.50-0.69`: 只确定大致喜欢这个类别。
- `0.30-0.49`: 关联较弱，缺少直接证据。
- `0.00-0.29`: 明确不喜欢、不需要，或与已知偏好冲突。

### 2. need_utility | 需求实用综合

- `0.90-1.00`: 正在明确需要，能解决近期问题，并预计每天或几乎每天使用。
- `0.70-0.89`: 有清楚需求，预计每周经常使用。
- `0.50-0.69`: 有一定用途，但不紧急，可能偶尔使用。
- `0.30-0.49`: 用途有限、频率低，或已有功能相近的物品。
- `0.00-0.29`: 明确不需要、已经很多、基本不会使用或很可能闲置。

不得仅因物品普遍实用就打高分。

### 3. emotional_personalization | 情感个性化

- `0.90-1.00`: 与重要共同经历、私人回忆或长期愿望直接相关，难以被普通礼物替代。
- `0.70-0.89`: 明显结合个人兴趣、经历或双方关系。
- `0.50-0.69`: 与兴趣有关，有一定针对性，但仍较常见。
- `0.30-0.49`: 稍微体现心思，但主要还是普通商品。
- `0.00-0.29`: 非常通用，换成送给其他人也基本没有区别。

情感个性化不等于价格昂贵。

### 4. aesthetic_confidence | 审美命中把握

- `0.90-1.00`: 对方明确选过这一款，或直接喜欢几乎相同的设计。
- `0.70-0.89`: 属于长期喜欢的品牌、颜色、材质或稳定风格。
- `0.50-0.69`: 设计中性、安全，但直接证据有限。
- `0.30-0.49`: 主要依靠猜测。
- `0.00-0.29`: 与已知审美明显冲突。

尺寸、色号、气味、肤质和兼容性由 `selection_safety` 评价。

### 5. selection_safety | 选择安全度

- `0.90-1.00`: 具体型号、版本、尺寸或款式已经确认。
- `0.70-0.89`: 大部分关键条件已掌握。
- `0.50-0.69`: 存在中等不确定性。
- `0.30-0.49`: 高度依赖尺寸、色号、肤质、发质、气味或兼容性。
- `0.00-0.29`: 关键条件未知，极可能选错，且不便退换或错误成本高。

### 6. storage_friendliness | 收纳友好度

- `0.90-1.00`: 小巧、易使用或属于消耗品；不会重复，几乎不增加收纳负担。
- `0.70-0.89`: 只有轻微占用空间。
- `0.50-0.69`: 占用一定空间或可能与已有物品重复，但仍可接受。
- `0.30-0.49`: 同类物品较多，或礼物较占空间、容易闲置。
- `0.00-0.29`: 明显造成堆积、重复或严重收纳压力。

### 7. value_fit | 价值匹配

默认预算假设：学生情侣日常送礼通常控制在约 1000 元以内；接近 1000 元已算较贵，明显超过后应更严格考虑性价比。

- `0.90-1.00`: 舒适预算内，质量、设计、情感或实用价值突出。
- `0.70-0.89`: 价格基本合理，品质和设计与价格匹配。
- `0.50-0.69`: 总体可接受，但性价比普通。
- `0.30-0.49`: 价格偏高、品牌溢价明显，或与实际使用程度不匹配。
- `0.00-0.29`: 明显超预算、质量与价格严重不符，或大概率花钱后闲置。

评价重点是“获得的价值是否配得上付出的价格”，不是单独看价格高低。

## target_liking | 最终喜爱程度

`target_liking` 是训练标签 `y`。综合考虑明确兴趣、需求、情感、审美、选择风险、收纳负担、价值感，以及资料中明确的正面或负面证据。不要机械平均七项特征。

- `0.90-0.98`: 非常喜欢。明确愿望、精确命中长期偏好、指定款式或来源，或有很强情感意义。
- `0.81-0.89`: 强烈喜欢。明显高匹配，但仍有轻微选择、价格或收纳折损。
- `0.60-0.80`: 一般喜欢。大概率愿意收到，但存在若干限制。
- `0.53-0.59`: 略偏喜欢。整体略正面，但证据不强。
- `0.38-0.52`: 中立或不确定。可能接受，但缺乏明确兴趣。
- `0.21-0.37`: 偏不喜欢。匹配较弱、容易闲置或存在明显风险。
- `0.05-0.20`: 明确不想要或明显冲突。

默认不要输出 `0.00` 或 `1.00`；只有证据极端且明确时才可使用。

## 类别 one-hot 规则

- 首饰、项链、手链、耳饰、发饰等 -> `cat_jewelry_accessories`
- IP 或艺人周边、手办、毛绒、卡牌、盲盒等 -> `cat_fandom_collectibles`
- 书籍、画集、字帖、手账、纸本文创等 -> `cat_books_stationery`
- 相机、手机、耳机、游戏机、键盘、电器等 -> `cat_electronics_imaging`
- 彩妆、护肤、香水、个护等 -> `cat_beauty_fragrance`
- 包、衣服、鞋、帽等 -> `cat_bags_clothing`
- 食品、鲜花、水杯、家居小物、按摩用品、日用品等 -> `cat_daily_life`

七个类别值必须且只能有一个为 `1`。

## 输出 JSON 格式

以下示例是一条“书籍文创”类别样本，因此 `cat_books_stationery` 为 `1`，其他六个类别均为 `0`。

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

输出前必须自检：

- 每条样本恰好有 14 个特征。
- 前七个连续特征均在 `0.00-1.00`。
- 后七个类别字段只能为 `0` 或 `1`，且总和等于 `1`。
- `target_liking` 在 `0.00-1.00`。
- `sample_id` 唯一并按顺序编号。
- JSON 不包含具体礼物名称或其他可识别信息。
- JSON 不包含注释、尾逗号、Markdown 代码块或额外说明。
- `feature_order` 与上方固定顺序完全一致。

---

# English Version

You are a strict, conservative, and auditable data annotator. Based on the recipient-preference material and candidate-gift list that I provide, generate one regression-training sample for each candidate gift.

## Input

### Recipient Preference Material

{{Paste wish lists, explicit likes and dislikes, brand, IP, and style preferences, existing possessions, current needs, budget, relationship context, and real feedback}}

### Candidate Gift List

{{Paste candidate gifts one by one, including categories, prices, models, sizes, colors, materials, and intended uses where available}}

## General Rules

1. Score only from supplied evidence and reasonable common-sense priors. Be conservative when evidence is missing.
2. Evidence priority: explicit statements > long-term behavior > known brand, category, or style preferences > pure inference.
3. The first seven features and `target_liking` must be within `0.00-1.00`, with at most two decimal places.
4. Every continuous feature uses a higher-is-better direction.
5. Exactly one of the seven category fields must equal `1`.
6. Do not calculate `target_liking` as a simple average of the seven features.
7. Do not include gift names, brands, people, IP names, private nicknames, or other identifying details. Use anonymous IDs such as `sample_001`.
8. Output valid JSON only, with no Markdown fences or explanations.
9. The default five-fold workflow requires at least five samples. Do not duplicate gifts merely to increase the count.
10. If two gifts receive identical 14-dimensional inputs, recheck whether they should remain separate samples.
11. Do not place target labels, source colors, confidence labels, gift names, or other leakage fields inside `features`.

## Fixed Feature Order

1. `interest_match`
2. `need_utility`
3. `emotional_personalization`
4. `aesthetic_confidence`
5. `selection_safety`
6. `storage_friendliness`
7. `value_fit`
8. `cat_jewelry_accessories`
9. `cat_fandom_collectibles`
10. `cat_books_stationery`
11. `cat_electronics_imaging`
12. `cat_beauty_fragrance`
13. `cat_bags_clothing`
14. `cat_daily_life`

## Continuous-Feature Rubrics

### interest_match

- `0.90-1.00`: Exact request, wish-list item, or precise brand, IP, design, or material match.
- `0.70-0.89`: Clear interest in the related brand, series, style, or category.
- `0.50-0.69`: Only a broad category preference is known.
- `0.30-0.49`: Weak connection with little direct evidence.
- `0.00-0.29`: Explicitly disliked, unnecessary, or conflicting.

### need_utility

- `0.90-1.00`: Clearly needed now and likely to be used daily.
- `0.70-0.89`: Clear need with frequent weekly use.
- `0.50-0.69`: Some use, but not urgent.
- `0.30-0.49`: Limited use or a similar item is already owned.
- `0.00-0.29`: Unnecessary, abundant, or likely unused.

### emotional_personalization

- `0.90-1.00`: Strong shared memory, private meaning, or long-term wish.
- `0.70-0.89`: Clearly reflects personal knowledge or relationship context.
- `0.50-0.69`: Some tailoring, but still a common choice.
- `0.30-0.49`: Limited thought and mostly generic.
- `0.00-0.29`: Highly generic.

### aesthetic_confidence

- `0.90-1.00`: Exact item selected or nearly identical design explicitly liked.
- `0.70-0.89`: Stable preferred brand, color, material, or style.
- `0.50-0.69`: Neutral and relatively safe.
- `0.30-0.49`: Mainly guessed.
- `0.00-0.29`: Conflicts with known taste.

### selection_safety

- `0.90-1.00`: Exact model, version, size, or design confirmed.
- `0.70-0.89`: Most key conditions known.
- `0.50-0.69`: Moderate uncertainty.
- `0.30-0.49`: Strongly dependent on size, shade, skin type, scent, or compatibility.
- `0.00-0.29`: Key conditions unknown and high risk of a wrong choice.

### storage_friendliness

- `0.90-1.00`: Compact, consumable, non-duplicative, and easy to store.
- `0.70-0.89`: Minor storage burden.
- `0.50-0.69`: Some space or duplication risk.
- `0.30-0.49`: Similar items are abundant or the gift may remain unused.
- `0.00-0.29`: Serious clutter or duplication burden.

### value_fit

Use the project assumption that ordinary gifts between a student couple are usually kept within approximately RMB 1,000.

- `0.90-1.00`: Comfortably within budget and clearly worth the quality or usefulness.
- `0.70-0.89`: Price broadly matches quality and design.
- `0.50-0.69`: Acceptable but ordinary value.
- `0.30-0.49`: Expensive, affected by brand premium, or poorly matched to expected use.
- `0.00-0.29`: Over budget, poor value, or highly likely to remain unused.

## target_liking

- `0.90-0.98`: Very strong liking.
- `0.81-0.89`: Strong liking.
- `0.60-0.80`: General liking.
- `0.53-0.59`: Slightly positive.
- `0.38-0.52`: Neutral or uncertain.
- `0.21-0.37`: Mild dislike.
- `0.05-0.20`: Clearly unwanted or conflicting.

Do not mechanically average the seven features. Avoid `0.00` and `1.00` unless evidence is extreme and explicit.

## Category Mapping

- Jewelry and accessories -> `cat_jewelry_accessories`
- Fandom and collectibles -> `cat_fandom_collectibles`
- Books and stationery -> `cat_books_stationery`
- Electronics and imaging -> `cat_electronics_imaging`
- Beauty and fragrance -> `cat_beauty_fragrance`
- Bags and clothing -> `cat_bags_clothing`
- Daily-life items -> `cat_daily_life`

Exactly one category must equal `1`.

## Required JSON Output

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

Before outputting, verify:

- Every sample has exactly 14 features.
- The first seven values are within `0.00-1.00`.
- The seven category values are binary and sum to `1`.
- `target_liking` is within `0.00-1.00`.
- `sample_id` values are unique and sequential.
- The JSON contains no names or identifying details.
- The JSON contains no comments, trailing commas, Markdown fences, or extra explanations.
- `feature_order` exactly matches the fixed order.