> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。



## G0.1 覆写记录（2026-11-24）
本节为当前有效的 Greenfield 版本；上方为保留的 V1.1 历史基线，不再适用的部分已明确标注。完整未改历史快照及 SHA256 见 [research/design-baselines/V1.1/WORKFLOW_ENGINE_DESIGN.md](research/design-baselines/V1.1/WORKFLOW_ENGINE_DESIGN.md)。项目状态以 G0.1 为准：没有生产系统待兼容，没有真实小红书账号自动化。

# MVP 小红书图文生产 Workflow

## 流程（固定版本、可读顺序）
1 用户Brief校验/补充 → 2 产品资料分析 → 3 用户需求分析 → 4 选题生成 → 5 标题/正文/话题 → 6 封面与逐页分镜 → 7 绘图提示词 → 8 质量审核 → 9 用户审阅/确认 → 10 Markdown/ZIP内容包。

首版主链条按顺序执行，不使用自由规划、并行、动态代码或子Agent。五个专业Skill由节点复用：资料、用户、选题、文案、结构/审核；节点仍可独立显示和编辑。用户输入数量决定生成候选量，默认输出可配置。

## 节点契约
节点均接收 project_id、run_id、revision、明确输入Artifact refs及Skill/模型版本；输出独立JSON与Artifact。上下游只通过版本化引用，不在Agent隐式上下文传全部历史。错误则节点显示“等待补充/可重试失败/不可重试”，后续节点停止。

|节点|最小输出|
|---|---|
|Brief|主题/资料/目标用户/风格/数量及校验状态|
|资料分析|事实、证据来源、卖点、限制、unknowns|
|需求分析|用户场景、需求、阻力、明确假设|
|选题|N个选题方案、角度、事实引用|
|文案|标题候选、完整正文、标签建议|
|视觉|封面方案、页序/每页文案与画面、真实绘图Prompt|
|审核|结构/长度/重复/事实引用/敏感风险规则结果，修改建议|
|确认|用户对固定内容包hash确认或退回；修改后旧确认无效|
|导出|Markdown与manifest/JSON zip，含来源、版本、审核及图片状态|

## 生成图片边界
MVP将生成“图片生成Prompt”和封面/分镜方案。ImageGenerationAdapter定义generate(prompt, assets?, settings)→真实文件/服务job/error，但provider可未配置；未配置状态显示 not_configured，绝不伪造 generated image。将来配置真实服务也需模型/服务版本、成本、图像hash、许可/安全结果记录；失败不阻断文字内容包（除非用户明确要求图片文件）。

## 编辑、恢复和成本
节点编辑创建新revision；相关后代stale，从最早依赖节点重跑；未变前驱可复用。失败节点继续/重试不重跑已提交无关节点。取消写入持久状态，worker停止新节点并尽力取消模型调用。暂时错误有界重试，输出修复有限一次。执行前按用户输出数量和token上限估算成本，无法确定需在确认前展示估值/未知状态并由配置策略限制。

## 第一条工作流成功定义
在无真实账号、无图片服务、可使用已配置LLM或固定Mock的环境中，从完整输入创建run，依次产出所有文字/结构字段、质量报告和用户确认；输出内容包hash可验证；失败节点可恢复且不把stale版本混用；全程没有发布/登录/评论调用。
