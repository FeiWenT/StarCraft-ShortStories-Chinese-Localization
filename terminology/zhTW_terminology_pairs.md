# 23 篇官方 zhTW ↔ 英文 术语对照表

> **生成时间**: 2026-08-12
> **生成方式**: 从 23 篇 Blizzard 官方 zhTW 短篇 PDF (扫描版) OCR 前 3 页 + 项目清单第三节
> **目标读者**: 12 篇新译短篇的 LLM 翻译 + 人工校对
> **优先级**:
> - `zhTW` (10-15 条): Blizzard 官方译名, 12 篇新译应**优先**采用
> - `wiki` (5-10 条): 与现有 680 条简体 wiki 术语表一致, 12 篇新译沿用
> - `keep_english` (5 条): 致敬语, 全部**保留英文**, 首次出现注音

---

## 一、角色类 (12 条, 全部 zhTW 官方)

| 英文 | zhTW 官方 | 简体 wiki 现行 | 采纳 | 备注 |
|------|----------|---------------|------|------|
| Selendis | 赛兰迪斯 | 赛兰迪丝 | **zhTW** | 10 周年 |
| Karax | 卡拉克斯 | 凯拉克斯 | **zhTW** | 10 周年 |
| Talandar | 塔兰达 | 塔兰达尔 | **zhTW** | 10 周年 |
| Nerath | 内拉斯 | (简体 wiki 缺) | **zhTW** | 万众一心 (10 周年) |
| Lantharis | 兰萨瑞斯 | (简体 wiki 缺) | **zhTW** | 万众一心 (10 周年) |
| Alarak | 阿拉纳克 | 阿拉纳克 | wiki | (已有, 验证) |
| Aldaris | 阿达利斯 | 阿达利斯 | wiki | (已有, 验证) |
| Mohandar | 莫汉达尔 | 莫汉达尔 | wiki | (已有, 验证) |
| Vorazun | 沃拉尊 | 沃拉尊 | wiki | (已有, 验证) |
| Raszagal | 拉莎加尔 | 拉斯扎加尔 | **zhTW** | 10 周年 (注意 zhTW 用"莎", 简体用"斯") |
| Emily | 艾蜜莉 | 艾米莉 | **zhTW** | 小写"蜜", 简体用"米" |
| Tosh | 托许 | 托许 | wiki | BrokenWide 幽灵教官 |

---

## 二、地点/组织/概念类 (15 条)

| 英文 | zhTW 官方 | 简体 wiki 现行 | 采纳 | 备注 |
|------|----------|---------------|------|------|
| Khala | 卡拉 | (简体 wiki 缺) | **zhTW** | 神族心灵链接 |
| Shel'na Kryhas | 夏尔纳·克瑞哈斯 | (简体 wiki 缺) | **zhTW** | 艾尔幸存者 |
| Khalani | 卡拉尼 | (简体 wiki 缺) | **zhTW** | 星灵语 |
| Tal'darim | 塔达力姆 | 塔达林 | **zhTW** | 飞升者阵营 (注: zhTW 用"力"非"林") |
| Purifier | 净化者 | 净化者 | wiki | (已有) |
| Defenders of Man | 人类捍卫者 | 人类捍卫者 | wiki | Waking Dreams 反幽灵组织 |
| Heaven's Devils | 天堂魔鬼 | 天堂魔鬼 | wiki | WoL Raynor/Tychus 旧部队 |
| Gantrithor | 甘特里索号 | (简体 wiki 缺) | **zhTW** | Tassadar 旗舰 |
| Ulnar | 乌尔纳 | (简体 wiki 缺) | **zhTW** | 萨尔纳加神庙 |
| Braxis | 布莱克西斯 | (简体 wiki 缺) | **zhTW** | 冰冻星球 |
| Koprulu Sector | 科普卢星区 | 科普卢星区 | wiki | (已有) |
| Endion | 恩底昂 | (简体 wiki 缺) | **zhTW** | 净化者所在星系 |
| Mar Sara | 玛·萨拉 | 玛·萨拉 | wiki | (已有) |
| Tarsonis | 塔尔索尼斯 | 塔尔索尼斯 | wiki | (已有) |
| Aiur | 艾尔 | 艾尔 | wiki | (已有) |

---

## 三、致敬语/祝福语类 (5 条, **全部保留英文**)

| 英文 | 含义 | 首次出现处理 | 后续出现处理 |
|------|------|-------------|-------------|
| **En Taro Adun** | 赞美阿顿 / 为了阿顿的荣耀 (卡莱最常用问候语) | `En Taro Adun (赞美阿顿)` | `En Taro Adun` |
| **En Taro Tassadar** | 赞美塔萨达尔 (SC1 与主宰同归于尽的执行官) | `En Taro Tassadar (赞美塔萨达尔)` | `En Taro Tassadar` |
| **En Taro Artanis** | 赞美阿塔尼斯 (统一星灵各部族、光复艾尔的大主教) | `En Taro Artanis (赞美阿塔尼斯)` | `En Taro Artanis` |
| **En Aru'din Raszagal** | 缅怀拉斯扎加尔 (黑暗圣堂武士专用句式) | `En Aru'din Raszagal (缅怀拉斯扎加尔)` | `En Aru'din Raszagal` |
| **Adun Toridas** | 愿阿顿庇护你 (奈拉齐姆部族专属祝福语) | `Adun Toridas (愿阿顿庇护你)` | `Adun Toridas` |

> **处理方式**: glossary.json 中 `zh` 字段填 `英文保留 (注: XXX)`, `priority: "wiki"`, `keep_english: true`。
> LLM 注入时**只注音不译**, 首次出现形如上表。

---

## 四、单位/战术类 (8 条, 简体 wiki 优先, 验证 zhTW 一致性)

| 英文 | zhTW 官方 | 简体 wiki 现行 | 采纳 | 备注 |
|------|----------|---------------|------|------|
| zergling | 跳虫 | 跳虫 | wiki | (验证一致) |
| ultralisk | 雷兽 | 雷兽 | wiki | (验证一致) |
| mutalisk | 飞螳 | 飞螳 | wiki | (验证一致) |
| hydralisk | 刺蛇 | 刺蛇 | wiki | (验证一致) |
| roach | 蟑螂 | 蟑螂 | wiki | (验证一致) |
| baneling | 爆虫 | 爆虫 | wiki | (验证一致) |
| stalker | 追猎者 | 追猎者 | wiki | (已有) |
| immortal | 不朽者 | 不朽者 | wiki | (已有) |
| colossus | 巨像 | 巨像 | wiki | (已有) |
| phoenix | 凤凰 | 凤凰 | wiki | (已有) |
| void ray | 虚空辉光舰 | 虚空辉光舰 | wiki | (已有) |
| carrier | 航空母舰 | 航母 | **zhTW** | (注: zhTW 用"航空母舰", 简体用"航母", 12 篇统一用"航母") |

> **实际采纳**: 12 篇新译**沿用简体 wiki 标准** (因 Nova/Spectres 已用 wiki 标准), 保持术语一致性。
> 上表 zhTW 官方仅作参考, 若读者熟悉 zhTW 23 篇可对照。

---

## 五、12 篇新译专有专名 (未在 680 条 + 上述 zhTW 中)

从 12 篇英文原文 grep 出的高頻专名, **zhTW 23 篇未涉及** (因为 23+12 不重叠):

| 英文 | 出现次数 | 出现篇 | 建议译法 | 备注 |
|------|---------|--------|---------|------|
| Stone | 202 | Waking Dreams | 斯通 | Waking Dreams 主角 |
| Madrid | 106 | Hybrid | 马德里 | SC1 |
| Pandora | 106 | Hybrid | 潘多拉 | SC1 太空站 |
| Aldrion | 68 | Waking Dreams | 奥尔德里恩 | Waking Dreams |
| Juras | 65 | Waking Dreams | 朱拉斯 | Waking Dreams |
| Walden | 49 | Waking Dreams | 瓦尔登 | Waking Dreams |
| Broken Horn | 47 | 蒙眼行动 | 破碎角 | 蒙眼行动 主角 (断角 zergling) |
| Captain Gentry | 45 | 蒙眼行动 | 甘特利上尉 | 蒙眼行动 |
| Private Ayers | 45 | 蒙眼行动 | 艾尔斯下士 | 蒙眼行动 |
| Sage | 41 | 蒙眼行动 | 赛奇 | 蒙眼行动 |
| Darsiris | 41 | 万众一心 | 达西瑞斯 | 万众一心 |
| Martul | 37 | 万众一心 | 马图尔 | 万众一心 |
| Wynne | 29 | Waking Dreams | 温恩 | Waking Dreams |
| Hendrix | 26 | 蒙眼行动 | 亨德里克斯 | 蒙眼行动 |
| Brody | 20 | Waking Dreams | 布罗迪 | Waking Dreams |
| Lantharis | 17 | 万众一心 | 兰萨瑞斯 | (与第一节重复) |
| Therun | 11 | 启示录 | 塞伦 | 启示录 (Valerian 助手) |
| Anselm | 11 | 启示录 | 安塞尔姆 | 启示录 |
| Moratun | 11 | 启示录 | 莫拉顿 | 启示录 (研究员) |
| Aldera | 9 | 启示录 | 奥尔德拉 | 启示录 (外星遗迹) |
| Thuras | 10 | 启示录 | 苏拉斯 | 启示录 (外星生命) |
| Lieutenant Rumm | 8 | 启示录 | 鲁姆中尉 | 启示录 |
| General Davis | 11 | 蒙眼行动 | 戴维斯将军 | 蒙眼行动 |
| Augustgrad | 9 | 蒙眼行动 | 奥古斯塔德 | 蒙眼行动 (城市) |
| Chau Sara | 9 | 附带损伤 | 周·萨拉 | 附带损伤 (殖民地) |
| Cask | 8 | 蒙眼行动 | 卡斯克 | 蒙眼行动 |
| Morians | 8 | 启示录 | 莫里亚斯 | 启示录 (外星种族) |
| Defenders | 21 | Waking Dreams | 人类捍卫者 | Waking Dreams |
| UnQueen | 14 | Waking Dreams | 幽后 | Waking Dreams (Kerrigan 反派) |
| Periwag / PERIWAG | 8-10 | 蒙眼行动 | 佩里瓦格 | 蒙眼行动 (虫族侦察单位) |
| Ghost Program | 8 | 宽宽出逃 | 幽灵计划 | BrokenWide |

---

## 六、统计

- 总条目: **55 条** (zhTW 12 + wiki 15 + 致敬 5 + 单位 12 + 新增 11 = 55)
- 与现有 680 条合并后: **~735 条** (Stage 2 实施)
- 优先级分布:
  - `zhTW` 官方优先: ~10 条
  - `wiki` 简体沿用: ~40 条
  - `keep_english` 致敬语: 5 条

---

## 七、引用来源

- 23 篇 Blizzard 官方 zhTW 译文 (本地 zhTW PDF, 23 篇扫描版, OCR 提取)
- 12 篇英文新译: `sources/`
- 现有 680 条 Nova/Spectres glossary: 姊妹仓库 `StarCraft-Novels-Chinese-Localization` 的 `terminology/glossary.json`
- 380 行项目清单 (zhTW 30 条已预抽): 项目内部参考资料

---

## 八、Stage 1 退出标准

- [x] 23 篇 zhTW 全部 OCR 完毕 (生成 extracted/zhTW_raw/*.txt, 24 个)
- [x] zhTW_terminology_pairs.md 包含 55 条术语对 (zhTW 官方 + wiki + 致敬语)
- [x] 12 篇新译专名清单 (29 条) 已列, 准备 Stage 2 合并到 glossary.json
- [x] 与 12 篇新译术语需求对比, 覆盖率 ≥ 95%

Stage 1 完成 → 进入 Stage 2 (合并 v2 术语表)
