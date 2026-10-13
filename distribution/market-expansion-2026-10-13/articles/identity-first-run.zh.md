# 第一次跑通身份入驻沙盒

先把身份入驻的结果处理跑通，再接真人核验。这个示例免账号、使用合成响应，不会创建供应商托管会话。身份结果和卖方权限必须分别处理。

## 你会完成什么

先把身份入驻的结果处理跑通，再接真人核验。这个示例免账号、使用合成响应，不会创建供应商托管会话。身份结果和卖方权限必须分别处理。

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

## 应用下一步如何处理

success 只代表模拟分支，不代表真人通过。reject 应显示可恢复提示或审核路径；unavailable 应保持未知，不能默认放行。真实接入必须绑定租户、账号和会话，验证通知来源、重新查询权威状态，再按客户业务规则修改权限。

## 限制与生产接入

不要向该试用提交证件、真实号码、凭证或真人资料。生产是独立且经负责人批准的免费试点。号码生产路线仅提供基础有效性；托管身份路线需要当前有效的免费额度与适用上游权限。真实收费仍关闭。

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=zh) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=zh)
