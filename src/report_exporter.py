#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告输出模块
负责将批改结果导出为JSON、HTML、TXT等格式，并支持批量处理
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class ReportExporter:
    """报告导出器类，负责将批改结果导出为多种格式"""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """确保输出目录存在"""
        os.makedirs(self.output_dir, exist_ok=True)

    def export_json(self, result: Dict[str, Any], filename: str = None) -> str:
        """导出为JSON格式"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"grading_result_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return filepath

    def export_txt(self, result: Dict[str, Any], filename: str = None) -> str:
        """导出为TXT格式"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"grading_result_{timestamp}.txt"

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("              实训报告智能批改结果\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"批改时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"学生报告：{result.get('student_file', '未知')}\n")
            f.write(f"参考报告：{result.get('reference_file', '未知')}\n\n")

            scoring = result.get('scoring_result', {})
            f.write(f"总分：{scoring.get('total_score', 0):.1f} / {scoring.get('max_score', 100):.1f}")
            f.write(f" ({scoring.get('percentage', 0):.1f}%)\n\n")

            f.write("-" * 60 + "\n")
            f.write("各部分得分详情：\n")
            f.write("-" * 60 + "\n")

            section_scores = scoring.get('section_scores', {})
            for key, section in section_scores.items():
                f.write(f"  {section['description']}: ")
                f.write(f"{section['score']:.1f} / {section['max_score']:.1f}\n")

            deductions = scoring.get('deductions', [])
            if deductions:
                f.write("\n扣分说明：\n")
                for ded in deductions:
                    f.write(f"  - [{ded['section']}] {ded['reason']}: ")
                    f.write(f"{ded['details']} (扣{ded['points_deducted']:.1f}分)\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("个性化评语：\n")
            f.write("=" * 60 + "\n")
            f.write(result.get('comment', ''))

        return filepath

    def export_html(self, result: Dict[str, Any], filename: str = None) -> str:
        """导出为HTML格式"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"grading_result_{timestamp}.html"

        filepath = os.path.join(self.output_dir, filename)

        scoring = result.get('scoring_result', {})
        section_scores = scoring.get('section_scores', {})
        deductions = scoring.get('deductions', [])

        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>实训报告智能批改结果</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
        }}
        .info {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .total-score {{
            text-align: center;
            font-size: 24px;
            margin: 20px 0;
            padding: 20px;
            background-color: #3498db;
            color: white;
            border-radius: 8px;
        }}
        .score-box {{
            margin: 15px 0;
        }}
        .score-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            margin: 5px 0;
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            border-radius: 0 5px 5px 0;
        }}
        .deductions {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .comment {{
            background-color: #d1ecf1;
            border: 1px solid #17a2b8;
            padding: 20px;
            border-radius: 5px;
            white-space: pre-wrap;
            line-height: 1.6;
        }}
        h2 {{
            color: #34495e;
            margin-top: 25px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 实训报告智能批改结果</h1>

        <div class="info">
            <p><strong>批改时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>学生报告：</strong>{result.get('student_file', '未知')}</p>
            <p><strong>参考报告：</strong>{result.get('reference_file', '未知')}</p>
        </div>

        <div class="total-score">
            <strong>总分：</strong> {scoring.get('total_score', 0):.1f} / {scoring.get('max_score', 100):.1f}
            <span style="font-size: 16px;">({scoring.get('percentage', 0):.1f}%)</span>
        </div>

        <h2>各部分得分详情</h2>
        <div class="score-box">
"""

        for key, section in section_scores.items():
            html_content += f"""
            <div class="score-item">
                <span>{section['description']}</span>
                <span><strong>{section['score']:.1f}</strong> / {section['max_score']:.1f}</span>
            </div>
"""

        if deductions:
            html_content += f"""
        </div>

        <h2>扣分说明</h2>
        <div class="deductions">
            <ul>
"""
            for ded in deductions:
                html_content += f"<li><strong>{ded['section']}：</strong>{ded['reason']} - {ded['details']} (扣{ded['points_deducted']:.1f}分)</li>"

            html_content += """
            </ul>
        </div>
"""

        html_content += f"""
        <h2>个性化评语</h2>
        <div class="comment">
{result.get('comment', '')}
        </div>
    </div>
</body>
</html>
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return filepath

    def export_all(self, result: Dict[str, Any], base_name: str = None) -> Dict[str, str]:
        """导出所有格式"""
        if base_name is None:
            base_name = f"grading_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        paths = {
            'json': self.export_json(result, f"{base_name}.json"),
            'txt': self.export_txt(result, f"{base_name}.txt"),
            'html': self.export_html(result, f"{base_name}.html")
        }

        return paths
