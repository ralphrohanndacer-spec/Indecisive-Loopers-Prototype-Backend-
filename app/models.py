import enum
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class StallType(enum.Enum):
    STALL = "stall"
    STUDENTPRENEUR = "studentpreneur"
    COOP = "coop"


class Stall(Base):
    __tablename__ = "stalls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    location: Mapped[str] = mapped_column(String, index = True)
    is_open: Mapped[bool] = mapped_column(Boolean, index=True)
    stall_type: Mapped[StallType] = mapped_column(Enum(StallType), default=StallType.STALL, index=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    menu_items: Mapped[list["MenuItem"]] = relationship(back_populates="stall", cascade="all, delete-orphan")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stall_id: Mapped[int] = mapped_column(Integer, ForeignKey("stalls.id"))
    name: Mapped[str] = mapped_column(String, index=True)
    food_category: Mapped[str] = mapped_column(String, index=True)
    is_halal: Mapped[bool] = mapped_column(Boolean, index=True)
    is_available: Mapped[bool] = mapped_column(Boolean, index=True)
    is_best_seller: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    price: Mapped[float] = mapped_column(Float, index=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    stall: Mapped["Stall"] = relationship(back_populates="menu_items")