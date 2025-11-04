#!/usr/bin/env python3
"""
Markdown生成器模块
将OCR结果转换为结构化Markdown文档
"""

from pathlib import Path
from typing import List, Dict, Any
import re


class MarkdownGenerator:
    """Markdown生成器，将OCR结果转换为结构化文档"""
    
    def __init__(self):
        """初始化Markdown生成器"""
        self.content = []
        
    def add_title(self, title: str, level: int = 1):
        """
        添加标题
        
        Args:
            title: 标题文本
            level: 标题级别 (1-6)
        """
        prefix = "#" * level
        self.content.append(f"{prefix} {title}\n")
        
    def add_text(self, text: str):
        """
        添加普通文本
        
        Args:
            text: 文本内容
        """
        if text.strip():
            self.content.append(f"{text}\n")
            
    def add_paragraph(self, text: str):
        """
        添加段落（带空行分隔）
        
        Args:
            text: 段落文本
        """
        if text.strip():
            self.content.append(f"{text}\n\n")
            
    def add_horizontal_line(self):
        """添加分隔线"""
        self.content.append("---\n\n")
        
    def add_page_break(self, page_num: int):
        """
        添加页面分隔
        
        Args:
            page_num: 页码
        """
        self.content.append(f"\n---\n\n## 第 {page_num} 页\n\n")
        
    def add_image_reference(self, image_path: str, alt_text: str = ""):
        """
        添加图片引用
        
        Args:
            image_path: 图片路径
            alt_text: 图片替代文本
        """
        if not alt_text:
            alt_text = Path(image_path).stem
        self.content.append(f"![{alt_text}]({image_path})\n\n")
        
    def process_ocr_result(self, ocr_text: str) -> str:
        """
        处理OCR识别结果，提取结构化信息
        
        Args:
            ocr_text: OCR原始文本
            
        Returns:
            处理后的文本
        """
        # 移除多余的空行
        lines = [line.rstrip() for line in ocr_text.split('\n')]
        
        # 合并过短的行（可能是断行）
        processed_lines = []
        temp_line = ""
        
        for line in lines:
            if not line.strip():
                if temp_line:
                    processed_lines.append(temp_line)
                    temp_line = ""
                processed_lines.append("")
            elif len(line) < 40 and temp_line and not line.endswith(('.', '!', '?', '。', '！', '？')):
                # 短行且未结束，可能是断行
                temp_line += " " + line
            else:
                if temp_line:
                    processed_lines.append(temp_line)
                temp_line = line
                
        if temp_line:
            processed_lines.append(temp_line)
            
        return '\n'.join(processed_lines)
        
    def generate_from_ocr_results(
        self, 
        ocr_results: List[Dict[str, Any]],
        pdf_name: str = "文档"
    ) -> str:
        """
        从OCR结果生成完整的Markdown文档
        
        Args:
            ocr_results: OCR识别结果列表
            pdf_name: PDF文档名称
            
        Returns:
            生成的Markdown文本
        """
        self.content = []
        
        # 添加文档标题
        self.add_title(f"{pdf_name} - OCR识别结果", level=1)
        self.add_paragraph(f"总页数: {len(ocr_results)}")
        self.add_horizontal_line()
        
        # 处理每一页
        for idx, result in enumerate(ocr_results, 1):
            # 添加页面标题
            self.add_page_break(idx)
            
            # 如果处理出错，添加错误信息
            if "error" in result:
                self.add_text(f"⚠️ **处理错误**: {result['error']}\n")
                continue
            
            # 添加原始图片引用（相对路径）
            image_path = result.get("image_path", "")
            if image_path:
                rel_path = f"pages/{Path(image_path).name}"
                self.add_image_reference(rel_path, f"第{idx}页原始图片")
            
            # 添加标注图片引用
            annotated_path = result.get("annotated_image", "")
            if annotated_path:
                rel_path = f"pages/{Path(annotated_path).name}"
                self.add_image_reference(rel_path, f"第{idx}页标注图片")
            
            # 添加OCR识别内容
            self.add_title("识别内容", level=3)
            
            ocr_text = result.get("result", "")
            if ocr_text:
                processed_text = self.process_ocr_result(ocr_text)
                
                # 检查是否包含表格、公式等特殊内容
                if "Table Recognition:" in ocr_text or "|" in ocr_text:
                    self.add_text("**包含表格内容**\n")
                    self.add_text("```")
                    self.add_text(processed_text)
                    self.add_text("```\n")
                elif "Formula" in ocr_text or "$" in ocr_text:
                    self.add_text("**包含公式内容**\n")
                    self.add_text(processed_text)
                else:
                    self.add_text(processed_text)
            else:
                self.add_text("*未识别到内容*\n")
            
            self.add_text("\n")
        
        return self.get_markdown()
        
    def get_markdown(self) -> str:
        """
        获取生成的Markdown文本
        
        Returns:
            Markdown文本
        """
        return ''.join(self.content)
        
    def save_to_file(self, output_path: str):
        """
        保存Markdown到文件
        
        Args:
            output_path: 输出文件路径
        """
        content = self.get_markdown()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Markdown已保存到: {output_path}")
        
    def generate_summary(self, ocr_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成处理摘要
        
        Args:
            ocr_results: OCR识别结果列表
            
        Returns:
            摘要信息字典
        """
        total_pages = len(ocr_results)
        successful_pages = len([r for r in ocr_results if "error" not in r])
        failed_pages = total_pages - successful_pages
        
        # 统计总字符数
        total_chars = 0
        for result in ocr_results:
            if "result" in result:
                total_chars += len(result["result"])
        
        return {
            "total_pages": total_pages,
            "successful_pages": successful_pages,
            "failed_pages": failed_pages,
            "total_characters": total_chars,
            "success_rate": f"{(successful_pages / total_pages * 100):.1f}%" if total_pages > 0 else "0%"
        }

