#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动评分模块
根据配置的权重和比对结果计算得分，提供详细的扣分依据
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path


class ScoringEngine:
    """评分引擎类，负责根据配置计算得分"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'scoring_config.json')
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载评分配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def score_structure(self, section_comparison: Dict[str, Any]) -> Dict[str, Any]:
        """计算结构完整性得分"""
        config = self.config['scoring']['sections']['structure']
        weight = config['weight']
        match_ratio = section_comparison.get('section_match_ratio', 0.0)

        score = match_ratio * weight
        deductions = []

        missing = section_comparison.get('missing', [])
        if missing:
            deductions.append({
                'reason': '缺少章节',
                'details': missing,
                'points_deducted': (1 - match_ratio) * weight
            })

        return {
            'score': score,
            'max_score': weight,
            'description': config['description'],
            'deductions': deductions,
            'details': section_comparison
        }

    def score_content(self, comparison_result: Dict[str, Any]) -> Dict[str, Any]:
        """计算内容准确性得分"""
        config = self.config['scoring']['sections']['content']
        weight = config['weight']
        similarity = comparison_result.get('text_similarity', 0.0)
        threshold = config.get('similarity_threshold', 0.7)

        if similarity >= threshold:
            score = weight
        else:
            score = (similarity / threshold) * weight

        deductions = []
        if similarity < threshold:
            deductions.append({
                'reason': '内容相似度低于阈值',
                'details': f"相似度: {similarity:.2%}, 阈值: {threshold:.0%}",
                'points_deducted': weight - score
            })

        return {
            'score': score,
            'max_score': weight,
            'description': config['description'],
            'deductions': deductions,
            'similarity': similarity
        }

    def score_images(self, image_comparison: Dict[str, Any]) -> Dict[str, Any]:
        """计算图片质量得分"""
        config = self.config['scoring']['sections']['images']
        weight = config['weight']
        min_count = config.get('min_count', 3)
        stu_count = image_comparison.get('student_count', 0)

        score_per_image = config.get('max_score_per_image', 5)
        score = min(stu_count * score_per_image, weight)

        deductions = []
        if stu_count < min_count:
            deductions.append({
                'reason': '图片数量不足',
                'details': f"应有: {min_count}张, 实际: {stu_count}张",
                'points_deducted': weight - score
            })

        return {
            'score': score,
            'max_score': weight,
            'description': config['description'],
            'deductions': deductions,
            'count': stu_count
        }

    def score_format(self, student_content: Dict[str, Any]) -> Dict[str, Any]:
        """计算格式规范性得分（简化版本）"""
        config = self.config['scoring']['sections']['format']
        weight = config['weight']

        score = weight * 0.8
        deductions = []

        text = student_content.get('text', '')
        if len(text) < 500:
            deductions.append({
                'reason': '文档内容过短',
                'details': f"文本长度: {len(text)}字",
                'points_deducted': weight * 0.2
            })
            score -= weight * 0.2

        return {
            'score': max(0, score),
            'max_score': weight,
            'description': config['description'],
            'deductions': deductions
        }

    def score_reflection(self, student_content: Dict[str, Any]) -> Dict[str, Any]:
        """计算反思深度得分"""
        config = self.config['scoring']['sections']['reflection']
        weight = config['weight']

        text = student_content.get('text', '')
        reflection_keywords = ['反思', '总结', '体会', '收获', '改进', '问题', '错误']
        has_reflection = any(keyword in text for keyword in reflection_keywords)

        if has_reflection:
            score = weight
            deductions = []
        else:
            score = 0
            deductions = [{
                'reason': '缺少反思/总结内容',
                'details': '未找到反思、总结相关内容',
                'points_deducted': weight
            }]

        return {
            'score': score,
            'max_score': weight,
            'description': config['description'],
            'deductions': deductions
        }

    def calculate_total_score(self, reference_content: Dict[str, Any],
                            student_content: Dict[str, Any],
                            comparison_result: Dict[str, Any]) -> Dict[str, Any]:
        """计算总分"""
        section_comparison = comparison_result.get('section_comparison', {})
        image_comparison = comparison_result.get('image_comparison', {})

        scores = {
            'structure': self.score_structure(section_comparison),
            'content': self.score_content(comparison_result),
            'images': self.score_images(image_comparison),
            'format': self.score_format(student_content),
            'reflection': self.score_reflection(student_content)
        }

        total_score = sum(s['score'] for s in scores.values())
        total_max = self.config['scoring']['total_score']

        all_deductions = []
        for key, section_score in scores.items():
            for deduction in section_score['deductions']:
                deduction['section'] = section_score['description']
                all_deductions.append(deduction)

        return {
            'total_score': round(total_score, 2),
            'max_score': total_max,
            'percentage': round((total_score / total_max) * 100, 2),
            'section_scores': scores,
            'deductions': all_deductions
        }
