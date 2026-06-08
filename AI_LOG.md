# 实训报告智能批改系统 - 开发日志

**项目名称**：实训报告智能批改系统  
**开发时间**：2026年6月  
**开发者**：[请填写姓名]

---

## 开发时间线

| 日期 | 阶段 | 主要工作 |
|------|------|----------|
| 2026-06-08 | 项目初始化 | 创建项目结构、配置文件、基础架构 |
| 2026-06-08 | 模块开发 | 实现文档读取模块、结构化比对模块 |
| 2026-06-08 | 模块开发 | 实现自动评分模块、评语生成模块 |
| 2026-06-08 | 模块开发 | 实现报告输出模块、命令行入口 |
| 2026-06-08 | 扩展开发 | 实现 Streamlit Web 界面 |
| 2026-06-08 | 集成测试 | 完整系统测试、功能验证 |

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

**问题4**：是否需要 Web 界面？
- **思考**：命令行界面适合批量处理，但可视化界面更直观
- **决策**：同时提供命令行和 Web 界面
- **实现**：使用 Streamlit 开发 Web 界面

**问题5**：如何处理图片评分？
- **思考**：需要识别文档中的图片数量和质量
- **决策**：通过 python-docx 提取图片信息
- **实现**：在 DocumentReader 中添加图片提取逻辑

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
- 多维度加权评分，支持配置权重
- 每个维度独立计算，记录详细扣分依据
- 结构完整性、内容准确性、图片质量、格式规范性、反思深度五个维度

**关键代码**：
```python
class ScoringEngine:
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)

    def score_structure(self, section_comparison):
        """计算结构完整性得分"""
        config = self.config['scoring']['sections']['structure']
        weight = config['weight']
        match_ratio = section_comparison.get('section_match_ratio', 0.0)
        score = match_ratio * weight
        # 记录扣分原因
        return {'score': score, 'max_score': weight, 'deductions': [...]}

    def score_content(self, comparison_result):
        """计算内容准确性得分"""
        config = self.config['scoring']['sections']['content']
        weight = config['weight']
        similarity = comparison_result.get('text_similarity', 0.0)
        threshold = config.get('similarity_threshold', 0.7)
        
        if similarity >= threshold:
            score = weight
        else:
            score = (similarity / threshold) * weight
        return {'score': score, 'max_score': weight, 'similarity': similarity}

    def score_images(self, image_comparison):
        """计算图片质量得分"""
        config = self.config['scoring']['sections']['images']
        weight = config['weight']
        stu_count = image_comparison.get('student_count', 0)
        score_per_image = config.get('max_score_per_image', 5)
        score = min(stu_count * score_per_image, weight)
        return {'score': score, 'max_score': weight, 'count': stu_count}

    def calculate_total_score(self, reference, student, comparison):
        scores = {
            'structure': self.score_structure(...),
            'content': self.score_content(...),
            'images': self.score_images(...),
            'format': self.score_format(...),
            'reflection': self.score_reflection(...)
        }
        total_score = sum(s['score'] for s in scores.values())
        return {
            'total_score': round(total_score, 2),
            'percentage': round((total_score / total_max) * 100, 2),
            'section_scores': scores,
            'deductions': all_deductions
        }
```

**评分维度权重配置**（scoring_config.json）：
```json
{
    "scoring": {
        "total_score": 100,
        "sections": {
            "structure": {"weight": 20, "description": "结构完整性"},
            "content": {"weight": 35, "description": "内容准确性", "similarity_threshold": 0.7},
            "images": {"weight": 20, "description": "图片质量", "min_count": 3},
            "format": {"weight": 15, "description": "格式规范性"},
            "reflection": {"weight": 10, "description": "反思深度"}
        }
    }
}
```

---

#### 2.4 评语生成模块（comment_generator.py）

**实现思路**：
- 基于评分结果动态生成评语
- 每个维度独立生成评价
- 根据分数等级选择积极或改进表述
- 基于扣分原因生成针对性改进建议

**关键代码**：
```python
class CommentGenerator:
    def generate_content_comment(self, scoring_result):
        """生成内容相关评语"""
        content = scoring_result['section_scores']['content']
        score, max_score = content['score'], content['max_score']
        similarity = content.get('similarity', 0)
        ratio = score / max_score
        
        if ratio >= 0.8:
            return f"内容准确性得分{score:.1f}/{max_score}，相似度达{similarity:.1%}"
        elif ratio >= 0.5:
            return f"内容准确性得分{score:.1f}/{max_score}，核心内容基本覆盖"
        else:
            return f"内容准确性得分{score:.1f}/{max_score}，需要加强核心内容"

    def generate_suggestions(self, scoring_result):
        """根据扣分原因生成改进建议"""
        suggestions = []
        for deduction in scoring_result.get('deductions', []):
            reason = deduction.get('reason', '')
            if '缺少章节' in reason:
                suggestions.append("补充缺失的章节内容，完善报告结构")
            elif '内容相似度' in reason:
                suggestions.append("参考评分标准，加强核心内容的描述")
            elif '图片数量不足' in reason:
                suggestions.append("增加实验过程图片，丰富报告内容")
            elif '缺少反思' in reason:
                suggestions.append("认真总结实验收获，撰写深刻的反思内容")
        return suggestions

    def generate_comment(self, scoring_result):
        """生成完整的评语（≥100字）"""
        total_score = scoring_result['total_score']
        percentage = scoring_result['percentage']
        
        opening = f"本次实训报告得分：{total_score:.1f}分（{percentage:.1f}%）。\n\n"
        details = "各部分评分：\n"
        details += f"  - {self.generate_structure_comment(...)}"
        details += f"  - {self.generate_content_comment(...)}"
        details += f"  - {self.generate_image_comment(...)}"
        details += f"  - {self.generate_format_comment(...)}"
        details += f"  - {self.generate_reflection_comment(...)}"
        
        suggestions = self.generate_suggestions(scoring_result)
        suggestion_text = "改进建议：\n"
        for i, sug in enumerate(suggestions, 1):
            suggestion_text += f"  {i}. {sug}\n"
        
        closing = "\n希望在今后的实验中继续努力，不断提升！"
        return opening + details + suggestion_text + closing
```

**评语生成示例**：
```
本次实训报告得分：92.8分（92.8%）。

各部分评分：
  - 结构完整性得分15.8/20，部分章节有所缺失
  - 内容准确性得分35.0/35，相似度达83.9%，内容较为详实
  - 图片质量得分20.0/20，共4张图片，图文并茂
  - 格式规范性得分12.0/15，排版较为规范
  - 反思深度得分10.0/10，有较为深刻的总结和反思

改进建议：
  1. 补充缺失的章节内容，完善报告结构

希望在今后的实验中继续努力，不断提升！
```

---

#### 2.5 报告输出模块（report_exporter.py）

**实现思路**：
- 支持 JSON、TXT、HTML 三种格式
- HTML 格式带样式，方便展示
- 自动创建输出目录

---

#### 2.6 Web 界面模块（web_app.py）

**实现思路**：
- 使用 Streamlit 构建可视化界面
- 支持文件上传和一键批改
- 展示评分结果和评语
- 提供报告下载功能

**关键功能**：
- 📁 文件上传组件
- 🚀 一键批改按钮
- 📊 可视化评分展示
- 💬 评语展示
- 📤 多格式导出

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

**问题3**：类名不一致错误
- **现象**：Web 界面导入 DocumentComparer 失败
- **原因**：comparison.py 中的类名是 ReportComparator
- **解决**：修改 web_app.py 中的导入语句

**问题4**：端口占用问题
- **现象**：Streamlit 启动时提示端口已被占用
- **原因**：其他服务占用了 8501/8502 端口
- **解决**：使用新端口 8601

**问题5**：图片提取不完整
- **现象**：部分图片未被识别
- **原因**：docx 中图片存储方式不同
- **解决**：增加对 inline 图片的识别

---

## 功能验证过程

### 测试用例1：单份报告批改

**测试步骤**：
1. 准备参考报告 reference.docx
2. 准备学生报告 student1.docx
3. 运行命令：`python src/main.py --reference ... --student ...`
4. 检查 outputs/ 目录下的结果文件

**测试结果**：
- ✅ 成功读取两份报告
- ✅ 正确计算相似度
- ✅ 评分结果合理
- ✅ 评语有针对性
- ✅ 三种格式输出正常

### 测试用例2：含图片报告批改

**测试步骤**：
1. 准备含图片的学生报告
2. 运行批改命令
3. 检查图片评分是否正确

**测试结果**：
- ✅ 成功识别图片数量
- ✅ 图片质量评分正常
- ✅ 总分从 33.7 分提升到 92.8 分

### 测试用例3：Web 界面测试

**测试步骤**：
1. 启动 Web 服务器：`python start_web.py`
2. 上传参考报告和学生报告
3. 点击批改按钮
4. 查看评分结果

**测试结果**：
- ✅ Web 界面正常启动
- ✅ 文件上传功能正常
- ✅ 一键批改功能正常
- ✅ 可视化评分展示正常
- ✅ 报告导出功能正常

### 测试用例4：批量批改

**测试步骤**：
1. 在 reports/ 目录下放置多份学生报告
2. 运行命令：`python src/main.py --reference ... --dir ...`
3. 检查是否每份报告都有对应的输出

**测试结果**：
- [ ] 待测试

---

## 修改记录

| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| v1.0 | 2026-06-08 | 初始版本，实现核心功能 | [请填写] |
| v1.1 | 2026-06-08 | 添加图片评分功能 | [请填写] |
| v1.2 | 2026-06-08 | 添加 Streamlit Web 界面 | [请填写] |

---

## 心得与体会

[请填写开发过程中的心得体会、收获和反思]

---

## 参考资料

1. python-docx 官方文档：https://python-docx.readthedocs.io/
2. Python difflib 模块：https://docs.python.org/3/library/difflib.html
3. Streamlit 官方文档：https://docs.streamlit.io/
4. Pillow 官方文档：https://pillow.readthedocs.io/
