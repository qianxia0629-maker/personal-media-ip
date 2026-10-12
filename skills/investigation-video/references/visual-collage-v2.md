# 视觉升级 v2：已认可的质感样片

2026-09-09，用户明确纠正本轮目标：“内容当然是值得学习的，但我要你学的是画面和质感。”随后要求优化一轮并交付 30 秒样例，观看后回复“OK，更新SKILL”。本次认可适用于该样片的视觉方向，不代表认可前一轮内容改写方案，也不要求后续选题照搬蛋糕、金额或三段布局。

后续长片的素材数量与实拍占比须另按 [长片制作流程](long-form-workflow.md) 核查。此处生成蛋糕仅说明通用概念物件的做法，不覆盖真实品牌产品优先用真实抠图的要求。

## 先看资产

- 原始 30 秒成片、拼板、检查记录与指纹未随开源仓库附带；公开样片见 [assets/sample-preview.mp4](../assets/sample-preview.mp4)。
- `assets/reference-project-v2/`：与成片对应的最小 Remotion 工程。

对标：https://www.douyin.com/video/7681566244243344666 ，黑白夜谈《一口气看懂比特币》。当次对标分析只做章节与代表画面抽查，未完成原片连续听审、逐镜计时或全量下载。不要将推测的动画速度、视差、音乐表现写成已验证事实。复现自身样片的动作可直接查看工程。

## 学习的视觉方法

核心是**真实材质＋前后景分离＋统一拼贴处理**。物件保留清晰纹理，背景交代环境并适度虚化；前景放大、局部出画和遮挡形成纵深。白描边、轻投影与略不规则边缘让来自不同来源的元素协调。胶带、纸片、网格是局部表现手段，颗粒、浮尘、暗角只做轻量统一，不用于掩盖低清素材。

在镜头里让主体占据明确空间，避免所有东西都完整、等大地装进规整卡片。报价或短信息可以错落排放，证据可以作为有边缘与阴影的摄影纸片；数据须继续保持可读和准确。借鉴真实影像、抠图拼贴、图解之间的变化，不把整条长片做成持续漂浮的静帧。

| 样片区间 | 实际做法 | 复用价值 |
|---|---|---|
| 0–5.13 秒 | 6 秒原报道视频作为虚化背景，前景蛋糕带白描边和投影；100、90、80 报价逐项滑入并保持，最后一条为信号绿 | 真实物件与动态背景形成层次；同类信息通过小角度错落避免机械排列 |
| 5.13–14.23 秒 | 原报道截图放在浅灰画面，白纸边缘、胶带与投影；绿色划线；蛋糕移到右下角 | 证据承担信息，装饰退后；跨镜重复主体建立视觉联系 |
| 14.23–30 秒 | 蛋糕移到左侧，上方比例条按 50.4／121.9／80 分段；分账信息按音轨出现，最后保留等式与配送说明 | 同一主体贯穿，MG 继续解释实际金额；明暗镜头变化保持品牌一致 |

跨镜是切镜与重新构图，不能把这个示例说成已实现连续三维运镜。物件轻微位移、背景缩放与帧驱动纹理由工程控制；不是三维物体转动。

## 工程中的可调整起点

以 1920×1080、30fps 为例：蛋糕使用透明 PNG，约 4px 四向 `drop-shadow` 模拟白描边，后接柔投影；纸片小角度旋转约 −4°～3°，用轻微不规则 polygon 边缘。背景模糊约 23px，主体保持清晰；明暗、饱和度须按素材调整。短入场约 13–23 帧，之后保持文字稳定。以上是本例参数，不能未经观看就应用到所有素材与画幅。

新主题选择相应主体物件；证据、数值和 Logo 不用生成图替代。当前账号品牌仍从配置读取，包内占位值为 SignPainter 手写签名＋星芒＋底划和 #10C46F。保留原旁白、字幕时间戳及句序，视觉调整不触发重配音。

## 复现

把 `template/remotion/` 与 `assets/BrandStamp.jsx` 一起复制到新的工作目录，保持工程对 `../../assets/BrandStamp.jsx` 的引用。`public` 必须是实际文件，不能链接到外部素材目录。

```sh
# 在复制后的 reference-project-v2 目录内
npm install
npm run still -- frame.png --frame=825 --scale=0.6
npm run render
```

依赖固定为 Remotion 4.0.508、React 19.2.8；若复用本机既有 node_modules，先核实版本。需要 macOS SignPainter 字体，Noto Sans SC 随示例保存；不能无声回退到普通字体。包内未复制 node_modules、系统字体、缓存或密钥。

## 素材与事实范围

本例仍是《幽灵外卖》原节选，不是比特币新片。继续使用原 30 秒音轨、时间戳和案例金额：252.3 = 50.4 + 121.9 + 80；80 − 3.2 = 76.8，76.8 包含配送费用，不能表述为利润。

- 央视画面：https://tv.cctv.com/2026/04/18/VIDEvJ82PBHiJ3O8Z6u5zDYV260418.shtml
- 新华社口径：https://www.news.cn/20260417/1db3d428b5024488a51bd20221508c29/c.html
- 原视频和截图为 480×270，放大不能增加细节；未来优先补高清证据。
- 蛋糕由内置 imagegen 生成，透明 PNG，片内已标注“AI 概念示意，非涉事实物”。它展示的是通用物件的材质，不是假造案件证物。

生成提示词：

> Create one photorealistic isolated strawberry cream birthday cake cutout asset for a documentary motion collage. Genuine transparent background with alpha. Three quarter view slightly from above, entire round cake and thin silver cake board visible, generous transparent margins. White whipped cream with realistic tiny ridges, six fresh red strawberries on top, delicate green leaves, natural imperfect bakery texture, no candles, no text, no brand, no decoration outside cake, no scene, no plate under board. Soft directional natural light from upper left, crisp detailed edges, realistic food photography, not CGI. Square 1024x1024. This is a generic conceptual food object, not evidence of any real case.

提示词要求尺寸不等于生成结果实测尺寸；使用实际文件尺寸。复用该资产无需再次生成。

## 已完成检查与局限

视频 900 帧／30fps，画面时长 30 秒；含 AAC 尾部封装的容器时长约 30.059 秒。全片解码通过；未检出设置阈值内的黑段；音轨为 48kHz 双声道，mean_volume −19.5dB、max_volume −2.0dB，这两项不是 LUFS 或真峰值测量。

关键帧已检查字标、描边、字幕与布局，修正蛋糕碰文字和白色金额落在奶油背景上的问题。未完成全片逐秒人工听审；用户认可视觉方向不改变这个检查范围。长片需要更多匹配素材和镜头变化，不能循环本例扩展。
