> AI Content Workforce / AI 新媒体智能工作台 · V1.1 · 2026-11-24（Asia/Shanghai）
> 状态：研究与设计草案，待产品负责人验收；不构成生产可用或阶段验收证明。

# 全球 Skill 生态研究

## 方法与覆盖边界
本轮是有限公开生态抽样，不声称遍历全网或已完成生产验证。先查指定项目，再查官方规范、开发/评估工具、两类 Awesome 索引、n8n、MCP、LangGraph、内容营销和视频 Skill。登记见 `research/sources.registry.json`；逐文件路径、哈希、固定提交/分支与失败请求见 `research/evidence/`。没有按 Star 排名。

GitHub API metadata/commit/tree/issues 请求全部遇到 403 rate limit；通过 git 获取部分固定提交，通过 raw 获取其他正文。raw 的 branch 内容只有采集时 SHA256，commit 为 null，复用前必须重新固定。Issues 未核实，不声称没有缺陷。测试目录/依赖存在只代表结构观察，未运行测试或供应链扫描。研究脚本不执行第三方代码，不调用模型。

## 对象与实质发现
|来源|检查到的非 README 资料|可借鉴能力/限制|
|---|---|---|
|white0dew/XiaohongshuSkills|SKILL、AGENTS、全部核心脚本、配置、requirements、LICENSE、内部 code-review|CDP 发布/搜索/评论/导出模式；默认自动发布、串号和成功判定须阻断；无自动化测试套件|
|openai/skills|skill-creator SKILL、quick_validate.py、子目录 LICENSE.txt|frontmatter 及最小校验；README 明确标 deprecated 并指向 openai/plugins；不是当前通用规范的唯一权威|
|openai/plugins|README|当前官方例子入口；只发现登记，尚未检查具体插件代码/许可，不能选入生产|
|anthropics/skills|skill-creator SKILL、run_eval.py、references/schemas.md、子目录许可证|evals/expectations/history/grading 模式；run_eval 主要测触发且依赖 Claude CLI、子进程和 select，不能当跨平台业务质量测试直接搬用|
|agentskills/agentskills|specification.mdx、skills-ref/validator.py、pyproject、LICENSE|规范与参考校验；metadata 字符串映射，allowed-tools 是实验字段，不是安全边界|
|VoltAgent/awesome-agent-skills|README 分类索引、LICENSE|提供营销/SEO/研究等候选；目录 MIT 不覆盖所链接第三方；未逐个审查，discovered|
|github/awesome-copilot|具体 SKILL、scan.py、inventory_skills.py、测试夹具、references、package.json、LICENSE|来源质量/字段检查和能力目录；开发者工具偏多，不能证明小红书业务可用|
|n8n-io/n8n|workflow-execute.ts、package.json、LICENSE.md（master）|节点执行栈、等待/取消/恢复可借鉴；Sustainable Use 和 .ee 限制，不默认可嵌入商业工作台|
|modelcontextprotocol/servers|filesystem/index.ts、package.json、LICENSE|目录 realpath、read-only/confine-roots 的隔离思路；存在 HTTP/stdio 与依赖边界；当前许可过渡有 Apache/MIT/文档 CC-BY 差异，需文件级确认|
|langchain-ai/langgraph|pregel/_loop.py、pyproject、checkpoint-conformance tests、LICENSE|检查点、interrupt、durability、retry；要自行增加项目权限/预算/Artifact 契约；当前固定 git 与 raw 可能不同，不能混成同一版本结论|
|coreyhaines31/marketingskills|seo-audit/copywriting SKILL|先产品上下文、网页不可信、事实证据、用户声音；主要英文网站营销，需中文小红书本地化；README 声称 MIT 但 LICENSE 未取到，禁止复制|
|remotion-dev/skills|remotion-best-practices SKILL|路由到创作/字幕/渲染参考；顶层 version 字段并非严格通用 frontmatter，需适配；未核许可证及渲染源码，不作为已审核视频方案|

## 规范差异与落地判断
OpenAI quick_validate 的 allowed_properties 未包含 compatibility，与当前 Agent Skills 规范/参考 validator 不完全相同；而且该最小校验对空字符串检查存在条件分支缺口。不能把“某脚本返回有效”当内部契约通过。XHS 原始 name 为 RedBookSkills，大小写不符合统一小写命名；通过外部适配器保留其来源名，不改研究快照。

Anthropic 的触发测试不能替代业务质量测试；建议借鉴其分例/expectation 数据格式，内部自行制定权限、异常、回归和人工量表。Marketing copywriting 中的统计/效果主张仍需证据，不因出自 Skill 就可信。n8n 模板还须逐模板审查许可、凭据占位、节点版本、webhook 和外部服务费用；本轮未找到并验证可直接复用的小红书完整模板。

## 领域覆盖与下一轮检索
小红书运营由指定参考覆盖；内容营销/SEO由 marketingskills 覆盖；市场研究/竞品/画像/选题目前只有营销模式和索引候选，不是完成评审的成品。文案有初步参考；图片生成仅提示词设计，本轮未审核图像服务/模型许可证；视频为 Remotion 初研；社媒管理/数据分析参考 XHS 与 n8n/MCP；调度与管理参考 LangGraph、官方 Skill 规范及校验工具。

Phase 1 待检索关键词组合：xiaohongshu/rednote + skill/mcp/workflow；market research/competitor/persona/content strategy；image generation/video rendering/social media analytics。按领域至少两个独立候选或明确记录未找到原因。缺口：官方平台可用 API、中文内容质量基线、实际 n8n 工作流、图片模型服务条款、现网适配。候选不得因 README 声称覆盖领域就标 reviewed。

## 研究状态
现有登记没有 approved 项。reviewed 仅表示本轮已完成一定范围静态审阅，不等于通过上线。评分是保守预评分，unknown 不能抵消否决项。openai/skills 登为 deprecated；n8n 在“默认嵌入商业产品”用途中暂 rejected，获得合适许可可重新研究。其他对象按研究深度登记 researching/reviewed/discovered。
