# 模型文件下载说明

由于GitHub对大文件的限制，模型文件（约2GB）未包含在此仓库中。

## 📥 需要下载的文件

1. **model.safetensors** (~1.8GB) - 主模型文件
2. **PP-DocLayoutV2/inference.pdiparams** (~203MB) - 布局检测参数
3. **PP-DocLayoutV2/inference.pdmodel** (~17MB) - 布局检测模型

## 🔽 下载方法

### 方法1：使用ModelScope CLI（推荐）

```bash
cd /path/to/project
pip install modelscope

python -c "
from modelscope import snapshot_download
snapshot_download('PaddlePaddle/PaddleOCR-vL-0.9B', 
                  cache_dir='./models', 
                  revision='master')
"
```

### 方法2：使用HuggingFace CLI

```bash
pip install huggingface-hub

huggingface-cli download PaddlePaddle/PaddleOCR-vL-0.9B \
    --local-dir ./models/paddleocr-vl
```

### 方法3：手动下载

访问以下任一平台下载：

- **ModelScope**: https://modelscope.cn/models/PaddlePaddle/PaddleOCR-vL-0.9B
- **HuggingFace**: https://huggingface.co/PaddlePaddle/PaddleOCR-vL-0.9B

下载后将文件放置到此目录下，保持以下结构：

```
models/paddleocr-vl/
├── model.safetensors
├── PP-DocLayoutV2/
│   ├── inference.pdiparams
│   ├── inference.pdmodel
│   └── ...
└── (其他配置文件已包含在仓库中)
```

## ✅ 验证安装

下载完成后，确认文件存在：

```bash
ls -lh models/paddleocr-vl/model.safetensors
ls -lh models/paddleocr-vl/PP-DocLayoutV2/inference.pdiparams
```

如果文件存在且大小正确，就可以开始使用了！

## 📝 注意事项

- 确保有足够的磁盘空间（至少3GB）
- 下载可能需要较长时间，请耐心等待
- 建议使用稳定的网络连接

