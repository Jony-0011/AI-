#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实训报告智能批改系统 - Web 启动脚本
启动 Streamlit Web 界面
"""

import subprocess
import sys
import os

def main():
    # 设置环境变量
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    # 启动 Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 
        'web_app.py', 
        '--server.port', '8601',
        '--server.address', '0.0.0.0'
    ]
    
    print("🚀 正在启动实训报告智能批改系统...")
    print("📡 Web 界面地址: http://localhost:8601")
    print("🔄 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\n✅ 服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
