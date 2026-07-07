# 🎤 AI 语音识别与翻译系统

基于 [OpenAI Whisper](https://github.com/openai/whisper) 的语音识别 API 服务，支持自动语言检测，并可将识别结果翻译成目标语言。

## ✨ 功能特性

- 🎯 自动检测音频语言（支持中、英、日、韩、法、德、西、俄、阿、葡等 10+ 种语言）
- 🌐 自动翻译识别结果（内置中↔英翻译）
- 🔌 RESTful API，方便集成到其他系统
- 🖥️ 内置 Web Demo 页面（`index.html`），上传音频即可试用
- 🐳 支持 Docker 一键部署

## 📁 项目结构

```
voice-reco/
├── app.py            # Flask API 服务（语音识别 + 翻译）
├── index.html        # Web Demo 前端页面
├── Dockerfile         # Docker 镜像构建配置
├── start.sh           # 一键构建并启动脚本
├── test_api.sh        # API 测试脚本
└── requirements.txt   # Python 依赖
```

## 🚀 快速开始

```bash
bash start.sh
```

该脚本会自动构建镜像、启动容器并进行健康检查。也可手动执行：

```bash
docker build -t voice-recognition:latest .
docker run -d --name voice-api -p 5000:5000 --memory=6g voice-recognition:latest
```

### 使用 Web Demo

API 启动后，直接用浏览器打开 `index.html` 即可上传音频进行测试（默认请求 `http://localhost:5000`）。

### 测试 API

```bash
bash test_api.sh
```

## 📡 API 说明

| 接口 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/languages` | GET | 获取支持的语言列表 |
| `/transcribe` | POST | 上传音频，返回识别（及可选翻译）结果 |

示例请求：

```bash
curl -X POST http://localhost:5000/transcribe \
  -F "audio=@audio.mp3" \
  -F "target_language=en"
```

示例响应：

```json
{
  "transcribed_text": "你好，这是一个测试",
  "detected_language": "zh",
  "language_name": "Chinese",
  "translated_text": "Hello, this is a test",
  "target_language": "en"
}
```

## ⚙️ 配置

Whisper 模型大小可在 `app.py` 中修改（`tiny`/`base`/`small`/`medium`/`large-v3-turbo`），模型越大准确度越高，但耗时和内存占用也越大。
