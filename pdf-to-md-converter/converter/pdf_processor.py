#!/usr/bin/env python3
"""
PDF处理模块
将PDF文件转换为JPG图片
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Tuple
import os


class PDFProcessor:
    """PDF处理器，负责将PDF转换为图片"""
    
    def __init__(self, dpi: int = 300):
        """
        初始化PDF处理器
        
        Args:
            dpi: 输出图片的DPI（默认300）
        """
        self.dpi = dpi
        self.zoom = dpi / 72  # PDF默认72 DPI
        
    def pdf_to_images(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        将PDF转换为JPG图片
        
        Args:
            pdf_path: PDF文件路径
            output_dir: 输出目录路径
            
        Returns:
            生成的图片路径列表
        """
        pdf_path = Path(pdf_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 打开PDF文档
        doc = fitz.open(str(pdf_path))
        image_paths = []
        
        print(f"正在转换PDF: {pdf_path.name}")
        print(f"总页数: {len(doc)}")
        
        try:
            for page_num in range(len(doc)):
                # 加载页面
                page = doc.load_page(page_num)
                
                # 设置缩放矩阵（提高分辨率）
                mat = fitz.Matrix(self.zoom, self.zoom)
                
                # 渲染页面为图像
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # 保存为JPG
                img_filename = f"page_{page_num + 1:03d}.jpg"
                img_path = output_dir / img_filename
                pix.save(str(img_path))
                
                image_paths.append(str(img_path))
                print(f"  ✓ 页面 {page_num + 1}/{len(doc)} 已转换")
                
        finally:
            doc.close()
            
        print(f"✓ PDF转换完成！生成 {len(image_paths)} 张图片")
        return image_paths
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        获取PDF文档信息
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            包含PDF元数据的字典
        """
        doc = fitz.open(pdf_path)
        
        info = {
            "page_count": len(doc),
            "metadata": doc.metadata,
            "file_size": os.path.getsize(pdf_path),
            "filename": Path(pdf_path).name
        }
        
        doc.close()
        return info

