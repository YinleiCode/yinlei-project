# Git 完整学习笔记

> 作者：Yinlei
> 状态：基础部分 ✅ 已掌握 | 进阶部分 🔴🟡🟢 分级学习中
> 用途：日常开发速查 + 学习复习

---

## 📚 目录

### 第一部分：基础知识（已掌握）
1. [Git 是什么](#1-git-是什么)
2. [四个空间](#2-四个空间)
3. [文件三态](#3-文件三态)
4. [日常基础命令](#4-日常基础命令)
5. [分支操作](#5-分支操作)
6. [完整工作流程](#6-完整工作流程)

### 第二部分：进阶日常技能（10道题）
7. [🔴 撤销工作区的修改](#7-撤销工作区的修改)
8. [🔴 撤销暂存区（add错了）](#8-撤销暂存区add错了)
9. [🔴 修改最近一次commit message](#9-修改最近一次commit-message)
10. [🔴 .gitignore（哪些文件不该进Git）](#10-gitignore哪些文件不该进git)
11. [🔴 git diff（看看我改了什么）](#11-git-diff看看我改了什么)
12. [🟡 git stash（临时存修改）](#12-git-stash临时存修改)
13. [🟡 git pull vs git fetch](#13-git-pull-vs-git-fetch)
14. [🟡 解决冲突（conflict）](#14-解决冲突conflict)
15. [🟢 git reset vs git revert](#15-git-reset-vs-git-revert)
16. [🟢 搞砸了怎么恢复](#16-搞砸了怎么恢复)

---

# 第一部分：基础知识（已掌握）

---

## 1. Git 是什么

Git 是一个**分布式版本控制系统**。

大白话：**Git 帮你记录文件的每一次修改，让你可以随时回到任何一个历史版本。**

就像游戏里的"存档"功能：
- 每次你觉得"这个状态不错"就存一个档（commit）
- 搞砸了可以读取之前的存档（回退）
- 想试新玩法可以开个新分支（branch）
- 试完了可以合并回主线（merge）

### 为什么要学 Git

1. **防丢**：代码永远有备份，不怕电脑坏
2. **回退**：改坏了可以随时恢复
3. **协作**：多人同时改代码不会互相覆盖
4. **记录**：每一次修改都有记录，知道谁在什么时候改了什么

---

## 2. 四个空间

Git 的世界里有四个"空间"，代码在这四个空间之间流动：

```
工作区 → 暂存区 → 本地仓库 → 远程仓库
```

| 空间 | 在哪里 | 比喻 |
|---|---|---|
| **工作区（Working Directory）** | 你电脑上的项目文件夹 | 你的**工作台** |
| **暂存区（Staging Area）** | Git 内部的一个"待发货区" | **快递打包区**：挑好要寄的东西 |
| **本地仓库（Local Repository）** | 你电脑上的 `.git` 文件夹 | **本地仓库**：打包好的快递堆在家里 |
| **远程仓库（Remote Repository）** | GitHub/GitLab 上 | **快递站**：把快递发出去，别人也能取 |

### 代码在四个空间之间怎么流动

```
工作区 --git add--> 暂存区 --git commit--> 本地仓库 --git push--> 远程仓库
                                                     <--git pull-- 远程仓库
```

---

## 3. 文件三态

在 Git 的眼里，每个文件处于三种状态之一：

| 状态 | 意思 | 类比 |
|---|---|---|
| **Untracked（未追踪）** | Git 完全不认识这个文件 | 路人甲，Git 假装看不见 |
| **Staged（已暂存）** | 文件被 `git add` 放进了暂存区，准备被 commit | 排队等发货 |
| **Committed（已提交）** | 文件已经被 `git commit` 安全保存 | 快递已发出 |

### 状态转换

```
Untracked --git add--> Staged --git commit--> Committed
                ↑                                  |
                |        修改文件后                 |
                ←──────── Modified ←───────────────┘
```

修改已经 commit 过的文件后，它的状态会变成 **Modified（已修改）**，你需要重新 `git add` 和 `git commit`。

### 查看状态

```bash
git status
```

这条命令随时可以敲，它会告诉你每个文件当前是什么状态。**这是你用得最多的命令，没有之一。**

---

## 4. 日常基础命令

### 初始化与克隆

```bash
# 在当前文件夹创建一个新的 Git 仓库
git init

# 从 GitHub 克隆一个已有的仓库到本地
git clone https://github.com/用户名/仓库名.git
```

### 三件套（每天用无数次）

```bash
# 第一步：把修改的文件放进暂存区
git add 文件名        # 添加单个文件
git add .            # 添加所有修改的文件

# 第二步：提交到本地仓库
git commit -m "这次提交做了什么"

# 第三步：推送到远程仓库（GitHub）
git push
```

**记忆口诀**：**add → commit → push，三步走**

### 查看信息

```bash
# 查看文件状态（最常用！）
git status

# 查看提交历史
git log

# 查看简洁版提交历史（一行一个commit）
git log --oneline

# 查看更详细的提交历史（带分支图）
git log --oneline --graph --all
```

### 远程仓库操作

```bash
# 查看远程仓库信息
git remote -v

# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 从远程拉取最新代码
git pull
```

---

## 5. 分支操作

### 什么是分支

分支就是**开辟一条平行的开发路线**。你可以在分支上放心修改，不影响主线。改好了再合并回来。

就像你在写论文：主线是正式版本，你开了个分支"试试新的第三章"——写得好就合进正式版，写砸了直接删掉分支，正式版毫发无损。

### 分支命令

```bash
# 查看所有分支（*号标记当前所在分支）
git branch

# 创建新分支
git branch 分支名

# 切换到某个分支
git checkout 分支名
# 或者新版 Git 推荐用：
git switch 分支名

# 创建并立刻切换到新分支（一步到位）
git checkout -b 分支名
# 或者：
git switch -c 分支名

# 合并分支（先切回主分支，再合并）
git checkout main
git merge 要合并的分支名

# 删除已合并的分支（合并完就可以删了，保持整洁）
git branch -d 分支名
```

### 分支命名建议

| 前缀 | 用途 | 例子 |
|---|---|---|
| `feature/` | 新功能 | `feature/login` |
| `fix/` | 修复 bug | `fix/button-crash` |
| `docs/` | 文档修改 | `docs/update-readme` |
| `test/` | 测试相关 | `test/add-unit-tests` |

### rebase（变基）

```bash
# 把当前分支的 commit "移动"到目标分支的最前面
git rebase main
```

**merge vs rebase 的区别**：
- **merge**：保留分支历史，创建一个"合并节点"，历史看起来像"分叉又合拢"
- **rebase**：把分支的 commit 搬到主线末端，历史看起来像"一条直线"

**新手建议**：日常用 merge 就够了，rebase 等熟练后再用。

---

## 6. 完整工作流程

一个典型的"从零到推送"的流程：

```bash
# 1. 创建新分支
git checkout -b feature/新功能名

# 2. 写代码...（在编辑器里修改文件）

# 3. 看看改了啥
git status
git diff

# 4. 把修改放进暂存区
git add .

# 5. 提交
git commit -m "添加了xxx功能"

# 6. 切回主分支
git checkout main

# 7. 合并
git merge feature/新功能名

# 8. 推送到 GitHub
git push

# 9. 删除用完的分支（可选，保持整洁）
git branch -d feature/新功能名
```

**口诀**：**建分支 → 写代码 → add → commit → 切主线 → merge → push → 删分支**

---

# 第二部分：进阶日常技能（10道题）

> 优先级说明：
> - 🔴 **今天必须学**：随时会遇到
> - 🟡 **近期要学**：做项目会遇到
> - 🟢 **以后再学**：进阶场景

---

## 7. 🔴 撤销工作区的修改

### 场景

你在改 `main.py`，改了半天发现**改错方向了**，想回到上次 commit 的干净状态。

### 命令

```bash
git restore main.py
```

把 `main.py` 恢复到**最近一次 commit 的状态**。你改的东西全部消失。

如果要恢复**所有**修改过的文件：

```bash
git restore .
```

### ⚠️ 危险等级：高！

**这个操作不可逆！** 你改的内容会**永远消失**，没有回收站。用之前要确定你真的不要那些修改。

### 记忆口诀

> **改错了想恢复？`git restore 文件名`。但改的东西会永远消失，用之前想清楚。**

---

## 8. 🔴 撤销暂存区（add错了）

### 场景

你不小心 `git add` 了一个不该 add 的文件，想把它从暂存区**退回来**。

### 命令

```bash
git restore --staged main.py
```

把 `main.py` **从暂存区退回工作区**。

### 安全！

**文件内容不会丢！** 你的修改还在，只是从"准备提交"退回到"已修改但没暂存"。

### 用文件三态理解

```
git add：     工作区 → 暂存区（推进去）
git restore --staged：暂存区 → 工作区（拉回来）
```

### 对比两个 restore（必须分清！）

| 命令 | 做什么 | 内容会丢吗 |
|---|---|---|
| `git restore 文件名` | 恢复工作区修改 | ⚠️ **会！不可逆！** |
| `git restore --staged 文件名` | 从暂存区退回 | ✅ **不会，安全** |

**一个有 `--staged` 一个没有，差别巨大。** 加了 `--staged` 是安全操作，不加的话修改会永远消失。

### 记忆口诀

> **add 错了？`git restore --staged 文件名`。文件还在，只是退回工作区。**

---

## 9. 🔴 修改最近一次 commit message

### 场景

你刚 commit 了，结果发现 message 写错了，想改一下。

### 命令

```bash
git commit --amend -m "新的commit message"
```

把最近一次 commit 的 message **替换**成你写的新内容。

### ⚠️ 限制

- **只能改最近一次** commit
- 如果**已经 push 到 GitHub**，改完需要 `git push --force` 才能推上去（慎用）
- **最佳实践**：在 push 之前发现并修改

### 记忆口诀

> **commit message 写错了？`git commit --amend -m "改正后的message"`。只能改最近一次，最好在 push 之前改。**

### 补充：如果你还想往最近一次 commit 里追加文件

```bash
# 先 add 漏掉的文件
git add 漏掉的文件.py

# 然后用 --amend 追加进去（不改 message 就不加 -m）
git commit --amend --no-edit
```

`--no-edit` 表示"message 不改，就追加文件"。

---

## 10. 🔴 .gitignore（哪些文件不该进Git）

### 场景

项目文件夹里有些文件**不应该被 Git 追踪**：
- `.DS_Store`（Mac 自动生成的隐藏文件）
- `node_modules/`（npm 安装的依赖包，几千个文件）
- `.env`（存密码、密钥的环境变量文件）
- `__pycache__/`（Python 自动生成的缓存）
- `.vscode/`（VS Code 的个人配置）

### 怎么做

在项目根目录创建 `.gitignore` 文件：

```
# Mac 系统文件
.DS_Store

# Python 缓存
__pycache__/
*.pyc

# 环境变量（有密码密钥）
.env

# Node 依赖
node_modules/

# VS Code 个人配置
.vscode/

# 编译产物
*.o
*.exe
dist/
build/
```

### 写完之后

```bash
git add .gitignore
git commit -m "添加 .gitignore 文件"
```

从此 Git 会自动无视这些文件。

### ⚠️ 已经追踪的文件怎么办

`.gitignore` 只能**防止新文件被追踪**。如果文件**已经被 Git 追踪了**，需要先移除追踪：

```bash
git rm --cached .env
```

`--cached` 是关键——不加这个，文件会被**真的删掉**。加了 `--cached`，只是让 Git 不再追踪它，文件本身还在你电脑上。

### 记忆口诀

> **不该进 Git 的文件写进 `.gitignore`。已经被追踪的要先 `git rm --cached` 再 ignore。**

---

## 11. 🔴 git diff（看看我改了什么）

### 场景

改了几个文件，commit 之前想**看看自己到底改了什么**。

### 命令

```bash
git diff
```

显示工作区里**所有修改过但还没 add 的文件**的改动详情。

### 输出怎么看

```diff
- old_line = "旧的内容"       ← 红色，表示被删除/替换的旧内容
+ new_line = "新的内容"       ← 绿色，表示新增/替换后的新内容
```

### 三种 diff 的区别

| 命令 | 对比什么 | 用途 |
|---|---|---|
| `git diff` | 工作区 vs 暂存区 | 看还没 add 的改动 |
| `git diff --staged` | 暂存区 vs 最近一次 commit | 看已经 add 但没 commit 的改动 |
| `git diff HEAD` | 工作区 vs 最近一次 commit | 看所有改动（不管有没有 add） |

**最常用的是第一个**：`git diff`——commit 之前扫一眼，确认改动内容没问题。

### 记忆口诀

> **commit 之前先 `git diff` 看一眼。这是你的"提交前体检"。**

---

## 12. 🟡 git stash（临时存修改）

### 场景

你正在 `feature/login` 分支上写登录功能，写到一半，突然老板说"线上有个紧急 bug 要修"。你需要切到 `main` 分支去修 bug，但手头的代码**还没写完，不想 commit 一个半成品**。

### 命令

```bash
# 把当前的修改"暂存"起来（藏到一个临时抽屉里）
git stash

# 现在工作区干净了，可以安全切换分支
git checkout main
# ...修 bug、commit、push...

# 修完 bug，切回来
git checkout feature/login

# 把之前藏起来的修改"拿出来"
git stash pop
```

### 理解方式

`git stash` 就像你桌上正在画的画——突然有急事要处理，你不想把画扔了，也不想草草收工。于是你把画**临时塞进抽屉**（stash），处理完急事回来再**从抽屉拿出来**（stash pop）继续画。

### 常用命令

```bash
git stash          # 藏起来
git stash pop      # 拿出来（并删除这条 stash 记录）
git stash list     # 看看抽屉里有几份暂存
git stash apply    # 拿出来（但不删除记录，可以重复使用）
git stash drop     # 手动删除最近一条 stash 记录
```

### 记忆口诀

> **写到一半要切分支？`git stash` 先藏起来，回来后 `git stash pop` 拿出来。**

---

## 13. 🟡 git pull vs git fetch

### 两者的区别

| 命令 | 做什么 | 类比 |
|---|---|---|
| `git fetch` | 从远程**下载**最新代码到本地仓库，但**不合并** | 快递到了楼下，但你还没上去拿 |
| `git pull` | 从远程**下载并自动合并**到当前分支 | 快递到了楼下，直接送到你手上 |

### 关系

```bash
git pull = git fetch + git merge
```

`git pull` 是 `git fetch` 和 `git merge` 的**合体**。

### 什么时候用哪个

| 场景 | 用什么 |
|---|---|
| **日常工作**，想快速同步最新代码 | `git pull`（简单省事） |
| 想**先看看**远程有什么更新，再决定要不要合并 | `git fetch`，看完再手动 `git merge` |

### 新手建议

**直接用 `git pull` 就行**。等你以后做多人协作、需要更精细控制的时候，再学 `git fetch` 的玩法。

### 记忆口诀

> **`git pull` = 下载 + 合并（一步到位）。`git fetch` = 只下载不合并（先看看再说）。日常用 pull 就够了。**

---

## 14. 🟡 解决冲突（conflict）

### 什么时候会冲突

当**两个人（或两个分支）同时修改了同一个文件的同一行**，Git 不知道该听谁的，就会报冲突。

### 冲突长什么样

当你 `git merge` 或 `git pull` 遇到冲突时，文件里会出现这样的标记：

```
<<<<<<< HEAD
你的版本：这里是你写的代码
=======
对方的版本：这里是对方写的代码
>>>>>>> feature/other-branch
```

三个标记把冲突分成两块：
- `<<<<<<< HEAD` 到 `=======` 之间：**你当前分支**的内容
- `=======` 到 `>>>>>>>` 之间：**要合并进来的分支**的内容

### 怎么解决

1. **打开冲突文件**（VS Code 会高亮显示冲突区域，特别直观）
2. **手动选择**：保留你的版本、保留对方版本、或者两个都留、或者写一个全新的版本
3. **删掉冲突标记**（`<<<<<<<`、`=======`、`>>>>>>>`）
4. **保存文件**
5. **标记冲突已解决**：

```bash
git add 冲突文件名
git commit -m "解决xxx文件的合并冲突"
```

### 举个例子

假设冲突内容是这样的：

```
<<<<<<< HEAD
greeting = "你好"
=======
greeting = "Hello"
>>>>>>> feature/english
```

你决定两种语言都要：

```python
greeting_cn = "你好"
greeting_en = "Hello"
```

然后删掉所有冲突标记，保存，`git add`，`git commit`。搞定。

### VS Code 的便捷操作

VS Code 遇到冲突会在冲突区域上方显示几个按钮：
- **Accept Current Change**（保留你的）
- **Accept Incoming Change**（保留对方的）
- **Accept Both Changes**（两个都留）
- **Compare Changes**（对比看看）

点一下按钮就能快速选择，不用手动删标记。

### 记忆口诀

> **冲突 = Git 不知道听谁的。你手动选一个版本，删掉冲突标记，然后 add + commit。**

---

## 15. 🟢 git reset vs git revert

### 核心区别

| 命令 | 做什么 | 历史记录 | 安全性 |
|---|---|---|---|
| `git reset` | **回退到**某个 commit，之后的 commit 被"删除" | 历史被**改写** | ⚠️ 危险 |
| `git revert` | **创建一个新 commit** 来"撤销"某个旧 commit 的修改 | 历史**保留** | ✅ 安全 |

### 比喻

- **reset** = 穿越时光机回到过去，未来的事直接**不存在了**
- **revert** = 不穿越，而是在当下做一个"**反向操作**"来抵消之前的修改。历史完整保留

### git reset 的三种模式

```bash
# 软重置：回退 commit，但修改保留在暂存区
git reset --soft HEAD~1

# 混合重置（默认）：回退 commit，修改保留在工作区
git reset HEAD~1

# 硬重置：回退 commit，修改全部丢弃
git reset --hard HEAD~1
```

**`HEAD~1` 表示"上一个 commit"。`HEAD~2` 表示"上两个 commit"，以此类推。**

| 模式 | commit | 暂存区 | 工作区 | 危险程度 |
|---|---|---|---|---|
| `--soft` | 回退 | 保留 | 保留 | ✅ 安全 |
| 默认（`--mixed`） | 回退 | 清空 | 保留 | ✅ 安全 |
| `--hard` | 回退 | 清空 | 清空 | ⚠️ **危险！** |

### git revert

```bash
# 撤销最近一次 commit 的修改（创建一个新的"反向"commit）
git revert HEAD
```

Git 会自动创建一个新 commit，内容是"把上一次 commit 的修改反过来"。历史完整保留，安全。

### 什么时候用哪个

| 场景 | 用什么 |
|---|---|
| 还**没 push**，想悄悄撤回 | `git reset`（改写历史没关系，因为还没公开） |
| 已经 **push 了**，别人可能已经拉了你的代码 | `git revert`（不改写历史，安全） |

### 黄金原则

> **已经 push 的 commit，永远用 `revert`，不要用 `reset`。**
>
> 因为 `reset` 会改写历史——如果别人已经基于你的 commit 做了开发，你突然把历史改了，别人的代码就乱了。

### 记忆口诀

> **没 push 用 reset（悄悄改历史），已 push 用 revert（安全撤销）。`reset --hard` 是核弹，慎用！**

---

## 16. 🟢 搞砸了怎么恢复

### 终极后悔药：`git reflog`

当你觉得"完了，我彻底搞砸了"的时候——**别慌，Git 有后悔药**。

```bash
git reflog
```

这条命令会显示你**所有操作的历史记录**——包括你以为"删掉了"的 commit、`reset` 回退掉的 commit、所有你做过的事情。

输出大概是这样的：

```
abc1234 HEAD@{0}: reset: moving to HEAD~3
def5678 HEAD@{1}: commit: 添加登录功能
ghi9012 HEAD@{2}: commit: 修复首页bug
...
```

找到你想回到的那个 commit 的 hash（前面那串字母数字），然后：

```bash
git reset --hard abc1234
```

**时光倒流，回到那个状态。**

### ⚠️ reflog 的限制

- reflog 只记录**本地操作**，不记录远程的
- reflog 记录默认保留 **90 天**，过期会被清理
- 它不能恢复**从未 commit 过**的修改——如果你改了文件但从来没 add、没 commit 就丢了，那是真的丢了

### 常见"搞砸了"的场景和解法

| 搞砸了什么 | 解法 |
|---|---|
| commit 了不该 commit 的东西 | `git reset --soft HEAD~1`（保留修改，撤回 commit） |
| `git reset --hard` 用猛了 | `git reflog` 找回来 |
| 合并搞坏了 | `git merge --abort`（放弃这次合并） |
| rebase 搞坏了 | `git rebase --abort`（放弃这次 rebase） |
| 分支删错了 | `git reflog` 找到删除前的 commit，`git branch 分支名 commit哈希` 恢复 |
| 文件改坏了但还没 commit | `git restore 文件名`（恢复到上次 commit） |

### 终极记忆口诀

> **搞砸了先别慌，`git reflog` 是你的后悔药。只要 commit 过的东西，90天内都能找回来。**

### 最最重要的一条

> **养成勤 commit 的习惯。** 每做完一小步就 commit 一次，这样你的"存档点"就多，不管怎么搞砸，都能找到一个离你最近的安全点回退。

---

# 🎯 速查表：日常最常用命令

| 我想做什么 | 命令 | 安全吗 |
|---|---|---|
| 看看什么文件改了 | `git status` | ✅ |
| 看看具体改了什么 | `git diff` | ✅ |
| 把修改存进暂存区 | `git add 文件名` 或 `git add .` | ✅ |
| 提交 | `git commit -m "message"` | ✅ |
| 推到 GitHub | `git push` | ✅ |
| 从 GitHub 拉最新 | `git pull` | ✅ |
| 改错了想恢复文件 | `git restore 文件名` | ⚠️ 不可逆 |
| add 错了想撤回 | `git restore --staged 文件名` | ✅ |
| commit message 写错了 | `git commit --amend -m "新message"` | ✅（push前） |
| 写到一半要切分支 | `git stash` → 切 → 回来 → `git stash pop` | ✅ |
| 已 push 的 commit 要撤销 | `git revert HEAD` | ✅ |
| 没 push 的 commit 要撤销 | `git reset --soft HEAD~1` | ✅ |
| 搞砸了找后悔药 | `git reflog` | ✅ |

---

# 📝 考试准备：10道题的自测清单

学完后用这个清单自测，每题能用自己的话回答 + 能在终端里操作就算过关：

- [ ] 1. 我改错了一个文件，怎么恢复？这个操作危险吗？为什么？
- [ ] 2. 我 `git add` 错了一个文件，怎么从暂存区退回来？内容会丢吗？
- [ ] 3. `git restore` 和 `git restore --staged` 的区别是什么？（必须分清！）
- [ ] 4. 我刚 commit 完发现 message 写错了，怎么改？
- [ ] 5. `.gitignore` 是干什么的？已经被 Git 追踪的文件加进 `.gitignore` 有用吗？
- [ ] 6. commit 之前怎么看自己到底改了什么？
- [ ] 7. 写代码写到一半要紧急切分支修 bug，怎么办？
- [ ] 8. `git pull` 和 `git fetch` 的区别是什么？日常用哪个？
- [ ] 9. 合并代码时遇到冲突了，文件里那些 `<<<<<<<` 和 `=======` 是什么意思？怎么解决？
- [ ] 10. 已经 push 的 commit 要撤销，用 `reset` 还是 `revert`？为什么？
- [ ] 11.（附加）搞砸了怎么办？后悔药叫什么？

---

*最后更新：2026 年 4 月*
*学习状态：🔴 已学完 | 🟡🟢 待实操巩固*
*学习方式：结对学习 + 大白话 + 比喻 + 动手实操*
