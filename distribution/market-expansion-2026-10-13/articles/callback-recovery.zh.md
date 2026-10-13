# 处理迟到的核验回调

回调迟到时不要重复创建核验会话。本地可运行示例用 SQLite 持久化状态、设置截止时间，并阻止超时后的权限授予。回调通道明确为模拟，不是生产签名验证器。

## 你会完成什么

回调迟到时不要重复创建核验会话。本地可运行示例用 SQLite 持久化状态、设置截止时间，并阻止超时后的权限授予。回调通道明确为模拟，不是生产签名验证器。

## 运行并检查三种结果



```bash
for scenario in success reject unavailable; do
  curl -fsS https://gridzen.ai/console/api/quickstart/trial \
    -H 'Content-Type: application/json' \
    -d '{"task":"identity_onboarding","scenario":"'"$scenario"'"}'
done
```

## 预期输出（模拟）



```json
{
  "mode": "synthetic_fixture",
  "source": "local_response_trial",
  "task": "identity_onboarding",
  "scenario": "success",
  "verified": false,
  "real_person_verified": false,
  "billable": false,
  "amount_minor": 0,
  "upstream_calls": 0,
  "result": {
    "status": "Approved",
    "reason": "synthetic_scenario",
    "hosted_url": null
  },
  "business_decision": "caller_owned",
  "next_step": "connect_verified_account_for_persisted_sandbox",
  "production_available_from_this_trial": false
}
```

## 本地状态机：重启、重复事件与截止时间

本地脚本仅接受 fixture 标识。运行下方仓库里的代码与测试，无需账号或供应商密钥。真实回调仍需独立的签名验证与授权。

```bash
git clone https://github.com/immurray/gridzen-developer-kit.git
cd gridzen-developer-kit
python3 examples/verification_delivery/delivery.py identity --db /tmp/gridzen-local-delivery.sqlite3
python3 -m venv .venv
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest examples/verification_delivery/test_delivery.py -q
```

## 应用下一步如何处理

success 只代表模拟分支，不代表真人通过。reject 应显示可恢复提示或审核路径；unavailable 应保持未知，不能默认放行。真实接入必须绑定租户、账号和会话，验证通知来源、重新查询权威状态，再按客户业务规则修改权限。

## 限制与生产接入

不要向该试用提交证件、真实号码、凭证或真人资料。生产是独立且经负责人批准的免费试点。号码生产路线仅提供基础有效性；托管身份路线需要当前有效的免费额度与适用上游权限。真实收费仍关闭。

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=zh) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=zh)
