#!/usr/bin/env python3
"""
PDF to Markdown Converter Web Application
FastAPI后端服务
"""

import os
import uuid
import json
import shutil
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

from converter.pdf_processor import PDFProcessor
from converter.ocr_processor import OCRProcessor
from converter.markdown_generator import MarkdownGenerator


# 初始化FastAPI应用
app = FastAPI(
    title="PDF to Markdown Converter",
    description="基于PaddleOCR-VL-0.9B的PDF文档转换服务",
    version="1.0.0"
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置目录
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

# 确保目录存在
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 全局处理器（单例）
pdf_processor = PDFProcessor(dpi=300)
ocr_processor = None  # 延迟加载（模型较大）
markdown_generator = MarkdownGenerator()

# 任务状态存储（简单实现，生产环境应使用数据库或Redis）
tasks: Dict[str, Dict[str, Any]] = {}


def get_ocr_processor():
    """获取OCR处理器实例（延迟加载）"""
    global ocr_processor
    if ocr_processor is None:
        ocr_processor = OCRProcessor()
    return ocr_processor


async def process_pdf_task(task_id: str, pdf_path: str):
    """
    异步处理PDF任务
    
    Args:
        task_id: 任务ID
        pdf_path: PDF文件路径
    """
    # 初始化日志列表
    tasks[task_id]["logs"] = []
    
    def add_log(message: str):
        """添加日志消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        tasks[task_id]["logs"].append(log_entry)
        print(log_entry)
    
    try:
        # 更新任务状态
        tasks[task_id]["status"] = "processing"
        tasks[task_id]["progress"] = 5
        tasks[task_id]["message"] = "开始处理..."
        add_log("✓ 任务开始处理")
        
        tasks[task_id]["progress"] = 10
        tasks[task_id]["message"] = "正在转换PDF为图片..."
        add_log("📄 开始转换PDF为图片...")
        
        # 创建输出目录
        output_dir = OUTPUT_DIR / task_id
        pages_dir = output_dir / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        
        # 步骤1: PDF转图片
        add_log(f"  - 输出目录: {pages_dir}")
        image_paths = pdf_processor.pdf_to_images(pdf_path, str(pages_dir))
        add_log(f"✓ PDF转换完成，共 {len(image_paths)} 页")
        tasks[task_id]["progress"] = 30
        tasks[task_id]["message"] = f"已转换 {len(image_paths)} 页为图片"
        
        # 步骤2: OCR识别
        tasks[task_id]["progress"] = 35
        tasks[task_id]["message"] = "正在加载OCR模型..."
        add_log("🤖 正在加载OCR模型...")
        
        processor = get_ocr_processor()
        add_log("✓ OCR模型加载完成")
        
        tasks[task_id]["progress"] = 40
        tasks[task_id]["message"] = f"正在识别第 1/{len(image_paths)} 页..."
        add_log(f"📝 开始OCR识别，共 {len(image_paths)} 页")
        
        # 批量处理，带进度更新
        ocr_results = []
        for idx, img_path in enumerate(image_paths, 1):
            progress = 40 + int((idx / len(image_paths)) * 30)
            tasks[task_id]["progress"] = progress
            tasks[task_id]["message"] = f"正在识别第 {idx}/{len(image_paths)} 页..."
            add_log(f"  - 处理第 {idx}/{len(image_paths)} 页: {Path(img_path).name}")
            
            try:
                result = processor.process_image(img_path, task_type="ocr")
                annotated_path = pages_dir / f"{Path(img_path).stem}_annotated.jpg"
                processor.create_annotated_image(img_path, result, str(annotated_path))
                result["annotated_image"] = str(annotated_path)
                ocr_results.append(result)
                add_log(f"    ✓ 识别成功 ({len(result['result'])} 字符)")
            except Exception as e:
                add_log(f"    ✗ 识别失败: {str(e)}")
                ocr_results.append({"image_path": img_path, "error": str(e)})
        
        add_log(f"✓ OCR识别完成，成功 {len([r for r in ocr_results if 'error' not in r])}/{len(image_paths)} 页")
        
        tasks[task_id]["progress"] = 70
        tasks[task_id]["message"] = "OCR识别完成，生成Markdown..."
        add_log("📋 开始生成Markdown文档...")
        
        # 步骤3: 生成Markdown
        pdf_name = Path(pdf_path).stem
        generator = MarkdownGenerator()
        add_log("  - 解析OCR结果...")
        markdown_content = generator.generate_from_ocr_results(ocr_results, pdf_name)
        add_log(f"  - 生成Markdown文档 ({len(markdown_content)} 字符)")
        
        # 保存Markdown文件
        md_path = output_dir / "document.md"
        generator.save_to_file(str(md_path))
        add_log(f"✓ Markdown已保存: {md_path.name}")
        
        # 保存OCR结果JSON
        json_path = output_dir / "ocr_results.json"
        processor.save_results(ocr_results, str(json_path))
        add_log(f"✓ OCR结果已保存: {json_path.name}")
        
        # 生成元数据
        add_log("📊 生成处理摘要...")
        summary = generator.generate_summary(ocr_results)
        add_log(f"  - 总页数: {summary['total_pages']}")
        add_log(f"  - 成功页数: {summary['successful_pages']}")
        add_log(f"  - 识别字符数: {summary['total_characters']}")
        
        metadata = {
            "task_id": task_id,
            "pdf_name": pdf_name,
            "processed_at": datetime.now().isoformat(),
            "summary": summary,
            "files": {
                "markdown": str(md_path.relative_to(OUTPUT_DIR)),
                "ocr_json": str(json_path.relative_to(OUTPUT_DIR)),
                "images": [str(Path(p).relative_to(OUTPUT_DIR)) for p in image_paths]
            }
        }
        
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        add_log(f"✓ 元数据已保存: {metadata_path.name}")
        
        # 任务完成
        add_log("=" * 50)
        add_log("🎉 处理完成！")
        add_log(f"✓ 输出目录: {output_dir}")
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["progress"] = 100
        tasks[task_id]["message"] = "处理完成！"
        tasks[task_id]["result"] = metadata
        
    except Exception as e:
        add_log(f"✗ 处理失败: {str(e)}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["message"] = f"处理失败: {str(e)}"
        tasks[task_id]["error"] = str(e)
        print(f"任务 {task_id} 失败: {e}")
        import traceback
        traceback.print_exc()


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回主页"""
    html_file = TEMPLATE_DIR / "index.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return """
    <html>
        <head><title>PDF to Markdown Converter</title></head>
        <body>
            <h1>PDF to Markdown Converter</h1>
            <p>API服务正在运行！</p>
            <p>请访问 <a href="/docs">/docs</a> 查看API文档</p>
        </body>
    </html>
    """


@app.post("/api/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    上传PDF文件并开始处理
    
    Args:
        file: 上传的PDF文件
        
    Returns:
        任务信息
    """
    # 验证文件类型
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持PDF文件")
    
    # 生成任务ID
    task_id = str(uuid.uuid4())
    
    # 保存上传的文件
    pdf_path = UPLOAD_DIR / f"{task_id}.pdf"
    
    try:
        async with aiofiles.open(pdf_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    
    # 创建任务记录
    tasks[task_id] = {
        "task_id": task_id,
        "filename": file.filename,
        "status": "queued",
        "progress": 0,
        "message": "任务已创建，等待处理...",
        "created_at": datetime.now().isoformat(),
        "logs": []  # 初始化日志列表
    }
    
    # 添加后台任务
    background_tasks.add_task(process_pdf_task, task_id, str(pdf_path))
    
    return JSONResponse({
        "success": True,
        "task_id": task_id,
        "message": "文件上传成功，开始处理..."
    })


@app.get("/api/status/{task_id}")
async def get_task_status(task_id: str):
    """
    查询任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        任务状态信息
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return JSONResponse(tasks[task_id])


@app.get("/api/download/{task_id}/markdown")
async def download_markdown(task_id: str):
    """
    下载Markdown文件
    
    Args:
        task_id: 任务ID
        
    Returns:
        Markdown文件
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if tasks[task_id]["status"] != "completed":
        raise HTTPException(status_code=400, detail="任务尚未完成")
    
    md_path = OUTPUT_DIR / task_id / "document.md"
    
    if not md_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=str(md_path),
        filename=f"{tasks[task_id]['filename'].replace('.pdf', '')}.md",
        media_type="text/markdown"
    )


@app.get("/api/download/{task_id}/images/{filename}")
async def download_image(task_id: str, filename: str):
    """
    下载图片文件
    
    Args:
        task_id: 任务ID
        filename: 图片文件名
        
    Returns:
        图片文件
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    img_path = OUTPUT_DIR / task_id / "pages" / filename
    
    if not img_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=str(img_path),
        filename=filename,
        media_type="image/jpeg"
    )


@app.get("/api/tasks")
async def list_tasks():
    """
    列出所有任务
    
    Returns:
        任务列表
    """
    return JSONResponse({
        "tasks": list(tasks.values()),
        "total": len(tasks)
    })


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """
    删除任务及其相关文件
    
    Args:
        task_id: 任务ID
        
    Returns:
        删除结果
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 删除文件
    upload_file = UPLOAD_DIR / f"{task_id}.pdf"
    output_dir = OUTPUT_DIR / task_id
    
    if upload_file.exists():
        upload_file.unlink()
    
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    # 删除任务记录
    del tasks[task_id]
    
    return JSONResponse({
        "success": True,
        "message": "任务已删除"
    })


@app.get("/api/health")
async def health_check():
    """
    健康检查
    
    Returns:
        服务状态
    """
    return JSONResponse({
        "status": "healthy",
        "service": "PDF to Markdown Converter",
        "version": "1.0.0",
        "tasks_count": len(tasks)
    })


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("PDF to Markdown Converter - Web Application")
    print("=" * 70)
    print()
    print("启动服务...")
    print(f"访问地址: http://localhost:8000")
    print(f"API文档: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

