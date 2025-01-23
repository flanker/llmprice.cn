# 大模型价格对比

## 简介

这个文档的目的是对比国内外各个厂商的大模型，主要针对文本生成类模型。

对比内容会包括：

- 价格（输入价格、输出价格）
- 文本/Token 转化率（即将推出）
- 支持上下文的长度（输入限制、输出限制）
- 其他一些备注

大模型厂商：

- 国外：OpenAI，Anthropic，Google
- 国内大厂：阿里通义千问，百度文心一言，字节豆包，腾讯混元
- 初创：月之暗面 Moonshot，百川，智谱，MiniMax，零一万物

## 对比列表

- 输入输出长度限制，如无特别限制，一般输入输出加起来不超过总的上下文长度即可
- 美元人民币按 7 计算

| 厂商         | 模型                 | 输入价格        | 输出价格      | 上下文 Token 长度 | 最大输入 Token | 最大输出 Token |
| ------------ | -------------------- | --------------- | ------------- | ----------------- | -------------- | -------------- |
| OpenAI       | gpt-4o               | 17.5 元 ($2.5)  | 70 元 ($10)   | 128k              | -              | 16k            |
| OpenAI       | gpt-4o-mini          | 1.05 元 ($0.15) | 4.2 元 ($0.6) | 128k              | -              | 16k            |
| OpenAI       | o1-preview           | 105 元 ($15)    | 420 元 ($60)  | 128k              | -              | 32k            |
| OpenAI       | o1-mini              | 21 元 ($3)      | 84 元 ($12)   | 128k              | -              | 32k            |
| Anthropic    | Claude 3.5 Sonnet    | 21 元 ($3)      | 105 元 ($15)  | 200k              | -              | 8k             |
| Anthropic    | Claude 3.5 Haiku     | 5.6 元 ($0.8)   | 28 元 ($4)    | 200k              | -              | 8k             |
| Anthropic    | Claude 3 Opus        | 105 元 ($15)    | 525 元 ($75)  | 200k              | -              | 4k             |
| 阿里通义千问 | qwen-max             | 20 元           | 60 元         | 32k               | 30k            | 8k             |
| 阿里通义千问 | qwen-plus            | 0.8 元          | 2 元          | 128k              | 126k           | 8k             |
| 阿里通义千问 | qwen-turbo           | 0.3 元          | 0.6 元        | 1000k             | 1000k          | 8k             |
| 阿里通义千问 | qwq-32b-preview      | 3.5 元          | 7 元          | 32k               | 30k            | 16             |
| 字节豆包     | Doubao-1.5-pro-32k   | 0.8             | 2             | 32k               | -              | 4k             |
| 字节豆包     | Doubao-1.5-pro-256k  | 5               | 9             | 256k              | -              | 4k             |
| 字节豆包     | Doubao-1.5-lite-32k  | 0.3             | 0.6           | 32k              | -              | 4k             |
| 字节豆包     | Doubao-pro-4k        | 0.8             | 2             | 4k                | -              | 4k             |
| 字节豆包     | Doubao-pro-32k       | 0.8             | 2             | 32k               | -              | 4k             |
| 字节豆包     | Doubao-pro-128k      | 5               | 9             | 128k              | -              | 4k             |
| 字节豆包     | Doubao-pro-256k      | 5               | 9             | 256k              | -              | 4k             |
| 字节豆包     | Doubao-lite-4k       | 0.3             | 0.6           | 4k                | -              | 4k             |
| 字节豆包     | Doubao-lite-32k      | 0.3             | 0.6           | 32k               | -              | 4k             |
| 字节豆包     | Doubao-lite-128k     | 0.8             | 1             | 128k              | -              | 4k             |
| Deepseek    | deepseek-chat       | 2               | 8             | 64K               | -              | 8K             |
| 月之暗面     | moonshot-v1-8k       | 12 元           | 12 元         | 8k                | -              | -              |
| 月之暗面     | moonshot-v1-32k      | 24 元           | 24 元         | 32k               | -              | -              |
| 月之暗面     | moonshot-v1-128k     | 60 元           | 60 元         | 128k              | -              | -              |
| 百川智能     | Baichuan4            | 100 元          | 100 元        | 32k               | -              | 2k             |
| 百川智能     | Baichuan4-Turbo      | 15 元           | 15 元         | 32k               | -              | 2k             |
| 百川智能     | Baichuan4-Air        | 0.98 元         | 0.98 元       | 32k               | -              | 2k             |
| 百川智能     | Baichuan3-Turbo      | 12 元           | 12 元         | 32k               | -              | 2k             |
| 百川智能     | Baichuan3-Turbo-128k | 24 元           | 24 元         | 128k              | -              | 2k             |
| 智谱         | GLM-4-Plus           | 50 元           | 50 元         | 128k              | -              | 8k             |
| 智谱         | GLM-4-AirX           | 10 元           | 10 元         | 8k                | -              | 8k             |
| 智谱         | GLM-4-Air            | 1 元            | 1 元          | 128k              | -              | 8k             |
| 智谱         | GLM-4-Long           | 1 元            | 1 元          | 1024k             | -              | 8k             |
| 零一万物     | yi-lightning         | 0.99 元         | 0.99 元       | 16k               | -              | -              |
| 零一万物     | yi-medium            | 2.5 元          | 2.5 元        | 16k               | -              | -              |
| 零一万物     | yi-medium-200k       | 12 元           | 12 元         | 200k              | -              | -              |
| 零一万物     | yi-large             | 20 元           | 20 元         | 32k               | -              | -              |
| 零一万物     | yi-large-turbo       | 12 元           | 12 元         | 16k               | -              | -              |

## 参考

- OpenAI: [https://openai.com/api/pricing/](https://openai.com/api/pricing/)
- Anthropic: [https://www.anthropic.com/pricing#anthropic-api](https://www.anthropic.com/pricing#anthropic-api)
- 阿里通义千问： [https://help.aliyun.com/zh/model-studio/developer-reference/what-is-qwen-llm](https://help.aliyun.com/zh/model-studio/developer-reference/what-is-qwen-llm)
- 字节豆包： [https://www.volcengine.com/pricing?product=ark_bd&tab=1](https://www.volcengine.com/pricing?product=ark_bd&tab=1)
- 月之暗面： [https://platform.moonshot.cn/docs/pricing/chat](https://platform.moonshot.cn/docs/pricing/chat)
- 百川智能： [https://platform.baichuan-ai.com/price](https://platform.baichuan-ai.com/price)
- 智谱： [https://bigmodel.cn/pricing](https://bigmodel.cn/pricing)
- 零一万物： [https://platform.lingyiwanwu.com/docs](https://platform.lingyiwanwu.com/docs)

## 问题

1. 为什么没有百度文心一言？

我花费了 5 分钟时间，没有找到百度文心一言的价格页面。😅

2. 希望增加更多的模型价格？

请在这里提交 [https://github.com/flanker/llmprice.cn/issues/new](https://github.com/flanker/llmprice.cn/issues/new) 我会更新

3. 价格/上下文长度有错误？

请在这里提交 [https://github.com/flanker/llmprice.cn/issues/new](https://github.com/flanker/llmprice.cn/issues/new) 我会更新。多谢。🙏

4. 最后更新时间

2024-12-08
