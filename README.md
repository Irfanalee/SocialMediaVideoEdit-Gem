# Agentic Video Editor

An AI-powered video editing tool that automatically analyzes long-form videos, extracts the most engaging highlights, and creates social media-ready teasers.

## Features

- 🎥 **AI Video Analysis** - Uses Google Gemini 1.5 Pro to analyze video content
- ✂️ **Automatic Highlight Extraction** - Identifies 3-5 most engaging moments
- 🎬 **Video Processing** - Cuts and stitches clips using FFmpeg
- 🚀 **Modern Web Interface** - Built with Next.js and React
- 🐳 **Docker Support** - Easy deployment with Docker Compose

## Architecture

- **Frontend**: Next.js (React) + Tailwind CSS
- **Backend**: FastAPI (Python)
- **AI Engine**: Google Gemini 1.5 Pro
- **Video Processing**: FFmpeg

## Prerequisites

- Docker and Docker Compose
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SocialMediaVideoEdit-Gem
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Usage

1. Open http://localhost:3000 in your browser
2. Upload a video file (drag & drop or click to browse)
3. Click "Start Processing"
4. Wait for the AI to analyze and process your video
5. Download the generated highlight reel

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload a video file
- `POST /process/{file_id}` - Start processing a video
- `GET /jobs/{job_id}` - Check job status
- `GET /static/{filename}` - Download processed video

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Pricing

Uses Google Gemini 1.5 Pro with generous free tier:
- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day

Estimated cost per video:
- 10-minute video: ~$0.03
- 1-hour video: ~$0.13

## License

MIT
