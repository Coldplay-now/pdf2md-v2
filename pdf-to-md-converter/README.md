# PDF to Markdown Converter

基于 **PaddleOCR-VL-0.9B** 模型的智能文档转换工具，将PDF文档转换为高质量的Markdown格式，同时生成原始和标注JPG图片。

## ✨ 功能特性

- 📄 **PDF转换**: 将PDF每一页转换为高清JPG图片（300 DPI）
- 🖼️ **双重输出**: 生成原始图片和带标注的可视化图片
- 📝 **结构化识别**: 智能识别文档结构（标题、段落、表格、公式等）
- 📋 **Markdown生成**: 自动生成结构化的Markdown文档
- 🌐 **Web界面**: 现代化的Web界面，支持拖拽上传
- ⚡ **实时进度**: 实时显示处理进度和状态
- 💾 **批量处理**: 支持多页PDF的批量识别
- 🔒 **本地运行**: 完全在本地运行，数据安全有保障

## 🎯 技术栈

- **后端**: FastAPI + Uvicorn
- **OCR模型**: PaddleOCR-VL-0.9B (Transformers)
- **PDF处理**: PyMuPDF
- **图像处理**: Pillow + OpenCV
- **前端**: HTML5 + CSS3 + JavaScript (原生)

## 📋 系统要求

### 基础要求

- Python 3.10 或更高版本
- 8GB+ RAM
- 10GB+ 可用磁盘空间

### 推荐配置

- Python 3.10
- 16GB+ RAM
- NVIDIA GPU（显存4GB+，可选但推荐）
- 20GB+ 可用磁盘空间

## 🚀 快速开始

### 1. 克隆或下载项目

```bash
cd /path/to/your/workspace
# 项目已在 /personal/1102case/pdf-to-md-converter
```

### 2. 创建虚拟环境（推荐）

```bash
# 使用venv
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 使用conda
conda create -n pdf-converter python=3.10 -y
conda activate pdf-converter
```

### 3. 安装依赖

```bash
cd pdf-to-md-converter
pip install -r requirements.txt
```

### 4. 配置模型路径

确保PaddleOCR-VL-0.9B模型已下载到正确位置：

```bash
# 默认模型路径: /personal/1102case/models/paddleocr-vl
# 如需修改，请编辑 converter/ocr_processor.py 中的 model_path 参数
```

### 5. 启动Web应用

**方式一：使用启动脚本（推荐）**

```bash
./start.sh
```

启动脚本会自动：
- ✅ 检查Python环境和依赖
- ✅ 检查模型路径
- ✅ 检查端口占用
- ✅ 后台运行服务
- ✅ 保存进程PID
- ✅ 显示访问地址

**方式二：直接运行**

```bash
python app.py
```

**服务管理命令：**

```bash
./start.sh      # 启动服务
./stop.sh       # 停止服务
./restart.sh    # 重启服务
tail -f app.log # 查看日志
```

服务将在 `http://localhost:8000` 启动。

### 6. 访问Web界面

打开浏览器访问：
- 主页: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📖 使用说明

### Web界面使用

1. **上传PDF**: 
   - 拖拽PDF文件到上传区域
   - 或点击上传区域选择文件

2. **开始转换**: 
   - 点击"开始转换"按钮
   - 系统会自动处理PDF并显示实时进度

3. **查看结果**: 
   - 转换完成后会显示统计信息
   - 可以预览Markdown内容
   - 点击"下载Markdown文档"获取结果

4. **输出文件**: 
   所有输出文件保存在 `outputs/{task_id}/` 目录下：
   ```
   outputs/{task_id}/
   ├── pages/
   │   ├── page_001.jpg           # 原始图片
   │   ├── page_001_annotated.jpg # 标注图片
   │   ├── page_002.jpg
   │   └── ...
   ├── document.md                # Markdown文档
   ├── ocr_results.json          # OCR原始结果
   └── metadata.json             # 元数据
   ```

### API使用

#### 上传PDF并处理

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@your_document.pdf"
```

返回：
```json
{
  "success": true,
  "task_id": "uuid-string",
  "message": "文件上传成功，开始处理..."
}
```

#### 查询任务状态

```bash
curl "http://localhost:8000/api/status/{task_id}"
```

#### 下载Markdown文档

```bash
curl -O "http://localhost:8000/api/download/{task_id}/markdown"
```

#### 下载图片

```bash
curl -O "http://localhost:8000/api/download/{task_id}/images/page_001.jpg"
```

## 📁 项目结构

```
pdf-to-md-converter/
├── app.py                      # FastAPI主应用
├── converter/                  # 核心转换模块
│   ├── __init__.py
│   ├── pdf_processor.py        # PDF转JPG处理器
│   ├── ocr_processor.py        # OCR识别处理器
│   └── markdown_generator.py  # Markdown生成器
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css          # 样式表
│   └── js/
│       └── main.js            # 前端脚本
├── templates/
│   └── index.html             # Web界面模板
├── uploads/                    # 上传文件临时目录
├── outputs/                    # 输出文件目录
├── requirements.txt           # Python依赖
├── .gitignore                 # Git忽略文件
└── README.md                  # 项目说明
```

## ⚙️ 配置说明

### 修改模型路径

编辑 `converter/ocr_processor.py`：

```python
def __init__(self, model_path: str = "/your/model/path"):
    ...
```

### 修改DPI设置

编辑 `app.py`：

```python
pdf_processor = PDFProcessor(dpi=300)  # 修改DPI值
```

### 修改服务端口

编辑 `app.py`：

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,  # 修改端口号
    log_level="info"
)
```

## 🔧 常见问题

### 1. 依赖包缺失

**问题**: 提示缺少某个Python包（如 einops, timm 等）

**解决**:
```bash
# 重新安装所有依赖
pip install -r requirements.txt

# 或安装特定包
pip install einops

# 重启服务
./restart.sh
```

### 2. 模型加载失败

**问题**: 提示找不到模型文件

**解决**: 
- 检查模型路径是否正确
- 确保模型文件完整下载
- 检查文件权限

### 3. GPU内存不足

**问题**: CUDA Out of Memory

**解决**:
- 减小PDF的DPI设置（默认300，可降至150）
- 使用CPU模式（自动降级）
- 分批处理大型PDF

### 4. 识别结果不准确

**问题**: OCR识别质量不理想

**解决**:
- 提高PDF转图片的DPI（300-600）
- 确保PDF清晰度良好
- 检查PDF是否为扫描件

### 5. 处理速度慢

**问题**: 转换速度较慢

**解决**:
- 使用GPU加速（推荐）
- 降低DPI设置
- 升级硬件配置

## 📊 性能参考

| 硬件配置 | 处理速度 | 备注 |
|---------|---------|------|
| CPU (8核) | ~5-10秒/页 | 基础配置 |
| RTX 3060 | ~1-2秒/页 | 推荐配置 |
| RTX 4090 | ~0.5-1秒/页 | 高性能配置 |

*基于10页PDF、300 DPI设置的测试结果*

## 🛠️ 开发

### 运行测试

```bash
# 测试PDF处理器
python -c "from converter.pdf_processor import PDFProcessor; PDFProcessor().pdf_to_images('test.pdf', 'output')"

# 测试OCR处理器
python -c "from converter.ocr_processor import OCRProcessor; OCRProcessor().process_image('test.jpg')"
```

### 调试模式

```bash
# 启用调试日志
uvicorn app:app --reload --log-level debug
```

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - OCR模型
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF处理

## 📧 联系方式

如有问题或建议，欢迎提Issue或PR。

## 🔄 更新日志

### v1.0.0 (2025-11-04)

- ✨ 初始版本发布
- 📄 支持PDF转JPG
- 🖼️ 生成原始和标注图片
- 📝 结构化Markdown输出
- 🌐 Web界面
- 📡 RESTful API

## 🚀 未来计划

- [ ] 支持批量PDF处理
- [ ] 添加多语言支持
- [ ] 优化识别准确率
- [ ] 支持更多输出格式（Word、HTML等）
- [ ] 添加用户认证
- [ ] 数据库存储支持

---

**Made with ❤️ using PaddleOCR-VL-0.9B**

