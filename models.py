from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Float, Enum, DateTime
from sqlalchemy.orm import relationship

class BaseRepr:
    """ generischhe __repr__Methode
        alle Klassen, die von  BaseRepr erben, bekommen automatisch eine
        def __repr__-Methode
    """
    def __repr__(self):
        fields = ", ".join(
            f"{col.name}={getattr(self, col.name)!r}"
            for col in self.__table__.columns
        )
        return f"<{self.__class__.__name__}({fields})>"

class Todo(Base, BaseRepr):
    __tablename__="todos"
    id=Column(Integer, primary_key=True)
    home_city=Column(String(150))
    departure_id=Column(String(150))
    destination_city=Column(String(150))
    arrival_id=Column(String(150))
    vacation_start=Column(Date) # format="YYYY.MM.DD"
    vacation_end=Column(Date) # format="YYYY.MM.DD"
    #state=Column(Enum("OPEN","IN_PROGRESS","DONE"), nullable=False, default="OPEN")
    user_id = Column(Integer,ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    user = relationship("User", back_populates="todos")
    flights = relationship("Flight", back_populates="todos",  cascade="all, delete-orphan")
    hotels = relationship("Hotel", back_populates="todos",  cascade="all, delete-orphan")

    # def __repr__(self):
    #     return f"Todo id={self.id}, home_city={self.home_city}, destination_city={self.destination_city}, vacation_start={self.vacation_start}, vacation_end={self.vacation_end}, user_id={self.user_id}, flight_id={self.flight_id}" #to string

# 1
class User(Base,BaseRepr):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True) #default auto_increment
    username = Column(String(50), nullable=False)
    password = Column(String(100))
    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan") # back_populates="user" -> Bidirectional

    def __repr__(self):
        return f"Todo id={self.id}, username={self.username}, password={self.password}"
    

class Flight(Base,BaseRepr):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True) #default auto_increment
    departure_airport = Column(String(100))
    departure_id = Column(String(100))
    departure_time = Column(DateTime)
    arrival_airport = Column(String(100))
    arrival_id = Column(String(100))
    arrival_time = Column(DateTime)
    airplane = Column(String(100))
    airline = Column(String(100))
    flight_number = Column(String(100))
    total_duration = Column(Integer())
    price = Column(Integer())
    todo_id = Column(Integer,ForeignKey("todos.id", ondelete="CASCADE"))
    todos = relationship("Todo", back_populates="flights") # back_populates="flights" -> Bidirectional

    # def __repr__(self):
        
    #     return f"Todo id={self.id}"

class Hotel(Base,BaseRepr):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True) #default auto_increment
    type = Column(String(50))
    name = Column(String(255))
    link = Column(String(500))
    check_in_date = Column(String(20))
    check_out_date = Column(String(20))
    hotel_class = Column(Integer())
    total_rate = Column(Integer())
    overall_rating = Column(Float())
    location_rating = Column(Float())
    todo_id = Column(Integer,ForeignKey("todos.id", ondelete="CASCADE"))
    todos = relationship("Todo", back_populates="hotels") # back_populates="flights" -> Bidirectional

    # def __repr__(self):
        
    #     return f"Todo id={self.id}"