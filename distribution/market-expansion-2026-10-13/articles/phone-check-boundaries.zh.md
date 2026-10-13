# 接入号码检查，不混淆号码有效性与持有权

在注册前加入号码检查，区分号码无效与服务暂不可用。格式和有效性不能证明号码持有权或短信可达。这个示例不返回线路类型，也不发送 OTP。

## 你会完成什么

在注册前加入号码检查，区分号码无效与服务暂不可用。格式和有效性不能证明号码持有权或短信可达。这个示例不返回线路类型，也不发送 OTP。

## 运行并检查三种结果



```bash
for scenario in success reject unavailable; do
  curl -fsS https://gridzen.ai/console/api/quickstart/trial \
    -H 'Content-Type: application/json' \
    -d '{"task":"signup_phone","scenario":"'"$scenario"'"}'
done
```

## 预期输出（模拟）



```json
{
  "mode": "synthetic_fixture",
  "source": "local_response_trial",
  "task": "signup_phone",
  "scenario": "success",
  "verified": false,
  "real_person_verified": false,
  "billable": false,
  "amount_minor": 0,
  "upstream_calls": 0,
  "result": {
    "source": "mock_transport",
    "mode": "simulation",
    "identity_match": "not_checked",
    "ownership": "not_checked",
    "checked_at": 1791873442.4620345,
    "status": "completed",
    "number_valid": true
  },
  "business_decision": "caller_owned",
  "next_step": "connect_verified_account_for_persisted_sandbox",
  "production_available_from_this_trial": false
}
```

## 应用下一步如何处理

success 只代表模拟分支，不代表真人通过。reject 应显示可恢复提示或审核路径；unavailable 应保持未知，不能默认放行。真实接入必须绑定租户、账号和会话，验证通知来源、重新查询权威状态，再按客户业务规则修改权限。

## 限制与生产接入

不要向该试用提交证件、真实号码、凭证或真人资料。生产是独立且经负责人批准的免费试点。号码生产路线仅提供基础有效性；托管身份路线需要当前有效的免费额度与适用上游权限。真实收费仍关闭。

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=zh) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=zh)
