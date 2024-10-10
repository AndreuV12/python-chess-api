from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Enum
from app.models import Base


from sqlalchemy.orm import relationship


class Opening(Base):
    __tablename__ = "openings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)
    preview_fen = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    data = Column(JSON)

    # Relación con la tabla `users`
    user = relationship("User", backref="openings")
