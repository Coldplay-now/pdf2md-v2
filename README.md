<div align="center">

# 📄 PDF2MD-V2

**基于 PaddleOCR-VL 的智能 PDF 转 Markdown 文档转换系统**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-00a393.svg)](https://fastapi.tiangolo.com/)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR--VL-0.9B-orange.svg)](https://github.com/PaddlePaddle/PaddleOCR)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Coldplay-now/pdf2md-v2?style=social)](https://github.com/Coldplay-now/pdf2md-v2/stargazers)

[功能特性](#-核心功能) • [快速开始](#-快速开始) • [安装部署](#️-首次使用下载模型文件) • [技术栈](#-技术栈) • [文档](#-相关文档)

---

### 🎯 项目展示

<img src="docs/images/screenshot.png" alt="PDF2MD-V2 界面展示" width="800">

</div>

## 📁 目录结构

```
pdf2md-v2/
├── pdf-to-md-converter/    # 主项目：PDF转Markdown转换器
│   ├── app.py             # FastAPI Web应用
│   ├── converter/         # 核心转换模块
│   ├── static/           # 前端静态资源
│   ├── templates/        # HTML模板
│   ├── uploads/          # 上传文件存储
│   └── outputs/          # 转换结果输出
│
├── models/                # AI模型文件
│   └── paddleocr-vl/     # PaddleOCR-VL-0.9B模型
│
├── temp/                  # 临时文件目录（可删除）
│   ├── test_scripts/     # 测试脚本
│   ├── test_data/        # 测试数据
│   ├── install_files/    # 安装文件
│   └── docs/            # 临时文档
│
└── 文档/
    ├── PaddleOCR本地部署规划.md     # 部署规划文档
    ├── DeepSeek-OCR部署规划.md       # DeepSeek OCR规划
    └── 部署完成总结.md              # 部署总结
```

## ⚠️ 首次使用：下载模型文件

由于模型文件较大（约2GB），未包含在Git仓库中。首次使用前需要下载：

### 方法1：从ModelScope下载（推荐）

```bash
# 确保已安装modelscope
pip install modelscope

# 下载模型到正确位置
python -c "
from modelscope import snapshot_download
snapshot_download('PaddlePaddle/PaddleOCR-vL-0.9B', cache_dir='./models', revision='master')
"
```

### 方法2：从HuggingFace下载

```bash
# 确保已安装huggingface-hub
pip install huggingface-hub

# 下载模型
huggingface-cli download PaddlePaddle/PaddleOCR-vL-0.9B --local-dir ./models/paddleocr-vl
```

### 方法3：手动下载

访问 [ModelScope](https://modelscope.cn/models/PaddlePaddle/PaddleOCR-vL-0.9B) 下载以下文件到 `models/paddleocr-vl/` 目录：
- `model.safetensors` (~1.8GB)
- `PP-DocLayoutV2/inference.pdiparams` (~203MB)
- `PP-DocLayoutV2/inference.pdmodel` (~17MB)

## 🚀 快速开始

### 安装依赖

```bash
# 进入项目目录
cd pdf-to-md-converter

# 安装Python依赖
pip install -r requirements.txt
```

### 启动Web应用

```bash
cd pdf-to-md-converter
bash start.sh
```

访问: http://localhost:8000

### 使用步骤

1. **打开浏览器** - 访问 `http://localhost:8000`
2. **选择文件** - 点击或拖拽PDF文件到上传区域
3. **开始转换** - 点击"开始转换"按钮
4. **查看进度** - 实时查看转换进度和详细日志
5. **下载结果** - 转换完成后预览并下载Markdown文件

### 停止应用

```bash
cd pdf-to-md-converter
bash stop.sh
```

### 重启应用

```bash
cd pdf-to-md-converter
bash restart.sh
```

## ✨ 核心功能

### 📄 智能文档转换
- **PDF图片化**: 自动将PDF的每一页转换为高质量图片
- **批量处理**: 支持多页PDF文档的批量OCR识别
- **格式保留**: 尽可能保留原文档的结构和格式
- **Markdown输出**: 生成标准格式的Markdown文档

### 🤖 高精度OCR识别
- **PaddleOCR-VL-0.9B**: 基于最新的视觉语言模型
- **多语言支持**: 支持中文、英文及多种语言混合识别
- **版面分析**: 智能识别标题、段落、列表等文档结构
- **表格识别**: 支持表格内容的识别和转换
- **GPU加速**: 利用GPU显著提升处理速度

### 🌐 现代化Web界面
- **拖拽上传**: 支持文件拖拽上传，操作便捷
- **实时进度**: 动态显示处理进度条和百分比
- **详细日志**: 实时展示处理过程中的每一步操作
- **结果预览**: 在线预览转换后的Markdown内容
- **一键下载**: 直接下载生成的Markdown文档
- **响应式设计**: 支持桌面和移动设备访问

### 📊 处理流程
1. **文件上传** → 用户上传PDF文档
2. **PDF解析** → 将PDF转换为图片序列
3. **OCR识别** → 使用PaddleOCR-VL识别文字
4. **结构分析** → 分析文档布局和层次结构
5. **格式转换** → 生成Markdown格式文档
6. **结果输出** → 提供预览和下载

### 🔒 数据安全
- **本地运行**: 所有处理完全在本地服务器进行
- **无需联网**: 不依赖任何外部API服务
- **数据私密**: 上传的文件不会发送到任何第三方
- **可控删除**: 用户可随时删除处理结果

### 📈 性能特点
- **GPU加速**: 充分利用CUDA加速OCR识别
- **异步处理**: 后台异步处理，不阻塞界面
- **进度追踪**: 实时查询任务状态和进度
- **高效转换**: 单页处理速度约2-5秒（取决于GPU性能）

### 📦 输出内容
每次转换会生成：
- `document.md` - Markdown格式的文档
- `ocr_results.json` - 完整的OCR识别结果
- `metadata.json` - 处理元数据和统计信息
- `pages/` - PDF转换的图片文件（可选保留）

## 🎯 适用场景

- 📚 学术论文转文本
- 📖 电子书内容提取
- 📝 合同文档数字化
- 📊 报告文档转换
- 🗂️ 扫描件文字识别
- 📄 历史文档数字化保存

## 🔧 技术栈

- **后端**: FastAPI + Python 3.10
- **前端**: 原生HTML/CSS/JavaScript
- **OCR引擎**: PaddleOCR-VL-0.9B
- **PDF处理**: PyMuPDF (fitz)
- **GPU加速**: PaddlePaddle GPU

## 📝 相关文档

- [项目完整文档](pdf-to-md-converter/README.md)
- [快速开始指南](pdf-to-md-converter/QUICKSTART.md)
- [变更日志](pdf-to-md-converter/CHANGELOG.md)
- [脚本说明](pdf-to-md-converter/SCRIPTS_README.md)

## 🗑️ 清理说明

`temp/` 目录包含开发和测试文件，不影响主项目运行。如果磁盘空间紧张，可以安全删除：

```bash
rm -rf temp/
```

## 📊 系统要求

- **操作系统**: Linux (推荐 Ubuntu 20.04+)
- **Python**: 3.10+
- **GPU**: NVIDIA GPU with CUDA 11.8+
- **内存**: 至少8GB
- **存储**: 至少10GB可用空间

---

**项目状态**: ✅ 生产就绪

**最后更新**: 2025年11月4日

