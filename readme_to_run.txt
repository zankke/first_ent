1. Start Backend 
   cd backend \
   python -m venv venv \
   source venv/bin/activate \
   pip install -r requirements.txt \
   flask db upgrade \
   ../scripts/start_backend.sh \

2. Start Frontend 
   cd frontend
   npm install
   ./scripts/start_frontend.sh