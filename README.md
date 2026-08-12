# StarCraft 短篇汉化 (12 篇英文独有) — Chinese Localization

> **非官方同人项目** — 使用前请阅读 [DISCLAIMER.md](DISCLAIMER.md)
>
> 范围: 12 篇 StarCraft 英文独有短篇 (Blizzard 官方 2008-2016)
> 译者: 本地 LLM (Qwen2.5-14B-Instruct) 机器翻译 + 人工逐篇校对
> 状态: ✅ **12 篇全部完成, GitHub 仓库已建立 ([FeiWenT/StarCraft-ShortStories-Chinese-Localization](https://github.com/FeiWenT/StarCraft-ShortStories-Chinese-Localization))**

姊妹仓库:
- [StarCraft-Novels-Chinese-Localization](https://github.com/FeiWenT/StarCraft-Novels-Chinese-Localization) — Nova + Spectres 长篇 (已上线)
- 本仓库: [StarCraft-ShortStories-Chinese-Localization](https://github.com/FeiWenT/StarCraft-ShortStories-Chinese-Localization) — 12 篇短篇 (待 push)

---

## 📚 12 篇导航

### 🏆 Tier 1 · 4-5 星 (4 篇)

| # | 英文标题 | 中文标题 | 时代 | 字符数 | 难度 | 译文 |
|---|---------|---------|------|--------|------|------|
| 1 | Operation Blind Devil | 蒙眼行动 | 10 周年 | 55,804 | ⭐⭐⭐⭐⭐ | [out](out/10th_anniversary__operation_blind_devil_zh.md) |
| 2 | Waking Dreams | 清醒梦境 | 10 周年 | 56,939 | ⭐⭐⭐⭐ | [out](out/10th_anniversary__waking_dreams_zh.md) |
| 3 | One People, One Purpose | 万众一心 | 10 周年 | 61,781 | ⭐⭐⭐⭐ | [out](out/10th_anniversary__one_people_one_purpose_zh.md) |
| 4 | Revelations | 启示录 | SC1 / Brood War | 43,043 | ⭐⭐⭐⭐ | [out](out/sc_brood_war__revelations_zh.md) |

### ⭐ Tier 2 · 3 星 (5 篇)

| # | 英文标题 | 中文标题 | 时代 | 字符数 | 难度 | 译文 |
|---|---------|---------|------|--------|------|------|
| 5 | Hybrid | 混合体 | SC1 / Brood War | 28,053 | ⭐⭐⭐ | [out](out/sc_brood_war__hybrid_zh.md) |
| 6 | Colossus | 巨像 | Wings of Liberty | 38,795 | ⭐⭐⭐ | [out](out/wings_of_liberty__colossus_zh.md) |
| 7 | Mothership | 母舰 | Wings of Liberty | 28,560 | ⭐⭐⭐ | [out](out/wings_of_liberty__mothership_zh.md) |
| 8 | Changeling | 变形虫 | Wings of Liberty | 27,398 | ⭐⭐⭐ | [out](out/wings_of_liberty__changeling_zh.md) |
| 9 | Stealing Thunder | 夺雷 | Wings of Liberty | 39,311 | ⭐⭐⭐ | [out](out/wings_of_liberty__stealing_thunder_zh.md) |

### Tier 3 · 2 星 (3 篇)

| # | 英文标题 | 中文标题 | 时代 | 字符数 | 难度 | 译文 |
|---|---------|---------|------|--------|------|------|
| 10 | Collateral Damage | 附带损伤 | Wings of Liberty | 35,337 | ⭐⭐ | [out](out/wings_of_liberty__collateral_damage_zh.md) |
| 11 | Heavens Devils Lost Transmissions | 天堂魔鬼遗失的电讯 | Wings of Liberty | 9,833 | ⭐⭐ | [out](out/wings_of_liberty__heavens_devils_lost_transmissions_zh.md) |
| 12 | BrokenWide | 宽宽出逃 | Wings of Liberty | 35,521 | ⭐⭐ | [out](out/wings_of_liberty__broken_wide_zh.md) |

**总计**: 12 篇 / ~460K 字符英文 → ~152K 字符中文 / ~85 分钟 GPU + ~3 小时人工

---

## 🗂️ 仓库结构

```
StarCraft_短篇汉化/
├── README.md                       # 本文件
├── DISCLAIMER.md                   # 12 篇版权声明
├── LICENSE.md                      # MIT
├── _新对话启动包.md                 # 多会话 handoff
├── _分阶段进度.md                   # 8 阶段追踪
├── sources/                        # 12 篇英文原文 (本地, GitHub 不上传)
├── out/                            # 12 篇中文终稿 (GitHub 上传主目标)
├── terminology/                    # 术语表 v2 (730 条 + priority)
├── drafts/                         # 工作区 (不入 GitHub)
└── tools/                          # 翻译工具链
```

---

## 🔧 翻译流水线 (8 阶段)

| # | 阶段 | 状态 | 交付 |
|---|------|------|------|
| 0 | 目录 + 12 篇原文 | ✅ | sources/*.txt + sha256 |
| 1 | OCR 23 篇 zhTW 官方 | ✅ | [terminology/zhTW_terminology_pairs.md](terminology/zhTW_terminology_pairs.md) (55 条) |
| 2 | 术语表 v2 | ✅ | terminology/glossary.json (730 条) |
| 3 | 工具改造 | ✅ | tools/mt_story.py + 4 个 audit 工具 |
| 4 | MVP 蒙眼行动 | ✅ | out/operation_blind_devil_zh.md (5★) |
| 5 | 批量 11 篇 | ✅ | 全部部署 out/ |
| 6 | 审计 + 后修 | ✅ | 12 份 terminology_audit + 跨篇一致性 (本地保留) |
| 7 | GitHub 发布 | ✅ | [FeiWenT/StarCraft-ShortStories-Chinese-Localization](https://github.com/FeiWenT/StarCraft-ShortStories-Chinese-Localization) 上线 |

---

## 🤖 LLM 翻译子系统 (mt_story.py)

**模型**: Ollama + Qwen2.5-14B-Instruct Q4_K_M (本地, RTX 4070 SUPER 12GB)

**关键设计** (继承自 Nova/Spectres 验证管线):
- **篇级** (1800 字符/块, 9-35 块/篇, 段间落边界)
- **两遍翻译**: v0 (温度 0.3) + v1 自校 (温度 0.1)
- **术语注入**: `glossary.json` 730 条, **zhTW 官方优先** + wiki + 5 致敬语 `keep_english`
- **风格锚**: 从 Nova 终稿抽 400 字 (统一锚源)
- **每篇独立 style_notes.md**: 翻译守则 + POV 规则 + 关键术语
- **缓存**: `_mt_cache.json`, key = `{slug}_chunk{NN}_v{0,1}`
- **自检**: 英文残留 + 术语未对齐 + 12 篇 pitfall 检测

---

## 📊 翻译质量总览 (12 篇)

| # | 标题 | 字符 | 未对齐 | 残留 | 保留 | pitfall |
|---|------|------|--------|------|------|---------|
| 1 | 蒙眼行动 | 16,906 | 0 | 2 | 0 | ✓ |
| 2 | 清醒梦境 | 17,694 | 0 | 31 | 0 | ⚠ 标题 |
| 3 | 万众一心 | 20,689 | 0 | 1 | 4 | ✓ |
| 4 | 启示录 | 13,262 | 0 | 15 | 14 | ✓ |
| 5 | 混合体 | 8,066 | 0 | 20 | 0 | ✓ |
| 6 | 巨像 | 12,070 | 0 | 1 | 0 | ✓ |
| 7 | 母舰 | 8,816 | 0 | 0 | 0 | ✓ |
| 8 | 变形虫 | 8,325 | 0 | 3 | 1 | ✓ |
| 9 | 夺雷 | 12,663 | 0 | 10 | 0 | ✓ |
| 10 | 附带损伤 | 10,574 | 0 | 2 | 0 | ✓ |
| 11 | 天堂魔鬼 | 2,994 | 0 | 3 | 1 | ✓ |
| 12 | 宽宽出逃 | 10,873 | 0 | 0 | 0 | ✓ |

**总未对齐**: 0 (12 篇全部 ✓, 1 处已修: 变形虫 Protoss → 星灵)
**总残留**: 88 (品牌/型号/对话人名/语气词/拟声词, 全部预期保留)
**总保留**: 20 (致敬语 + 品牌缩写)
**总 pitfall**: 1 (清醒梦境 "清醒梦境" 标题未在 v1 出现, 因 LLM 改写段落丢失原文标题)

---

## 🔗 姊妹项目

- **Nova + Spectres 长篇**: [github.com/FeiWenT/StarCraft-Novels-Chinese-Localization](https://github.com/FeiWenT/StarCraft-Novels-Chinese-Localization)
- **CROSS†CHANNEL 工程**: [github.com/FeiWenT/CrossChannelSteamEditionChineseLocalization](https://github.com/FeiWenT/CrossChannelSteamEditionChineseLocalization)
- **本项目 (12 篇英文独有短篇)**: [github.com/FeiWenT/StarCraft-ShortStories-Chinese-Localization](https://github.com/FeiWenT/StarCraft-ShortStories-Chinese-Localization)

---

## 🙏 致谢

- **原作者**: Cassandra Rose Clarke / EC Myers / Alex Acks / Blizzard staff 等
- **版权方**: Blizzard Entertainment, Inc.
- **术语参考**: 《星际争霸》中文维基 + Blizzard 23 篇官方 zhTW 译文
- **翻译模型**: Qwen2.5-14B-Instruct (阿里云通义千问团队)
- **工程范式**: Nova + Spectres 仓库 (mt_chapter.py 已验证管线)

---

## 📜 License

本仓库**译文**与**工具脚本**采用 MIT License 发布。
原短篇版权与世界观归 Blizzard Entertainment 与原作者所有, 详见 [DISCLAIMER.md](DISCLAIMER.md)。
