#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
评语生成模块
根据比对结果和评分情况生成个性化评语，指出优劣并给出改进建议
"""

from typing import Dict, Any, List


class CommentGenerator:
    """评语生成器类，负责生成个性化的批改评语"""

    def __init__(self):
        self.positive_templates = [
            "该报告结构较为完整，{}.",
            "内容方面，{}，表现良好。",
            "图片部分{}，值得肯定。",
            "{}，体现了一定的思考深度。"
        ]
        self.negative_templates = [
            "但报告结构存在不足，{}.",
            "内容方面，{}，需要加强。",
            "图片部分{}，建议补充完善。",
            "{}，请认真思考实验的收获与不足。"
        ]
        self.suggestion_templates = [
            "建议：{}.",
            "可以尝试：{}.",
            "今后注意：{}."
        ]

    def generate_structure_comment(self, scoring_result: Dict[str, Any]) -> str:
        """生成结构相关评语"""
        section_scores = scoring_result.get('section_scores', {})
        structure = section_scores.get('structure', {})
        score = structure.get('score', 0)
        max_score = structure.get('max_score', 1)
        ratio = score / max_score

        if ratio >= 0.8:
            return f"结构完整性得分{score:.1f}/{max_score}，章节覆盖较为全面"
        elif ratio >= 0.5:
            return f"结构完整性得分{score:.1f}/{max_score}，部分章节有所缺失"
        else:
            return f"结构完整性得分{score:.1f}/{max_score}，需要补充更多章节内容"

    def generate_content_comment(self, scoring_result: Dict[str, Any]) -> str:
        """生成内容相关评语"""
        section_scores = scoring_result.get('section_scores', {})
        content = section_scores.get('content', {})
        score = content.get('score', 0)
        max_score = content.get('max_score', 1)
        similarity = content.get('similarity', 0)
        ratio = score / max_score

        if ratio >= 0.8:
            return f"内容准确性得分{score:.1f}/{max_score}，与参考报告相似度达{similarity:.1%}，内容较为详实"
        elif ratio >= 0.5:
            return f"内容准确性得分{score:.1f}/{max_score}，与参考报告相似度{similarity:.1%}，核心内容基本覆盖"
        else:
            return f"内容准确性得分{score:.1f}/{max_score}，与参考报告相似度{similarity:.1%}，需要加强核心内容的描述"

    def generate_image_comment(self, scoring_result: Dict[str, Any]) -> str:
        """生成图片相关评语"""
        section_scores = scoring_result.get('section_scores', {})
        images = section_scores.get('images', {})
        score = images.get('score', 0)
        max_score = images.get('max_score', 1)
        count = images.get('count', 0)

        if score >= max_score * 0.8:
            return f"图片质量得分{score:.1f}/{max_score}，共{count}张图片，图文并茂"
        elif score >= max_score * 0.5:
            return f"图片质量得分{score:.1f}/{max_score}，共{count}张图片，基本满足要求"
        else:
            return f"图片质量得分{score:.1f}/{max_score}，共{count}张图片，建议增加实验过程图片"

    def generate_format_comment(self, scoring_result: Dict[str, Any]) -> str:
        """生成格式相关评语"""
        section_scores = scoring_result.get('section_scores', {})
        format_score = section_scores.get('format', {})
        score = format_score.get('score', 0)
        max_score = format_score.get('max_score', 1)

        if score >= max_score * 0.8:
            return f"格式规范性得分{score:.1f}/{max_score}，排版较为规范"
        elif score >= max_score * 0.5:
            return f"格式规范性得分{score:.1f}/{max_score}，格式基本符合要求"
        else:
            return f"格式规范性得分{score:.1f}/{max_score}，需要注意排版规范"

    def generate_reflection_comment(self, scoring_result: Dict[str, Any]) -> str:
        """生成反思相关评语"""
        section_scores = scoring_result.get('section_scores', {})
        reflection = section_scores.get('reflection', {})
        score = reflection.get('score', 0)
        max_score = reflection.get('max_score', 1)

        if score >= max_score * 0.8:
            return f"反思深度得分{score:.1f}/{max_score}，有较为深刻的总结和反思"
        elif ratio >= 0.5:
            return f"反思深度得分{score:.1f}/{max_score}，有一定的总结内容"
        else:
            return f"反思深度得分{score:.1f}/{max_score}，缺少实验总结和反思内容"

    def generate_suggestions(self, scoring_result: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        suggestions = []
        deductions = scoring_result.get('deductions', [])

        for deduction in deductions:
            reason = deduction.get('reason', '')
            if '缺少章节' in reason:
                suggestions.append("补充缺失的章节内容，完善报告结构")
            elif '内容相似度' in reason:
                suggestions.append("参考评分标准，加强核心内容的描述")
            elif '图片数量不足' in reason:
                suggestions.append("增加实验过程图片，丰富报告内容")
            elif '文档内容过短' in reason:
                suggestions.append("详细描述实验步骤和结果，增加报告篇幅")
            elif '缺少反思' in reason:
                suggestions.append("认真总结实验收获，撰写深刻的反思内容")

        if not suggestions:
            suggestions.append("继续保持，可进一步提升实验报告的深度")

        return suggestions

    def generate_comment(self, scoring_result: Dict[str, Any]) -> str:
        """生成完整的评语"""
        total_score = scoring_result.get('total_score', 0)
        percentage = scoring_result.get('percentage', 0)

        opening = f"本次实训报告得分：{total_score:.1f}分（{percentage:.1f}%）。\n\n"

        structure_comment = self.generate_structure_comment(scoring_result)
        content_comment = self.generate_content_comment(scoring_result)
        image_comment = self.generate_image_comment(scoring_result)
        format_comment = self.generate_format_comment(scoring_result)
        reflection_comment = self.generate_reflection_comment(scoring_result)

        details = "各部分评分：\n"
        details += f"  - {structure_comment}\n"
        details += f"  - {content_comment}\n"
        details += f"  - {image_comment}\n"
        details += f"  - {format_comment}\n"
        details += f"  - {reflection_comment}\n\n"

        suggestions = self.generate_suggestions(scoring_result)
        suggestion_text = "改进建议：\n"
        for i, sug in enumerate(suggestions, 1):
            suggestion_text += f"  {i}. {sug}\n"

        closing = "\n希望在今后的实验中继续努力，不断提升！"

        return opening + details + suggestion_text + closing
