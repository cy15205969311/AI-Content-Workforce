> AI Content Workforce / AI 新媒体智能工作台 · V1.1 · 2026-11-24（Asia/Shanghai）
> 状态：研究与设计草案，待产品负责人验收；不构成生产可用或阶段验收证明。

# Skill 许可证政策

公开可见不等于允许复制、修改或商用。许可证按固定版本、文件和依赖核实；目录索引的许可证不能覆盖链接项目；README 声明不能替代许可证正文。无法取得 LICENSE、存在来源不明或用途不兼容时保持待审，不进入 approved。

## 分类决策
|类型|要求|
|---|---|
|MIT|保留版权声明和完整许可，适用复制件/实质部分，跟踪来源修改|
|Apache-2.0|保留许可证及适用 NOTICE、标明修改、检查专利/商标和依赖义务|
|GPL/AGPL 或其他 copyleft|按链接、修改、分发、网络服务模式专项审查，不能笼统判可用/不可用|
|Sustainable Use/商业/自定义许可|核目标商业产品、托管、嵌入、收费和第三方使用；必要时单独获得许可|
|未知/无许可|只作隔离研究；不可引入生产或分发|
|文档/图片/字体/模型/数据|分别审核 CC 条款、字体授权、素材来源、模型服务及数据条款|

## 本轮特别结论
XiaohongshuSkills LICENSE 为 MIT，版权 `Copyright (c) 2026 angiin`；仓库 owner white0dew 不等于应替换版权作者。metadata source 指向 Angiin/Post-to-xhs，要核实来源链和其他依赖，保留原声明，不把 MIT 当平台授权。

openai/skills 的 skill-creator 子目录确认为 Apache-2.0，不推断全库每个 Skill 同许可；README 已 deprecated，后续官方资源需重新审核。anthropics/skills 本轮只确认 skill-creator 子目录 Apache-2.0，不推断全部目录。agentskills 规范仓库本轮 LICENSE 为 Apache-2.0。

github/awesome-copilot、VoltAgent 索引、LangGraph 在已取到 LICENSE 范围分别为 MIT；具体依赖/链接项目仍单审。MCP servers 当前 LICENSE 明确许可过渡，新贡献 Apache-2.0、未同意重许可的历史部分仍 MIT，部分文档 CC-BY-4.0；必须以实际文件来源确定，不能统一写 MIT。marketingskills README 声称 MIT，但请求 LICENSE/ LICENSE.md 均失败，Remotion Skill LICENSE 同样未核实，均不能 approved。

n8n master LICENSE.md 为 Sustainable Use，`.ee.` 文件另需企业许可；允许的内部使用不等于可嵌入收费 SaaS。默认商业内嵌复用路径否决，独立内部使用或获得相应商业许可需新评审。其社区工作流模板可能另有作者许可，不能沿用引擎许可结论。

## 分发检查与审批记录
每个引入组件记录 source_id、commit、路径、license SPDX/LicenseRef、版权主体、依赖、修改、使用模式、分发方式、NOTICE、审核者/日期与证据哈希。构建前生成第三方清单并检查原许可随包提供；缺项阻断。许可证审核不能授权用户账号操作、平台数据抓取、著作权内容再传播或模型训练。上述是工程准入判断，复杂商业条款由有权负责人确认。
