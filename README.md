# DocMind

DocMind is an intelligent document assistant that helps users understand and analyze their documents effectively. The application uses advanced AI capabilities to process various document formats and enables interactive conversations about their content.

## Features

- 📄 Support for multiple document formats (PDF, DOCX, PPTX, TXT)
- 💬 Interactive chat interface with AI-powered responses
- 🔒 Secure user authentication system
- 📱 Responsive web interface
- 🤖 Powered by Google's Gemini 1.5 Flash model
- 📊 Document chunking and vector storage for efficient retrieval

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- LangChain (AI/LLM framework)
- Google Gemini (LLM model)
- ChromaDB (Vector store)
- JWT (Authentication)

### Frontend
- React
- Tailwind CSS
- Shadcn/ui components
- Axios (API client)

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Google API key (for Gemini model)

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost/docmind
GOOGLE_API_KEY=your_google_api_key
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/charans2702/DocMind.git
cd DocMind
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## API Endpoints

### Authentication
- POST `/api/v1/auth/signup` - Register new user
- POST `/api/v1/auth/login` - User login
- GET `/api/v1/auth/me` - Get current user info

### Documents
- POST `/api/v1/documents/upload` - Upload document
- GET `/api/v1/documents/chunks` - Get document chunks

### Chat
- POST `/api/v1/chat` - Send message to chat

## Project Structure

### Backend
```
app/
├── api/
│   ├── endpoints/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── documents.py
│   └── routes.py
├── core/
│   ├── config.py
│   ├── deps.py
│   └── security.py
├── db/
│   ├── database.py
│   └── models.py
├── schemas/
├── services/
│   ├── auth_service.py
│   ├── chat_manager.py
│   └── document_processor.py
main.py
```


## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Request validation using Pydantic
- Protected API endpoints

## Document Processing Pipeline

1. Document Upload
   - File validation
   - Content extraction
   - Text chunking
   - Vector embedding generation
   - Storage in ChromaDB

2. Chat Processing
   - Context retrieval from vector store
   - LLM query processing
   - Response generation with source attribution

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[MIT License](LICENSE)
