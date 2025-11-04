# 快速启动指南

## 🚀 5分钟快速启动

### 1. 确认环境

```bash
python --version  # 确保 >= 3.10
```

### 2. 安装依赖

```bash
cd /personal/1102case/pdf-to-md-converter
pip install -r requirements.txt
```

### 3. 启动服务

**方式一：使用启动脚本（推荐）**

```bash
./start.sh
```

**方式二：直接运行**

```bash
python app.py
```

**其他脚本命令：**

```bash
./stop.sh      # 停止服务
./restart.sh   # 重启服务
```

### 4. 访问应用

打开浏览器访问: http://localhost:8000

## 📝 第一次使用

1. **上传PDF**: 将PDF文件拖拽到上传区域
2. **开始转换**: 点击"开始转换"按钮
3. **等待处理**: 查看实时进度（约1-2秒/页）
4. **下载结果**: 
   - 点击下载Markdown文档
   - 或在 `outputs/{task_id}/` 查看所有输出文件

## 📂 输出文件说明

```
outputs/{task_id}/
├── pages/
│   ├── page_001.jpg           # 原始JPG（300 DPI）
│   ├── page_001_annotated.jpg # 带标注的JPG
│   └── ...
├── document.md                # 完整的Markdown文档
├── ocr_results.json          # OCR原始数据（JSON格式）
└── metadata.json             # 处理元数据
```

## 🔍 测试API

### 健康检查

```bash
curl http://localhost:8000/api/health
```

### 上传并处理PDF

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@test.pdf"
```

## ⚙️ 配置选项

### 修改端口（app.py）

```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # 改为其他端口
```

### 修改DPI设置（app.py）

```python
pdf_processor = PDFProcessor(dpi=300)  # 150-600均可
```

### 修改模型路径（converter/ocr_processor.py）

```python
def __init__(self, model_path: str = "/your/path"):
```

## 🐛 故障排查

### 查看服务日志

```bash
# 实时查看日志
tail -f app.log

# 查看最后100行日志
tail -n 100 app.log
```

### 问题1: 模块导入错误

```bash
# 确保在项目根目录
cd /personal/1102case/pdf-to-md-converter
python app.py
```

### 问题2: 端口被占用

```bash
# 使用start.sh会自动检测端口占用
./start.sh

# 或手动杀死占用进程
lsof -ti:8000 | xargs kill -9
```

### 问题3: 模型加载失败

```bash
# 检查模型路径
ls -la /personal/1102case/models/paddleocr-vl
```

### 问题4: 服务启动失败

```bash
# 查看详细错误日志
cat app.log

# 停止所有相关进程后重新启动
./stop.sh
./start.sh
```

### 问题5: 脚本没有执行权限

```bash
# 添加执行权限
chmod +x start.sh stop.sh restart.sh
```

## 💡 性能优化建议

- **GPU加速**: 确保CUDA可用，自动启用GPU
- **内存优化**: 处理大PDF时可降低DPI
- **并发处理**: 当前版本单任务队列，后续可优化

## 📚 更多信息

- 详细文档: [README.md](README.md)
- API文档: http://localhost:8000/docs
- 项目结构: 查看 [README.md#项目结构](README.md)

## 🎉 完成！

现在您可以开始使用PDF to Markdown Converter了！

