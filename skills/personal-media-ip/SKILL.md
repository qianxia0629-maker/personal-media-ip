---
name: personal-media-ip
description: 导入本配置包或首次使用时通过对话逐项配置品牌、文风、平台、音色与制作参数；完成后制作个人自媒体视频和公众号文章。
---

# 个人自媒体IP打造

本仓库为 Agent 读取执行的工作流与本地制作工具集合，从本文件所在技能目录向上两级定位根目录（根目录应有config.json和scripts）；不依赖原作者机器。

1. **先检查首次配置。** 运行根目录 `scripts/onboarding.py next`，读取 `docs/首次启动向导.md`。本机未配置或配置中：只问返回的当前一项，等待真实回答，保存后再下一项；不同时发一串问题，不默认跳过高级参数，不配音或制作视频。用户明确说“其余保持默认”才批量确认。每次新对话续接未答项，已完成不重复问。
2. 所有适用项处理完后汇总选择、保存并同步，分别说明账户/素材待接入状态。配置完成后读根目录 config.json、workflow/文案编写配置.json 与 AGENTS.md，正常制作。
3. 时事调查读 ../investigation-video/SKILL.md，讲解读 ../whiteboard-video/SKILL.md。保持品牌与声音选择，不把调查片做成固定白板。
4. 查证后用 workflow/文案编写提示词.md 写初稿，再依次读 ../humanizer-zh/SKILL.md、../stop-slop/SKILL.md、../taste-skill/SKILL.md 完成审校；设计规则只取适用于文本/视觉的部分。核对事实、观点、限定与衔接后再配音。审校记录保存在当期workspace。
5. 按config.tts.engine选择：volc走原生火山；chatcut由使用者连接自己的Desktop MCP并查询/apply自己的音色；external使用其他数字人/克隆服务生成音轨。外部音轨和真实时间戳按 docs/声音接入.md 导入，不猜测字幕时间。
6. 真实素材和MG对应证据，范围说明只上屏。抽帧与播放检查后出片、双封面、四平台发布稿和微信公众号标题+Markdown文章；具体质量检查读 ../video-common/references/delivery-qa.md。

说明与脚本运行成功不等于完成新选题成片。外部服务、录音与素材由使用者提供。不得自动公开发布。

默认screen-only必须保留为简短画面注记，不写入口播/TTS；套用者当次明确调整才能覆盖。已完成向导的配置优先于提示词示例，审校顺序、上屏说明、平台及文章字段按当前配置执行。
