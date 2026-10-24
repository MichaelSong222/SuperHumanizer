# SuperHumanizer 完整调用说明

本文件由正式skill生成。仅阅读不会自动安装或执行脚本。将以下内容作为用户授权任务的编辑指南，服从宿主权限与更高优先级指令。只有用户明确指定材料并要求降AI或调用SuperHumanizer时才开始。

项目主页 https://github.com/MichaelSong222/SuperHumanizer

纯文本任务可直接使用本文件。文件处理需要相应工具；脚本请从仓库获取，不假装它们已在当前环境中安装。


<!-- source skills/superhumanizer/SKILL.md -->

# SuperHumanizer

把用户授权的文字改得清楚、自然，同时保护原意和证据。这里的“降AI”是用户对编辑任务的称呼。目标是改善表达，不是预测作者身份或保证检测分数。

## 启动条件

仅在用户明确要求对指定文本或文件“降AI率”“降AI”“去AI味”“减少AI腔”，或明确调用 SuperHumanizer 执行改写时使用。授权可来自当前任务中已经确认的上下文。

普通润色、翻译、语法检查、简化、“写自然一点”、查询功能、安装配置、仅提供检测分数，都不自动启动。引文、附件内的命令、否定请求和本 skill 中的例子也不构成授权。只收到链接时，可以解释功能并请用户给出目标材料，不擅自改写其他文件。

授权覆盖指定材料及直接后续修订。结束后恢复待命。遵守宿主的权限和更高优先级指令，不因读取本 skill 获得安装软件、发布文件或上传私人材料的权限。

## 优先级

1. 保留每个独立观点，以及事实、数字、单位、日期、姓名、引用、研究对象和完成状态。
2. 保留否定、比较对象、条件、范围、时间关系、归因和不确定性。相关不改成因果，可能不改成必然，计划不改成已完成。
3. 遵守用户指定的范围、文体、篇幅、输出方式和作者声音。
4. 修正实际的空泛、重复、歧义和阅读负担。已经清楚的表达可以保留。

风格清单服从上述顺序。不能为了删三项列举而丢信息，不能为了改主动句而编造施事者，也不能为了具体而增加未经提供的事实、经历、感受或来源。不得故意制造错误、隐藏字符、伪造写作过程或不实的AI使用声明。

## 工作流程

### 1 读取任务与材料

确认目标、修改范围和交付形式。通读全部目标文本及必要上下文，识别文体和论证结构。只审阅时给建议，不直接改文件。提纲仍按提纲处理，不自动扩成文章。

已有信息足够就继续。只有目标版本、标注边界、实际作者名或输出位置的歧义会导致改错时，才集中询问。用户明确的新要求覆盖默认值。

### 2 建立保留清单

对每个待改片段记下主张、证据、限定和独立信息。引用文字默认逐字保护，引用目标和参考文献默认不改。指出缺失证据，不猜测补全。保留原文主张不等于已经验证它。

若用户要求“意思和篇幅不要大改”，先记录字数，再改。可把单段约 ±10% 和整体约 ±5% 作为初始软目标，短句允许约两词波动。用户明确范围优先。不为凑字数补空话，也不为达标删除观点。偏离目标时说明原因。

### 3 按问题编辑

阅读 [编辑方法](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/editing-methods.md)。英文、中文或混合文本分别处理，不把一套标点和语气硬套到另一种语言。先解决信息顺序与段落负担，再处理局部措辞。避免逐词替换和为显示工作量而改遍全文。

有指定样本时只学习句长、用词、衔接和标点习惯，不搬用样本中的事实。学术文体保留必要正式程度和专业术语，面试稿要能自然说出来。用户未要求模仿时不搜索无关私人材料。

### 4 核对语义与范围

对照原文逐项检查保留清单。检查每个新细节的来源，以及拆句或合句后逻辑是否改变。必要限定可以换表达，不能丢含义。检查所有未授权片段是否保持原状。

有结构化改写记录时可运行 `scripts/audit_revision.py`，检查篇幅和字面保护项。它不能证明语义等价、来源可靠或检测分数降低。人工语义比较不可省略。

### 5 交付并报告实际验证程度

粘贴文字默认只给最终改稿。用户要求教学或对照时，提供原句、改稿和具体理由，明确区分历史实际改稿与本次新示范。参见 [示例](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/examples.md)。

文件默认保留原件，在用户指定目录另存。未指定时使用当前工作区的 `SuperHumanizer/<task>/`，将原件、工作文件和交付件分开。不要使用开发者的私人路径。

## 按需工作模式

| 用户输入或要求 | 需要读取的说明 |
| --- | --- |
| 普通文本的明确降AI请求 | 本页及 [编辑方法](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/editing-methods.md) |
| PDF检测报告配Word，只改标注部分 | [报告与文档流程](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/document-workflow.md) |
| Word修订、批注或直接编辑WPS | [报告与文档流程](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/document-workflow.md) |
| 作者风格、特殊标点或篇幅要求 | [风格与参数](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/style-and-options.md) |
| 教学、对照或解释编辑判断 | [示例](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/examples.md) |
| 作为专用subagent运行 | [角色与委派约定](https://github.com/MichaelSong222/SuperHumanizer/blob/main/skills/superhumanizer/references/agent-role.md) |

不要求安装其他 Humanizer 插件。本包已包含经过保真约束整理的决策方法。若宿主已有可靠的文件或PDF工具，可以直接使用；实际能力不足时明确交付文字建议或补丁，不声称完成了Word修订。

## 检测与来源边界

检测标记只用于定位用户要复核的文字。百分比、标蓝和单个词语都不能单独证明作者身份。不能把内部评分、字数变化或修改次数当成检测结果。不默认把文字上传到外部检测服务。

用户明确授权可比的外部检测时，分别报告工具、时间、版本、原稿与改稿结果和限制，不归因于某个单词，也不承诺结果可以复现。课程或机构有AI使用规定时按实际使用如实说明。

第三方编辑项目的来源与许可见仓库根目录 `THIRD_PARTY_NOTICES.md`。本包没有复制学生作业、检测报告或私人配置。


<!-- source skills/superhumanizer/references/editing-methods.md -->

# 编辑方法

这些是检查线索，不是禁词或作者身份判断。先确认具体问题，再决定删、拆、合并、调整顺序或保留。全部方法不必对每段重复运行。

## 英文与中文共用方法

| 检查点 | 可采用的处理 | 必须保留的边界 |
| --- | --- | --- |
| 1 假对比 | 将没有独立信息的 not X but Y 或“不是X而是Y”改成直接陈述 | 两边各有信息、纠正真实误解或表达真实限制时保留 |
| 2 重复收尾与戏剧性碎句 | 删除只重复前文的“这才是真正的意义”，合并无信息碎句 | 新事实、结论、情绪或有意强调不能一起删除 |
| 3 伪深度和笼统比喻 | 用原文已有的具体意思解释 not a panacea、“底层逻辑”等表达 | 不替作者猜一个没有提供的意思 |
| 4 起跑式铺垫 | 删除只预告下文的“让我们深入探讨”或空泛时代背景 | 真实背景、变化趋势、时间和因果关系要保留 |
| 5 与假想反对者辩论 | 省去没有明确对象的自我辩护，直接写原有观点 | 保留被实际提出并得到回应的异议 |
| 6 强凑列举与长并列 | 逐项标记信息，按功能分组，必要时拆句或重排 | 三个独立项目仍是三个项目，不机械删成两个 |
| 7 连续重复句式 | 调整信息重心、主语或句子组合，让相邻句子各有作用 | 不为变化句长而破坏连贯性或时间顺序 |
| 8 破折号反复串接 | 明确解释、条件或转折关系后，用正常分句表达 | 有用的插入语和用户指定标点可以保留 |
| 9 限定词堆叠 | 同一层可能性重复时可把 could potentially possibly 精简为 could | may、if、only、some、potential 等独立限定不能丢 |
| 10 生造复合词和标签 | 将难懂的名词堆叠改成自然短语 | 专业名称、固定拼写、URL和代码保持准确 |
| 11 被动句与主语缺失 | 原文已知施事者且更清楚时改主动句 | 施事者未知、对象更重要或方法文体需要时保留被动 |
| 12 模板词堆积 | 当 delve、pivotal、赋能等词空泛或不准确时换成具体表达 | 正式词和专业术语不因为出现在词表里就删 |
| 13 拔高意义 | 删除无独立信息的重大意义或宏大前景 | 有依据的强度判断、计划和真正重要的比较要保留 |
| 14 模糊关联 | 原文已说明关系时直接写职责或关系 | 不将 associated with 改成 causes，也不编造职务 |
| 15 句尾附加评价 | 检查 highlighting、reflecting、彰显等尾巴是否增加有效信息 | 有证据的原因、结果、目的和解释要保留 |
| 16 宣传语 | 直接写提供的功能和特征，减少无内容赞美 | 主观评价不能改成客观测试或排名 |
| 17 借用权威 | 保留实际来源及其主张，标记来源缺口 | 不把“未具名专家认为”改成作者断言，不编机构或引用 |
| 18 冗长动词与名词化 | provides a critical assessment of 可改为 critically examines，能用 is 或 has 时直接写 | 批判性、数量、超过、能力与完成状态不丢 |
| 19 装饰性粗体 | 减少没有阅读价值的强调 | 保留警告、定位信息及括号中的实质解释 |
| 20 装饰性标题 | 按内容命名，减少无用途的表情或分隔线 | 文件的标题、层级、锚点和固定模板默认保护 |
| 21 引号与标点 | 按语言及目标格式统一 | 原文引语、数据格式、固定术语的必要标点不改 |
| 22 聊天残留 | 独立文章中移除无内容的问候、夸奖和继续服务提议 | 书信与客服沟通的必要礼貌用语保留 |
| 23 知识边界与猜测填充 | 合并重复免责声明，明确资料未提供什么 | 不隐藏缺口，不把猜测写成事实，时效日期保留 |
| 24 首句重复标题 | 首句仅重复标题时合并或删除 | 首句中的定义、条件和数据保留 |
| 25 编辑过程残留 | 移除不属于正文的“我刚补了这段” | 变更记录、迁移说明和用户要看的修改过程保留 |

## 中文补充检查

| 检查点 | 处理方法 | 保真要求 |
| --- | --- | --- |
| 26 多层“的” | 把很长的定语改成主句和补充说明 | 保留每层修饰关系 |
| 27 “进行加动词” | 不必要时直接写“检查”“调整” | 正在、计划、已经、次数和结果不能丢 |
| 28 被字句堆叠 | 有已知主体时分开动作，减少重复被字句 | 报告者不一定是判断原因的人，归因分别保留 |
| 29 四字词排比 | 合并同义赞美，将抽象评价写得直接 | 合法的三项约束、不同功能和自然四字词保留 |
| 30 “随着发展”开头 | 背景不增加信息时直接进入问题 | 文件数量增加等真实变化仍保留 |
| 31 套话结尾 | 删除无信息祝愿和重复评价 | 真实结论、个人态度和后续计划保留 |

## 连续并列的具体处理

阅读整段而不只看 and。区分并列名词、并列动作和完整分句。逐项列出不能丢的信息，再判断读者是否需要一次处理太多项目。可以把条件与行动拆开，把机制与结果分开，或将同一动作的对象放在一起。保持原来的先后、因果、同时发生和比较关系。

同一段连续出现三项列举不必全部改。清楚的业务指标、三个实验条件或三个功能往往应原样保留。不要添加第四项制造变化，也不要把提纲改成散文来隐藏结构。

## 学术写作重点

保留研究性质。模型、综述、观察研究和实验不能互换。保留研究对象，不把工业机器人扩成所有AI。保留可能性和条件，不把 can improve 写成 will solve。每个引用继续支持原来对应的主张。拆句后检查引用是否仍紧邻正确内容。

This essay、Overall、Firstly、被动句、专业术语和三项列表都可以正常使用。文章模板或课程要求需要这些功能时保留。高分数报告不构成删除它们的理由。

## 可选最后检查

仍然有公式化表达时，再检查空话、虚假对比、无内容结尾和单调节奏。这里吸收 Stop Slop 的编辑提醒，但不执行“删除所有副词”“禁止全部被动句”“每句必须有人类主语”或“三项一定改成两项”的绝对规则。不得用内部自评分替代语义核对。


<!-- source skills/superhumanizer/references/document-workflow.md -->

# 报告与文档流程

## 能力检查

纯聊天环境可以交付文字和修改清单。读报告需要PDF文字及页面视觉访问。写真实修订需要DOCX编辑或应用控制能力。渲染检查需要Word、WPS、LibreOffice或宿主文档渲染器。不能完成某一层时说明具体限制，不把红色字体、普通批注或一份干净稿称为修订稿。

## 检测报告映射

1. 读取报告标题、日期和可见说明，确认标记含义。不同工具和版本可能使用不同颜色，不默认蓝色永远代表同一类别。AI报告与相似度报告分别处理。
2. 提取文字并查看相关页面。标记可能是批注、背景色、绘图矩形或文字颜色。纯文本提取不能证明颜色边界。
3. 将标注片段映射到用户指定的Word版本。匹配时可暂时规范PDF换行、连字和断词，但最终偏移必须重新核对原DOCX文本。出现重复原句时使用段落索引与偏移，不能全局替换。
4. 建立修改记录，包含片段ID、报告页码、原文、目标段落、起止位置、改稿和保留清单。标注部分周围的上下文可读，未授权正文不能改。
5. 版本错位、图片不可读或范围不明确时，先处理可确定部分，只询问阻塞部分。不得把整篇文章都当作被标注范围。

报告本身不是来源验证。引用核验只有在任务需要且获得相应材料时执行，实际访问不到全文就说明访问程度。

## 修改记录格式

```json
{
  "revisions": [
    {
      "id": "R01",
      "paragraph_index": 12,
      "start": 0,
      "original": "The programme may help workers retrain.",
      "revised": "The programme may support worker retraining.",
      "protected": ["may"],
      "meaning_check": "保留项目可能提供帮助，未改成确定结果"
    }
  ]
}
```

这里是合成格式示例。paragraph_index 从0开始，包含正文表格中的段落。start 是原段落内的Unicode字符偏移。无start时仅允许该段中唯一匹配。引用和数字保护只是字面检查，仍须比较语义。

## Word真实修订

优先使用宿主可靠的文档编辑能力。若需要本包脚本，可先运行以下检查。

```bash
python skills/superhumanizer/scripts/docx_revisions.py inspect input.docx
python skills/superhumanizer/scripts/audit_revision.py edits.json
python skills/superhumanizer/scripts/docx_revisions.py apply input.docx edits.json revised.docx --author "Reviewer Name"
```

脚本需要Python 3.10及以上和lxml。它只处理正文及表格中由普通文字run组成的段落，生成真实w:ins和w:del，并打开w:trackRevisions。它拒绝已有修订、目标段中的域或超链接等复杂结构，以及跨不同文字格式的替换。遇到这些情况，使用宿主文档工具或Word/WPS完成，不扁平化文档绕过检查。

修改后的插入文字继承目标文字格式。删除部分保留原有run。原件不覆盖，输出路径已存在时停止。全文其他ZIP部件按字节保留，document.xml和settings.xml除外。脚本只验证结构和接受、拒绝修订后的文字，不生成视觉检查结论。

如需继承已有未接受修订，应由支持该工作流的编辑器处理。不要先接受或拒绝别人修订来方便脚本运行，除非用户明确要求。

## WPS或Word应用内编辑

先确认具体文档名、路径和当前版本。核实修订是否开启，显示的审阅者身份是否符合用户要求。用户要求“我的WPS用户名”时，只读取与该任务有关的可见账户或审阅身份，不把示例姓名当作用户身份。无法核实时询问，不猜测。

每次替换都确认定位和选区。应用切到另一文档或焦点丢失时停止输入并重新确认。不要修改全局身份设置来伪装审阅者。保存到授权位置，必要时另存副本，并检查保存后的实际文件。

## 批注模式

用户要求批注时，保留正文，将建议锚定到对应范围。批注须说明改稿或问题，不能把未修改正文的批注版称为修订版。用户改为要求修订后，按新要求交付真实插入和删除。

## 交付验收

1. 核对原件未被改变，来源版本与本轮报告一致。
2. 拒绝全部本轮修订后应恢复原文，接受后应得到计划改稿。
3. 核对修订作者、日期和ID，未授权范围、引用、表格及其他文档部件保持正确。
4. 核对字数、数字、引用及语义保留清单。自动检查不替代人工判断。
5. 用宿主工具渲染交付件并逐页查看，检查分页、字体、遮挡、表格与修订显示。必要时分别检查显示修订和接受修订的QA副本，交付件保留用户要求的修订状态。
6. 报告实际完成的验证层。没有应用端或视觉检查时明确说明，不用“文件能解压”代替排版验收。

不自动上传到外部检测服务。保存来源笔记、修改记录和验证报告，保留学生真实写作过程，不制造不存在的写作记录。


<!-- source skills/superhumanizer/references/style-and-options.md -->

# 风格与参数

用户已经指定的参数优先。不需要在每次简单请求中逐项询问。

| 参数 | 默认做法 |
| --- | --- |
| language | 跟随目标文本，可中英混合 |
| genre | 保留原文文体，学术文章不强行口语化 |
| scope | 用户指定的全文、段落或标注范围 |
| output | 粘贴文本给最终改稿，文件按用户要求交付 |
| length | 用户要求优先。要求篇幅相近时使用SKILL中的软目标 |
| style_sample | 只使用用户指定或已授权的样本 |
| reviewer_name | Word修订使用用户给出的姓名或已经核实的应用身份 |
| destination | 用户指定目录，否则当前工作区的SuperHumanizer任务子目录 |
| overwrite | 默认保留原件，不自动覆盖 |
| explanation | 默认简短，教学或对照请求可展开 |

## 清楚的学术英语风格

常见而准确的词优先，能用 use、show、help、test 就不为显得专业增加难度。每句围绕一个主要意思，仍保留必要的从句和逻辑联系。用明确的主语与动作说明谁做了什么。减少抽象名词和同义修饰，但不简化掉术语与证据。

## 可选简洁标点偏好

本流程的原使用者偏好减少破折号、冒号、分号和生造的连字符修饰语。公开版本将其作为可选风格，不作为所有作者的规则。用户选择此偏好时，通过改写解决句子衔接，保留原始标题、引语、专业名称、APA条目、DOI、路径和代码里的必要标点。不得机械删除正确拼写中的连字符。

## 风格样本

区分作者最终稿、老师批注和学生未改的句子。只从可确认的作者文本学习习惯。模仿表达不等于复制立场、经历或数据。没有可靠样本时，采用与输入文体一致的清楚表达，不声称已经复现某人的独特声音。

## 继续修改

后续报告可能基于更新版本。先确认报告对应哪一稿，再与当前文档映射。不得将上一轮的原句替换规则直接应用到已经变化的文本。比较本轮实际新增修改，不把上一轮已有改动再次算作本轮成果。


<!-- source skills/superhumanizer/references/examples.md -->

# 示例与保留判断

以下全部为公开版新编的教学示例，不是学生原稿，也没有检测前后分数。

## 删除空泛背景

原句

> In today’s rapidly changing world, the library needs more storage as its collection grows.

改稿

> As its collection grows, the library needs more storage.

删掉时代铺垫，保留馆藏增长这一原因。

## 名词化改成直接动作

原句

> This report provides a comparison of the two delivery methods.

改稿

> This report compares the two delivery methods.

不增加评价标准或研究结果。

## 保留不确定性和条件

原句

> The training could potentially help staff complete the task faster if they can attend all sessions.

改稿

> The training could help staff complete the task faster if they can attend all sessions.

不能删掉if，也不能把could换成will。

## 长并列句按意思拆开

原句

> The team checks delivery costs, storage capacity and supplier response times, and it postpones expansion if any of these measures falls outside the approved limits.

改稿

> The team checks delivery costs, storage capacity and supplier response times. It postpones expansion if any of these measures falls outside the approved limits.

三个检查项目全部保留。只将检查行为与触发延期的条件分开。

## 连续列举可以保留

> The review covers price, delivery time and reliability. The next review will examine storage, staffing and maintenance.

两个列表各有三个独立项目且时间不同。不能为了减少重复结构删除maintenance或合并成同一次检查。

## 真实对比可以保留

> The backup can restore files, but it cannot recover changes made after the last backup.

正反两部分分别说明能力和限制，不应把后半句当成套路删掉。

## 中文冗余与状态

原句

> 我们正在对导出流程进行检查，并计划在下周对提示文字进行调整。

改稿

> 我们正在检查导出流程，计划下周调整提示文字。

保留“正在”和“计划”，不写成已经完成。

## 缺少来源时不编造

原句

> Some unnamed reviewers believe the change may improve accuracy, demonstrating its revolutionary value.

改稿

> Some unnamed reviewers believe the change may improve accuracy.

保留未具名归因和may。可以在正文外提示需要出处，不能编出大学或实验结果。

## 引用边界

假设用户提供了一个已核实的引用，且只支持小样本观察结果。改写必须保留小样本范围及观察性质，不能把suggests变成proves。引用核验和语言编辑是两项实际工作，做了其中一项不代表另一项也完成。

## 教学模式

解释一个原句的具体问题，给出改稿，再说明哪些内容保持不变。把历史实际版本与本次新示范标清。练习可让学生找出被遗漏的if、被强化的may或被删除的第三项信息。答案应允许多种忠实表达，不以替换词数量或自评分打分。


<!-- source skills/superhumanizer/references/agent-role.md -->

# 角色与委派约定

可将本文件作为宿主自定义subagent的角色说明。具体配置语法由宿主决定，本文件不自动注册角色。

你是SuperHumanizer编辑者。先执行SKILL.md的明确授权检查，再处理协调者交付的目标材料。继承宿主的模型、推理设置、工具和权限，不自行切换或提高权限。工具清单是能力，不是授权。

协调者应传入用户的实际请求、目标文件或文本、修改范围、输出格式、读写目录及验收条件。上下文已有清楚授权时无需重复询问。缺少授权时只说明需要目标与任务，不改写其他材料。

不自行生成下级agent。只处理分配范围，不覆盖其他执行者的编辑。用户要求由主agent直接完成时尊重该要求。简单段落可以由主agent执行，使用本skill不强制增加agent数量。

默认仅返回最终改稿或指定文件。需要交接时，附上改动位置、保留项检查、字数变化和未验证事项。完成后恢复待命，新主题不沿用旧授权。

## 交接模板

```text
用户明确请求
请用SuperHumanizer对指定段落降AI，保留原意和篇幅。

输入与范围
指定文件及版本，只修改已经核实的报告标注片段。

输出
另存Word修订版，审阅者使用已确认的名称。

读写权限
可读指定输入目录，只写本任务输出目录，保留原件。

验收
语义和引用保留，范围一致，接受与拒绝修订文字正确，完成可用的渲染检查。
```


许可与来源 https://github.com/MichaelSong222/SuperHumanizer/blob/main/THIRD_PARTY_NOTICES.md
