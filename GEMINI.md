# Project Overview: AI-based Artist Management Framework

This project is an internal system designed to register, manage, and view information about affiliated artists. It's an "AI-based Artist Management Framework" with a focus on efficient artist data handling and media monitoring.

## Key Features:
1.  **Artist Information Management**: Register, manage, and view artist profiles.
2.  **Social Media Channel Integration**: Connect and collect statistics from Instagram and YouTube channels.
3.  **News Monitoring**: Automated news crawling for active artists using Perplexity API, scheduled daily at 5 AM. Includes sentiment analysis, relevance scoring, and real-time monitoring via a web interface.
4.  **Account Management**: System for managing user accounts.
5.  **Board Management**: Create and manage 게시판 (bulletin boards).
6.  **API Key Management**: Securely manage API keys for various services (e.g., Instagram, YouTube, Perplexity).
7.  **Database Configuration Management**: Manage database connection settings.

## Architecture:
*   **Frontend**: Streamlit, streamlit_antd_components, TailwindCSS, Bootstrap
*   **Backend**: Python, Streamlit, streamlit_antd_components
*   **Database**: MySQL (Docker container, container name 'mysql-dev' port 3306, database name: `first_ent`)
*   **Development Environment**: MacOS M2 PRO (ARM)

## Database Schema:
The project utilizes the following standardized database schemas:
*   **artists**: Basic artist information.
*   **channels**: Social media channel information (Instagram, YouTube, etc.).
*   **accounts**: System user accounts.
*   **boards**: Bulletin board management.
*   **api_keys**: API key management.
*   **database_configs**: Database connection settings.
*   **channel_stats**: Channel statistics data.
*   **posts**: Post information.

## Building and Running:

### 1. Docker Container Setup:
Start the MySQL Docker container:
```bash
./scripts/start_docker.sh
```

### 2. Backend Setup:
Navigate to the `backend` directory, set up a virtual environment, install dependencies, run database migrations, and start the backend server:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
./scripts/start_backend.sh
```

### 3. Frontend Setup:
Navigate to the `frontend` directory, install Node.js dependencies, and start the frontend development server:
```bash
cd frontend
npm install
./scripts/start_frontend.sh
```

### 4. News Crawling Scheduler Setup:
Configure environment variables (in `backend/.env`) and then start the scheduler:
```bash
# Example .env content (replace with actual keys)
PERPLEXITY_API_KEY=your-perplexity-api-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Start the scheduler
./scripts/start_scheduler.sh
```

## Development Conventions:

### UI/UX Design Principles:
*   **Frameworks**: TailwindCSS, Shadcn UI are actively used.
*   **Aesthetics**: Designed to look like a top-tier commercial professional software.
*   **Color Palette**: Limited to 5 or fewer simple color codes.
*   **Global Background**: Luxurious deep navy perspective gradient.
*   **Buttons**: Orange-toned buttons.
*   **Readability**: High readability UI.
*   **Components**: Shadcn/ui patterns (rounded-2xl, muted/foreground scale, focus ring).
*   **Feedback**: Sonner toast for immediate success/error status notifications.
