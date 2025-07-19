
ASIN VIKING Real OAuth Backend

1. Upload this to GitHub as a new repo.
2. On Render.com, click 'New Web Service' and connect the repo.
3. Use these settings:

   Build Command:
       pip install fastapi uvicorn httpx

   Start Command:
       uvicorn main:app --host 0.0.0.0 --port 8000

4. Test your OAuth at:
   https://your-app.onrender.com/login

This will redirect to Amazon, authorize the app, and exchange for real tokens.
