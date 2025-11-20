import enum
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class AccessStatus(str, enum.Enum):
    SUCCESS = "success"
    DENIED = "denied"
    SPOOFING = "spoofing"

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100), nullable=True)
    face_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    access_logs: Mapped[list["AccessLog"]] = relationship(back_populates="employee")

class Terminal(Base):
    __tablename__ = "terminals"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True)
    location: Mapped[str] = mapped_column(String)
    access_logs: Mapped[list["AccessLog"]] = relationship(back_populates="terminal")

class AccessLog(Base):
    __tablename__ = "access_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=True)
    terminal_id: Mapped[int] = mapped_column(ForeignKey("terminals.id"))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[AccessStatus] = mapped_column(Enum(AccessStatus))
    liveness_score: Mapped[float] = mapped_column()
    snapshot_url: Mapped[str] = mapped_column(String, nullable=True)

    employee: Mapped["Employee"] = relationship(back_populates="access_logs")
    terminal: Mapped["Terminal"] = relationship(back_populates="access_logs")


class SystemConfig(Base):
    __tablename__ = "system_configs"
    
    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String)