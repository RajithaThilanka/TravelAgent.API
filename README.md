# Travel Agent API

A FastAPI-based travel agent chatbot that handles various travel-related inquiries and bookings using LangChain and OpenAI.

## Features

- Interactive chat interface for travel inquiries
- Support for multiple inquiry categories:
  - Booking Changes
  - Air Travel
  - Packages
  - Student Inquiry
  - Promotions
  - Complaints
- Step-by-step conversation flow with validation
- Session management
- Input validation
- CORS support for frontend integration
- LangChain integration for enhanced conversation handling
- OpenAI integration for natural language processing

## Project Structure

```
TravelAgent.API/
├── app/
│   ├── api/
│   │   └── routes.py         # API endpoints and route handlers
│   │
│   ├── models/
│   │   ├── enums.py         # Enumeration classes (ConversationStep, CategoryType)
│   │   └── schemas.py       # Pydantic models for request/response
│   │
│   ├── services/
│   │   └── conversation.py  # Core conversation logic and flow management
│   │
│   ├── config/             # Configuration files
│   │
│   ├── utils/              # Utility functions
│   │
│   └── main.py             # FastAPI application entry point
│
├── tests/                  # Test files
│
├── .env                    # Environment variables
│
├── .gitignore             # Git ignore file
│
├── Pipfile                # Python dependencies
│
└── README.md              # Project documentation
```

## Setup

### Option 1: Local Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd TravelAgent.API
```

2. Install dependencies using pipenv:

```bash
pipenv install
```

3. Create a `.env` file in the root directory with the following variables:

```
# Database Configuration
# Option 1: Individual components
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=travel_agent

# Option 2: Full database URL (overrides individual components)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/travel_agent

# API Configuration
OPENAI_API_KEY=your_openai_api_key

# For Docker
DOCKER_DB_HOST=db
```

4. Activate the virtual environment:

```bash
pipenv shell
```

5. Initialize the database:

```bash
# Create initial migration
pipenv run db-revision "initial"

# Apply migrations
pipenv run db-migrate
```

6. Run the application:

```bash
pipenv run start
```

### Option 2: Docker Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd TravelAgent.API
```

2. Create a `.env` file in the root directory with the following variables:

```
# Database Configuration
# Option 1: Individual components
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=travel_agent

# Option 2: Full database URL (overrides individual components)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/travel_agent

# API Configuration
OPENAI_API_KEY=your_openai_api_key

# For Docker
DOCKER_DB_HOST=db
```

3. Build and run using Docker Compose:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`

## Database Schema

The application uses PostgreSQL with the following main tables:

- **users**: Stores user information
  - id, email, name, created_at, updated_at

- **inquiries**: Stores travel inquiries
  - id, user_id, category, destination, travel_dates, tickets_count, status, created_at, updated_at

- **conversations**: Stores chat conversations
  - id, inquiry_id, current_step, collected_data, is_completed, created_at, updated_at

- **messages**: Stores individual chat messages
  - id, conversation_id, content, is_user, created_at

- **audit_logs**: Stores system audit information
  - id, table_name, record_id, action, old_values, new_values, user_id, timestamp, ip_address, user_agent

## API Documentation

Once the server is running, you can access:

- Swagger UI documentation: `http://localhost:5000/docs`
- ReDoc documentation: `http://localhost:5000/redoc`

## Conversation Flow

The chatbot follows a structured conversation flow based on the selected category. Here's how it works:

1. **Category Selection (GET_CATEGORY)**
   - User selects from available categories
   - Validates category input

2. **Name Collection (GET_NAME)**
   - Collects user's full name
   - Validates name format (no email addresses)

3. **Email Collection (GET_EMAIL)**
   - Collects user's email address
   - Validates email format

4. **Destination Collection (GET_DESTINATION)**
   - Collects travel destination
   - Validates destination input

5. **Date Collection (GET_DATES)**
   - Collects travel dates
   - Available for relevant categories

6. **Ticket Count (GET_TICKETS_COUNT)**
   - Collects number of tickets
   - Only for Air Travel and Packages categories

7. **Booking Confirmation (CONFIRM_BOOKING)**
   - Confirms booking details
   - Available for booking-related categories

8. **Completion (COMPLETED)**
   - Provides final confirmation
   - Category-specific completion messages

## API Endpoints

### POST /api/v1/chat

Send a message to the chat bot. The first message will automatically start a new chat session and is processed as the category selection.

Request:

```json
{
  "user_id": "user123",
  "message": "Air Travel"
}
```

Response:

```json
{
  "message": "Got it! What's your full name?",
  "current_step": "get_name",
  "collected_data": {
    "category": "Air Travel"
  }
}
```

## Development

### Running Tests

```bash
pipenv run pytest
```

### Code Formatting

```bash
pipenv run black .
```

### Linting

```bash
pipenv run flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.