# DocMind

DocMind is an intelligent document assistant that helps users understand and analyze their documents effectively. The application uses advanced AI capabilities to process various document formats and enables interactive conversations about their content.

![Demo](./gifs/docmind.gif)

## Features

### Core Features
- 📄 Support for multiple document formats (PDF, DOCX, PPTX, TXT)
- 💬 Interactive chat interface with AI-powered responses
- 🔒 Secure user authentication system
- 📱 Responsive web interface
- 🤖 Powered by Google's Gemini 1.5 Flash model
- 📊 Document chunking and vector storage for efficient retrieval

### Technical Features
- Asynchronous document processing
- Real-time chat capabilities
- Vectorized document storage for semantic search
- Memory-efficient document chunking
- Robust error handling and logging
- Stateless authentication using JWT
- Configurable document processing parameters

## Tech Stack

### Backend Framework
- **FastAPI**: High-performance Python web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM for database management

### AI/ML Components
- **LangChain**: Framework for developing AI-powered applications
  - Document loading and processing
  - Text splitting and chunking
  - Vector store integration
  - Chat memory management
- **Google Gemini**: Advanced language model for text processing
- **ChromaDB**: Vector database for efficient document storage and retrieval

### Security
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing
- **OAuth2**: Authentication flow implementation
- **CORS**: Cross-Origin Resource Sharing protection

## Prerequisites

- Python 3.8+
- Google API key (for Gemini model)
- PostgreSQL (optional, can use SQLite)
- Virtual environment tool (venv)

## Environment Variables

Required environment variables in `.env`:
```env
# Core Settings
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost/docmind
GOOGLE_API_KEY=your_google_api_key

# API Configuration
PROJECT_NAME=DocMind
VERSION=1.0.0
API_V1_STR=/api/v1

# Security Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Document Processing
UPLOAD_FOLDER=uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
VECTOR_STORE_PATH=./chroma_db
```

## Installation

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

## API Endpoints

### Authentication
- **POST** `/api/v1/auth/signup`
  - Create new user account
  - Body: `{"email": "string", "password": "string", "name": "string"}`
  - Returns: User information

- **POST** `/api/v1/auth/login`
  - Authenticate user and get access token
  - Form data: `username`, `password`
  - Returns: JWT token and user name

- **GET** `/api/v1/auth/me`
  - Get current user information
  - Requires: JWT token
  - Returns: User details

### Documents
- **POST** `/api/v1/documents/upload`
  - Upload and process document
  - Multipart form: `file`
  - Supports: PDF, DOCX, PPTX, TXT
  - Returns: Processing status and chunk count

### Chat
- **POST** `/api/v1/chat`
  - Send query about uploaded document
  - Body: `{"query": "string"}`
  - Returns: AI response with source attribution

## Project Structure
```
app/
├── api/
│   ├── endpoints/
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── chat.py         # Chat functionality
│   │   └── documents.py    # Document processing
│   └── routes.py           # API router configuration
├── core/
│   ├── config.py           # Application settings
│   ├── deps.py             # Dependencies (DB, Auth)
│   └── security.py         # Security utilities
├── db/
│   ├── database.py         # Database configuration
│   └── models.py           # SQLAlchemy models
├── services/
│   ├── auth_service.py     # Authentication logic
│   ├── chat_manager.py     # Chat handling
│   └── document_processor.py # Document processing
└── main.py                 # Application entry point
```

## Key Components

### ChatManager
- Manages conversation state and memory
- Handles document context retrieval
- Integrates with Google Gemini for response generation
- Maintains user-specific conversation history

### DocumentProcessor
- Validates and processes uploaded files
- Chunks documents for efficient processing
- Generates vector embeddings
- Manages persistent storage in ChromaDB
- Handles cleanup of temporary files

### Authentication Service
- User registration and validation
- Password hashing and verification
- JWT token generation and validation
- User session management

## Document Processing Pipeline

1. Document Upload
   - File validation and type checking
   - Size limit enforcement
   - Temporary storage management
   - Content extraction based on file type

2. Text Processing
   - Document chunking with configurable size
   - Chunk overlap for context preservation
   - Vector embedding generation
   - Metadata extraction and storage

3. Storage
   - Vector store initialization
   - Document indexing
   - User-specific storage management
   - Cleanup procedures

4. Chat Processing
   - Context retrieval from vector store
   - Relevant chunk selection
   - LLM query processing
   - Response generation with sources

## Security Features

- JWT-based authentication with configurable expiration
- Password hashing with bcrypt
- Protected API endpoints using OAuth2
- Request validation using Pydantic
- CORS protection with configurable origins
- File type validation and sanitization
- Secure temporary file handling

## Frontend Setup

1. Clone and Navigate to the frontend directory:
```bash
git clone https://github.com/charans2702/docmind-ui.git
cd docmind-ui
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
