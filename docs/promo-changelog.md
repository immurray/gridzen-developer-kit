# 宣传相关代码变更

## 2026-11-05 — 开发者入口 Skills 数量同步

需求方 Grok Bot（代 murray），批次二「现在转」网站文案项。开发者首页英文静态降级文案、四语动态文案统一14个Skills：6个研究/工作流＋8个单任务profile；商户profile须单独授权，并满足当前可用性和资金条件。修正英文/越文下载按钮的6个旧数值，不改工具、权限、付费或发布路径。

对外可说的变化：开发者套件14个Skills的数量与适用边界说明一致。未部署、未发布新版本。测试：nice -n 19 下22项开发者/本地化/站点壳回归通过；重建本地下载包后通过，生成包按仓库规则不提交；git diff --check通过。主仓帮助/GEO检查在配套PR通过（22话题×4语言），此仓没有help_docs.py。PR：https://github.com/immurray/gridzen-developer-kit/pull/1；主仓配套：https://github.com/immurray/gridzen/pull/32。

## 2026-11-11 · 全公开分发文案与链接核查

按 murray 授权修正当前指南、Skill 描述、四语言快速开始和下载包内链接；保留既有核验契约、14 个 Skill 身份、CEP/SPEI 与历史收据。无新增发布渠道、业务权限、收费逻辑或 PyPI 版本。测试见 `docs/public-surface-audit-2026-11-11.md`。

## 2026-11-11 · PyPI 0.7.1 发行准备（murray 明确授权）

将已上线的核验文案、14个Skills和公开指南并入新的wheel/sdist，补齐安装后本地文档与示例，修正中西语README旧发行/能力表述。沿用既有Trusted Publisher，仅新增包安装完整性验收，旧版不覆盖；远程Registry版本和业务权限不变。发布及干净PyPI安装的真实结果以发行收据为准。

### 0.7.1 发布验收结果

[PR #6](https://github.com/immurray/gridzen-developer-kit/pull/6) 已合并，v0.7.1 经原 Trusted Publisher 发布。官方PyPI全新环境的CLI、14个Skills和真实stdio MCP通过；127份随包文件与官网最新源ZIP逐字节一致，其中77份Skill文件与Skill ZIP一致。旧版哈希未变，官网仅更新源ZIP/校验清单两份文件，不改变服务代码或自动部署范围。详见 `distribution/release-0.7.1.json`。

## 2026-11-11 · README 与长说明文案后续修正（候选）

三语 README、安装说明及随包客户端指南统一使用核验和生产授权边界，价格说明沿用商户控制台与现有报价入口。补充词表回归并核对墨西哥身份与账户指南；保留既有 CEP/SPEI 凭证核验、兼容标识与接口行为。版本仍为 0.7.1；本候选未合并、未上传 PyPI，已发布长说明和线上内容不因此更新。

## 2026-11-11 · PR #8 文案清理补充

按 murray 点名复查追加：统一西语与中文开通边界，清理 NOTICE、随包示例、Skill 说明及十二篇三语分发文章的旧措辞，移除 Skill 说明中的定价页链接。词表新增 cobro/cobros 和中文旧否定句，并覆盖所有 Skill/示例 Markdown 与分发文章。保留 CEP 既有证据、接口事件与 Skill 标识；不改 API、默认行为或版本，不合并、不上传 PyPI。本记录仅代表 PR 候选内容，不能作为线上或已发布包已修复的证明。

验证：扩展文案专项115项、完整本地回归186项通过，分发结构校验及git diff --check通过。源码、默认接口、API枚举和所有Skill标识未修改。
