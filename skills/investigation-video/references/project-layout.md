# 项目文件夹结构（2026-09-14 定版）

一期一个工程目录加一个知识库目录。工程只放后台工序、大文件与冻结交付；正文、来源、文案、封面、复盘只在知识库维护，工程里用软链接指过去。新项目复制上一期工程后按此清理。

## 工程目录 `projects/<YYYY-MM-DD>-<slug>/`

```
README.md                       状态、路径、工序一句话说明；每次改版更新
work/
  research/
    capture.cjs                 来源页面全页截图 + 正文文本（Playwright）
    crops.cjs                   按关键词定位裁证据图
    pages/<id>.png|.txt         全页截图与 innerText，一来源一对
    crops/<id>.png              证据裁图原始（含站点侧栏，进 assets 前再裁）
    media/<src>.mp4             下载的原片；同名 -sheet.jpg / -dense.jpg 为带时间码拼板
    media/probe.txt             各源分辨率与时长
    screen/                     本片录屏（Playwright recordVideo）与其拼板
  production/
    sentences.json              由知识库口播稿正则生成，id sNNN / sNNNa
    tts-s20.mjs                 火山合成，speech_rate=20；跳过已存在句
    audio-s20/<id>.wav|.json    单句音频与元数据（json 含 words 逐字时间戳）
    audio-manifest-s20.json     全部句子的时长与 words
    preview-*.mp3               无停顿拼接试听
    asr/ asr.py                 仅回退用（旧音频无 words 时）
    subtitles-volc.py           字幕对齐（skill scripts 复制来）
    design.py                   分镜：SRC 源表 → shots/cuts → timeline.json + 裁切
    clips.json                  裁切清单（源、起点、帧数）
    renderer/
      index.jsx                 Remotion 组合，卡片 kind 在此定义
      BrandStamp.jsx            字标组件（skill assets 复制来）
      render.mjs                stills <frames…> / video
      timeline.json subtitles.json
      public/narration.wav      loudnorm 后旁白
      public/NotoSansSC-*.woff2
      public/assets/c*.mp4 ev-*.png   裁切片段与证据图（改镜头表后整目录清空重切）
      node_modules -> 已有依赖目录的软链（public 内不可用软链）
    stills/ stills-sheet-*.jpg  每镜头抽帧与拼板
    renders/
      ctrip-v2.mp4              Remotion 直出（无配乐）
      <题名>-完整v2.mp4 .srt     混配乐后的交付成片与字幕；旧版本保留
    mix-bgm.sh qa.py            配乐闪避混音、机器验收
    *.log                       每道工序独立日志
  covers/
    gen-cover-v2.mjs            codex imagegen，提示词右上角留净空不画签名
    cover-<ratio>-raw2.png      生图原图
    crop-<ratio>.png            裁到 1024×1365 / 1365×1024（按标题位置决定裁切起点）
    封面-<ratio>.png            brand-stamp.py 盖固定字标后的成品
outputs/
  <题名>-完整交付v<N>/          只由 assets/finalize-outputs.py 生成，不手工建。固定内容：
    <题名>-完整v<N>.mp4 .srt    实体拷贝（不是软链，Finder 可直接播放/拖走）
    素材使用区间-v<N>.json       实体拷贝
    口播稿-v<M>.md 事实与来源-v<M>.md 素材覆盖-v<M>.md
    素材与剪辑记录-v<N>.md 制作与检查-v<N>.md 发布包-v<M>/   软链到知识库 材料/
    gzh -> 材料/公众号图文-v<M>/  仅当已做公众号图文
  （不再有 draft-v1；草稿阶段文档只在知识库 材料/ 里）
```

## 知识库目录 `knowledge/<YYYY-MM-DD> <题名>/`

```
<题名>.md                       本期入口：frontmatter status、标题、叙事类型、事件摘要、成片路径、嵌入各文档、待办
材料/
  口播稿-v1.md                  稿头带叙事自检与版本说明；改句只加后缀不重排
  事实与来源-v1.md              S 编号来源台账，制作阶段补核追加章节
  素材覆盖-v1.md                逐句主视觉/证据/MG/缺口
  素材与剪辑记录-v<N>.md        真实动态秒数与占比、去重源、源清单
  制作与检查-v<N>.md            参数、已做检查、未做与需人工判断
  <题名>-完整v<N>.srt
  发布包-v1/
    八平台发布文案-v1.md
    封面-3x4.png 封面-4x3.png
```

另有 `选题/<YYYY-MM-DD> 热点选题候选.md` 存每日候选，`<账号名>.md` 为账号索引，每期收尾同轮更新。

## 版本规则

- 稿件、来源、覆盖按内容改动升版；成片、剪辑记录、检查随每次整片重渲染升版；发布包只在标题或封面变动时升版。
- 旧版本文件不删；`outputs/` 每个交付版本独立目录，且每个目录都用 `assets/finalize-outputs.py <工程> <知识库期目录> <题名> <N>` 生成，保证每期文件名、实体/软链规则一致。2026-09-15 前的四期 outputs 有实体与软链混用、多出 draft-v1 的情况，以本规则为准，不回改旧期。
- README 与知识库入口 status 必须指向当前可播放成片。
