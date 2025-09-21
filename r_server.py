# from mcp.server.fastmcp import FastMCP

# # mcp = FastMCP("WeatherTools",host="0.0.0.0", port=8002)
# mcp = FastMCP("WeatherTools")

# # Weather_tool_def = {
# #     "name": "getWeather",
# #     "description": "Get weather information for a city",
# #     "inputSchema": {
# #         "type": "object",
# #         "properties": {
# #             "city": {"type": "string"}
# #         },
# #         "required": ["city"]
# #     }
# # }

# # @mcp.tool(name=Weather_tool_def["name"], description=Weather_tool_def["description"])
# # def get_weather(city: str):
# #     """Returns weather information for a given city."""
# #     return f"The weather in {city} is sunny with 25°C"


# @mcp.tool()
# def weather(city: str) -> str:
#     """Returns the current weather of a city."""
#     return f"The weather in {city} is sunny, 25°C."


# if __name__ == "__main__":
#     # Run on port 8001
#     mcp.run(transport="streamable-http")


#########################################################################################################################

from fastapi import HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
import getpass

# Get macOS username
user = getpass.getuser()

# Database URL: No password, connect as local user
# DATABASE_URL = f"postgresql://{user}@localhost/nagesh"
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/nagesh"

# Set up the SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = "student"  # table name
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    roll_number = Column(String, unique=True, index=True)
    percentage = Column(Float, nullable=False)
    student_class = Column(String, nullable=False)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Define Pydantic model for validation
class StudentCreate(BaseModel):
    name: str
    roll_number: str
    percentage: float
    student_class: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize FastMCP app
mcp = FastMCP("StudentTools")

# MCP tool to create a student
@mcp.tool()
def create_student_tool(
    name: str,
    roll_number: str,
    percentage: float,
    student_class: str
) -> Dict[str, Any]:
    """
    Creates a new student record in the database.
    
    Args:
        name: The name of the student.
        roll_number: The unique roll number of the student.
        percentage: The percentage score of the student.
        student_class: The class/grade of the student.
    
    Returns:
        A dictionary containing the created student's details or an error message.
    """
    # Create a Pydantic model instance for validation
    try:
        student_data = StudentCreate(
            name=name,
            roll_number=roll_number,
            percentage=percentage,
            student_class=student_class
        )
    except ValueError as e:
        return {"error": f"Invalid input: {str(e)}"}

    # Get database session
    db_gen = get_db()
    db = next(db_gen)

    try:
        # Check if the roll_number already exists
        db_student = db.query(Student).filter(Student.roll_number == student_data.roll_number).first()
        if db_student:
            return {"error": "Student with this roll number already exists."}

        # Create and insert the new student into the database
        db_student = Student(**student_data.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        # Return the created student's details
        return {
            "id": db_student.id,
            "name": db_student.name,
            "roll_number": db_student.roll_number,
            "percentage": db_student.percentage,
            "student_class": db_student.student_class,
            "message": "Student created successfully."
        }

    except Exception as e:
        db.rollback()
        return {"error": f"Failed to create student: {str(e)}"}

    finally:
        db.close()

# Existing weather tool for reference
@mcp.tool()
def weather(city: str) -> str:
    """Returns the current weather of a city."""
    return f"The weather in {city} is sunny, 25°C."

if __name__ == "__main__":
    # Run on port 8001
    mcp.run(transport="streamable-http")