# 大模型价格对比

## 简介

这是一个静态页面项目，用来对比主流文本模型的 API 价格。

当前页面直接使用 LiteLLM 的完整模型配置，不再维护仓库内的固定模型清单。
页面会在浏览器端：

1. 读取上一次成功同步到本地缓存的 LiteLLM 数据
2. 再请求 LiteLLM 最新价格表
3. 按 provider 自动分组，展示全部可定价的文本模型

## 数据来源

- 主数据源：
  `https://cdn.jsdelivr.net/gh/BerriAI/litellm@main/model_prices_and_context_window.json`
- 回退源：
  `https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json`
- 最终回退：
  `https://raw.githubusercontent.com/BerriAI/litellm/main/litellm/model_prices_and_context_window_backup.json`
- 本地体验兜底：浏览器 `localStorage` 缓存

说明：

- LiteLLM 价格字段按 `美元 / token` 维护
- 页面统一换算为 `元 / 百万 Token`
- 默认换算汇率为 `$1 = ¥7`，并支持在页面头部手动输入
- 对于 LiteLLM 中的阶梯价模型，页面展示首档起始价格
- 页面只展示 `mode in {chat, completion, responses}` 且有价格信息的模型

## 展示逻辑

- 不再手工指定模型列表
- 所有模型都从 LiteLLM 配置动态生成
- 按 `litellm_provider` 分组展示
- 顶部筛选按 provider 类型粗分为：
  - 官方/直连
  - 云平台
  - 聚合/托管

## 参考

- LiteLLM Models:
  [https://models.litellm.ai/](https://models.litellm.ai/)
- LiteLLM cost map:
  [https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- LiteLLM backup cost map:
  [https://github.com/BerriAI/litellm/blob/main/litellm/model_prices_and_context_window_backup.json](https://github.com/BerriAI/litellm/blob/main/litellm/model_prices_and_context_window_backup.json)

## 问题

1. 希望增加新的筛选方式或字段？

请在这里提交
[https://github.com/flanker/llmprice.cn/issues/new](https://github.com/flanker/llmprice.cn/issues/new)
我会更新。

2. 价格或上下文长度显示有问题？

请在这里提交
[https://github.com/flanker/llmprice.cn/issues/new](https://github.com/flanker/llmprice.cn/issues/new)
我会更新。多谢。

3. 最后更新时间

2026-03-30
