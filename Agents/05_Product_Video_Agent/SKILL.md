---
name: tiktokshop-product-video
description: 为 TikTok Shop 优先的跨境电商商品制作 9:16 短视频脚本、强钩子、真实演示、分镜、AI 视频 Prompt、母语口播、字幕与创意测试方案；同时兼容 Shopee、Mercado Livre、Amazon 和 Shopify。用户要带货短视频、UGC 商品视频、产品演示、分镜、口播字幕或视频素材复测时使用。
metadata:
  version: 0.5.0
  category: e-commerce/video
  license: MIT
---

# TikTok Shop Product Video（05 Product Video Agent）

目标不是“把卖点念完”，而是做出一条在手机 Feed 中能停住、能看懂、能验证、能本地化复测的商品短视频。

## 默认策略

- `platform=tiktokshop` 时默认 **9:16、15–25 秒、短视频优先**；用户未指定时先交付 15 秒主版本。
- 0–1.5 秒必须出现产品或结果动作；0–3 秒完成“画面钩子 + 母语钩子 + 证据预告”。
- 一个视频只证明一个 `core_selling_point`。每个主张都必须映射到可拍到的证据。
- 先设计“怎么证明”，再写台词。画面可说明的内容不重复口播。
- 本地化是重写：按国家、受众、场景、语言习惯和购买顾虑重构，不把中文/英文逐句翻译。

其他平台沿用相同方法，但比例、时长、安全区和 CTA 以 [`references/video-specs.md`](references/video-specs.md) 为准。TikTok Shop 或 Feed 短视频必须额外读取 [`references/tiktok-short-video-playbook.md`](references/tiktok-short-video-playbook.md)。

## 最小输入

必需：`platform`、`target_market`、`product_name`、`core_selling_point`、`spec_table`、`forbidden_words`、`usage_scope_confirmed`。

强烈建议：目标人群、当地购买顾虑、评论原文、实物/素材清单、可演示动作、价格与 CTA、真人/实拍条件。

缺少能证明主卖点的素材时，不得假装已完成演示。输出 `[PROOF_MISSING]`，列出要补拍的最小镜头，并可继续给出拍摄方案。

## 工作流

1. 读取平台规范；TikTok/Feed 任务再读取短视频打法卡。
2. 建立 `claim_to_proof_map`：主卖点 → 证据 → 可拍动作 → 所需素材。
3. 生成 3 个不同机制的钩子候选，选 1 个主版本；禁止只换一句文案。
4. 先写 15 秒主版本，再按需要扩写 20/30 秒版本。
5. 输出逐镜分镜；每镜必须含动作、证据、字幕、安全区和素材来源。
6. 输出 AI Prompt 或实拍指令、母语口播与字幕。
7. 运行 `scripts/video_timing.py`；超时删词，不能靠加速语速解决。
8. 运行参数一致性检查，完成静音测试、本地化检查和合规扫描。
9. 给出 A/B 测试变量与胜出指标；一次只测试一个病因。

## 四个交付门槛

### 1. 强钩子

钩子同时具备：

- **视觉中断**：0–0.5 秒即产品/结果/动作，不使用 Logo 或静态封面开场。
- **单一承诺**：一句当地母语短句，明确痛点或结果。
- **证据预告**：3 秒内让观众知道接下来会看到什么证明。

### 2. 强演示

- 优先用真实实物、真实过程、真实结果。
- 参数卡不能替代演示；动画不能伪装成实测。
- 任何“更快、更大、更耐用”等比较都必须有可核对基准，否则改写为产品自身事实。
- 每 3–5 秒至少出现一次新的视觉证据或状态变化。

### 3. 强本地化

- 买家可见文本使用目标市场母语；内部备注用中文。
- 使用当地自然说法、常见场景、公制/当地币种和合适 CTA。
- 不编当地俚语，不套用未经证实的文化刻板印象。
- 口播必须经过母语自然度检查，不能保留翻译腔句序。

### 4. 可复测

每条成片必须附：主假设、唯一测试变量、首屏停留/完播/点击或转化指标、复测周期。未达标时回到钩子或证据诊断，不同时重写全部内容。

## 确定性校验

```bash
python scripts/video_timing.py --script narration.txt --target tiktok15
python scripts/video_timing.py --script narration.txt --target 20 --wps 2.8 --hook-window 1.5
```

TikTok 目标默认把第一句限制在约 1.5 秒；其他平台默认 3 秒。正式交付仍需按实际配音回听。

## 边界

- 不虚构参数、认证、销量、评价、前后对比或产品效果。
- 不代替用户发布视频、投放广告或修改卖家后台。
- AI 生成的人物不得冒充真实买家或特定真人；真实人物素材需有使用授权。
- 平台规则会变化，发布前必须在对应卖家中心复核。

