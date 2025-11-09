"""
Configuration file for PoseMind application
"""

import os


# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Flask Configuration
DEBUG = True
HOST = '0.0.0.0'

# Pose Generation Settings
POSE_STYLES = {
    'portrait': '人像摄影',
    'outdoor': '户外写真',
    'fashion': '时尚大片',
    'casual': '日常随拍',
    'professional': '职业形象',
    'art': '艺术照',
    'travel': '旅行打卡'
}

GENDER_OPTIONS = {
    'female': '女生',
    'male': '男生'
}

# Number of pose images to generate
NUM_POSES_TO_GENERATE = 4
# Port Configuration - 优先从环境变量读取
PORT = int(os.getenv('PORT', 5000))

# AI Model (Vision) API Configuration - 优先从环境变量读取
# 用于场景分析和姿势生成的AI模型
AI_MODELSCOPE_API_KEY = os.getenv('AI_MODELSCOPE_API_KEY', '')
AI_MODELSCOPE_BASE_URL = os.getenv('AI_MODELSCOPE_BASE_URL', 'https://api-inference.modelscope.cn/v1')

# Image Generation Model API Configuration - 优先从环境变量读取
# 用于图片生成的模型
IMAGE_MODELSCOPE_API_KEY = os.getenv('IMAGE_MODELSCOPE_API_KEY', '')
IMAGE_MODELSCOPE_BASE_URL = os.getenv('IMAGE_MODELSCOPE_BASE_URL', 'https://api-inference.modelscope.cn/')

# Model Configuration - 优先从环境变量读取
VISION_MODEL = os.getenv('VISION_MODEL', 'Qwen/Qwen3-VL-235B-A22B-Instruct')
IMAGE_GENERATION_MODEL = os.getenv('IMAGE_GENERATION_MODEL', 'Qwen/Qwen-Image')

# Timeout Configuration - 优先从环境变量读取
IMAGE_GENERATION_TIMEOUT = int(os.getenv('IMAGE_GENERATION_TIMEOUT', 150))  # seconds (4张图约2.5分钟)
IMAGE_GENERATION_CHECK_INTERVAL = int(os.getenv('IMAGE_GENERATION_CHECK_INTERVAL', 5))  # seconds
API_REQUEST_TIMEOUT = int(os.getenv('API_REQUEST_TIMEOUT', 30))  # seconds

