from enum import Enum

class CategoryType(str, Enum):
    BOOKING_CHANGES = "Booking Changes"
    AIR_TRAVEL = "Air Travel"
    PACKAGES = "Packages"
    STUDENT_INQUIRY = "Student Inquiry"
    PROMOTIONS = "Promotions"
    COMPLAINT = "Complaint"

class ConversationStep(str, Enum):
    GET_CATEGORY = "get_category"
    GET_NAME = "get_name"
    GET_EMAIL = "get_email"
    GET_DESTINATION = "get_destination"
    GET_DATES = "get_dates"
    GET_TICKETS_COUNT = "get_tickets_count"
    CONFIRM_BOOKING = "confirm_booking"
    COMPLETED = "completed" 