#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结构化比对模块
负责将待批改报告与参考答案进行文本和结构比对
"""

import difflib
from typing import List, Dict, Any, Tuple
from collections import Counter


class ReportComparator:
    """报告比对器类，处理参考报告与待批改报告的比对"""

    def __init__(self, reference_content: Dict[str, Any], student_content: Dict[str, Any]):
        self.reference = reference_content
        self.student = student_content
        self.differences = []
        self.similarity_score = 0.0

    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """使用difflib计算两个文本的相似度"""
        if not text1 or not text2:
            return 0.0

        seq_matcher = difflib.SequenceMatcher(None, text1, text2)
        return seq_matcher.ratio()

    def find_differences(self, text1: str, text2: str) -> List[Dict[str, Any]]:
        """找出两段文本的差异点"""
        differ = difflib.Differ()
        diff_result = list(differ.compare(text1.splitlines(), text2.splitlines()))

        differences = []
        for i, line in enumerate(diff_result):
            if line.startswith('- '):
                differences.append({
                    'type': 'missing',
                    'content': line[2:],
                    'position': i
                })
            elif line.startswith('+ '):
                differences.append({
                    'type': 'extra',
                    'content': line[2:],
                    'position': i
                })

        return differences

    def compare_sections(self, ref_sections: List[str], stu_sections: List[str]) -> Dict[str, Any]:
        """比对两个文档的章节结构"""
        missing_sections = []
        extra_sections = []
        matching_sections = []

        for section in ref_sections:
            if section in stu_sections:
                matching_sections.append(section)
            else:
                missing_sections.append(section)

        for section in stu_sections:
            if section not in ref_sections:
                extra_sections.append(section)

        return {
            'matching': matching_sections,
            'missing': missing_sections,
            'extra': extra_sections,
            'section_match_ratio': len(matching_sections) / max(len(ref_sections), 1)
        }

    def compare_images(self, ref_images: List[Dict], stu_images: List[Dict]) -> Dict[str, Any]:
        """比对图片信息"""
        ref_count = len(ref_images)
        stu_count = len(stu_images)

        return {
            'reference_count': ref_count,
            'student_count': stu_count,
            'count_difference': stu_count - ref_count,
            'ratio': stu_count / max(ref_count, 1)
        }

    def compare(self) -> Dict[str, Any]:
        """执行完整的比对流程"""
        ref_text = self.reference.get('text', '')
        stu_text = self.student.get('text', '')

        ref_sections = self._extract_sections(ref_text)
        stu_sections = self._extract_sections(stu_text)

        text_similarity = self.calculate_text_similarity(ref_text, stu_text)
        text_differences = self.find_differences(ref_text, stu_text)

        section_comparison = self.compare_sections(ref_sections, stu_sections)
        image_comparison = self.compare_images(
            self.reference.get('images', []),
            self.student.get('images', [])
        )

        self.differences = text_differences
        self.similarity_score = text_similarity

        return {
            'text_similarity': text_similarity,
            'text_differences': text_differences,
            'section_comparison': section_comparison,
            'image_comparison': image_comparison,
            'ref_text_length': len(ref_text),
            'stu_text_length': len(stu_text)
        }

    def _extract_sections(self, text: str) -> List[str]:
        """从文本中提取章节标题"""
        section_markers = ['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、',
                          '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.',
                          '实验目的', '实验原理', '实验步骤', '实验结果', '实验反思', '实验总结'
                         ]

        sections = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if any(marker in line for marker in section_markers) and len(line) < 50:
                if line not in sections:
                    sections.append(line)

        return sections
