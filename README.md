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
- 国内大厂：阿里通义千问，百度文心，字节豆包
- 初创：月之暗面 Moonshot，百川智能，智谱，零一万物，Deepseek

## 对比列表

- 输入输出长度限制，如无特别限制，一般输入输出加起来不超过总的上下文长度即可
- 美元人民币按 7 计算

| 厂商         | 模型                  | 输入价格          | 输出价格          | 上下文 Token 长度 | 最大输入 Token | 最大输出 Token |
| ------------ | --------------------- | ----------------- | ----------------- | ----------------- | -------------- | -------------- |
| OpenAI       | GPT-5.4               | 17.5 元 ($2.50)   | 105 元 ($15)      | 1M                | -              | 128k           |
| OpenAI       | GPT-5 mini            | 1.75 元 ($0.25)   | 14 元 ($2)        | 400k              | -              | 128k           |
| OpenAI       | o3                    | 14 元 ($2)        | 56 元 ($8)        | 200k              | -              | 100k           |
| OpenAI       | o4-mini               | 7.7 元 ($1.1)     | 30.8 元 ($4.4)    | 200k              | -              | 100k           |
| Anthropic    | Claude Opus 4.6       | 35 元 ($5)        | 175 元 ($25)      | 200k              | -              | 128k           |
| Anthropic    | Claude Sonnet 4.6     | 21 元 ($3)        | 105 元 ($15)      | 200k              | -              | 64k            |
| Anthropic    | Claude Haiku 4.5      | 7 元 ($1)         | 35 元 ($5)        | 200k              | -              | 64k            |
| Google       | Gemini 3.1 Pro        | 14 元 ($2)        | 84 元 ($12)       | 1M                | -              | 64k            |
| Google       | Gemini 3 Flash        | 3.5 元 ($0.50)    | 21 元 ($3)        | 1M                | -              | 64k            |
| Google       | Gemini 2.5 Pro        | 8.75 元 ($1.25)   | 70 元 ($10)       | 1M                | -              | 64k            |
| Google       | Gemini 2.5 Flash      | 2.1 元 ($0.30)    | 17.5 元 ($2.50)   | 1M                | -              | 64k            |
| Google       | Gemini 2.5 Flash-Lite | 0.7 元 ($0.10)    | 2.8 元 ($0.40)    | 1M                | -              | -              |
| Deepseek     | deepseek-chat         | 1.96 元 ($0.28)   | 2.94 元 ($0.42)   | 128k              | -              | 8k             |
| Deepseek     | deepseek-reasoner     | 1.96 元 ($0.28)   | 2.94 元 ($0.42)   | 128k              | -              | 64k            |
| 阿里通义千问 | qwen3.5-plus          | 0.8 元            | 4.8 元            | 1M                | 1M             | -              |
| 阿里通义千问 | qwen3-max             | 2.5 元            | 10 元             | 252k              | 250k           | 16k            |
| 阿里通义千问 | qwen-plus             | 0.8 元            | 2 元              | 1M                | 1M             | 8k             |
| 字节豆包     | Doubao-Seed-2.0-Pro   | 3.2 元            | 16 元             | 256k              | -              | -              |
| 字节豆包     | Doubao-Seed-2.0-Lite  | 0.6 元            | 3.6 元            | 256k              | -              | -              |
| 月之暗面     | kimi-k2.5             | 4 元              | 21 元             | 256k              | -              | -              |
| 月之暗面     | Kimi K2               | 4 元              | 16 元             | 256k              | -              | -              |
| 百川智能     | Baichuan-M3-Plus      | 5 元              | 9 元              | 32k               | -              | -              |
| 百川智能     | Baichuan4-Air         | 0.98 元           | 0.98 元           | 32k               | -              | -              |
| 智谱         | GLM-5                 | 4 元              | 18 元             | 200k              | -              | -              |
| 智谱         | GLM-4-Flash           | 免费              | 免费              | 128k              | -              | 8k             |
| 零一万物     | yi-lightning          | 1 元              | 1 元              | 16k               | -              | -              |
| 百度文心     | ERNIE-5.0             | 6 元              | 24 元             | 32k               | -              | -              |
| 百度文心     | ERNIE-4.5-Turbo       | 0.8 元            | 3.2 元            | 128k              | -              | -              |
| 百度文心     | ERNIE-Speed           | 免费              | 免费              | 8k                | -              | -              |

## 参考

- OpenAI: [https://openai.com/api/pricing/](https://openai.com/api/pricing/)
- Anthropic: [https://claude.com/pricing](https://claude.com/pricing)
- Google: [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)
- Deepseek: [https://api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing)
- 阿里通义千问：[https://help.aliyun.com/zh/model-studio/model-pricing](https://help.aliyun.com/zh/model-studio/model-pricing)
- 字节豆包：[https://www.volcengine.com/docs/82379/1544106](https://www.volcengine.com/docs/82379/1544106)
- 月之暗面：[https://platform.moonshot.cn/docs/pricing/chat](https://platform.moonshot.cn/docs/pricing/chat)
- 百川智能：[https://platform.baichuan-ai.com/price](https://platform.baichuan-ai.com/price)
- 智谱：[https://bigmodel.cn/pricing](https://bigmodel.cn/pricing)
- 零一万物：[https://platform.lingyiwanwu.com/docs](https://platform.lingyiwanwu.com/docs)
- 百度文心：[https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t)

## 问题

1. 希望增加更多的模型价格？

请在这里提交 [https://github.com/flanker/llmprice.cn/issues/new](https://github.com/flanker/llmprice.cn/issues/new) 我会更新

2. 价格/上下文长度有错误？

请在这里提交 [https://github.com/flanker/llmprice.cn/issues/new](https://github.com/flanker/llmprice.cn/issues/new) 我会更新。多谢。🙏

3. 最后更新时间

2026-03-07
