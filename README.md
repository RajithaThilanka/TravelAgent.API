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
OPENAI_API_KEY=your_openai_api_key
```

4. Activate the virtual environment:

```bash
pipenv shell
```

5. Run the application:

```bash
pipenv run start
```

The API will be available at `http://localhost:5000`

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
