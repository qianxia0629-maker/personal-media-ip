---
name: personal-media-ip
description: 制作可定制品牌的个人自媒体视频与公众号文章；用户要求做关于某个选题的视频或套用本仓库IP工作流时使用。
---

# 个人自媒体IP打造

本仓库为 Agent 读取执行的工作流与本地制作工具集合，根目录从本文件上两级定位；不依赖原作者机器。

1. 读根目录 config.json、workflow/文案编写配置.json 与 AGENTS.md。先用 scripts/apply_config.py 同步配置。
2. 时事调查读 ../investigation-video/SKILL.md，讲解读 ../whiteboard-video/SKILL.md。保持品牌与声音选择，不把调查片做成固定白板。
3. 查证后用 workflow/文案编写提示词.md 写初稿，再依次读 ../humanizer-zh/SKILL.md、../stop-slop/SKILL.md、../taste-skill/SKILL.md 完成审校；设计规则只取适用于文本/视觉的部分。核对事实、观点、限定与衔接后再配音。审校记录保存在当期workspace。
4. 按config.tts.engine选择：volc走原生火山；chatcut由使用者连接自己的Desktop MCP并查询/apply自己的音色；external使用其他数字人/克隆服务生成音轨。外部音轨和真实时间戳按 docs/声音接入.md 导入，不猜测字幕时间。
5. 真实素材和MG对应证据，范围说明只上屏。抽帧与播放检查后出片、双封面、四平台发布稿和微信公众号标题+Markdown文章；具体质量检查读 ../video-common/references/delivery-qa.md。

说明与脚本运行成功不等于完成新选题成片。外部服务、录音与素材由使用者提供。不得自动公开发布。
