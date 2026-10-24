# SuperHumanizer

**把“降AI”请求做成可复用的保真编辑流程。支持中英文、报告标注定位和 Word 真实修订。**

SuperHumanizer 来自实际的学术英语改写与文档交付流程。它帮助 AI 识别空泛、重复、长并列和模板化表达，在保留原意、引用、条件、作者声音及篇幅的前提下修改。

本项目是给 AI 阅读和执行的 skill。它不提供检测器，也不承诺降低某个检测分数。准确、清楚、可核对是交付标准。

## 直接把链接发给 AI

复制下面这段，再附上要处理的文字或文件。

```text
请读取并使用这个仓库中的 SuperHumanizer skill
https://github.com/MichaelSong222/SuperHumanizer

完整单文件入口
https://raw.githubusercontent.com/MichaelSong222/SuperHumanizer/main/SUPERHUMANIZER_PROMPT.md

请对我随后提供的材料降AI。保留原意、事实、引用、条件和确定程度，篇幅不要大幅变化。先判断需要修改的实际问题，再按 skill 流程改写和核对。
```

只发仓库链接时，AI可以先读取功能说明，再等待你提供目标和要求。网页读取不会自动安装skill，也不会让聊天AI获得文件编辑或WPS控制权限。

如果AI不能读取GitHub链接，可以下载并上传 [完整单文件说明](SUPERHUMANIZER_PROMPT.md)。如果只支持粘贴文字，也可以把该文件内容作为任务说明提供。

## 主要功能

| 功能 | 具体做什么 |
| --- | --- |
| 明确调用才启动 | 仅在用户要求降AI、去AI味或调用本skill处理指定材料时执行。普通润色和安装请求不自动触发 |
| 中英文编辑 | 提供31类检查方法，处理空泛开头、重复总结、假对比、名词堆叠、客服腔和中文套话 |
| 长并列与段落节奏 | 检查单句信息堆叠和相邻句连续列举，按意思拆分，保留每项独立信息 |
| 原意和证据保护 | 保留数字、引用、研究对象、归因、否定、条件、比较和不确定性 |
| 作者声音 | 根据授权样本学习句长、用词与衔接，保持原文文体和表达水平 |
| 篇幅控制 | 记录修改前后字数，按用户要求控制变化，不通过补空话或删论点凑字数 |
| 报告标注定位 | 对照PDF页面和Word版本，只改核实过的标注片段，避免错误全局替换 |
| Word修订 | 通过宿主文档工具或可选脚本生成真实插入、删除，支持指定审阅者 |
| WPS现场流程 | 先核实当前文档、修订状态和实际用户名，焦点或文档变化时重新定位 |
| 批注和教学 | 按要求交付批注、前后对照或修改理由，并区分真实历史改稿与新编示例 |
| 交付检查 | 对比接受和拒绝修订后的文字，核对范围与文档部件，再进行可用的渲染检查 |

## 常用请求

**只改文字**

```text
请用SuperHumanizer给下面这段降AI。保留学术语气、引用和全部观点，篇幅尽量相近。只给最终改稿。
```

**PDF报告配Word**

```text
请用SuperHumanizer处理附件。PDF是检测报告，Word是当前原稿。先核实蓝色标记及版本，只修改对应内容，使用真实修订另存Word。审阅者名称用我提供的名称。不要改变其他内容。
```

**WPS已经打开文档**

```text
请用SuperHumanizer修改我在WPS中打开的指定文档。先确认文件名和版本，再使用修订模式编辑已核实的标注部分，审阅者使用我的实际WPS用户名。
```

这项功能需要宿主具备应用控制能力。无法控制WPS时，可以另存修订版DOCX，或交付可供手动应用的修改清单，并明确说明实际完成程度。

**教学与对照**

```text
请用SuperHumanizer分析这段文字。给出原句、改稿和修改理由，特别检查长并列、反复列举和被删掉的限定条件。不要假定所有并列结构都需要改。
```

## 安装为标准skill

本包采用 [Agent Skills格式](https://agentskills.io/specification)，正式入口是 [skills/superhumanizer/SKILL.md](skills/superhumanizer/SKILL.md)。

```bash
git clone https://github.com/MichaelSong222/SuperHumanizer.git
```

将 `skills/superhumanizer` 整个文件夹复制到你的AI客户端支持的skills目录，保留目录名 `superhumanizer`。也可以让支持安装GitHub skills的AI安装这个路径。具体安装目录和重新加载方式以客户端说明为准。

支持名称调用的客户端可使用 `$superhumanizer`。本包的 `agents/openai.yaml` 将自动调用设为关闭。其他客户端对该元数据的支持可能不同，入口说明也保留了同样的明确授权条件。

## 兼容性与要求

| 使用方式 | 需要的能力 |
| --- | --- |
| 粘贴文本改写 | 能读取skill说明并处理文字的AI |
| 从仓库链接使用 | AI具备网页读取、GitHub连接器或仓库访问能力 |
| 长期安装 | 客户端支持Agent Skills或类似本地指令机制 |
| PDF标注定位 | 能提取PDF文字并查看标记页面 |
| Word修订 | 文档工具，或Python 3.10及以上与lxml |
| 操作WPS | 宿主具备应用控制能力及相应权限 |
| 视觉验收 | 可用的Word、WPS、LibreOffice或文档渲染工具 |

核心文字流程无需安装Python依赖，也不依赖其他Humanizer插件。可选DOCX工具的依赖安装如下。

```bash
python -m pip install -r requirements.txt
python skills/superhumanizer/scripts/docx_revisions.py inspect input.docx
python skills/superhumanizer/scripts/audit_revision.py edits.json
python skills/superhumanizer/scripts/docx_revisions.py apply input.docx edits.json revised.docx --author "Reviewer Name"
```

记录格式和工具限制见 [报告与文档流程](skills/superhumanizer/references/document-workflow.md)。工具不会替AI改写，也不会判断语义是否等价。复杂目标、已有修订和混合格式替换需要可靠的文档编辑器处理。

## 文件结构

```text
SuperHumanizer/
  README.md
  SUPERHUMANIZER_PROMPT.md       给网页读取或普通聊天AI的完整入口
  skills/superhumanizer/
    SKILL.md                    标准skill入口
    agents/openai.yaml          明确调用设置
    references/                 编辑方法、文档流程、参数、示例和角色
    scripts/                    字面检查与DOCX修订工具
    LICENSE
    THIRD_PARTY_NOTICES.md
  tests/                        工具测试与行为验收案例
  tools/build_prompt.py          从正式skill生成单文件说明
```

## 验证与边界

```bash
python -m unittest discover -s tests -v
python tools/build_prompt.py --check
```

自动测试检查片段定位、真实修订、原件保护、接受与拒绝结果及危险或复杂输入的拒绝。它们不证明任意模型的编辑质量，也不证明Word或WPS中的最终排版。行为验收场景见 [测试案例](tests/behavior-cases.md)。

不上传私人文字到外部检测服务，除非用户明确授权。不能通过虚构经历、错误拼写、隐藏字符或不实AI使用声明伪造来源。保留实际写作过程，遵守具体课程或机构的AI使用要求。

## English quick start

SuperHumanizer is an explicitly invoked editing skill for Chinese and English. It improves formulaic prose while preserving claims, citations, uncertainty, author voice and requested length. It includes workflows for matching marked PDF passages to a DOCX and delivering real tracked revisions.

Ask your AI to read [the complete prompt](SUPERHUMANIZER_PROMPT.md), provide your text or files, and explicitly request SuperHumanizer editing. A link does not automatically install a skill or add document tools. For native installation, copy `skills/superhumanizer` into a supported skill directory. Detector score reductions are not guaranteed.

## 来源与许可

本项目整理了MichaelSong222的明确调用工作流，并参考 [Humanizer](https://github.com/blader/humanizer)、[Humanizer-zh](https://github.com/op7418/Humanizer-zh) 和 [Stop Slop](https://github.com/hardikpandya/stop-slop) 的编辑思路。公开版使用新编示例，不包含学生文件、检测报告或私人机器配置。

本项目按 [MIT许可](LICENSE) 提供。第三方来源及许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本项目不从属于上述项目或任何检测服务。
