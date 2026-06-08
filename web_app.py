#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实训报告智能批改系统 - Streamlit Web 界面
提供直观的图形化界面进行报告批改
"""

import streamlit as st
import os
import sys
from io import BytesIO

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from document_reader import DocumentReader
from comparison import ReportComparator
from scoring import ScoringEngine
from comment_generator import CommentGenerator
from report_exporter import ReportExporter

# 设置页面配置
st.set_page_config(
    page_title="实训报告智能批改系统",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #1e3a5f;
        text-align: center;
        margin-bottom: 20px;
    }
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .score-value {
        font-size: 48px;
        font-weight: bold;
    }
    .score-label {
        font-size: 16px;
        opacity: 0.9;
    }
    .section-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .section-title {
        font-size: 14px;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    .progress-bar {
        height: 12px;
        background-color: #e8e8e8;
        border-radius: 6px;
        overflow: hidden;
        margin: 8px 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.5s ease;
    }
    .deduction-item {
        background: #fff5f5;
        border-left: 4px solid #ff4d4f;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 4px 4px 0;
        font-size: 13px;
        color: #d93026;
    }
    .suggestion-item {
        background: #f6ffed;
        border-left: 4px solid #52c41a;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 4px 4px 0;
        font-size: 13px;
        color: #389e0d;
    }
    .success-box {
        background: #f6ffed;
        border: 1px solid #b7eb8f;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }
    .warning-box {
        background: #fff7e6;
        border: 1px solid #ffd591;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 页面标题
    st.markdown('<div class="main-header">📝 实训报告智能批改系统</div>', unsafe_allow_html=True)
    st.markdown("---")

    # 侧边栏
    with st.sidebar:
        st.subheader("📁 文件上传")
        
        # 参考报告上传
        reference_file = st.file_uploader(
            "参考报告 (docx)",
            type=["docx"],
            help="上传满分参考报告作为评分标准"
        )
        
        # 学生报告上传
        student_file = st.file_uploader(
            "学生报告 (docx)",
            type=["docx"],
            help="上传待批改的学生实训报告"
        )
        
        # 批改按钮
        if st.button("🚀 开始批改", type="primary", disabled=not (reference_file and student_file)):
            with st.spinner("正在批改中..."):
                process_report(reference_file, student_file)

    # 主内容区
    if 'result' not in st.session_state:
        st.info("请在左侧上传参考报告和学生报告，然后点击开始批改")
        show_feature_intro()
    else:
        show_results()

def process_report(reference_file, student_file):
    """处理报告批改"""
    try:
        # 读取参考报告
        ref_reader = DocumentReader()
        ref_content = ref_reader.read_docx_from_bytes(reference_file.read())
        
        # 读取学生报告
        stu_reader = DocumentReader()
        student_content = stu_reader.read_docx_from_bytes(student_file.read())
        
        # 比对文档
        comparer = ReportComparator(ref_content, student_content)
        comparison_result = comparer.compare()
        
        # 评分
        scorer = ScoringEngine()
        scoring_result = scorer.calculate_total_score(ref_content, student_content, comparison_result)
        
        # 生成评语
        comment_gen = CommentGenerator()
        comment = comment_gen.generate_comment(scoring_result)
        
        # 保存结果到会话状态
        st.session_state['result'] = {
            'scoring': scoring_result,
            'comment': comment,
            'comparison': comparison_result,
            'reference_info': {
                'filename': reference_file.name,
                'text_length': len(ref_content.get('text', '')),
                'image_count': len(ref_content.get('images', []))
            },
            'student_info': {
                'filename': student_file.name,
                'text_length': len(student_content.get('text', '')),
                'image_count': len(student_content.get('images', []))
            }
        }
        
        st.success("批改完成！")
        
    except Exception as e:
        st.error(f"批改过程出错: {str(e)}")
        import traceback
        st.exception(traceback.format_exc())

def show_feature_intro():
    """显示功能介绍"""
    st.subheader("✨ 系统功能")
    
    features = [
        {
            "icon": "📄",
            "title": "文档读取",
            "desc": "支持docx格式报告读取，提取文本内容和图片信息"
        },
        {
            "icon": "🔍",
            "title": "智能比对",
            "desc": "与参考报告进行结构化比对，分析内容相似度"
        },
        {
            "icon": "📊",
            "title": "自动评分",
            "desc": "多维度加权评分，结构、内容、图片、格式、反思"
        },
        {
            "icon": "💬",
            "title": "评语生成",
            "desc": "基于评分结果生成个性化评语和改进建议"
        },
        {
            "icon": "📤",
            "title": "报告导出",
            "desc": "支持JSON、TXT、HTML多种格式输出"
        }
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="section-card">
                <div style="font-size: 28px; margin-bottom: 8px;">{feature['icon']}</div>
                <div class="section-title">{feature['title']}</div>
                <div style="font-size: 13px; color: #666;">{feature['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

def show_results():
    """显示批改结果"""
    result = st.session_state['result']
    scoring = result['scoring']
    comment = result['comment']
    ref_info = result['reference_info']
    stu_info = result['student_info']
    
    # 顶部统计信息
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("参考报告", ref_info['filename'].replace('.docx', ''))
    
    with col2:
        st.metric("学生报告", stu_info['filename'].replace('.docx', ''))
    
    with col3:
        st.metric("学生报告字数", f"{stu_info['text_length']:,}")
    
    with col4:
        st.metric("图片数量", f"{stu_info['image_count']}张")
    
    st.markdown("---")
    
    # 总分展示
    col_main, col_details = st.columns([1, 2])
    
    with col_main:
        st.markdown(f"""
        <div class="score-box">
            <div class="score-value">{scoring['total_score']}</div>
            <div class="score-label">总分 / {scoring['max_score']}</div>
            <div style="font-size: 18px; margin-top: 8px;">({scoring['percentage']}%)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 评分分布
        st.subheader("📈 评分分布")
        section_scores = scoring['section_scores']
        
        for section_name, score_info in section_scores.items():
            percentage = (score_info['score'] / score_info['max_score']) * 100
            color = get_progress_color(percentage)
            
            st.markdown(f"""
            <div class="section-card">
                <div class="section-title">{score_info['description']}</div>
                <div style="font-size: 18px; font-weight: bold; color: {color};">
                    {score_info['score']:.1f} / {score_info['max_score']}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%; background: {color};"></div>
                </div>
                <div style="font-size: 12px; color: #888;">{percentage:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_details:
        # 评语
        st.subheader("💬 批改评语")
        st.markdown(f"""
        <div class="section-card">
            <div style="white-space: pre-wrap; font-size: 14px; line-height: 1.6; color: #333;">
                {comment}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 扣分详情
        if scoring['deductions']:
            st.subheader("❌ 扣分详情")
            for deduction in scoring['deductions']:
                st.markdown(f"""
                <div class="deduction-item">
                    <strong>{deduction['section']}:</strong> {deduction['reason']}
                    <div style="margin-top: 4px; opacity: 0.8;">
                        {deduction['details']}
                    </div>
                    <div style="margin-top: 4px; font-weight: bold;">
                        - {deduction['points_deducted']:.1f}分
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 导出按钮
        st.subheader("📤 导出报告")
        export_formats = ['JSON', 'TXT', 'HTML']
        for fmt in export_formats:
            if st.button(f"导出 {fmt} 格式"):
                export_report(fmt.lower())

def get_progress_color(percentage):
    """根据百分比返回进度条颜色"""
    if percentage >= 80:
        return '#52c41a'
    elif percentage >= 60:
        return '#faad14'
    elif percentage >= 40:
        return '#fa8c16'
    else:
        return '#ff4d4f'

def export_report(format_type):
    """导出报告"""
    result = st.session_state['result']
    
    exporter = ReportExporter()
    output = BytesIO()
    
    if format_type == 'json':
        exporter.export_json(result, output)
        output.seek(0)
        st.download_button(
            label="下载 JSON",
            data=output,
            file_name=f"{result['student_info']['filename'].replace('.docx', '')}_result.json",
            mime="application/json"
        )
    elif format_type == 'txt':
        exporter.export_txt(result, output)
        output.seek(0)
        st.download_button(
            label="下载 TXT",
            data=output,
            file_name=f"{result['student_info']['filename'].replace('.docx', '')}_result.txt",
            mime="text/plain"
        )
    elif format_type == 'html':
        exporter.export_html(result, output)
        output.seek(0)
        st.download_button(
            label="下载 HTML",
            data=output,
            file_name=f"{result['student_info']['filename'].replace('.docx', '')}_result.html",
            mime="text/html"
        )

if __name__ == '__main__':
    main()
