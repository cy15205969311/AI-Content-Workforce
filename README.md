> AI Content Workforce · Engineering Foundation V1.0 · 2026-11-24（Asia/Shanghai）
> 项目模式：Greenfield · 当前阶段：Phase 1 已实施完成，等待阶段验收。

# AI Content Workforce

当前状态：Greenfield · Phase 1 Engineering Foundation V1.0 已实施完成，等待产品负责人验收。

本项目由零开始建设。此前文档中关于“已有部署平台/等待生产源码/旁路集成”的陈述已由产品负责人本轮纠正；当前没有生产业务代码、已部署Skill、生产数据库或账号自动化。详见 [PROJECT_STATUS.md](PROJECT_STATUS.md) 与 [V1.1_DOCUMENT_REVIEW.md](V1.1_DOCUMENT_REVIEW.md)。

## 当前决策材料
- [Greenfield 范围](GREENFIELD_SCOPE.md)
- [MVP 产品需求](MVP_PRD.md) 与 [验收标准](MVP_ACCEPTANCE_CRITERIA.md)
- [MVP 架构](GREENFIELD_ARCHITECTURE.md) 与 [模块职责](MODULE_RESPONSIBILITY.md)
- [Skill Runtime](SKILL_RUNTIME_DESIGN.md)、[Workflow](WORKFLOW_MVP_DESIGN.md)、[数据](DATA_MODEL_MVP.md)、[API](API_SPEC_MVP.md)
- [参考仓库边界](XIAOHONGSHU_REFERENCE_BOUNDARY.md)
- [技术选型](TECHNOLOGY_SELECTION.md)、[八阶段路线](GREENFIELD_DEVELOPMENT_ROADMAP.md)、[待决事项](OPEN_DECISIONS.md)

## V1.1 研究资产
V1.1研究与专题报告仍保留。七份核心设计的原文归档在 `research/design-baselines/V1.1/` 并在现行文件中标出覆写；详细逐文审查见 [V1.1_DOCUMENT_REVIEW.md](V1.1_DOCUMENT_REVIEW.md)。研究来源/安全/许可证/评估原则继续有效；全球研究中心暂为研发目录。

## 当前阶段
- 技术决定：[ADR-001](ADR/ADR-001-TECH-STACK.md)；决策记录：[DECISION_LOG.md](DECISION_LOG.md)
- Phase 1 状态：[PROJECT_STATUS.md](PROJECT_STATUS.md)
- 实施报告：[PHASE1_IMPLEMENTATION_REPORT.md](PHASE1_IMPLEMENTATION_REPORT.md)
- 测试报告：[PHASE1_TEST_REPORT.md](PHASE1_TEST_REPORT.md)
- 工程文档：[docs/engineering/](docs/engineering/PROJECT_STRUCTURE.md)
- 技术决策审查（历史）：[PHASE1_TECH_DECISION_REVIEW.md](PHASE1_TECH_DECISION_REVIEW.md)，已由 [Phase 1 授权](ADR/ADR-001-TECH-STACK.md) 取代。

Phase 1 只建立 Python API 工程底座。没有 PostgreSQL 连接、ORM、Worker、模型服务、图片生成、前端或小红书账号操作。验收后停止，等待产品负责人决定是否进入 Phase 2。

## GitHub 接入准备

正式远程：[cy15205969311/AI-Content-Workforce](https://github.com/cy15205969311/AI-Content-Workforce)。本地已初始化 main 并配置 origin，尚无提交或 push；远程历史查询受网络错误阻断，实际远程默认分支未核实，GitHub Actions 未验证。

首次提交拟排除全部 `research/` 原始研究资产（仍完整保留本地），以及虚拟环境、缓存和私密配置。文档中的 research 链接在首次公开版本可能不可用。详见 [接入报告](GITHUB_INTEGRATION_REPORT.md) 和 [候选公开清单/扫描结果](docs/engineering/GITHUB_PUBLICATION_SCAN.json)。提交和 push 待产品负责人确认；本轮不进入 Phase 2。
