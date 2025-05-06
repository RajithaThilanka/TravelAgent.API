# Travel Agent API

A FastAPI-based travel agent chatbot that handles various travel-related inquiries and bookings.

## Features

- Interactive chat interface for travel inquiries
- Support for multiple inquiry categories:
  - Booking Changes
  - Air Travel
  - Packages
  - Student Inquiry
  - Promotions
  - Complaints
- Step-by-step conversation flow
- Session management
- Input validation
- CORS support for frontend integration

## Project Structure

```
TravelAgent.API/
├── app/
│   ├── api/
│   │   └── routes.py         # API endpoints and route handlers
│   │
│   ├── models/
│   │   ├── enums.py         # Enumeration classes
│   │   └── schemas.py       # Pydantic models for request/response
│   │
│   ├── services/
│   │   └── conversation.py  # Core conversation logic
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
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/v1/chat

Send a message to the chat bot. The first message will automatically start a new chat session and is processed as the category selection.

## Conversation Flow and Request Examples

### Step 1: Select Category (GET_CATEGORY)

```bash
POST /api/v1/chat
```

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

### Step 2: Provide Name (GET_NAME)

```bash
POST /api/v1/chat
```

Request:

```json
{
  "user_id": "user123",
  "message": "John Doe"
}
```

Response:

```json
{
  "message": "Thank you, John Doe. Could you provide your email address for contact purposes?",
  "current_step": "get_email",
  "collected_data": {
    "category": "Air Travel",
    "name": "John Doe"
  }
}
```

### Step 3: Provide Email (GET_EMAIL)

```bash
POST /api/v1/chat
```

Request:

```json
{
  "user_id": "user123",
  "message": "john.doe@example.com"
}
```

Response:

```json
{
  "message": "Got your email. What's your destination?",
  "current_step": "get_destination",
  "collected_data": {
    "category": "Air Travel",
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```

### Step 4: Provide Destination (GET_DESTINATION)

```bash
POST /api/v1/chat
```

Request:

```json
{
  "user_id": "user123",
  "message": "Paris"
}
```

Response:

```json
{
  "message": "Great choice! When are you planning to travel?",
  "current_step": "get_dates",
  "collected_data": {
    "category": "Air Travel",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "destination": "Paris"
  }
}
```

### Step 5: Provide Travel Dates (GET_DATES)

```bash
POST /api/v1/chat
```

Request:

```json
{
  "user_id": "user123",
  "message": "2024-06-15 to 2024-06-22"
}
```

Response:

```json
{
  "message": "How many tickets would you like to book?",
  "current_step": "get_tickets_count",
  "collected_data": {
    "category": "Air Travel",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "destination": "Paris",
    "travel_dates": "2024-06-15 to 2024-06-22"
  }
}
```

### Step 6: Provide Number of Tickets (GET_TICKETS_COUNT)

```bash
POST /api/v1/chat
```

Request:

```json
{
  "user_id": "user123",
  "message": "2"
}
```

Response:

```json
{
  "message": "Confirm your booking: \nName: John Doe\nEmail: john.doe@example.com\nDestination: Paris\nDates: 2024-06-15 to 2024-06-22\nTickets: 2\n\nType 'yes' to confirm or 'no' to cancel.",
  "current_step": "confirm_booking",
  "collected_data": {
    "category": "Air Travel",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "destination": "Paris",
    "travel_dates": "2024-06-15 to 2024-06-22",
    "tickets_count": 2
  }
}
```

### Step 7: Confirm Booking (CONFIRM_BOOKING)

```bash
POST /api/v1/chat
```

Request:

```json
{
  "user_id": "user123",
  "message": "yes"
}
```

Response:

```json
{
  "message": "Thank you for your booking! Your request has been processed successfully. You will receive a confirmation email shortly.",
  "current_step": "completed",
  "collected_data": {
    "category": "Air Travel",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "destination": "Paris",
    "travel_dates": "2024-06-15 to 2024-06-22",
    "tickets_count": 2,
    "confirmed": true
  }
}
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 guidelines. Use a linter to ensure code quality:

```bash
flake8
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
