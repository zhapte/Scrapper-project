import uuid

from sqlalchemy import Column, Boolean, DateTime, ForeignKey, Numeric, Text, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    favorites = relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    amazon_asin = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    current_price = Column(Numeric(10,2))
    product_url = Column(Text, nullable=False)
    last_scraped = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    favorites = relationship(
        "Favorite",
        back_populates="product",
        cascade="all, delete-orphan"
    )

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='uq_favorites_user_product'),
    )

    favorite_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    target_price = Column(Numeric(10,2), nullable=False)
    notify_enabled = Column(Boolean, default=True)
    last_notified_at = Column(DateTime)
    last_notified_price = Column(Numeric(10,2))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="favorites")
