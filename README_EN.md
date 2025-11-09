# PoseMind

<div align="center">

![Version](https://img.shields.io/badge/version-4.0-ff2442?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/flask-3.0.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/license-Apache--2.0-green?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/AI-Powered-ff6b9d?style=for-the-badge)

**AI-powered photography pose generation system**

*Intelligent scene recognition • Automatic pose generation • Professional guidance*

[中文](README.md) • [Features](#-features) • [Quick Start](#-quick-start) • [Deployment](#-deployment)

</div>

---

## 📸 Project Showcase

<div align="center">

### Upload Interface
![Upload Interface](templates/e0de9b5a-1324-4021-9bbd-fcb8b233ebaa.png)

*Clean and beautiful upload interface with drag-and-drop support*

### Generation Results
![Generation Results](templates/1b8f42b4ed405df99a488846f86dd93c.png)

*AI Scene Analysis + Intelligent Pose Generation + Line Art Guidance*

</div>

---

## 📖 About

PoseMind is an AI-driven photography pose recommendation system that automatically analyzes scene context and generates personalized pose suggestions. Using advanced vision models and image generation AI, it creates professional pose guidance illustrations.

### Key Highlights

- 🧠 **AI Scene Analysis** - Automatically recognizes environment, lighting, and atmosphere
- 🎯 **Intelligent Pose Generation** - Creates unique poses based on scene context
- 🎨 **Line Art Illustrations** - Generates clear pose guidance diagrams
- 🚀 **Fully Automated** - Only requires gender selection, everything else is AI-powered
- 🌸 **Beautiful UI** - Modern, responsive design

---

## ✨ Features

### 🧠 AI-Powered Scene Recognition
- Automatic environment analysis (indoor/outdoor/urban/nature)
- Atmosphere detection (casual/formal/romantic/energetic)
- Lighting assessment (natural/artificial/backlight)

### 🎯 Intelligent Pose Generation
- **No fixed pose lists** - AI generates poses in real-time
- Context-adaptive suggestions based on scene analysis
- Unique poses every time

### 🎨 Professional Guidance
- Generates 4 diverse pose illustrations per request
- Clear line art diagrams showing body positioning
- Detailed pose descriptions and categories
- Download functionality for all generated images

<div align="center">

![Feature Showcase](templates/1b8f42b4ed405df99a488846f86dd93c.png)

*AI intelligently analyzes scenes and generates personalized pose guidance diagrams*

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- ModelScope API key ([Get one here](https://modelscope.cn/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/genz27/PoseMind.git
cd PoseMind
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API keys**

Set environment variables (recommended):
```bash
export AI_MODELSCOPE_API_KEY="your-ai-api-key"
export IMAGE_MODELSCOPE_API_KEY="your-image-api-key"
```

Or edit `config.py`:
```python
AI_MODELSCOPE_API_KEY = 'your-ai-api-key'
IMAGE_MODELSCOPE_API_KEY = 'your-image-api-key'
```

4. **Run the application**

**Docker (Recommended):**
```bash
docker-compose up -d
```

**Development mode:**
```bash
python app.py
```

**Production mode:**
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
├── gunicorn_config.py     # Gunicorn config
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Uploaded images
└── results/               # Generated images
```

---

## 🔧 Configuration

### Environment Variables

```bash
# AI Model API
AI_MODELSCOPE_API_KEY=your-ai-api-key
AI_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/v1

# Image Generation API
IMAGE_MODELSCOPE_API_KEY=your-image-api-key
IMAGE_MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/

# Server Configuration
PORT=5000
```

---

## 💻 Usage

### Web Interface

1. Upload a photo
2. Select gender (Female/Male)
3. Click "Start Generation"
4. Wait 2-3 minutes
5. View results and download images

### API Usage

#### Upload Image
```bash
curl -X POST http://localhost:5000/api/upload -F "image=@photo.jpg"
```

#### Generate Poses
```bash
curl -X POST http://localhost:5000/api/generate-poses \
  -H "Content-Type: application/json" \
  -d '{"image_filename": "photo.jpg", "gender": "female"}'
```

---

## 🛠️ Technology Stack

- **Backend**: Flask, Gunicorn
- **AI Models**: Qwen3-VL-235B-A22B-Instruct, Qwen-Image
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker, Docker Compose

---

## 🚀 Deployment

### Docker Deployment (Recommended)

```bash
# Use Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

### Production

```bash
# Use Gunicorn
gunicorn -c gunicorn_config.py app:app
```

### Cloud Platforms

Supports deployment to AWS EC2, Google Cloud, Azure, Heroku, Railway, Render, etc.

---

## 📊 API Reference

### POST /api/upload
Upload an image file

### POST /api/generate-poses
Generate pose suggestions

### GET /results/<filename>
Download generated pose image

---

## 🤝 Contributing

Contributions are welcome! Please submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ModelScope** - For providing powerful AI models
- **Qwen Series Models** - For vision understanding and image generation
- **Flask** - For the excellent web framework

---

## 📧 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/genz27/PoseMind/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/genz27/PoseMind/issues)

---

<div align="center">

**Made with ❤️ by the PoseMind Team**

[⬆ Back to Top](#posemind)

</div>

