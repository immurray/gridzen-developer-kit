# Gridzen 开发者工具包 0.6.0

工具包提供 198 个国家/地区的核验研究、接入方案、五种模拟结果、Python CLI/HTTP SDK、本地 MCP 和六个 Skills。当前没有启用真实供应商通道，模拟结果不代表真实人员通过核验。

在线试用与中文指南：https://gridzen.ai/developers/ 。页面右上角可切换中文、英文和西班牙文，并记住选择。研究快照日期为 2026-10-07，来源和原始接入限制保持原文。

## 安装

下载并解压 gridzen-developer-kit.zip，然后在解压目录的上一级运行。需要 Python 3.11 或更高版本。

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install './gridzen-developer-kit[mcp]'
gridzen plan --country ID --event payout
gridzen simulate --country ID --capability bank_account_match --scenario timeout
python gridzen-developer-kit/examples/payout.py
```

Windows 下使用 `.venv\Scripts\activate` 激活虚拟环境。CLI 和本地 MCP 安装后可离线使用；Python HTTP SDK 与示例调用公开沙盒。

## MCP 与 Skills

在兼容客户端添加本地 stdio 服务，将 command 替换为实际安装路径：

```json
{"mcpServers":{"gridzen":{"command":"/absolute/path/to/.venv/bin/gridzen-mcp","args":[]}}}
```

可输入：“为印度尼西亚制定付款核验接入方案，然后测试供应商超时。”五个工具分别查询覆盖、规划、生成模拟结果、读取结果和解释原因。客户端配置格式可能不同；当前没有远程生产 MCP 地址。

将 `skills/` 中各个文件夹复制到 Agent 支持的技能目录，保留 `SKILL.md` 和引用文件。六个 Skill 覆盖方案选择、沙盒接入、结果解释、供应商权限准备、提现政策和墨西哥试点规划。代码标识和技能名称保持英文，Agent 可以用中文讲解。

## 理解测试结果

- match：模拟匹配，不授权真实入驻或付款。
- mismatch：模拟不匹配，不构成欺诈判断。
- not_found：模拟无记录，结果无法确定。
- timeout：模拟供应商超时，结果无法确定。
- unsupported：模拟不支持的通道，结果无法确定。

所有结果保留 `simulated=true`、`verified=false`、`live_available=false`。沙盒只接受国家、能力和场景等已定义字段，不接受个人资料、证件、银行账户或供应商凭据。模拟 ID 是可复用的测试数据标识，不是真实交易编号。

工具包包含 Python 和 Next.js 示例；接口定义见 https://gridzen.ai/developers/api/openapi.json 。开发环境研究证据不等于商用授权。真实试点需先确认具体供应商通道；可将国家、核验类型和预计用量发送至 open@gridzen.ai。

## 公开发布与远程 MCP（0.2.0）

远程地址：`https://gridzen.ai/developers/mcp`，无需账号或 API Key。
提供相同的五个研究／模拟工具，真实验证通道仍为零。远程调用会把已记录的
工具参数发送到 Gridzen；本地 stdio 安装后仍可离线运行。

Skills 安装：`npx skills add immurray/gridzen-developer-kit`。
源码：https://github.com/immurray/gridzen-developer-kit 。PyPI 尚未发布，
当前请使用 GitHub 发布包或官网下载包。公开源码使用 MIT 许可证；第三方资料
权利及研究边界见 NOTICE.md。

## 市场发布状态

源码、版本下载、官方 MCP Registry 和三个 Skills.sh 技能页已公开；Docker 目录投稿待审核。各渠道真实状态及剩余步骤见[发布台账](distribution/STATUS.md)。


## Six bundled Skills (0.6.0)

`python -m pip install gridzen-developer-kit` installs the CLI, stdio MCP dependencies
and all six Skill directories. Version 0.6.0 is published on
[PyPI](https://pypi.org/project/gridzen-developer-kit/0.6.0/); clean installation,
CLI, stdio MCP and all six bundled Skill directories were verified. No extra MCP
dependency installation is required.

```sh
gridzen coverage --country MX
gridzen skills
gridzen-mcp
```

Connect `gridzen-mcp` as your client's stdio server, or use the remote endpoint
`https://gridzen.ai/developers/mcp`. `gridzen skills` prints the installed directories;
copy a complete directory into your assistant's configured Skills directory to
activate it. Installing a wheel does not automatically activate a client's Skills.

The existing select/integrate/explain Skills remain available. Added offline
workflows, version 1.0.0: `mexico-pilot-scoper`, `payout-policy-designer`, and
`provider-rights-readiness`. Each includes MIT, README, complete response fixtures
and agent acceptance prompts. They make no third-party calls and grant no real
verification, legal approval or regulatory conclusion.

## 统一接入十类助手

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

安装命令需要在 Python 3.11+ 虚拟环境中执行。先预览，再加 --apply。不会修改客户端全局设置；Desktop 和 Cline 需要手动导入，其他客户端需要信任工作区。配置生成成功不代表每个客户端或模型均已实测。

[Instructions / 使用说明](https://gridzen.ai/developers/harnesses.html) · [Compatibility / 测试记录](clients/compatibility.json)


## Customer tasks and voluntary feedback (0.6.0)

```sh
gridzen plan --country US --event onboarding --task signup_phone
gridzen plan --country US --event onboarding --task identity_onboarding
gridzen plan --country US --event onboarding --task identity_onboarding --stage production
python examples/customer_tasks.py
gridzen feedback --task signup_phone --country US --outcome blocked --blocker missing_workflow_step --output task-summary.json
# Only after choosing to share:
gridzen feedback --input task-summary.json --share
```

Phone intelligence is not OTP or ownership verification. Identity fixtures are not hosted document/liveness sessions. Payout matching remains a prototype with no real enabled route. Provider intake Skills are for provider operations/BYO, not a universal customer gate.

Remote APIs count fixed task/capability/country/stage/error categories for 90 days, including technical failures. They store no arguments, identity data, credentials, raw chats or per-user tracking. Local feedback is off by default. After explicit opt-in, CLI and stdio MCP automatically upload category-only events. Reading static Skills remains unobservable. Optional feedback requires explicit consent, contains only fixed categories, and is unverified self-reported evidence. A SHA-256 hash of its random receipt ID is retained 30 days for 30-day retry deduplication; the ID itself is not stored. Counters are capped at 10,000 requests/day and 500 summaries/day per database; missing history or offline usage is unknown. Requests are not unique customers.

## 首次同意后的本地自动反馈（0.6.0）

```sh
gridzen telemetry status
# Run only after reading and agreeing to category-only automatic sharing:
gridzen telemetry enable --consent
gridzen plan --country US --event onboarding --task signup_phone
# Send one queued event per invocation after reconnecting:
gridzen telemetry flush
# Disable future uploads and clear the pending queue:
gridzen telemetry disable
```

No network calls occur from local CLI/MCP when disabled. Consent is saved per OS user, not silently added to a project. Events contain only documented categories, ISO country, and a random per-event receipt, with no conversation, identity fields, credentials, user or project IDs. Feedback failures do not fail tool execution. The local queue is capped at 1,000 events/30 days; reconnect or `flush` retries one queued event, with a one-second HTTP timeout. Uploads are self-reported usage, not authenticated customers or completed verification. No background daemon is installed. Merely reading a Skill is unobservable; after consent, an Agent can explicitly record a fixed-category task summary.

本地反馈默认关闭。用户先阅读说明并同意，再运行 `gridzen telemetry enable --consent`；此后 CLI 和本地 MCP 自动反馈分类事件。`gridzen telemetry disable` 立即关闭并清空待发送队列。断网最多保留 1000 条、30 天；恢复后每次调用或 flush 发送一条，无后台守护进程。只发送固定分类、国家和随机事件回执，不发送对话、身份资料、凭证或用户/项目标识。按服务器收到的日期统计，延迟上传不是该日实际发生的全部调用。仅阅读 Skill 无法自动观察，Agent 可在用户已经同意时主动 record 分类小结。它们仍是自报线索，不代表认证客户或真实核验完成。

Local queued events expire after 30 days and are removed on the next enqueue/flush. Daily aggregates use server receipt date; delayed uploads are not proof that work occurred on that date.

## 独立的客户生产试点

已发行的 0.6.0 工具包与公开五个工具仍提供研究和模拟，不自动启用真人核验。客户可以申请独立试点：[申请入口](https://gridzen.ai/console/pilot?lang=zh)、[接入指南](https://gridzen.ai/console/pilot-guide?lang=zh)、[公开范围](https://gridzen.ai/zh/guides/customer-pilot/)。

申请不会自动开通。负责人核对供应商权限、下游协议、能力、次数和有效期后批准，仅用确认的免费额度。生产试点使用独立下载的 MCP 客户端和商户 Key；不向研究 MCP 提交证件、人脸或供应商密钥。号码基础有效性不提供 OTP 或号码归属证明。

已真实验收基础号码查询和历史 Approved 本人身份结果经新版 API/MCP 读取；新会话真人完成及最终真实回调尚未验收。自测、下载和费用意向不等于客户需求。这次只更新文档，不改变 PyPI 或 Registry 版本。
