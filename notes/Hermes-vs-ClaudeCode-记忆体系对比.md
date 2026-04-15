# Hermes Agent vs Claude Code — 记忆与上下文体系对比

> 作者: 尹磊 & Hermes Agent
> 日期: 2026-04-15
> 目的: 深入理解两个AI工具的记忆架构差异，帮助选择合适的使用场景

---

## 一、概述

Claude Code 和 Hermes Agent 都是基于 Claude 大模型的 CLI 工具，但在**记忆管理**方面有本质区别。Claude Code 更像一个"每次重新认识你的专家"，而 Hermes Agent 像一个"有笔记本的长期助手"。

---

## 二、核心概念对照表

| 概念 | Claude Code | Hermes Agent | 说明 |
|------|------------|--------------|------|
| 永久记忆 (Memory) | ❌ 没有 | ✅ memory 工具 | 跨对话记住用户偏好、习惯 |
| 技能库 (Skills) | ❌ 没有 | ✅ skills 系统 | 可复用的操作手册、踩坑记录 |
| 项目指令 (CLAUDE.md) | ✅ 有 | ✅ 有（兼容） | 项目级配置，进入目录自动读取 |
| 上下文窗口 (Context Window) | ✅ 有上限 | ✅ 有上限 | 单次对话的"短期记忆" |
| 历史对话搜索 | ❌ 没有 | ✅ session_search | 搜索过去对话的内容 |
| 定时任务 | ❌ 没有 | ✅ cronjob | 定时自动执行任务 |
| 多平台 | ❌ 仅终端 | ✅ 终端/Telegram/Discord | 多入口，同一套记忆 |

---

## 三、4层记忆架构详解

### 第1层: Memory（永久记忆）

```
位置: ~/.hermes/ 目录下
生命周期: 永久存在，除非手动删除
注入方式: 每次对话自动注入到上下文开头
容量: 有限，需保持精简（约1000-2000字符）
```

**作用**: 存储"关于你这个人"的信息

**分两类**:
- `user` — 用户画像（名字、偏好、习惯、纠正记录）
- `memory` — 环境笔记（系统配置、工具特性、经验教训）

**实际例子**（当前存储的内容）:
```
user类:
  - 尹磊(Yin Lei), Python+AI初学者, 用macOS
  - 沟通偏好: 直接给最优方案，不等追问
  - 教学偏好: 排查bug用链路分析+双语对照

memory类:
  - 环境信息、工具配置等
```

**类比**: 相当于一个老同事认识你，知道你的脾气、工作习惯

**Claude Code 对比**: Claude Code 没有这层。每次新对话，它不知道你是谁、不知道你的偏好，一切从零开始。

---

### 第2层: Skills（技能库）

```
位置: ~/.hermes/skills/ 目录下
生命周期: 永久存在
注入方式: 按需加载（任务匹配时自动或手动加载）
容量: 不限，每个skill是独立的markdown文件
```

**作用**: 存储"怎么做某件事"的操作手册

**结构示例**:
```
~/.hermes/skills/
├── productivity/
│   ├── ocr-and-documents/     # OCR文档处理技能
│   └── powerpoint/            # PPT处理技能
├── github/
│   ├── github-pr-workflow/    # PR工作流
│   └── github-code-review/   # 代码审查
└── software-development/
    ├── systematic-debugging/  # 系统化调试
    └── test-driven-development/
```

**每个skill包含**:
- 触发条件（什么时候该用这个skill）
- 操作步骤（具体命令和流程）
- 踩坑记录（常见错误和解决方案）
- 验证步骤（怎么确认做对了）

**类比**: 相当于公司内部的操作手册wiki，新来的人照着做就行

**Claude Code 对比**: Claude Code 没有这层。你每次都需要重新描述完整流程，或者自己维护文档手动粘贴进去。

---

### 第3层: CLAUDE.md（项目指令）

```
位置: 项目根目录下的 CLAUDE.md 文件
生命周期: 跟随项目
注入方式: 进入项目目录时自动发现并读取
容量: 建议精简，避免占用过多上下文窗口
```

**作用**: 告诉AI"这个项目是什么、有什么规范"

**这是两者都支持的功能!**

**实际例子**（你的 ~/CLAUDE.md）:
```markdown
# CLAUDE.md
## Workspace Overview
- Python learning scripts at root level
- yinlei-project/ — Git-tracked subproject
- weixin-project/ — WeChat Mini Program project

## Running Python Scripts
python3 <script.py>
```

**支持层级**:
```
~/CLAUDE.md                    # 全局指令
~/project-a/CLAUDE.md          # 项目A专属
~/project-a/src/CLAUDE.md      # 子目录专属（可选）
```

**Claude Code 对比**: 两者基本一致。都支持项目根目录的 CLAUDE.md，都会自动读取。

---

### 第4层: 上下文窗口 (Context Window)

```
位置: 内存中（运行时）
生命周期: 仅当前对话
容量: 有上限（通常100K-200K tokens）
```

**作用**: 当前对话中AI能"看到"的全部内容

**包含什么**:
```
上下文窗口 = [
    系统提示词,          # AI的基础人格和能力说明
    Memory注入,          # 第1层的永久记忆
    CLAUDE.md,           # 第3层的项目指令  
    对话历史,            # 你说的话 + AI的回复
    工具调用结果,         # 执行命令、读文件的输出
]
```

**关键问题 — 会满!**

```
对话开始: [系统 + Memory + CLAUDE.md + 对话]  ← 轻松
对话中期: [系统 + Memory + CLAUDE.md + 大量对话 + 工具输出]  ← 还行
对话后期: [系统 + Memory + ............超长内容被截断............]  ← 早期内容丢失!
```

**实际影响**: 
- 我们这次对话已经很长了（安装工具、多次OCR、反复调试）
- 对话开头的一些细节我可能已经"看不到"了
- 但重要的东西我已经存到Memory和文件里，不会真正丢失

**Claude Code 对比**: 两者一样，都有上下文窗口限制。但Hermes Agent可以用Memory把重要信息"捞出来"存到永久记忆，Claude Code只能靠CLAUDE.md。

---

## 四、信息流对比图

### Claude Code 的信息流

```
新对话开始
    │
    ├── 读取 CLAUDE.md ──────────────┐
    │                                │
    ├── 用户输入 ─────────────────────┤──→ 上下文窗口 ──→ AI回复
    │                                │
    └── 工具输出 ─────────────────────┘
    
对话结束 → 一切消失（下次重新开始）
```

### Hermes Agent 的信息流

```
新对话开始
    │
    ├── 自动注入 Memory ─────────────┐
    ├── 读取 CLAUDE.md ──────────────┤
    ├── 按需加载 Skills ─────────────┤──→ 上下文窗口 ──→ AI回复
    ├── 用户输入 ─────────────────────┤         │
    └── 工具输出 ─────────────────────┘         │
                                               │
    对话过程中 ←─────────────────────────────────┘
        │
        ├── 发现重要信息 → 存入 Memory（下次自动注入）
        ├── 学到新方法   → 存入 Skills（下次按需加载）
        └── 搜索历史     → session_search 查找过去对话
    
对话结束 → Memory和Skills永久保留
```

---

## 五、使用场景建议

### 适合用 Claude Code 的场景

- 一次性的编程任务（写个函数、改个bug）
- 不需要记住偏好的临时工作
- 项目规范已经写好在 CLAUDE.md 里
- 团队协作，CLAUDE.md 可以 git 共享

### 适合用 Hermes Agent 的场景

- 长期项目，需要记住上下文和偏好
- 学习过程，需要积累知识和技能
- 重复性任务，需要标准化流程（Skills）
- 多平台（终端 + Telegram + Discord）
- 需要定时任务（监控、定期报告等）

---

## 六、常见术语表（双语对照）

| 英文 | 中文 | 解释 |
|------|------|------|
| Context Window | 上下文窗口 | 一次对话AI能"看到"的内容总量 |
| Token | 令牌/词元 | AI处理文本的最小单位，约1个中文字=2-3 tokens |
| Memory | 永久记忆 | 跨对话保存的用户信息和环境笔记 |
| Skills | 技能库 | 可复用的操作流程文档 |
| Session | 会话/对话 | 从打开到关闭的一次完整交互 |
| Inject | 注入 | 自动把信息插入到上下文窗口里 |
| CLAUDE.md | 项目指令文件 | 放在项目根目录，AI自动读取的配置文件 |
| OOM (Out Of Memory) | 内存溢出 | 程序占用内存超过系统可用量 |
| Truncate | 截断 | 上下文太长时，丢弃早期内容 |

---

## 七、总结

一句话总结区别:

> **Claude Code = 强大但失忆的专家**（每次重新认识你）
> **Hermes Agent = 有笔记本的长期助手**（记得你、会成长）

Hermes Agent 在 Claude Code 的基础上，增加了 Memory + Skills + Session Search 三层持久化能力，让AI从"一次性工具"变成了"持续学习的伙伴"。
