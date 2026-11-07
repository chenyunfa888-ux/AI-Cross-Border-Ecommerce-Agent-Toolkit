# 输入模板 · 短视频优先视频简报

```yaml
task:
  platform*: tiktokshop
  target_market*: ""
  market_locale: ""           # 例 en-US / pt-BR / es-MX
  language_variant: ""
  content_goal: product_click  # organic | paid | product_click | retargeting
  durations: [15]
  production_mode*: mixed      # real_shoot | ai_generated | mixed
  mode: standard               # standard | variant

product:
  product_name*: ""
  category*: ""
  core_selling_point*: ""
  secondary_points: []
  spec_table*: {}
  package_content: []
  appearance:
    color: ""
    material: ""
    structure: ""

compliance:
  forbidden_words*: []
  usage_scope_confirmed*: []
  brand_authorization: []
  comparison_baseline: []      # 仅填真实可核对基准

audience_localization:
  target_persona: ""
  local_pain_points: []
  local_objections: []
  local_usage_contexts: []
  natural_product_terms: []
  creator_style: ""            # 例：实用型本地创作者，不写具体真人姓名
  cta_allowed: []
  price_or_offer: ""           # 无可靠输入则留空

proof_plan:
  has_real_product*: true
  proof_assets: []              # 已有实拍、测量、前后状态、包装等
  demo_actions: []              # 能真实完成的动作
  claims_that_cannot_be_filmed: []
  available_props: []
  locations: []
  can_shoot_people: false
  people_release_confirmed: false

visual_handoff:
  hero_visual: ""
  key_visual_moments: []
  visual_tone_confirmed: ""

voice:
  accent: ""
  tone: "natural, concise, locally fluent"
  gender: ""
```

提交前确认：所有数字有参数来源；主卖点能被镜头证明；已明确目标市场和受众；没有把尚未拍摄的内容写成已有证据。

