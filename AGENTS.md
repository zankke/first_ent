# Agentic Coding Guidelines

This repository contains a full-stack application with a React/Vite frontend and a Python backend.
These guidelines describe how AI agents should operate within this codebase to ensure consistency, safety, and quality.

## 1. Project Structure & Navigation

*   **Root (`/`)**: Contains the Frontend application (React + Vite).
    *   **Note**: `App.tsx`, `index.tsx`, and `types.ts` are located directly in the root, not in a `src/` directory.
    *   **Components**: located in `components/`.
    *   **Services**: Frontend API services in `services/`.
*   **Backend (`backend/`)**: Python services using Flask/FastAPI/SQLAlchemy.
    *   Contains standalone scripts (e.g., `artist_db_assistant.py`) and service modules.
*   **Puppeteer Service (`puppeteer_service/`)**: A separate Node.js service for scraping/automation.
*   **Scripts (`scripts/`)**: DevOps and utility scripts.

**Agent Rule**: Always use `glob` to verify file locations before reading or writing, as the structure (especially frontend) is slightly non-standard.

## 2. Build, Run, and Test Commands

### Frontend (Root)
*   **Install Dependencies**: `npm install`
*   **Development Server**: `npm run dev` (Runs Vite)
*   **Production Build**: `npm run build`
*   **Testing**:
    *   Currently, there are no configured frontend tests in `package.json`.
    *   **Agent Action**: If adding tests, use **Vitest** (compatible with Vite). Configure it in `vite.config.ts`.
    *   **Run Single Test**: If Vitest is set up: `npx vitest run path/to/test.file.ts`

### Backend (`backend/`)
*   **Environment**: Python 3.x.
*   **Install Dependencies**: `pip install -r backend/requirements.txt`
*   **Run Scripts**: `python backend/script_name.py`
*   **Testing**:
    *   `pytest` is listed in `requirements.txt`.
    *   **Run All Tests**: `pytest backend/`
    *   **Run Single Test**: `pytest backend/path/to/test_file.py::test_function_name`
    *   **Agent Action**: If no tests exist for a module you are modifying, create a `tests/` directory within `backend/` and add a `test_*.py` file.

## 3. Code Style & Conventions

### General
*   **Safety**: Never commit `.env` files, API keys (Gemini, OpenAI, etc.), or credentials.
*   **Paths**: Always use **absolute paths** when using tools (e.g., `/Users/itsme/KONIKT/first_ent/v2/...`).

### Frontend (TypeScript + React)
*   **Framework**: React 19+ with Vite.
*   **Language**: TypeScript (Strict mode enabled).
*   **Styling**: **Tailwind CSS**. Use inline classes (e.g., `className="p-4 bg-gray-900"`). Avoid external CSS files unless necessary.
*   **Type Definitions**:
    *   Use `interface` for defining object shapes (see `types.ts`).
    *   Example: `export interface ArtistProfile { ... }`
*   **Naming**:
    *   Components: `PascalCase` (e.g., `ProfileCard.tsx`).
    *   Functions/Variables: `camelCase`.
    *   Files: Match the export (e.g., `App.tsx`, `geminiService.ts`).
*   **State Management**: Use React Hooks (`useState`, `useEffect`).
*   **Imports**:
    *   Group imports: React/libs first, then local components, then types.
    *   Use relative paths for local files (e.g., `./components/SearchInput`).

### Backend (Python)
*   **Style Guide**: Follow **PEP 8**.
*   **Type Hints**: **Mandatory** for function arguments and return values.
    *   Example: `def artist_exists_in_db(artist_name: str) -> bool:`
*   **Docstrings**: Use triple-quotes `"""` for function and class documentation.
*   **Libraries**:
    *   Use `pydantic` for data validation models.
    *   Use `sqlalchemy` for database interactions.
    *   Use `requests` or `httpx` for HTTP calls.
*   **Error Handling**: Use `try/except` blocks specific to the expected error (avoid bare `except:`).

## 4. Workflow for Agents

1.  **Exploration**:
    *   Start by listing files (`ls -F`) or using `glob` to locate relevant code.
    *   Read `package.json` or `requirements.txt` to verify available libraries before importing them.

2.  **Implementation**:
    *   **Edit in place**: Use `edit` to modify existing files. Preserve indentation carefully.
    *   **New Files**: Use `write` to create new files. Ensure the directory exists first.
    *   **Conventions**: Mimic existing code patterns. If you see `import { useState } from 'react'`, do not change it to `import React from 'react'`.

3.  **Verification**:
    *   After changes, try to verify correctness.
    *   Since explicit test commands are missing in some areas, **create a small reproduction script** or a unit test to verify your logic if possible.
    *   **Frontend Check**: Ensure `npm run build` passes to catch TypeScript errors.

## 5. Specific Rules & known Issues

*   **Vite Config**: The project uses `vite.config.ts`. Any build configuration changes should happen there.
*   **Mixed Stack**: Be aware that `puppeteer_service` has its own `node_modules`. Do not confuse it with the root frontend dependencies.
*   **Database**: References to SQL files (`first_ent_20251025.sql`) imply a relational DB (likely MySQL/MariaDB given `PyMySQL` and `mysql-connector-python`).
*   **Secrets**: The `.env` file contains `GEMINI_API_KEY`. Ensure code reading this uses `os.getenv` (Python) or `import.meta.env` (Vite/Frontend).

## 6. Deprecation & Cleanup

*   If you encounter unused files (e.g., temp scripts in `tmp/`), ask the user before deleting, but feel free to ignore them during analysis.
*   Legacy files: `init_project.sh` and `start_firstent.sh` are executable scripts (`*`). Check them if you need to understand the startup sequence.

---
*Generated by opencode on Jan 29, 2026*
