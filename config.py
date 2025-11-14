"""
Configuration file for PoseMind application
"""

import os
import secrets


# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

DEBUG = os.getenv('DEBUG', 'false').lower() in ('1', 'true', 'yes', 'on')
HOST = '0.0.0.0'
SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_hex(32)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'false').lower() in ('1', 'true', 'yes', 'on')

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

# Prompt Configuration
POSE_CATEGORIES = ['经典', '动态', '坐姿', '情感', '艺术', '互动', '时尚', '倚靠']
SCENE_ANALYSIS_SYSTEM_PROMPT = (
    '你是摄影场景分析助手。必须只输出合法JSON；不得输出解释、Markdown或额外文本；不确定时用"未知"。'
)
SCENE_ANALYSIS_USER_PROMPT = (
    '请基于所给图片输出一个JSON对象，字段如下：\n'
    '- location_type：场所类型（室内|户外|城市|自然|建筑|商业|住宅），最多6字\n'
    '- scene：具体场景（如咖啡馆、公园、街道、海边、办公室、家中等），最多8字\n'
    '- ambiance：氛围（休闲|正式|浪漫|活力|艺术|安静|热闹），最多6字\n'
    '- lighting：光线（自然光|人工光|逆光|柔光|硬光|混合光），最多6字\n'
    '- style_advice：拍摄风格建议，12-30字\n'
    '输出要求：仅返回JSON；全部为简体中文；不得臆测。'
)
POSE_SYSTEM_PROMPT = (
    '你是专业摄影指导。必须只输出合法JSON数组；长度为N（由输入给定）；不得输出解释或Markdown；内容专业、健康、优雅。'
)
POSE_USER_PROMPT_TEMPLATE = (
    '根据以下场景分析与性别，为人物生成{n}个可实现的摄影姿势，返回JSON数组。\n'
    '每个元素包含：\n'
    '- name：姿势名称，≤12字，中文，不含性别后缀\n'
    '- description：详细动作说明，40-120字，覆盖身体、手臂、腿部、头部与表情要点，可包含道具/环境互动\n'
    '- category：类别（{categories}）\n'
    '约束：仅返回JSON；不得包含英文、emoji、Markdown；避免不当内容与暗示；避免不可能或危险动作；避免遮挡面部的手部特写；确保解剖结构正确（两臂两腿、五指且数量正确）。\n'
    '输入：\n场景分析：{scene}\n性别：{gender}'
)
ILLUSTRATION_PROMPT_TEMPLATE = (
    '黑白线条教学示意图，单人，{gender}人物；居中构图，白色纯背景；线宽均匀、简洁清晰，突出姿势关键部位与肢体走向；'
    '解剖结构正确：两臂两腿，手部五指且数量正确；无多肢体、无多手、多指、肢体融合或断裂；左右手与左右腿不混淆；关节角度合理、动作可实现；'
    '不写实、不照片风、不3D、不彩色；不包含文字、水印、Logo、复杂背景与阴影；风格专业、健康、优雅，适合摄影教学；'
    '负面：真实照片、复杂背景、彩色、文字、水印、Logo、阴影、3D、写实、多肢体、多手指、解剖错误、肢体融合、重影、透视混乱。'
)

