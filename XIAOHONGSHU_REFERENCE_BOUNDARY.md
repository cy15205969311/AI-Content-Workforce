> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。

# XiaohongshuSkills 参考项目边界

指定项目 `white0dew/XiaohongshuSkills` 是外部开源参考，固定静态取证提交 `251e1786bd03a530e2220fbd2a416b56da87026b`。它不是本项目源代码/生产平台/账号运行环境；本项目采用Greenfield，不以其Python CLI或CDP作为架构底座。

## 只借鉴的模式
Skill目录及输入分流写法；发布流程对内容/媒体完整性的校验思路（转换为本项目输出校验）；模块化脚本职责边界；Feed/数据字段映射、清晰CLI错误分类可作为分析模式；高频DOM失效提示帮助风险识别；专用Profile是未来账号隔离要求的反例/设计参考，不复用当前端口逻辑。

## 不复制代码或依赖
默认发布流程、Chrome launcher、CDP协议封装、XHS selectors、登录缓存/二维码、账号管理配置、搜索/评论/赞藏执行、互动/发布Pipeline、Downloader、页面内部接口、依赖requests/websockets均不进入MVP。若后续单独评估，固定文件/提交检查、安全测试及许可审批齐备才考虑；保留MIT原版权/许可和来源修改记录。

## 首版明确不做
真实小红书账号自动登录；小红书API或页面API集成；发布、排期、评论、回复、点赞、收藏、通知抓取、账号数据看板、浏览器自动化、搜索竞品网页自动化。竞品研究只接受有明确来源的用户资料/人工提供数据，或经单独批准的一般网络Research工具；不通过此仓库绕过数据源授权。

## 接口预留
正文/图文分镜输出采用内部通用 ContentPackage，PlatformProfile `xiaohongshu-image-text@v1` 只负责规则和导出格式，不调用平台。未来外部平台创建独立Adapter及能力许可，不让平台字段污染Skill核心Schema。此前“旁路集成现网/现有小红书部署”的假设作废。
