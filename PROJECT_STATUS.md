> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。

# 项目状态与研究基线纠正

## 当前真实状态
用户确认：本项目是 Greenfield。用户没有部署 XiaohongshuSkills 或任何小红书 Skill；该 GitHub 项目是外部参考，不是本项目生产代码。工作目录用于研究资料和设计文档，没有已确认的 AI Content Workforce 业务代码、生产数据库、Skill Registry、Workflow Engine 或 Agent 调度系统，也没有可直接使用的小红书发布 API。不要为寻找这些系统扫描整台计算机；只有用户之后提供某一应用源代码时，才审计该代码。

## 已有基线
上一轮已有 V1.1 研究/设计文档17份、XHS专题报告4份、外部来源登记12项及证据。它们是研究成果和设计提案，不代表任何产品模块已开发或阶段获批。指定 XHS 仓库固定 commit 只作为只读研究基线。旧的 PROJECT_AUDIT 结论“Phase 0 等待现网仓库和部署，才能开始 Phase 1”已被此用户状态纠正；不得继续作为当前路线门槛。

## 本轮变更约定
G0.1 设为 Greenfield 产品基准。14份新增决策文档覆盖现状、MVP、模块、Runtime、工作流、数据/API、参考项目边界、验收、选型和路线。对7份基础设计文档（PRD、SYSTEM_ARCHITECTURE、SYSTEM_BOUNDARY、MODULE_DESIGN、DATA_MODEL、API_SPEC、WORKFLOW_ENGINE_DESIGN）采用：原文快照归档 → 当前文件追加“V1.1历史基线”与“G0.1覆写”，不无记录地替换。对现有路线、项目审计、风险、决策及参考研究增补纠正日志。研究标准、安全、许可证、评估继续有效，按MVP缩减实现范围。

## 阶段状态
G0.1 Greenfield 基线已由产品负责人通过 Phase 1 正式授权书转入实施。Phase 1 Engineering Foundation V1.0 已实施完成，等待产品负责人验收；技术选型见 `ADR/ADR-001-TECH-STACK.md`，实现和测试结果分别见 `PHASE1_IMPLEMENTATION_REPORT.md` 与 `PHASE1_TEST_REPORT.md`。Phase 1 未验收前不进入 Phase 2。

## GitHub 接入补充（2026-11-24）

依本轮消息最后的 GitHub Integration 边界，只进行 Git 接入与公开前准备，不实施 Phase 2。已初始化本地 main、配置指定 origin；研究资产全部保留本地并排除首次提交范围。未commit、未push、未创建/覆盖远程历史。远程 refs 查询网络失败、备用API限流，历史/默认分支未知；Actions未实际运行。公开候选清单和实际检查见 GITHUB_INTEGRATION_REPORT.md，待产品负责人验收与首次提交/push确认。
