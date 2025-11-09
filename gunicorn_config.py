"""
Gunicorn configuration for PoseMind
用于生产环境的高并发部署配置
"""

import multiprocessing
import os

# 绑定地址和端口
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Worker进程数
# 建议: CPU核心数 * 2 + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Worker类型
worker_class = "sync"

# 每个worker的连接数
worker_connections = 1000

# 超时时间（秒）
# 图片生成需要2-3分钟，设置为5分钟
timeout = 300

# Keep-alive连接时间
keepalive = 5

# 最大请求数（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 日志配置
accesslog = "-"  # 输出到stdout
errorlog = "-"   # 输出到stderr
loglevel = "info"

# 进程名称
proc_name = "posemind"

# 预加载应用（提高性能）
preload_app = True

# 守护进程（生产环境建议使用supervisor管理）
daemon = False

