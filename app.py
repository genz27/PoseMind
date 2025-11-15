from flask import Flask, request, jsonify, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
import os
import base64
import requests
import time
import json
from PIL import Image, ImageDraw
from io import BytesIO
import logging
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = config.RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['SESSION_COOKIE_HTTPONLY'] = config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = config.SESSION_COOKIE_SAMESITE
app.config['SESSION_COOKIE_SECURE'] = config.SESSION_COOKIE_SECURE
app.secret_key = config.SECRET_KEY

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Note: We use direct API calls with requests instead of OpenAI client library
# to avoid version compatibility issues with the OpenAI library


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def add_composition_lines(image, line_type='rule_of_thirds', line_color=(255, 36, 66, 180), line_width=2):
    """
    在图片上添加构图线
    
    Args:
        image: PIL Image对象
        line_type: 构图线类型
            - 'rule_of_thirds': 三分法（九宫格）- 默认
            - 'diagonal': 对角线
            - 'center': 中心线
            - 'all': 所有构图线
        line_color: 线条颜色 (R, G, B, Alpha)，默认粉色半透明
        line_width: 线条宽度，默认2像素
    
    Returns:
        添加了构图线的PIL Image对象
    """
    # 创建图片副本，避免修改原图
    img_with_lines = image.copy()
    
    # 如果图片是RGB模式，转换为RGBA以支持透明度
    if img_with_lines.mode != 'RGBA':
        img_with_lines = img_with_lines.convert('RGBA')
    
    # 创建绘图对象
    draw = ImageDraw.Draw(img_with_lines, 'RGBA')
    
    width, height = img_with_lines.size
    
    if line_type == 'rule_of_thirds' or line_type == 'all':
        # 三分法构图线（九宫格）
        # 垂直线：1/3 和 2/3 位置
        x1 = width / 3
        x2 = width * 2 / 3
        draw.line([(x1, 0), (x1, height)], fill=line_color, width=line_width)
        draw.line([(x2, 0), (x2, height)], fill=line_color, width=line_width)
        
        # 水平线：1/3 和 2/3 位置
        y1 = height / 3
        y2 = height * 2 / 3
        draw.line([(0, y1), (width, y1)], fill=line_color, width=line_width)
        draw.line([(0, y2), (width, y2)], fill=line_color, width=line_width)
    
    if line_type == 'diagonal' or line_type == 'all':
        # 对角线
        draw.line([(0, 0), (width, height)], fill=line_color, width=line_width)
        draw.line([(width, 0), (0, height)], fill=line_color, width=line_width)
    
    if line_type == 'center' or line_type == 'all':
        # 中心线
        center_x = width / 2
        center_y = height / 2
        draw.line([(center_x, 0), (center_x, height)], fill=line_color, width=line_width)
        draw.line([(0, center_y), (width, center_y)], fill=line_color, width=line_width)
    
    # 如果原图是RGB，转换回RGB（保存为JPEG需要）
    if image.mode == 'RGB':
        # 创建白色背景
        background = Image.new('RGB', img_with_lines.size, (255, 255, 255))
        # 将RGBA图片合成到RGB背景上
        background.paste(img_with_lines, mask=img_with_lines.split()[3])  # 使用alpha通道作为mask
        img_with_lines = background
    
    return img_with_lines


def analyze_image_scene(image_path):
    """Analyze image to understand scene, location, and environment"""
    try:
        img_data = compress_image_for_api(image_path)
        image_url = f"data:image/jpeg;base64,{img_data}"
        
        system_prompt = config.SCENE_ANALYSIS_SYSTEM_PROMPT
        prompt = config.SCENE_ANALYSIS_USER_PROMPT

        # Use direct API call to avoid OpenAI client library version issues
        api_url = f"{config.AI_MODELSCOPE_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.AI_MODELSCOPE_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": config.VISION_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                },
            ],
            "stream": False,
            "max_tokens": 300,
        }
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=config.API_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        scene_info = result["choices"][0]["message"]["content"]
        logging.info(f"Scene analysis: {scene_info}")
        return scene_info
            
    except Exception as e:
        logging.exception(f"Scene analysis error: {str(e)}")
        return "户外自然场景"


def compress_image_for_api(image_path, max_size_kb=300):
    """Compress image to reduce API payload size - 更激进的压缩"""
    try:
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode not in ['RGB', 'L']:
            img = img.convert('RGB')
        
        # 更小的尺寸以适配 API 限制
        max_dimension = 768  # 从1024降低到768
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save to bytes with compression
        buffer = BytesIO()
        quality = 75  # 从85降低到75
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        # Reduce quality if still too large - 更激进的压缩
        while buffer.tell() > max_size_kb * 1024 and quality > 20:
            buffer = BytesIO()
            quality -= 10
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        final_size = buffer.tell() / 1024
        logging.info(f"Compressed image: {final_size:.2f} KB (quality: {quality})")
        
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        logging.error(f"Image compression error: {str(e)}")
        # Fallback: read original file
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')


def generate_pose_variant_from_original(image_path, pose_description, scene_context, gender, index):
    """Generate pose illustration using text-to-image (线条小人姿势指导图)"""
    try:
        base_url = config.IMAGE_MODELSCOPE_BASE_URL
        common_headers = {
            "Authorization": f"Bearer {config.IMAGE_MODELSCOPE_API_KEY}",
            "Content-Type": "application/json",
        }
        
        gender_text = "女生" if gender == "female" else "男生"
        
        illustration_prompt = config.ILLUSTRATION_PROMPT_TEMPLATE.format(
            gender=gender_text,
            pose=pose_description
        )
        
        logging.info(f"生成姿势指导图 {index}: {pose_description[:50]}...")
        logging.info(f"Prompt: {illustration_prompt[:100]}...")
        
        # Prepare request payload - 使用Qwen-Image生成
        payload = {
            "model": config.IMAGE_GENERATION_MODEL,  # 使用 Qwen/Qwen-Image
            "prompt": illustration_prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        logging.info(f"Submitting image generation request {index}...")
        logging.info(f"Using model: {config.IMAGE_GENERATION_MODEL}")
        
        # Submit async image generation task
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            timeout=config.API_REQUEST_TIMEOUT
        )
        
        # Log response for debugging
        logging.info(f"Response status code: {response.status_code}")
        if response.status_code != 200:
            logging.error(f"Response body: {response.text}")
            response.raise_for_status()
        
        result_data = response.json()
        logging.info(f"API Response: {result_data}")
        
        task_id = result_data.get("task_id")
        if not task_id:
            logging.error(f"No task_id in response: {result_data}")
            return None
        
        logging.info(f"Task {index} submitted with ID: {task_id}")
        
        # Poll for completion
        max_attempts = config.IMAGE_GENERATION_TIMEOUT // config.IMAGE_GENERATION_CHECK_INTERVAL
        for attempt in range(max_attempts):
            time.sleep(config.IMAGE_GENERATION_CHECK_INTERVAL)
            
            logging.info(f"Checking task {index} status (attempt {attempt + 1}/{max_attempts})...")
            
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                timeout=config.API_REQUEST_TIMEOUT
            )
            result.raise_for_status()
            data = result.json()
            
            task_status = data.get("task_status", "UNKNOWN")
            logging.info(f"Task {index} status: {task_status}")
            
            if task_status == "SUCCEED":
                output_images = data.get("output_images", [])
                if not output_images:
                    logging.error(f"No output images in response: {data}")
                    return None
                
                image_url = output_images[0]
                logging.info(f"Downloading generated image from: {image_url}")
                
                img_response = requests.get(image_url, timeout=config.API_REQUEST_TIMEOUT)
                img_response.raise_for_status()
                image = Image.open(BytesIO(img_response.content))
                
                # 添加构图线（三分法/九宫格）
                # 使用粉色半透明线条，宽度2像素
                image_with_lines = add_composition_lines(
                    image, 
                    line_type='rule_of_thirds',  # 三分法构图线
                    line_color=(255, 36, 66, 180),  # 粉色半透明 (#FF2442 with alpha)
                    line_width=2
                )
                
                filename = f"pose_variant_{index}_{int(time.time())}.jpg"
                filepath = os.path.join(app.config['RESULT_FOLDER'], filename)
                if image_with_lines.mode != 'RGB':
                    image_with_lines = image_with_lines.convert('RGB')
                image_with_lines.save(filepath, quality=90)
                
                logging.info(f"Successfully generated pose variant {index} with composition lines: {filename}")
                return filename
                
            elif task_status == "FAILED":
                error_msg = data.get("error", "Unknown error")
                logging.error(f"Task {index} failed: {error_msg}")
                return None
            elif task_status in ["PENDING", "RUNNING"]:
                continue
            else:
                logging.error(f"Unexpected task status: {task_status}")
                continue
        
        logging.error(f"Task {index} timed out after {max_attempts} attempts")
        return None
        
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error for pose variant {index}: {str(e)}")
        if e.response is not None:
            logging.error(f"Response status: {e.response.status_code}")
            logging.error(f"Response body: {e.response.text}")
        return None
    except Exception as e:
        logging.exception(f"Pose variant generation error {index}: {str(e)}")
        return None




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/plan-poses', methods=['POST'])
def plan_poses():
    data = request.get_json()
    image_filename = data.get('image_filename')
    gender = data.get('gender', 'female')

    today = time.strftime('%Y-%m-%d')
    usage_date = session.get('usage_date')
    if usage_date != today:
        session['usage_date'] = today
        session['usage_count'] = 0
    count = session.get('usage_count', 0)
    if count >= 20:
        return jsonify({'error': '今日次数已用完（20/20），请明日再试'}), 429
    session['usage_count'] = count + 1

    if not image_filename:
        return jsonify({'error': '请先上传图片'}), 400
    if not config.AI_MODELSCOPE_API_KEY or not config.IMAGE_MODELSCOPE_API_KEY:
        return jsonify({'error': '缺少API密钥，请配置AI与图片生成服务密钥'}), 500

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    if not os.path.exists(image_path):
        return jsonify({'error': '图片不存在'}), 404

    try:
        gender_name = config.GENDER_OPTIONS.get(gender, '女生')
        scene_context = analyze_image_scene(image_path)
        pose_descriptions = get_diverse_poses_for_scene(scene_context, gender)
        result = {
            'status': 'success',
            'scene_analysis': scene_context,
            'gender': gender_name,
            'poses': pose_descriptions
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'生成失败: {str(e)}'}), 500


@app.route('/api/generate-poses', methods=['POST'])
def generate_poses():
    """Generate diverse pose variants based on AI scene analysis and gender"""
    data = request.get_json()
    
    image_filename = data.get('image_filename')
    gender = data.get('gender', 'female')
    
    today = time.strftime('%Y-%m-%d')
    usage_date = session.get('usage_date')
    if usage_date != today:
        session['usage_date'] = today
        session['usage_count'] = 0
    count = session.get('usage_count', 0)
    if count >= 20:
        return jsonify({'error': '今日次数已用完（20/20），请明日再试'}), 429
    session['usage_count'] = count + 1
    
    if not image_filename:
        return jsonify({'error': '请先上传图片'}), 400
    if not config.AI_MODELSCOPE_API_KEY or not config.IMAGE_MODELSCOPE_API_KEY:
        return jsonify({'error': '缺少API密钥，请配置AI与图片生成服务密钥'}), 500
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    if not os.path.exists(image_path):
        return jsonify({'error': '图片不存在'}), 404
    
    try:
        gender_name = config.GENDER_OPTIONS.get(gender, '女生')
        
        # AI analyzes the scene to understand context
        logging.info("Analyzing scene...")
        scene_context = analyze_image_scene(image_path)
        
        # Get diverse poses based on scene analysis and gender
        logging.info("Selecting diverse poses...")
        pose_descriptions = get_diverse_poses_for_scene(scene_context, gender)
        
        # Generate pose variants by editing original image
        pose_variants = []
        for idx, pose_desc in enumerate(pose_descriptions[:config.NUM_POSES_TO_GENERATE], 1):
            logging.info(f"Generating pose variant {idx}/{config.NUM_POSES_TO_GENERATE}: {pose_desc['name']}")
            
            variant_filename = generate_pose_variant_from_original(
                image_path, 
                pose_desc['description'], 
                scene_context,
                gender, 
                idx
            )
            
            if variant_filename:
                pose_variants.append({
                    'name': pose_desc['name'],
                    'description': pose_desc['description'],
                    'category': pose_desc.get('category', ''),
                    'image': variant_filename
                })
            else:
                logging.error(f"Failed to generate pose variant {idx}")
        
        result = {
            'status': 'success',
            'scene_analysis': scene_context,
            'gender': gender_name,
            'pose_variants': pose_variants
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'生成失败: {str(e)}'}), 500


@app.route('/api/generate-pose-image', methods=['POST'])
def generate_pose_image():
    data = request.get_json()
    image_filename = data.get('image_filename')
    gender = data.get('gender', 'female')
    pose_description = data.get('pose_description')
    scene_context = data.get('scene_context', '')
    index = int(data.get('index', 1))

    if not image_filename or not pose_description:
        return jsonify({'error': '缺少必要参数'}), 400
    if not config.IMAGE_MODELSCOPE_API_KEY:
        return jsonify({'error': '缺少图片生成服务密钥'}), 500

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    if not os.path.exists(image_path):
        return jsonify({'error': '图片不存在'}), 404

    try:
        filename = generate_pose_variant_from_original(
            image_path,
            pose_description,
            scene_context,
            gender,
            index
        )
        if not filename:
            return jsonify({'error': '生成失败'}), 500
        return jsonify({'status': 'success', 'image': filename})
    except Exception as e:
        return jsonify({'error': f'生成失败: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    """Simple upload endpoint that returns the filename"""
    if 'image' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件格式'}), 400
    
    try:
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            Image.open(filepath).verify()
        except Exception:
            os.remove(filepath)
            return jsonify({'error': '文件内容无效或已损坏'}), 400
        
        return jsonify({
            'status': 'success',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500


def get_diverse_poses_for_scene(scene_context, gender='female'):
    """Use AI to intelligently generate diverse poses based on scene analysis"""
    try:
        gender_text = "女生" if gender == "female" else "男生"
        system_prompt = config.POSE_SYSTEM_PROMPT
        prompt = config.POSE_USER_PROMPT_TEMPLATE.format(
            n=config.NUM_POSES_TO_GENERATE,
            categories="|".join(config.POSE_CATEGORIES),
            scene=scene_context,
            gender=gender_text,
        )

        # Use direct API call to avoid OpenAI client library version issues
        api_url = f"{config.AI_MODELSCOPE_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.AI_MODELSCOPE_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": config.VISION_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "max_tokens": 1000,
        }
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=config.API_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"].strip()
        logging.info(f"AI pose suggestions: {ai_response}")
        
        # Parse JSON response
        import json
        # Extract JSON from potential markdown code blocks
        if '```json' in ai_response:
            ai_response = ai_response.split('```json')[1].split('```')[0].strip()
        elif '```' in ai_response:
            ai_response = ai_response.split('```')[1].split('```')[0].strip()
        
        poses = json.loads(ai_response)
        
        for pose in poses:
            if gender_text not in pose['name']:
                pose['name'] = f"{pose['name']} · {gender_text}"
        
        return poses[:config.NUM_POSES_TO_GENERATE]
        
    except Exception as e:
        logging.error(f"AI pose generation error: {str(e)}")
        # Fallback: simple default poses
        gender_suffix = "女生" if gender == "female" else "男生"
        return [
            {'name': f'自然站姿 · {gender_suffix}', 'description': '自然站立，一手插袋或垂放，微笑看向镜头', 'category': '经典'},
            {'name': f'轻松坐姿 · {gender_suffix}', 'description': '随意坐下，双手自然放置，表情放松', 'category': '坐姿'},
            {'name': f'侧身回望 · {gender_suffix}', 'description': '侧身站立，回头看向镜头，展现优雅线条', 'category': '经典'},
            {'name': f'自由漫步 · {gender_suffix}', 'description': '自然行走，捕捉动态瞬间', 'category': '动态'},
        ][:config.NUM_POSES_TO_GENERATE]






@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    print("\n" + "="*60)
    print("🎨 PoseMind - AI Photography Pose Recommendation System")
    print("="*60)
    print(f"\n✨ Server starting on http://{config.HOST}:{config.PORT}")
    print(f"📁 Upload folder: {config.UPLOAD_FOLDER}")
    print(f"📁 Results folder: {config.RESULT_FOLDER}")
    print(f"\n🤖 AI Model Configuration:")
    print(f"   Vision Model: {config.VISION_MODEL}")
    print(f"   API Base URL: {config.AI_MODELSCOPE_BASE_URL}")
    print(f"\n🎨 Image Generation Model Configuration:")
    print(f"   Generation Model: {config.IMAGE_GENERATION_MODEL}")
    print(f"   API Base URL: {config.IMAGE_MODELSCOPE_BASE_URL}")
    print(f"\n💡 Open your browser and visit: http://localhost:{config.PORT}")
    print("⏹  Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)

