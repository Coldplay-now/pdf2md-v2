# 更新日志

## v1.0.5 (2025-11-04)

### ✨ 新增功能

- **详细进度日志**: 添加实时滚动日志显示
  - 每个处理步骤都有详细日志
  - 显示时间戳和处理状态
  - 自动滚动到最新日志
  - 美观的等宽字体显示
  - 影响：用户可以清楚看到处理进度，不再担心卡死

- **进度细化**: 更细粒度的进度显示
  - 显示当前处理的页码
  - 显示每页识别的字符数
  - 区分各个处理阶段
  - 影响：进度更加准确和透明

### 💅 界面改进

- 添加日志窗口（300px高度，可滚动）
- 自定义滚动条样式（紫色渐变）
- 使用图标增强可读性（✓ ✗ 📄 🤖 等）
- 最新日志高亮显示

---

## v1.0.4 (2025-11-04)

### 🐛 Bug修复

- **修复依赖缺失**: 添加 `sentencepiece>=0.1.99` 到 requirements.txt
  - 问题：tokenizer需要sentencepiece包但未在依赖中声明
  - 解决：更新requirements.txt，添加sentencepiece包
  - 影响：修复tokenizer初始化失败的问题

### ✨ 新增功能

- **测试脚本**: 添加完整的依赖和流程测试脚本
  - `test_dependencies.py` - 测试所有依赖包和模型加载
  - `test_full_pipeline.py` - 测试完整的PDF转换流程
  - 帮助快速诊断环境问题

---

## v1.0.3 (2025-11-04)

### 🐛 Bug修复

- **修复依赖缺失**: 添加 `protobuf>=3.20.0` 到 requirements.txt
  - 问题：transformers库需要protobuf包但未在依赖中声明
  - 解决：更新requirements.txt，添加protobuf包
  - 影响：修复模型加载失败的问题

---

## v1.0.2 (2025-11-04)

### 🐛 Bug修复

- **修复依赖缺失**: 添加 `torchvision>=0.15.0` 到 requirements.txt
  - 问题：PaddleOCR-VL模型需要torchvision包但未在依赖中声明
  - 解决：更新requirements.txt，添加torchvision包
  - 影响：修复模型加载失败的问题

---

## v1.0.1 (2025-11-04)

### 🐛 Bug修复

- **修复依赖缺失**: 添加 `einops>=0.7.0` 到 requirements.txt
  - 问题：PaddleOCR-VL模型需要einops包但未在依赖中声明
  - 解决：更新requirements.txt，添加einops包
  - 影响：修复模型加载失败的问题

### 📝 文档更新

- 更新README.md，添加依赖缺失问题的故障排查

---

## v1.0.0 (2025-11-04)

### ✨ 新功能

- **核心转换功能**
  - ✅ PDF转高清JPG（300 DPI）
  - ✅ OCR结构化识别（基于PaddleOCR-VL-0.9B）
  - ✅ 生成Markdown文档
  - ✅ 双重图片输出（原始+标注）

- **Web应用**
  - ✅ FastAPI后端服务
  - ✅ 现代化Web界面
  - ✅ 拖拽上传
  - ✅ 实时进度显示
  - ✅ RESTful API

- **管理脚本**
  - ✅ start.sh - 启动服务
  - ✅ stop.sh - 停止服务
  - ✅ restart.sh - 重启服务
  - ✅ 自动环境检查
  - ✅ 日志管理

### 📚 文档

- ✅ README.md - 完整项目文档
- ✅ QUICKSTART.md - 快速启动指南
- ✅ USAGE_EXAMPLES.md - 使用示例
- ✅ SCRIPTS_README.md - 脚本使用说明
- ✅ PROJECT_SUMMARY.md - 项目总结

### 🔧 技术栈

- Python 3.10+
- FastAPI + Uvicorn
- PaddleOCR-VL-0.9B
- PyMuPDF
- Transformers
- Torch

---

## 📝 升级说明

### 从 v1.0.0 升级到 v1.0.1

```bash
# 1. 停止服务
./stop.sh

# 2. 更新代码
git pull  # 如果使用git

# 3. 安装新依赖
pip install -r requirements.txt

# 4. 启动服务
./start.sh
```

---

## 🐛 已知问题

目前没有已知问题。

---

## 🔜 计划功能

- [ ] 批量PDF处理队列
- [ ] 多语言支持
- [ ] 更多输出格式（Word, HTML）
- [ ] 用户认证系统
- [ ] 处理历史记录
- [ ] Docker部署支持

---

**维护者**: AI Assistant  
**项目地址**: /personal/1102case/pdf-to-md-converter

