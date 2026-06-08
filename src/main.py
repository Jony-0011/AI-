#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实训报告智能批改系统 - 主程序入口
包含命令行界面和批量处理功能
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.document_reader import DocumentReader
from src.comparison import ReportComparator
from src.scoring import ScoringEngine
from src.comment_generator import CommentGenerator
from src.report_exporter import ReportExporter


class GradingSystem:
    """智能批改系统主类"""

    def __init__(self):
        self.reader = None
        self.comparator = None
        self.scoring_engine = ScoringEngine()
        self.comment_generator = CommentGenerator()
        self.exporter = ReportExporter()

    def grade_single_report(self, reference_path: str, student_path: str,
                            output_formats: List[str] = None) -> Dict[str, Any]:
        """批改单份报告"""
        if output_formats is None:
            output_formats = ['json', 'txt', 'html']

        print(f"正在读取参考报告：{reference_path}")
        ref_reader = DocumentReader(reference_path)
        reference_content = ref_reader.read()

        print(f"正在读取学生报告：{student_path}")
        stu_reader = DocumentReader(student_path)
        student_content = stu_reader.read()

        print("正在进行比对分析...")
        comparator = ReportComparator(reference_content, student_content)
        comparison_result = comparator.compare()

        print("正在计算评分...")
        scoring_result = self.scoring_engine.calculate_total_score(
            reference_content, student_content, comparison_result
        )

        print("正在生成评语...")
        comment = self.comment_generator.generate_comment(scoring_result)

        result = {
            'reference_file': reference_path,
            'student_file': student_path,
            'reference_content': reference_content,
            'student_content': student_content,
            'comparison_result': comparison_result,
            'scoring_result': scoring_result,
            'comment': comment
        }

        print(f"\n===== 批改完成 =====")
        print(f"总分：{scoring_result['total_score']:.1f} / {scoring_result['max_score']:.1f}")
        print(f"得分率：{scoring_result['percentage']:.1f}%")

        print("\n正在导出批改结果...")
        base_name = Path(student_path).stem
        exported_paths = {}

        if 'json' in output_formats:
            exported_paths['json'] = self.exporter.export_json(result, f"{base_name}_result.json")
        if 'txt' in output_formats:
            exported_paths['txt'] = self.exporter.export_txt(result, f"{base_name}_result.txt")
        if 'html' in output_formats:
            exported_paths['html'] = self.exporter.export_html(result, f"{base_name}_result.html")

        print("\n导出的文件：")
        for fmt, path in exported_paths.items():
            print(f"  - {fmt.upper()}: {path}")

        return result

    def batch_grade(self, reference_path: str, reports_dir: str,
                    output_formats: List[str] = None) -> List[Dict[str, Any]]:
        """批量批改报告"""
        if output_formats is None:
            output_formats = ['json', 'txt', 'html']

        all_results = []

        print(f"参考报告：{reference_path}")
        print(f"报告目录：{reports_dir}")

        docx_files = list(Path(reports_dir).glob("*.docx"))

        if not docx_files:
            print("未找到任何 .docx 文件！")
            return all_results

        print(f"找到 {len(docx_files)} 份待批改报告\n")

        for i, docx_file in enumerate(docx_files, 1):
            print(f"\n--- 正在批改第 {i}/{len(docx_files)} 份报告 ---")
            try:
                result = self.grade_single_report(
                    reference_path, str(docx_file), output_formats
                )
                all_results.append(result)
            except Exception as e:
                print(f"批改失败：{docx_file}")
                print(f"错误：{e}")

        print(f"\n===== 批量批改完成 =====")
        print(f"成功批改：{len(all_results)}/{len(docx_files)} 份报告")

        return all_results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='实训报告智能批改系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  1. 批改单份报告：
     python src/main.py --reference reports/reference.docx --student reports/student1.docx

  2. 批量批改：
     python src/main.py --reference reports/reference.docx --dir reports/students

  3. 指定输出格式：
     python src/main.py --reference ref.docx --student stu.docx --format json html
'''
    )

    parser.add_argument(
        '--reference', '-r',
        required=True,
        help='参考报告文件路径 (.docx)'
    )

    parser.add_argument(
        '--student', '-s',
        help='单份学生报告文件路径 (.docx)'
    )

    parser.add_argument(
        '--dir', '-d',
        help='包含多份学生报告的目录路径'
    )

    parser.add_argument(
        '--format', '-f',
        nargs='+',
        choices=['json', 'txt', 'html'],
        default=['json', 'txt', 'html'],
        help='输出格式（可选：json, txt, html）'
    )

    args = parser.parse_args()

    if not args.student and not args.dir:
        print("错误：必须指定 --student 或 --dir 参数！")
        parser.print_help()
        return

    system = GradingSystem()

    if args.student:
        system.grade_single_report(
            args.reference,
            args.student,
            args.format
        )
    elif args.dir:
        system.batch_grade(
            args.reference,
            args.dir,
            args.format
        )


if __name__ == '__main__':
    main()
