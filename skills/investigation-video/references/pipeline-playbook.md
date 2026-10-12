# 长片制作管线手册（2026-09-14 携程定制游房价一期沉淀）

从选题到交付的实际可复用工序。路径以本机为准；新项目先复制上一期工程再改，不从零搭。参考工程：`projects/2026-09-14-ctrip-custom-tour/`（规则题、竖屏原片内嵌、四类新图解卡）与 `2026-09-13-liuxiang-buyout/`（账目题）。

## 0. 目录与知识库

完整目录树与版本规则见 [项目文件夹结构](project-layout.md)。

- 工程放 `projects/<date>-<slug>/`，下设 `work/research`（pages/ crops/ media/ screen/）、`work/production`、`work/covers`、`outputs/<题名>-完整交付v<N>/`。outputs 只由 `assets/finalize-outputs.py` 生成：成片、字幕、素材使用区间为实体拷贝，五份文档与发布包软链到知识库。
- 正文、来源、覆盖、剪辑记录、检查、发布包只在知识库 `knowledge/<date> <题名>/材料/` 维护；工程 outputs 里放软链。收尾同轮更新本期入口、`<账号名>.md` 索引、账号 README。

## 1. 选题：热榜抓取

- 直接可用：百度 `top.baidu.com/board?tab=realtime`（grep `"word"`）、头条 `www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc`、知乎 `api.zhihu.com/topstory/hot-list?limit=50`、B站 `api.bilibili.com/x/web-interface/wbi/search/square?limit=30`、36氪 `gateway.36kr.com/api/mis/nav/home/nav/rank/hot`（POST）。
- 微博、抖音接口 curl 直接失败；微博用内置浏览器打开 `m.weibo.cn/search?containerid=100103type%3D1%26q%3D<话题>` 可读到帖子和视频时长。
- 候选文件按 [叙事模式](narrative-modes.md) 标问题类型，写明上两期类型；存一份到知识库 `选题/`。

## 2. 稿件与配音

- 稿头写叙事自检（类型、上两期、黑名单、去金额测试、MG 形态、结尾回应）。句子编号 `sNNN`，插句用 `sNNNa`，不重排已配音句。
- `sentences.json` 由稿件正则生成；TTS 复制上一期 `tts-s20.mjs`：刘飞音色、`VOLC_TTS_SPEED=20`，产出 `audio-s20/` 与 `audio-manifest-s20.json`。改动句子时只删对应 wav/json 重跑，脚本会跳过已存在文件。
- 试听用无停顿拼接 mp3 发给用户。时长门槛按 1.2 倍速算：约 0.156 秒/字，10 分钟正文需 3800 字以上。

## 3. 事实核查与证据

- 页面全页截图与正文：`capture.cjs`（Playwright，`本机 playwright`，channel chrome）。gov.cn 旧链接常回门户页，法条改用文旅部政务公开（旅游法）、国家信访局法规库（消保法）；电商法未找到可截图政府页，用条文卡并在来源台账写明。
- 证据裁图：`crops.cjs` 用 TreeWalker 找含关键词的文本节点，滚到该位置后 clip 截图；再用 ffmpeg crop 去掉站点侧栏。腾讯、新浪页面正文列约在 2x 截图的 x 80–1640。
- 每条报道数字标"据报道"；原片到手后逐句核对稿件用词（本期纠正过"超豪华型"误读与整改公告条数）。

## 4. 素材

- YouTube：`yt-dlp ytsearch8:<词> --flat-playlist --print ...` 搜，`-f "bv*[height<=1080]+ba/b"` 下载。B站 search 接口 412，暂不可用。
- 微博原视频：内置浏览器找到 `m.weibo.cn/status/<id>`，`yt-dlp -f b` 可直接下 1080p。都市报道等地方台原片多为竖屏。
- 网页录屏：Playwright `recordVideo` 1920×1080 慢滚，webm 直接可用；携程定制旅行网页版 404，只能录旅游频道列表页并角标"本片录屏"。
- 每个源先出带时间码拼板（`fps=1/N,tile=6x8,drawtext pts`）再绑定；季节、人像、原片自带大字卡都在拼板阶段筛掉。

## 5. 分镜与裁切（design.py）

- `SRC` 每源记 file/label/zoom/ay；竖屏源加 `portrait=True`，裁切用 `crop=1080:1000:0:440`（去顶部标题条与底部字幕，保留身份条），`scale=-2:1080` 内嵌在同源 `boxblur=24:2,eq=brightness=-0.18:saturation=0.8` 底上。具体 y 值按原片实测，先抽帧确认。
- **裁切文件按序号命名会在镜头表变动后被同名复用，导致画面与标注错位。** 改动镜头表后必须 `rm renderer/public/assets/c*.mp4` 全部重切；或改为按 `src+ss+frames` 哈希命名。
- 图解形态由问题类型决定：五价并列 `prices`、责任链 `chain`、条文 `law`、四栏 `four`、时间线 `timeline`、并列 `split`、数字 `stat`；分账条 `ratio` 只用于确有资金流向的支线。条文和列表优先做成实拍叠字（`film(..., text=[...])`），用户明确要求过。
- 每镜头抽帧（0.6–0.7 处）拼板两轮复核，再整片渲染；渲染前先 `render.mjs stills` 三帧确认资源无 404。

## 6. 字幕、渲染、混音、验收

- **字幕时间戳直接来自火山**：`scripts/tts.mjs` 已在 `audio_params` 同时开 `enable_timestamp`（1.0 音色）与 `enable_subtitle`（2.0 音色，刘飞属此类），每句 json 的 `words` 为逐字 `{word,startTime,endTime}`，按原文打轴，1.2 倍速下准确。用 skill `scripts/subtitles-volc.py`（复制到工程）对齐：有 words 的句子直接用，没有的回退 whisper。2026-09-14 之前合成的音频没有 words，需要重合成或走 whisper。
- whisper 只作回退：`python3` asr.py`（Homebrew Python 升级会丢 mlx_whisper，venv 用 `/opt/homebrew/bin/python3.13` 建）。数字密集句编辑率 0.5 左右可接受，字符校验必须通过。
- 旁白：句音频直接 concat（不插停顿），`loudnorm=I=-16:TP=-1.5:LRA=11` 后放 `renderer/public/narration.wav`。
- 渲染：复制上一期 `renderer/`（index.jsx、SimonTalkBrand.jsx、render.mjs、public 字体），`node_modules` 软链到已有依赖目录（public 内不可用软链）。整片约 40 分钟，后台跑并用 until-grep 等 `RENDER_DONE`。
- 配乐必混：`mix-bgm.sh`，`assets/bgm.mp3`（自备无版权配乐） 0–97s 循环、volume 0.22、sidechaincompress threshold 0.02/ratio 6/attack 20/release 350，视频流 copy。验收电平：说话段约 -47 dB、句间隙 -33 至 -42 dB，整体约 -15.5 LUFS。
- `qa.py`：帧数对 timeline、解码无错、无黑帧、AAC 48k。再从成片抽 9 帧看 Logo、字幕、角标、CTA。

## 7. 封面与发布包

- `work/covers/gen-cover-v2.mjs` 走 codex imagegen，两比例分别生成后中心裁到 1024×1365 与 1365×1024。提示词写明真实物件道具、最粗字重、无品牌 Logo、**右上角留净空且不画签名**；生成约 5 分钟，可与渲染并行。
- 裁好后用 skill `assets/brand-stamp.py` 盖固定字标（右上角、22% 宽），规则见 [封面与发布](covers-and-publishing.md#字标固定合成2026-09-14-起)。
- 八平台文案一份 md：抖音、快手、B站、视频号、小红书、微博、公众号、YouTube，各含主推/备选标题、正文、话题、置顶评论，末尾共用免责段；CTA 与本期问题类型呼应。
- 交付文档五份：口播稿、事实与来源、素材覆盖、素材与剪辑记录（含真实动态秒数与占比、去重源、片段数）、制作与检查（参数、已做检查、未做与需人工判断）。版本号随改动递增，旧版本保留。
- 收尾最后一步固定跑一个打包脚本（作者私有的 `finalize-outputs.py`，未随仓库附带；目录结构见 [project-layout.md](project-layout.md) 的 `outputs/`，可按其自行实现），缺任何一份文档它应报错而不是生成半套目录；跑完再更新 README、知识库入口、账号索引。
