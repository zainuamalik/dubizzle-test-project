from sqlalchemy import Column, Integer, ForeignKey
from database.models.base import Base

class RolePrivilege(Base):
    __tablename__ = "role_privileges"
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    privilege_id = Column(Integer, ForeignKey("privileges.id", ondelete="CASCADE"), primary_key=True)