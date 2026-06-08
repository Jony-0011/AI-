# 实训报告智能批改系统 - 开发日志

**项目名称**：实训报告智能批改系统  
**开发时间**：2026年6月  
**开发者**：[请填写姓名]

---

## 开发时间线

| 日期 | 阶段 | 主要工作 |
|------|------|----------|
| 2026-06-08 | 项目初始化 | 创建项目结构、配置文件、基础架构 |
| [请填写] | 模块开发 | 实现文档读取模块 |
| [请填写] | 模块开发 | 实现结构化比对模块 |
| [请填写] | 模块开发 | 实现自动评分模块 |
| [请填写] | 模块开发 | 实现评语生成模块 |
| [请填写] | 模块开发 | 实现报告输出模块 |
| [请填写] | 集成测试 | 完整系统测试、功能验证 |

---

## 开发过程记录

### 1. 需求分析与架构设计（提问记录）

**问题1**：如何设计项目的整体架构？
- **思考**：需要模块化设计，各个功能独立又能协同工作
- **决策**：采用模块化架构，分为读取、比对、评分、生成评语、输出五个核心模块
- **实现**：创建 document_reader.py、comparison.py、scoring.py、comment_generator.py、report_exporter.py

**问题2**：支持哪些文件格式？
- **思考**：优先支持 docx，后续可扩展 PDF
- **决策**：第一版仅支持 docx，使用 python-docx 库
- **实现**：DocumentReader 类专门处理 docx 文件

**问题3**：评分系统如何设计？
- **思考**：需要可配置、多维度评分
- **决策**：使用 JSON 配置文件，支持权重调整
- **实现**：ScoringEngine 类读取 scoring_config.json

---

### 2. 核心功能实现（代码生成过程）

#### 2.1 文档读取模块（document_reader.py）

**实现思路**：
- 使用 python-docx 库读取 docx 文件
- 提取段落文本和表格内容
- 解析文档中的图片信息

**关键代码**：
```python
def read_docx(self):
    doc = Document(self.file_path)
    text_parts = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)
    # ... 提取表格和图片
```

**遇到的问题**：
- 问题：图片提取较复杂
- 解决：通过 doc.part.rels 访问图片关系

---

#### 2.2 结构化比对模块（comparison.py）

**实现思路**：
- 使用 difflib 计算文本相似度
- 按章节标题进行结构比对
- 统计图片数量差异

**关键代码**：
```python
def calculate_text_similarity(self, text1, text2):
    seq_matcher = difflib.SequenceMatcher(None, text1, text2)
    return seq_matcher.ratio()
```

---

#### 2.3 自动评分模块（scoring.py）

**实现思路**：
- 多维度加权评分
- 每个维度独立计算
- 记录详细扣分依据

**关键代码**：
```python
def calculate_total_score(self, reference, student, comparison):
    # 分别计算各维度得分
    structure_score = self.score_structure(...)
    content_score = self.score_content(...)
    # ... 其他维度
    return sum(...)
```

---

#### 2.4 评语生成模块（comment_generator.py）

**实现思路**：
- 基于模板生成评语
- 根据评分结果选择积极或消极表述
- 生成针对性改进建议

---

#### 2.5 报告输出模块（report_exporter.py）

**实现思路**：
- 支持 JSON、TXT、HTML 三种格式
- HTML 格式带样式，方便展示
- 自动创建输出目录

---

### 3. 调试与优化（问题与解决）

**问题1**：模块导入错误
- **现象**：运行 main.py 时报错找不到模块
- **原因**：Python 路径问题
- **解决**：在 main.py 开头添加 sys.path.insert(0, ...)

**问题2**：中文编码问题
- **现象**：JSON 文件中中文显示乱码
- **原因**：未设置 ensure_ascii=False
- **解决**：json.dump(..., ensure_ascii=False)

**问题3**：[请补充遇到的其他问题]
- **现象**：
- **原因**：
- **解决**：

---

## 功能验证过程

### 测试用例1：单份报告批改

**测试步骤**：
1. 准备参考报告 reference.docx
2. 准备学生报告 student1.docx
3. 运行命令：`python src/main.py --reference ... --student ...`
4. 检查 outputs/ 目录下的结果文件

**测试结果**：
- [ ] 成功读取两份报告
- [ ] 正确计算相似度
- [ ] 评分结果合理
- [ ] 评语有针对性
- [ ] 三种格式输出正常

### 测试用例2：批量批改

**测试步骤**：
1. 在 reports/ 目录下放置多份学生报告
2. 运行命令：`python src/main.py --reference ... --dir ...`
3. 检查是否每份报告都有对应的输出

**测试结果**：
- [ ] 成功识别所有 docx 文件
- [ ] 批量处理顺利完成
- [ ] 错误处理正常

---

## 修改记录

| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| v1.0 | 2026-06-08 | 初始版本，实现核心功能 | [请填写] |
| [请填写] | [请填写] | [请填写] | [请填写] |

---

## 心得与体会

[请填写开发过程中的心得体会、收获和反思]

---

## 参考资料

1. python-docx 官方文档：https://python-docx.readthedocs.io/
2. Python difflib 模块：https://docs.python.org/3/library/difflib.html
3. [请补充其他参考资料]
