#!/usr/bin/env python3
"""
OCR处理模块
基于PaddleOCR-VL-0.9B模型进行文档结构化识别
"""

import os
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoModelForCausalLM, AutoProcessor
from pathlib import Path
from typing import Dict, List, Any, Optional
import json


class OCRProcessor:
    """OCR处理器，使用VL模型进行文档结构化识别"""
    
    def __init__(self, model_path: str = "/personal/1102case/models/paddleocr-vl"):
        """
        初始化OCR处理器
        
        Args:
            model_path: VL模型路径
        """
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        
        print(f"使用设备: {self.device}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            
    def load_model(self):
        """加载VL模型（延迟加载）"""
        if self.model is None:
            print(f"正在加载模型: {self.model_path}")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16
            ).to(self.device).eval()
            
            self.processor = AutoProcessor.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            print("✓ 模型加载完成")
            if torch.cuda.is_available():
                print(f"  显存占用: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
                
    def process_image(self, image_path: str, task_type: str = "ocr") -> Dict[str, Any]:
        """
        处理单张图片
        
        Args:
            image_path: 图片路径
            task_type: 任务类型 (ocr, table, formula, chart)
            
        Returns:
            包含识别结果的字典
        """
        self.load_model()
        
        # 任务提示词映射
        prompts = {
            "ocr": "OCR with format:",  # 结构化OCR
            "table": "Table Recognition:",
            "formula": "Formula Recognition:",
            "chart": "Chart Recognition:",
        }
        
        prompt = prompts.get(task_type, prompts["ocr"])
        
        # 加载图像
        image = Image.open(image_path).convert("RGB")
        
        # 准备输入
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt},
                ]
            }
        ]
        
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.device)
        
        # 生成输出
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=2048)
        
        # 解码结果
        result = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
        
        return {
            "image_path": image_path,
            "task_type": task_type,
            "result": result,
            "image_size": image.size
        }
    
    def create_annotated_image(
        self, 
        image_path: str, 
        ocr_result: Dict[str, Any],
        output_path: str
    ) -> str:
        """
        创建带标注的可视化图片
        
        Args:
            image_path: 原始图片路径
            ocr_result: OCR识别结果
            output_path: 输出图片路径
            
        Returns:
            输出图片路径
        """
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        
        # 尝试加载字体
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            # 如果找不到，使用默认字体
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 在图片上添加识别结果标记
        # 由于VL模型返回的是结构化文本，我们在顶部添加一个信息框
        width, height = image.size
        
        # 添加半透明背景
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # 绘制顶部信息条
        overlay_draw.rectangle([(0, 0), (width, 40)], fill=(0, 0, 0, 180))
        
        # 合并图层
        image = image.convert('RGBA')
        image = Image.alpha_composite(image, overlay)
        image = image.convert('RGB')
        
        # 重新创建draw对象
        draw = ImageDraw.Draw(image)
        
        # 添加文字信息
        info_text = f"Page: {Path(image_path).stem} | Task: {ocr_result.get('task_type', 'OCR')}"
        draw.text((10, 10), info_text, fill=(255, 255, 255), font=font)
        
        # 保存图片
        image.save(output_path, quality=95)
        return output_path
    
    def batch_process_images(
        self, 
        image_paths: List[str], 
        output_dir: str,
        task_type: str = "ocr"
    ) -> List[Dict[str, Any]]:
        """
        批量处理图片
        
        Args:
            image_paths: 图片路径列表
            output_dir: 输出目录
            task_type: 任务类型
            
        Returns:
            识别结果列表
        """
        self.load_model()
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        total = len(image_paths)
        
        print(f"\n开始批量处理 {total} 张图片...")
        
        for idx, img_path in enumerate(image_paths, 1):
            print(f"\n处理进度: {idx}/{total}")
            print(f"当前图片: {Path(img_path).name}")
            
            try:
                # 执行OCR识别
                ocr_result = self.process_image(img_path, task_type)
                
                # 创建带标注的图片
                img_filename = Path(img_path).stem
                annotated_path = output_dir / f"{img_filename}_annotated.jpg"
                self.create_annotated_image(img_path, ocr_result, str(annotated_path))
                
                ocr_result["annotated_image"] = str(annotated_path)
                results.append(ocr_result)
                
                print(f"✓ 完成")
                
            except Exception as e:
                print(f"✗ 处理失败: {e}")
                results.append({
                    "image_path": img_path,
                    "error": str(e)
                })
        
        print(f"\n✓ 批量处理完成！成功处理 {len([r for r in results if 'error' not in r])}/{total} 张图片")
        
        return results
    
    def save_results(self, results: List[Dict[str, Any]], output_file: str):
        """
        保存识别结果到JSON文件
        
        Args:
            results: 识别结果列表
            output_file: 输出文件路径
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✓ 结果已保存到: {output_file}")

