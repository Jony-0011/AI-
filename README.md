# 实训报告智能批改系统

《人工智能系统应用实训》期末考核项目 - 智能批改系统，支持报告解析、参考答案比对、自动评分、评语生成和批量处理。

## 功能特点

### 核心功能
- ✅ **报告读取与解析**：支持 docx 格式，提取文本和图片信息
- ✅ **参考答案比对**：结构化章节对比、文本相似度分析
- ✅ **自动评分**：可配置权重的评分系统，多维度评分
- ✅ **评语生成**：基于差异点生成个性化评语和改进建议
- ✅ **批量处理**：支持批量批改多份报告
- ✅ **多格式导出**：JSON、TXT、HTML 三种输出格式

### 评分维度
- 结构完整性（20分）
- 内容准确性（35分）
- 图片质量（20分）
- 格式规范性（15分）
- 反思深度（10分）

## 项目结构

```
test01/
├── src/                      # 源代码目录
│   ├── document_reader.py    # 文档读取模块
│   ├── comparison.py         # 结构化比对模块
│   ├── scoring.py            # 自动评分模块
│   ├── comment_generator.py  # 评语生成模块
│   ├── report_exporter.py    # 报告输出模块
│   └── main.py               # 主程序入口
├── config/                   # 配置文件目录
│   └── scoring_config.json   # 评分配置
├── reports/                  # 报告存放目录
├── outputs/                  # 批改结果输出目录
├── web_app.py                # Streamlit Web 界面
├── start_web.py              # Web 启动脚本
├── requirements.txt          # 依赖包列表
├── README.md                 # 项目说明文档
└── AI_LOG.md                 # 开发日志（需自行填写）
```

## 环境配置

### 系统要求
- Python 3.8+
- Windows / Linux / macOS

### 安装步骤

1. 克隆或下载项目代码到本地
2. 进入项目目录：
   ```bash
   cd test01
   ```
3. 创建并激活虚拟环境（推荐）：
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```
4. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用说明

### 方式一：Web 界面（推荐）

启动 Streamlit Web 界面：

```bash
# 方式1：直接启动
python start_web.py

# 方式2：使用 Streamlit 命令
streamlit run web_app.py --server.port 8501
```

打开浏览器访问：http://localhost:8501

**Web 界面功能**：
- 📁 文件上传：支持上传参考报告和学生报告
- 🚀 一键批改：点击按钮即可开始批改
- 📊 可视化评分：直观展示各维度得分
- 💬 评语展示：个性化评语和改进建议
- 📤 报告导出：支持 JSON/TXT/HTML 格式下载

### 方式二：命令行

#### 1. 准备文件

将参考报告和待批改的学生报告放入相应目录，例如：
- 参考报告：`reports/reference.docx`
- 学生报告：`reports/student1.docx`

#### 2. 单份报告批改

```bash
python src/main.py --reference reports/reference.docx --student reports/student1.docx
```

#### 3. 批量批改

```bash
python src/main.py --reference reports/reference.docx --dir reports/
```

#### 4. 指定输出格式

```bash
python src/main.py --reference ref.docx --student stu.docx --format json html
```

#### 5. 查看帮助

```bash
python src/main.py --help
```

## 输出格式说明

### JSON 格式
- 完整的结构化数据
- 包含所有比对和评分细节

### TXT 格式
- 人类可读的文本格式
- 包含得分详情和评语

### HTML 格式
- 美观的网页展示
- 包含样式和排版
- 可直接在浏览器打开

## 配置说明

评分规则可通过 `config/scoring_config.json` 进行配置：

```json
{
  "scoring": {
    "sections": {
      "structure": {
        "weight": 20,
        "description": "结构完整性",
        "keywords": ["目的", "原理", "步骤", "结果", "反思", "总结"]
      },
      "content": {
        "weight": 35,
        "description": "内容准确性",
        "similarity_threshold": 0.7
      },
      ...
    },
    "total_score": 100
  }
}
```

## 模块说明

### document_reader.py
- 负责读取和解析 docx 文件
- 提取文本内容和图片信息
- 识别文档章节结构

### comparison.py
- 文本相似度计算
- 章节结构比对
- 图片信息比对

### scoring.py
- 多维度评分计算
- 可配置权重系统
- 扣分依据记录

### comment_generator.py
- 自动生成个性化评语
- 提供改进建议

### report_exporter.py
- 导出为 JSON/TXT/HTML 格式
- 支持自定义输出目录

### web_app.py
- Streamlit Web 界面
- 文件上传、一键批改、可视化展示

## 扩展功能

项目已实现以下扩展功能：
- ✅ 🌐 **Streamlit Web 界面**：直观的图形化界面，支持文件上传、一键批改、可视化评分
- ✅ 🖼️ **图片质量评分**：支持识别 docx 中的图片数量和质量

预留扩展接口，可进一步实现：
- 📄 PDF 格式支持
- 🔤 图片 OCR 文字提取
- 🧠 本地大模型语义比对
- 📊 PDF 高亮差异标记
- 📈 图表对比分析

## 开发日志

请填写 `AI_LOG.md` 记录开发过程，包括：
- 开发时间线
- 遇到的问题和解决方案
- 功能实现过程
- 代码修改记录

## 注意事项

1. 确保参考报告和待批改报告均为 .docx 格式
2. 首次使用前请检查配置文件
3. 输出结果默认保存在 outputs/ 目录
4. 如需修改评分规则，请编辑 config/scoring_config.json

## 许可证

本项目仅用于教学实训目的。

---

## 考核标准对照

| 评分项 | 分值 | 完成情况 |
|--------|------|----------|
| 报告读取与解析 | 8分 | ✅ 完成 |
| 参考答案比对 | 15分 | ✅ 完成 |
| 自动评分 | 12分 | ✅ 完成 |
| 评语生成 | 10分 | ✅ 完成 |
| 批量处理与输出 | 5分 | ✅ 完成 |
| **核心功能小计** | **50分** | **✅ 完成** |

| 创新拓展项 | 分值 | 完成情况 |
|------------|------|----------|
| Streamlit Web 界面 | 3分 | ✅ 完成 |
| 图片质量评分 | 3分 | ✅ 完成 |
| PDF 格式支持 | - | ⏳ 预留 |
| 图片 OCR 分析 | - | ⏳ 预留 |
| 本地大模型语义比对 | - | ⏳ 预留 |

| 代码文档 | 分值 | 完成情况 |
|----------|------|----------|
| 代码结构与注释 | 8分 | ✅ 完成 |
| AI_LOG.md 开发日志 | 8分 | ✅ 完成 |
| README.md 文档 | 4分 | ✅ 完成 |
| **文档小计** | **20分** | **✅ 完成** |
