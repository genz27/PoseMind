# PoseMind

<div align="center">

![Version](https://img.shields.io/badge/version-4.0-ff2442?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/flask-3.0.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/AI-Powered-ff6b9d?style=for-the-badge)

**AI-powered photography pose generation system**

*Intelligent scene recognition • Automatic pose generation • Professional guidance*

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 About

PoseMind is an AI-driven photography pose recommendation system that automatically analyzes scene context and generates personalized pose suggestions. Using advanced vision models and image generation AI, it creates professional pose guidance illustrations tailored to your photos.

### Key Highlights

- 🧠 **AI Scene Analysis** - Automatically recognizes environment, lighting, and atmosphere
- 🎯 **Intelligent Pose Generation** - Creates unique poses based on scene context
- 🎨 **Line Art Illustrations** - Generates clear pose guidance diagrams
- 🚀 **Fully Automated** - Only requires gender selection, everything else is AI-powered
- 🌸 **Beautiful UI** - Modern, responsive design with pink gradient theme

---

## ✨ Features

### 🧠 AI-Powered Scene Recognition
- Automatic environment analysis (indoor/outdoor/urban/nature)
- Atmosphere detection (casual/formal/romantic/energetic)
- Lighting assessment (natural/artificial/backlight)
- Context-aware pose suggestions

### 🎯 Intelligent Pose Generation
- **No fixed pose lists** - AI generates poses in real-time
- Context-adaptive suggestions based on scene analysis
- Unique poses every time
- Unlimited creative possibilities

### 🎨 Professional Guidance
- Generates 4 diverse pose illustrations per request
- Clear line art diagrams showing body positioning
- Detailed pose descriptions and categories
- Download functionality for all generated images

### 🚀 Fully Automated Workflow
- **User only selects gender** - AI handles everything else
- No manual style or scene selection needed
- 2-3 minutes to get personalized poses
- One-click regeneration

### 🌸 Modern UI/UX
- Pink gradient theme
- Responsive design (desktop/tablet/mobile)
- Smooth animations and transitions
- Intuitive user interface

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- ModelScope API key ([Get one here](https://modelscope.cn/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/PoseMind.git
cd PoseMind
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API keys**

Set environment variables (recommended):
```bash
# AI Model API (for scene analysis and pose generation)
export AI_MODELSCOPE_API_KEY="your-ai-api-key"
export AI_MODELSCOPE_BASE_URL="https://api-inference.modelscope.cn/v1"

# Image Generation API (for pose illustrations)
export IMAGE_MODELSCOPE_API_KEY="your-image-api-key"
export IMAGE_MODELSCOPE_BASE_URL="https://api-inference.modelscope.cn/"
```

Or edit `config.py`:
```python
AI_MODELSCOPE_API_KEY = 'your-ai-api-key'
IMAGE_MODELSCOPE_API_KEY = 'your-image-api-key'
```

4. **Run the application**

**Option 1: Docker (Recommended)**
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t posemind:latest .
docker run -d -p 5000:5000 \
  -e AI_MODELSCOPE_API_KEY="your-key" \
  -e IMAGE_MODELSCOPE_API_KEY="your-key" \
  posemind:latest
```

**Option 2: Development mode**
```bash
python app.py
```

**Option 3: Production mode (with Gunicorn)**
```bash
gunicorn -c gunicorn_config.py app:app
```

5. **Access the web interface**

Open your browser and visit: `http://localhost:5000`

---

## 📁 Project Structure

```
PoseMind/
├── app.py                 # Flask application
├── config.py              # Configuration file
├── gunicorn_config.py     # Gunicorn production config
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore file
├── README.md              # This file
├── LICENSE                # MIT License
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Uploaded images
└── results/               # Generated pose images
```

---

## 🔧 Configuration

### Environment Variables

All configuration can be set via environment variables (recommended for production):

```bash
# Server Configuration
PORT=5000

# AI Model API (Scene Analysis & Pose Generation)
AI_MODELSCOPE_API_KEY=your-ai-api-key
AI_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/v1
VISION_MODEL=Qwen/Qwen3-VL-235B-A22B-Instruct

# Image Generation API
IMAGE_MODELSCOPE_API_KEY=your-image-api-key
IMAGE_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/
IMAGE_GENERATION_MODEL=Qwen/Qwen-Image

# Timeout Settings
IMAGE_GENERATION_TIMEOUT=150
IMAGE_GENERATION_CHECK_INTERVAL=5
API_REQUEST_TIMEOUT=30
```

### Config File

Edit `config.py` for local development:

```python
# Number of poses to generate
NUM_POSES_TO_GENERATE = 4

# Model Configuration
VISION_MODEL = 'Qwen/Qwen3-VL-235B-A22B-Instruct'
IMAGE_GENERATION_MODEL = 'Qwen/Qwen-Image'
```

---

## 💻 Usage

### Web Interface

1. **Upload a photo** - Click or drag & drop an image
2. **Select gender** - Choose "Female" or "Male"
3. **Generate poses** - Click "Start Generation" button
4. **View results** - See scene analysis and 4 pose illustrations
5. **Download images** - Click download button on any pose card
6. **Regenerate** - Click "Regenerate" button to get new poses

### API Usage

#### Upload Image
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "image=@photo.jpg"
```

#### Generate Poses
```bash
curl -X POST http://localhost:5000/api/generate-poses \
  -H "Content-Type: application/json" \
  -d '{
    "image_filename": "photo.jpg",
    "gender": "female"
  }'
```

### Python Example
```python
import requests

# Upload image
with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/upload',
        files={'image': f}
    )
    filename = response.json()['filename']

# Generate poses
response = requests.post(
    'http://localhost:5000/api/generate-poses',
    json={
        'image_filename': filename,
        'gender': 'female'
    }
)

result = response.json()
print(f"Scene: {result['scene_analysis']}")
for pose in result['pose_variants']:
    print(f"- {pose['name']}: {pose['description']}")
```

---

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **OpenAI API Client** - AI model integration
- **Pillow** - Image processing
- **Gunicorn** - Production WSGI server

### AI Models (ModelScope)
- **Qwen3-VL-235B-A22B-Instruct** - Vision model for scene analysis
- **Qwen3-VL-235B-A22B-Instruct** - AI model for pose generation
- **Qwen-Image** - Image generation model

### Frontend
- **HTML5 + CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **Responsive Design** - Mobile-first approach

---

## 📊 API Reference

### POST /api/upload

Upload an image file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `image` (file, max 16MB)

**Response:**
```json
{
  "status": "success",
  "filename": "timestamp_hash.jpg"
}
```

### POST /api/generate-poses

Generate pose suggestions based on uploaded image.

**Request:**
```json
{
  "image_filename": "timestamp_hash.jpg",
  "gender": "female"
}
```

**Response:**
```json
{
  "status": "success",
  "scene_analysis": "Detailed scene analysis...",
  "gender": "Female",
  "pose_variants": [
    {
      "name": "Pose Name",
      "description": "Detailed description",
      "category": "Category",
      "image": "pose_variant_1.jpg"
    }
  ]
}
```

### GET /results/<filename>

Download generated pose image.

---

## 🚀 Deployment

### Docker Deployment (Recommended)

#### Prerequisites
- Docker installed ([Get Docker](https://www.docker.com/get-started))
- Docker Compose (optional, for easier deployment)

#### Quick Start with Docker

1. **Build the Docker image**
```bash
docker build -t posemind:latest .
```

2. **Run the container**
```bash
docker run -d \
  -p 5000:5000 \
  -e AI_MODELSCOPE_API_KEY="your-ai-api-key" \
  -e IMAGE_MODELSCOPE_API_KEY="your-image-api-key" \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/results:/app/results \
  --name posemind \
  posemind:latest
```

3. **Access the application**
```
http://localhost:5000
```

#### Using Docker Compose (Recommended)

1. **Create `.env` file** (optional)
```env
AI_MODELSCOPE_API_KEY=your-ai-api-key
IMAGE_MODELSCOPE_API_KEY=your-image-api-key
AI_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/v1
IMAGE_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/
```

2. **Start with Docker Compose**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f
```

4. **Stop the application**
```bash
docker-compose down
```

#### Docker Commands

```bash
# Build image
docker build -t posemind:latest .

# Run container
docker run -d -p 5000:5000 --name posemind posemind:latest

# View logs
docker logs -f posemind

# Stop container
docker stop posemind

# Start container
docker start posemind

# Remove container
docker rm posemind

# Remove image
docker rmi posemind:latest
```

#### Docker Volume Management

Persist uploads and results data:
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/results:/app/results \
  posemind:latest
```

#### Environment Variables

Set environment variables in Docker:
```bash
docker run -d \
  -p 5000:5000 \
  -e AI_MODELSCOPE_API_KEY="your-key" \
  -e IMAGE_MODELSCOPE_API_KEY="your-key" \
  -e PORT=5000 \
  posemind:latest
```

Or use `.env` file with Docker Compose:
```yaml
environment:
  - AI_MODELSCOPE_API_KEY=${AI_MODELSCOPE_API_KEY}
  - IMAGE_MODELSCOPE_API_KEY=${IMAGE_MODELSCOPE_API_KEY}
```

### Production with Gunicorn

#### Direct Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -c gunicorn_config.py app:app
```

#### Systemd Service (Linux)

Create `/etc/systemd/system/posemind.service`:
```ini
[Unit]
Description=PoseMind Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/PoseMind
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable posemind
sudo systemctl start posemind
```

### Cloud Deployment

#### AWS EC2 / Google Cloud / Azure

1. **Launch a VM instance**
2. **Install Docker**
3. **Clone repository**
4. **Configure environment variables**
5. **Run with Docker Compose**

#### Heroku

```bash
# Create Procfile
echo "web: gunicorn -c gunicorn_config.py app:app" > Procfile

# Deploy
git push heroku main
```

#### Railway / Render / Fly.io

1. **Connect GitHub repository**
2. **Set environment variables**
3. **Deploy automatically**

### Environment Variables

Set all required environment variables in your deployment environment:

```bash
# Server Configuration
PORT=5000

# AI Model API
AI_MODELSCOPE_API_KEY=your-ai-api-key
AI_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/v1
VISION_MODEL=Qwen/Qwen3-VL-235B-A22B-Instruct

# Image Generation API
IMAGE_MODELSCOPE_API_KEY=your-image-api-key
IMAGE_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/
IMAGE_GENERATION_MODEL=Qwen/Qwen-Image

# Timeout Settings
IMAGE_GENERATION_TIMEOUT=150
IMAGE_GENERATION_CHECK_INTERVAL=5
API_REQUEST_TIMEOUT=30
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/PoseMind.git
cd PoseMind

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ModelScope** - For providing powerful AI models
- **Qwen Series Models** - For vision understanding and image generation
- **Flask** - For the excellent web framework
- **All Contributors** - For their valuable contributions

---

## 📧 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/yourusername/PoseMind/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/yourusername/PoseMind/issues)
- 📖 **Documentation**: Check the [Wiki](https://github.com/yourusername/PoseMind/wiki)

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ by the PoseMind Team**

[⬆ Back to Top](#posemind)

</div>
