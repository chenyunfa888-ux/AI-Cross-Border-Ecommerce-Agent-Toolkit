# 05 · Product Video Agent v0.5

TikTok Shop 优先的跨境电商商品短视频模块，兼容 Shopee、Mercado Livre、Amazon 与 Shopify。

本版从“脚本 + 分镜”升级为四层交付：

1. **短视频优先**：TikTok 默认 9:16、15 秒主版本，先短版后扩写。
2. **强钩子**：0–0.5 秒视觉动作、0.5–1.5 秒母语钩子、3 秒内证据预告。
3. **强演示**：每个主张映射到可观察证据；缺素材输出补拍清单，不用字幕冒充证明。
4. **强本地化**：按国家、受众、使用场景和购买顾虑重写，不逐句翻译。

## 使用顺序

```text
填写 templates/input_video_brief.md
→ 读取 SKILL.md 与平台参考
→ prompts/01_script_and_storyboard.md
→ prompts/02_ai_video_and_voice.md
→ scripts/video_timing.py
→ 输出 templates/output_video_pack.yaml
```

TikTok/Feed 任务必须读取 `references/tiktok-short-video-playbook.md`。完整示例见 `examples/tiktok_air_fryer_15s.md`。

## 主要输入

- 产品事实：主卖点、参数、使用范围、禁用词
- 本地化：目标市场、语言变体、目标人群、当地顾虑和 CTA
- 证明素材：实物、已有视频、可演示动作、场地道具和人物授权情况

## 主要输出

- 卖点—证据映射
- 三种不同机制的钩子及主版本
- 15 秒竖版脚本与逐镜分镜
- AI Prompt / 实拍指令、母语口播、字幕和素材清单
- 静音、本地化、参数与合规检查
- 单变量 A/B 测试方案

本模块不直接发布、投放或操作卖家后台。平台规则会变化，发布前必须在目标站点卖家中心复核。

