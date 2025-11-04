# PDF2MD-V2

基于 PaddleOCR-VL 的智能 PDF 转 Markdown 文档转换系统

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

### 启动Web应用

```bash
cd pdf-to-md-converter
bash start.sh
```

访问: http://localhost:8000

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

## 📖 主要功能

- **PDF转换**: 上传PDF文件，自动转换为Markdown格式
- **OCR识别**: 使用PaddleOCR-VL进行高精度文字识别
- **实时进度**: Web界面实时显示转换进度和日志
- **结果预览**: 在线预览转换后的Markdown内容

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

