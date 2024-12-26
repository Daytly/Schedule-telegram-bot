from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)
    class_name = Column(String(10), nullable=True)

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, username='{self.username}', class_name='{self.class_name}')>"


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True)

    # Определяем связь с таблицей users
    user = relationship("User", back_populates="admin")

    def __repr__(self) -> str:
        return f"<Admin(id={self.id}, user_id={self.user_id})>"


# Обратная связь для пользователя
User.admin = relationship("Admin", back_populates="user")


class ClassSchedule(Base):
    __tablename__ = 'class_schedules'

    class_name = Column(String(10), primary_key=True)
    schedule = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<ClassSchedule(class_name='{self.class_name}', schedule='{self.schedule}')>"
