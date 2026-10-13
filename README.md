# 个人自媒体IP打造

把选题、事实核查、文案编写、三轮审校、配音、视频、封面和发布稿组织成一套可修改的 Agent 工作流。默认演示品牌是 **RayTalk**，你可以换成自己的账号。

适合 Codex、Claude Code 等能读文件、运行本地工具的 Agent。本仓库包含提示词、技能和制作脚本；需要 Agent 判断与执行，不是输入选题后无需配置就能运行的独立软件。

## 首次导入：通过对话逐项配置

把完整配置包放进Codex项目，首次对话可说：**“帮我初始化这套自媒体工作流，带我一项一项配置。”** 也可调用 `$personal-media-ip`；第一次相关使用都会先检查本机配置状态。

Codex先问品牌名，再依次带你选视频文风、公众号笔风、平台、字体/图形/颜色、声音、音乐、水印和所有适用高级参数。**一次只问一项**，你回答后才进入下一项。每项会说明用途与默认值；不必自己改JSON。

你可以说“保留默认”，或明确说“其余保持默认”来跳过余下逐项确认。中途关闭/换对话会从未答项继续；全部完成后保存并同步，之后使用不再重复初始化。私有进度保存在被Git忽略的 `.local/onboarding.json`。

没有回答不会自动当默认确认。音色、配乐、字体未接入时会标明待办，配置完成不等于服务已连通。密钥只在本机`.env`填写，不发在对话里。

导入/安装本身没有通用执行回调；自动引导发生在Codex首次读取项目规则或调用技能的对话中。保持完整仓库结构，仅复制一个SKILL.md不能运行向导。详细说明见[首次启动向导](docs/首次启动向导.md)。

## 默认工作流与交付

```text
“帮我做关于〔选题〕的视频”
    ├─ 时事调查 → investigation-video：真实素材、证据与动态图解
    └─ 其他讲解 → whiteboard-video：手绘白板，边画边讲

查证 → 按写作配置编写初稿
     → Humanizer-zh → stop-slop → taste-skill适用规则
     → 事实与表达复核 → 配音/字幕/画面/闪避混音 → 验收
     → 成片 + SRT + 4:3/3:4双封面
       + 抖音/哔哩哔哩/小红书/微信视频号标题与发布文案
       + 微信公众号一个标题和完整Markdown文章
```

公众号默认**辛辣锐评**：短段落、分节论证、重点加粗、事实支撑判断；只交标题与文章，不另附摘要、封面文案、配图建议或发布提示。视频默认**自然中文口播**：具体、直接、少套话。两种文风都能修改。

范围说明如“这是个案，不能代表行业”默认改为画面文字，不念出。普通事实句中的“可能”“据报道”仍按证据需要保留。公众号文章中的必要限定自然写进正文。

## 快速开始

1. 克隆或下载本仓库，放在自己选定的工作目录。不要照抄原作者盘符。
2. 安装 Python 3.10+、Node.js 20.12+、FFmpeg/FFprobe，确认它们能从命令行运行。Windows使用PowerShell与下文Python入口；原`bin/wb`是Bash，不要求在PowerShell直接执行。
3. 在Codex中启动逐项配置向导，让Agent保存你的选择；熟悉配置的用户也可手动修改根`config.json`和`workflow`。
4. 同步配置，安装白板渲染依赖：

```bash
python scripts/apply_config.py
cd skills/whiteboard-video
npm ci
cd ../..
python -m pip install pillow
```

Playwright的安装会下载Chromium；也可设置`WB_CHROMIUM_EXECUTABLE`指向现有兼容浏览器。缓存位置可以通过`PLAYWRIGHT_BROWSERS_PATH`和`npm_config_cache`按自己的磁盘规划设置。

让Agent先读根目录`AGENTS.md`完成首次逐项配置，之后说：**帮我做关于〔你的选题〕的视频**。可以直接引用`skills/personal-media-ip/SKILL.md`；若安装技能，保持各技能在同一仓库目录，避免移动后失去根配置引用。

## 所有常用可更改项：在哪里改

**根`config.json`是制作配置入口。修改后运行`python scripts/apply_config.py`。生成的白板`config.json`、调查`profile.json`及本机字体副本由Git忽略；新克隆先同步配置再运行。** `workflow/文案编写配置.json`是平台格式与字数入口。下表涉及文字规则时，同时改对应提示词，避免JSON和文字要求互相冲突。

| 可更改项 | 当前演示值 | 修改文件与字段 | 同步/额外动作 |
|---|---|---|---|
| 品牌名 | RayTalk | `config.json → brand.name` | 同步水印、片尾、调查字标；写稿时读此值，不手动在多处换名 |
| 品牌字体 | 免费小赖Xiaolai | `brand.font.family/file` | 放入有使用权的TTF/OTF；脚本复制并注册到两种渲染器；family是说明名，换字体必须同时指定真实file |
| 正文字体 | 小赖Xiaolai | `brand.bodyFont.family/file` | 可与签名字体不同；同步后重新检查行宽与排版 |
| 品牌图形 | 星芒+下划线 | `brand.graphic.type/sparkle/underline` | `sparkle`为星芒，`none`为无星芒，`logo`配透明PNG；其他图形可直接做成Logo |
| 品牌色 | `#A5B0E3` | `brand.accent` | 输入屏幕HEX；当前只是PANTONE 2113 C近似色，不是官方色彩校准 |
| 正文/墨色 | `#1E1E1E` | `brand.ink` | 白板文字与品牌墨色；调查项目也读取配置，实拍上的文字需检查对比 |
| 透明Logo | 未设置 | `brand.logo` | 路径以仓库根目录为准，例`assets/logo.png`，替代手写名 |
| 品牌口号 | 空 | `brand.slogan` | 空就不生成；不要使用示例账号口号 |
| 片尾CTA | 空 | `brand.endCard.cta` | 按账号需要写，不自动强塞关注文案 |
| 白板水印开关/位置 | 开/右上 | `brand.watermark.enabled/position` | 支持四角；改位置后检查实际内容与字幕避让 |
| 水印透明度/字号/边距 | `.72` / `36` / `56px` | `brand.watermark.opacity/size/margin` | `drawInSeconds=1.2`控制首场画入时间；传0直接出现 |
| 水印星芒/下划线 | 开/开 | `brand.graphic` | 由同步脚本写入派生`watermark.sparkle/underline`，不要同时改两处 |
| 白板片尾 | 开/5.5秒 | `brand.endCard.enabled/seconds/holdSeconds` | 最后1.5秒停留，按需要关闭或改时长 |
| 动画笔颜色 | `#F5B942` | `brand.pen.color` | 仅控制白板动画铅笔 |
| 旁白来源 | external | `tts.engine` | `volc`、`chatcut`或`external`；详见下面声音选项 |
| 音色 | 套用者自己的音色 | `tts.voiceName/customVoiceId`或`tts.voice/resourceId` | 不包含原作者私有音色ID；名称不等于API ID |
| 语速 | 1.2倍 | `tts.speed` | 火山原生语速；外部音轨保音高变速并同步时间戳，源音频应为1倍速 |
| 配乐文件/开关 | `assets/bgm.mp3` / 开 | `bgm.file/enabled` | 不附原作者音乐，导入自己的；缺文件或关闭则出无配乐 |
| 配乐音量 | 总`.5`、说话`.1`、间隙`.22` | `bgm.gain/speak/gap` | 基于真实旁白做闪避，不能仅固定音量叠加 |
| 配乐截取/过渡/淡出 | 整首、`.35s`、`3.5s` | `bgm.trim/rampSeconds/tailFadeSeconds` | `trim=[开始秒,结束秒]`；开头1.5秒淡入当前在`lib/mix-bgm.mjs` |
| 视频口播风格 | 自然、直接、具体 | `writing.videoStyle` + `workflow/文案编写提示词.md` | 同步脚本写入文案配置；文风描述优先于提示词示例 |
| 公众号风格 | 辛辣锐评 | `writing.wechatStyle` + 同上提示词公众号部分 | 可改成温和评论、专业解读等；审校保留所选文风 |
| 公众号篇幅/字段 | 1500–3000字参考，只标题/文章 | `workflow/文案编写配置.json → wechatArticle` | 需改交付范围时，同步提示词与模板 |
| 公众号Markdown格式 | 标题、分节、加粗、短段落 | `workflow/微信公众号文章模板.md` | `#`主标题、`##`分节、`**`重点、按需引用/列表；MD与TXT都保留语法 |
| 平台集合与顺序 | 抖音/B站/小红书/视频号 | `workflow/文案编写配置.json → platforms` | 同时改四平台模板；`scripts/check_publish.py`动态读取配置，不把四平台写死 |
| 标题策略 | 数字/关键词/情绪点与平台钩子 | `workflow/文案编写提示词.md`与配置`titleGeneration` | 数字有来源，标题兑现；每平台主推1个、备选1个 |
| 标题长度 | 抖音30、B站40、小红书20、视频号16 | 各平台`titleMaxChars` | 含标点，校验自动按配置；小红书`titleContainsBrand=false` |
| 视频号标题符号 | 仅书名号、引号、冒号、加号、问号、百分号、摄氏度；逗号改为空格 | 微信视频号条目的`titleAllowedSymbols`、`titleAllowedSymbolSequences`、`titleSymbolRule` | 主推/备选均检查，空格也计入16字；不允许emoji及其他特殊字符；不限制发布正文 |
| 小红书篇幅/格式 | 300–800字参考 | 对应平台`bodyCharsReference/format` | 不强制emoji，相关标签自然安排 |
| 三轮审校 | Humanizer/stop-slop/taste | `writing.reviewSkills` + `workflow/文案审校流程.md` | 若替换/关闭，需同时更新Agent入口与执行顺序，不能只改数组 |
| 只上屏的范围说明 | 开启 | `writing.scopeNotes` + 写作/审校提示词 | 这是Agent规则，不能只改JSON就以为口播自动过滤 |
| 帧率/并发 | 30fps/4路 | `render.fps/workers` | 按机器性能调并发；不同时写同一输出 |
| 场景前后停留 | `.3s` / `.7s` | `render.leadSeconds/holdSeconds` | 改后重渲染并检查字幕偏移 |
| 笔速/填充/抬笔 | 1000/9000px每秒/.12秒 | `render.pen.*` | 最短元素`.35s`、每字`.06–.2s`、跨段`.35`、移动上限`1.6s`、填充上限`1.2s` |
| 字幕开关/字号/位置 | 开/46/基线1022 | `captions.enabled/fontSize/baselineY/safeTop` | 每条6–20字，提前`.08s`、延后`.25s`，按实际音频对齐 |
| 双封面比例/标签/边框 | 4:3+3:4 | `cover.ratios/seriesTag/frame/frameColor` | 默认1440×1080和1080×1440，分别排版，字标后期合成 |
| 工程与成片位置 | `workspace` | `dirs.projects/build/investigation` | 支持相对路径/自选绝对路径；生成物被Git忽略 |
| 每期事实、口播、镜头 | 当期内容 | 白板`scenes.js`；调查工程的权威稿/镜头表 | 不是根配置项；改稿须重新审校、更新对应音频及字幕 |

**画幅注意：** 白板内核目前采用1920×1080固定坐标，不提供一个JSON开关就变竖屏。竖屏需修改`lib/render.html`、`lib/render.js`、`lib/scene-dsl.js`及场景坐标、安全区。调查片在新Remotion工程的`Composition`里改`width/height`并重新排版；时长由当期旁白和内容决定，不强制十分钟。

## 旁白可以选火山、ChatCut或其他克隆音色

### 火山引擎官方/复刻音色

1. 将根目录`.env.example`复制为`.env`，填自己的凭证。切换`config.json → tts.engine="volc"`。
2. 在`tts.voice`填音色ID，或留空从`.env`的`VOLC_TTS_VOICE`读取。
3. 官方2.0音色使用`VOLC_TTS_RESOURCE_ID=seed-tts-2.0`；`S_`开头的声音复刻音色使用`volc.megatts.default`，以实际账户资源权限为准。`tts.resourceId`非空时覆盖环境变量。
4. 白板用`python scripts/wb.py tts <期目录>`；调查/独立旁白可用`node scripts/synthesize_text.mjs narration.txt output.wav`，会另存真实逐字时间戳JSON。

不要把`.env`提交到GitHub。本仓库没有内置可用凭证，不能声称已验证套用者账户的在线合成。

### ChatCut Desktop 自己的数字人/克隆音色

切换`tts.engine="chatcut"`，连接**你电脑上的**ChatCut Desktop MCP。注册名可用`chatcut_desktop`，可执行文件使用自己ChatCut提供的命令，不复制原作者路径。

通过真实`get_active_project`请求验证连接，再查询自己的`manage_voice`列表、选择ready音色并apply。把显示名称和返回的真实音色ID填入自己的配置；通过`submit_voice`生成旁白，导出音轨与真实转写时间。配音生成通常使用账户额度，具体权限由你的ChatCut账户决定。

该路径是Agent与自己的MCP连接，不是Python脚本自动登录原作者账户。本仓库不包含私有音色、MCP会话文件或服务端令牌。

### 其他数字人或声音克隆服务

切换`tts.engine="external"`。使用你自己的服务生成旁白并取得实际词级时间戳；没有时间戳时，先对实际音频转写和核对。

按[声音接入说明](docs/声音接入.md)整理清单，然后执行：

```bash
python scripts/import_narration.py --project "workspace/whiteboard/episodes/日期 题名" --manifest "workspace/narration-manifest.json"
python scripts/wb.py build "workspace/whiteboard/episodes/日期 题名"
```

这条导入通道不限定服务商，但不是每家服务的直接API插件。Agent负责生成/导出音轨，导入器负责核实文字和时间，并转换成渲染器需要的格式。缺音频、缺实测时间或稿件不匹配时停止，不自动换音色。

## 制作命令

```bash
python scripts/wb.py new "为什么计划总是坚持不下去"
# Agent修改新期scenes.js，查证、写稿并三轮审校后：
python scripts/wb.py scenes "workspace/whiteboard/episodes/日期 题名"
python scripts/wb.py stills "workspace/whiteboard/episodes/日期 题名"
# 火山先tts；外部音色先按上文导入
python scripts/wb.py build "workspace/whiteboard/episodes/日期 题名"
python scripts/check_publish.py "workspace/当期/四平台发布文案.md"
python scripts/brand_stamp.py cover.png cover-branded.png
```

调查模式需要按选题在`workspace/investigation`建立工程：复制`skills/investigation-video/template/remotion`作起点，安装其固定依赖（Remotion 4.0.508/React 19.2.8），替换演示时间轴与素材。演示只展示品牌/图解，不代表某项真实调查，不能循环样片拼成长片。调用`apply_config.py`生成的品牌配置和字体应随新工程一起复制。

`scripts/check_publish.py`只做结构、平台和标题长度检查，不能证明文案自然或事实真实。三轮审校由Agent阅读技能实际执行；记录真实改动，不以评分或字数减少代替检查。

## 联系方式与使用范围

- 邮箱：[hanshinei7@gmail.com](mailto:hanshinei7@gmail.com)
- 微信：`mokusei275`

**本项目仅供学习交流。未经本人许可，禁止转载或商用。** 需要转载、商业使用或合作，请通过以上方式联系Ray取得许可。

这项限制适用于本项目的原创配置、提示词适配、工作流编排、文档和新增代码；第三方开源组件继续遵循各自原许可证，见[THIRD_PARTY.md](THIRD_PARTY.md)。不能以本项目的限制替换其已有开源权利。此前已发布版本的许可按该版本文件保留，本说明不追溯撤销旧版已授予的权利。

## 来源、许可与验证范围

制作工具基于[trustfuture/simon-skills](https://github.com/trustfuture/simon-skills)，三轮审校技能与字体许可见[THIRD_PARTY.md](THIRD_PARTY.md)。可选`dbs-xhs-title`不随包分发，需另装并注意其非商业许可；标题可以只用本仓库的原生策略。

本版本原创配置、工作流、新增脚本和项目文档仅供学习交流，未经Ray许可禁止转载或商用，具体见根LICENSE。配乐、Logo、音色、新闻素材与第三方字体各自遵循其许可。默认不公开分发原作者BGM和私人文章。

发布前进行配置同步、字体/品牌渲染、外部音轨导入、闪避混音和四平台限制的离线检查。没有在线验证别人的火山凭证、ChatCut音色权限或任意第三方服务，也不保证自动出片或通过平台审核。生产成片必须逐期核验实际音画、来源、双封面及交付文件。
