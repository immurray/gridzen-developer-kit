# 宣传相关代码变更

## 2026-11-05 — 开发者入口 Skills 数量同步

需求方 Grok Bot（代 murray），批次二「现在转」网站文案项。开发者首页英文静态降级文案、四语动态文案统一14个Skills：6个研究/工作流＋8个单任务profile；商户profile须单独授权，并满足当前可用性和资金条件。修正英文/越文下载按钮的6个旧数值，不改工具、权限、付费或发布路径。

对外可说的变化：开发者套件14个Skills的数量与适用边界说明一致。未部署、未发布新版本。测试：nice -n 19 下22项开发者/本地化/站点壳回归通过；重建本地下载包后通过，生成包按仓库规则不提交；git diff --check通过。主仓帮助/GEO检查在配套PR通过（22话题×4语言），此仓没有help_docs.py。PR：https://github.com/immurray/gridzen-developer-kit/pull/1；主仓配套：https://github.com/immurray/gridzen/pull/32。
