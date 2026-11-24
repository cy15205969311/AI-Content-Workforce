# GitHub 工程接入报告

日期：2026-11-24（Asia/Shanghai）。范围：Phase 1 Git 接入及首次提交准备。**不进入 Phase 2**。

## Git 与历史

执行前工作区无 `.git`，不存在本项目的本地提交、分支或暂存内容。现已执行 `git init -b main`，配置 `origin=https://github.com/cy15205969311/AI-Content-Workforce.git`。main 是无提交的初始分支（unborn）；没有生成首次 commit，也没有 push、强推、合并或覆盖历史。

远程历史检查：`git ls-remote --symref` 在普通 HTTPS/HTTP1.1 下分别出现连接重置、连接失败和 Empty reply；GitHub API 备用检查返回 HTTP403 rate limit。**远程是否为空、是否已有提交、实际默认分支均未核实**，不能将网络失败当成空仓库。提交前再次获取远程 refs；若远程已有历史，先 fetch 并分析共同祖先和文件冲突，不覆盖远程。配置 main 只代表本地意向，不证明远程默认分支是 main。

## 拟公开范围

首批候选仅包括 Phase 1 应用代码、测试、锁文件、环境示例、CI、工程/产品设计 Markdown、ADR 和本次接入材料。具体逐文件清单、大小与 SHA256 见 [GITHUB_PUBLICATION_SCAN.json](docs/engineering/GITHUB_PUBLICATION_SCAN.json)。这是一份公开前候选清单，**不是已公开的内容**。

|本地资产|首次提交政策|理由|
|---|---|---|
|src/、tests/、.github/、pyproject.toml、uv.lock|候选|工程源码、mock/in-process 测试和配置，无业务用户资料|
|根目录设计/报告 Markdown、ADR/、docs/engineering/|候选|项目需求与工程说明；包含用户已指定的项目路径和远程仓库地址，需负责人确认可公开|
|research/sources/|全部排除|嵌套Git克隆、外部源码和素材，不能默认作为本项目源码发布|
|research/evidence/|全部排除|原始响应、外部许可证/源码/作者信息与取证元数据，尚未逐文件批准分发|
|research/design-baselines/|全部排除|保留本地历史快照；本轮不授权对外发布|
|research/下脚本、登记JSON和说明|全部排除|含本地路径/来源记录；待单独公开范围及隐私审查|
|.venv/、.phase1-clean-env/、各缓存、__pycache__/|忽略|本地依赖和生成文件，不应公开|
|.env、.env.*|忽略（仅.env.example例外）|不得提交密钥和私人配置；工作区未创建真实.env|

research 共137个非Git元数据文件在本次目录清单中登记为排除；只检查了目录清单、研究说明、来源登记样例及证据说明，**没有声称已逐项审完其隐私或许可证**。不执行外部源码、不删除文件、不移动原资料。项目文档中指向 research 的链接在GitHub将无法打开，这是本次缩减公开范围的已知限制。

## 安全检查

实际运行 `git check-ignore -v .env .venv .phase1-clean-env research/`：全部匹配预期规则。`git status --ignored` 确认虚拟环境、工具缓存和Python缓存被排除。没有真实 `.env`，`.env.example` 仅包含 APP_ENV、LOG_LEVEL 非敏感默认值。

执行本地候选文件扫描：私钥块、GitHub token、常见模型key格式、AWS access ID、含用户名密码的服务URL、敏感扩展名，以及当前环境中已有敏感变量值的逐文件匹配。对已暂存文件直接读取Git index blob进行扫描，不回显疑似密钥值；清单记录每个 blob 的字节数和 SHA256。候选文件中未发现命中。测试中的 `secret-like` 字符串为明确的无效测试标记。未调用真实模型服务/账号。

模式扫描不是完整DLP，也不能保证不存在所有形式的个人资料或凭据；公开范围仍须产品负责人审核。扫描脚本位于 docs/engineering/github_preflight.py，不依赖第三方扫描服务。暂存完成后另对每个 Git index blob 重扫并核对路径/内容一致性；结果记录在本报告的最终核对节。

## 本地工程回归与 CI

本次重新运行：Ruff lint通过、格式检查通过、mypy检查8个源码文件通过、Phase 1全部13测试通过、uv lock --check通过。应用代码/业务功能未修改。

`.github/workflows/ci.yml` 本地核对：PR及main push触发，Python 3.12，uv sync --locked，Ruff format/lint、mypy、pytest步骤齐全，无secret、数据库或真实账号要求。YAML解析及结构核对通过。**GitHub Actions 未运行，状态 NOT VERIFIED**；首次提交和push尚未批准，没有可汇报的托管run或URL。

## 首次提交建议与停止点

建议提交信息：`chore: initialize AI Content Workforce engineering foundation`。

本地只准备暂存区；提交和首次 push 均等待产品负责人批准公开文件清单及敏感检查结果。另需恢复远程只读访问、核实既有历史后，才能确定后续提交/合并方式。不得使用force push。未获批准时不执行commit或push，不进入Phase2。

## 最终核对

首次提交候选已在本地 main 暂存：74个文件、约3050行；`git diff --cached --check` 通过，暂存区与工作区差异为空。发布扫描清单记录73个候选文件及SHA256；扫描报告自身作为第74个文件单独暂存，避免自引用哈希。扫描未命中所列密钥模式/扩展名/敏感环境值。137个research文件保持忽略、未暂存。`.env`不存在，`.env`、虚拟环境和 `research/` 实际匹配忽略规则。

产品负责人仍需审阅 `git diff --cached --name-only` 的逐文件公开清单，尤其根目录产品需求/架构文档是否适合发布到该远程的可见性级别。远程历史/默认分支因连接失败和API限流仍未确认；本地暂存不代表远程存在或为空。未commit、未push、GitHub Actions 未运行。请先恢复远程只读访问并由产品负责人批准公开文件范围与提交/推送，之后才能首次提交或push。
