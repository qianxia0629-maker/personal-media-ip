---
name: whiteboard-video
description: 手绘白板讲解视频制作，按本仓库品牌、文案审校和声音配置输出成片。
---

# 白板讲解视频

首次使用本配置包先进入同级 personal-media-ip 的逐项对话配置向导。未完成本机配置时先提问和保存进度；完成后再执行下面的制作步骤。


先读根目录 AGENTS.md、config.json 和 workflow 中的文案规则。使用者的品牌/声音/文体覆盖任何上游参考的占位账号与路径。

先按审校后的scenes.js生成场景，字幕区y≥960、右上水印区保持净空。用根目录 scripts/wb.py 执行命令。技能配置由根config同步；完整出片前需真实旁白音轨与对齐JSON。参考 references/dsl.md、scene-patterns.md 和 stickers.md。

新稿必须先经Humanizer-zh、stop-slop、taste-skill适用部分与事实复核，再配音/字幕/制作。读同级 ../video-common/references/fact-check.md、delivery-qa.md，按需要读compliance.md。四平台+微信公众号独立文章及双封面交付；仅完成实际检查后称已交付，不自动发布。
