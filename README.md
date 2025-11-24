# Meeting Assistant

A FastAPI-based meeting assistant application with recording, transcription, and summarization features.

## Features

- Record meetings directly from the browser
- Upload audio files for processing
- Automatic transcription and summarization
- Save meeting details to Supabase database
- Dark mode support

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. Push your code to a GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and set up the service

### Method 2: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the following settings:
   - **Name**: meeting-assistant (or your preferred name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or your preferred plan)

5. Add environment variables (if needed):
   - `PYTHON_VERSION`: 3.11.0

6. Click "Create Web Service"

### Important Notes

- **API URLs**: After deployment, update the fetch URLs in `meeting.html`:
  - Change `http://localhost:8000/meetings` to your Render app URL (e.g., `https://your-app-name.onrender.com/meetings`)
  
- **CORS**: The app is configured to allow all origins. For production, update the `allow_origins` in `main.py` to your specific domain.

- **Supabase**: The Supabase credentials are currently hardcoded in `main.py`. Consider using environment variables for production.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Open your browser to `http://localhost:8000`

## Environment Variables (Optional)

For better security in production, consider moving sensitive data to environment variables:

- `SUPABASE_URL`
- `SUPABASE_API_KEY`
- `WEBHOOK_URL` (update in the HTML)

## License

MIT
