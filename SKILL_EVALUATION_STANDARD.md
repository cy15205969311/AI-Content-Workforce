> AI Content Workforce / AI 新媒体智能工作台 · V1.1 · 2026-11-24（Asia/Shanghai）
> 状态：研究与设计草案，待产品负责人验收；不构成生产可用或阶段验收证明。

# Skill 质量评估规范

先定义测试集再实现 Skill。评估中心独立于运行时与生成模型；采用 JSON Schema、程序规则、固定样本、人工盲审结合。LLM judge 可辅助发现问题，但不能单独决定通过；触发准确率也不等于业务质量。

## 八类必测与期望
|类型|测试输入|预期判定|
|---|---|---|
|正常|完整主题、授权资料和事实引用|输出 Schema 正确，事实有引用，无外部副作用|
|缺参|缺主题/缺必需证据|INPUT_INVALID/列缺项；允许假设的字段须明示，不编造|
|极端|空白、超长、多语言、特殊字符、上限边界|可预测拒绝/限制，合法 Unicode 不损坏|
|格式|错误类型、额外字段、畸形 JSON、错误引用|Schema 阻断；不静默丢字段|
|异常|模型5xx、超时、下载失败、worker崩溃|有界重试/失败状态；不产生伪成功|
|权限|其他项目引用、未注册工具、审批重放|全部拒绝且无泄露/动作|
|业务质量|固定真实脱敏 brief 与冲突/不足事实|引用可核、受众匹配、可执行、人工量表达标|
|回归|前版案例及历史缺陷、不同模型版本|硬门禁全过，无已修复缺陷复发|

每 Skill 建议至少24例（每类≥3），另含不触发/近邻 Skill 冲突集；计数不替代场景覆盖。首批失败恢复测试用本地 mock，不需真实发布。资料分析需逐条可追溯事实；标题需数量/重复/长度检查，平台长度规则由版本化平台 profile 定义，不能把参考脚本的38权重直接当现行官方限制；审核员需含应拦与不应拦案例，测漏报/误报。

## 结果结构
EvaluationResult 必有 case_id、suite_version/hash、test_input、expected_result、actual_result（或脱敏 ArtifactRef）、passed、error_reason、skill_id/version/hash、model_provider/model_version、prompt_hash、tool_versions、duration_ms、token_usage(input/output/cache)、usage_unknown、price_version、cost、rule_results、human_review、evaluation_result、executed_at。没有调用模型时 usage=null、usage_unknown=true，不记 0 伪装实际用量；失败输出也保留，不能只统计成功案例。

## 门禁建议（待验收）
Schema/缺参/权限/预算/高风险硬规则 100%；跨项目泄漏、未经确认动作、重大事实编造均为0，任一失败不可上架。业务由至少两位评审对事实、受众匹配、结构、可用性、表达各1–5分盲审，均值≥4且单维≥3；重大分歧由第三人裁决。至少20%随机样本人工抽检，首版或高风险用例全审。固定基线同输入对照、保存所有输出，随机任务每例重复3次报告方差/最差项，不挑最好结果。阈值需产品签收，不声称本轮已达标。

## 回归触发与测试环境
Prompt/模型/工具/Schema/权限/平台 DOM/依赖/数据集改变均触发相关回归。隔离 mock 优先；未来真实账号验证单独审批，用脱敏测试账号，日志脱敏。评估运行锁定版本和随机参数；数据集人工变更需新版本，防止模型迎合测试。结果不能由 Skill 自写 passed；规则引擎和审核员判定。
