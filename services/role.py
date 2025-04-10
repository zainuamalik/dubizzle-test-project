from sqlalchemy.orm import Session
from database.models.roles import Role
from database.models.privileges import Privilege
from database.models.role_privileges import RolePrivilege

class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def assign_role_to_user(self, user, role_name: str) -> None:
        user.role = role_name
        self.db.commit()

    def add_privilege_to_role(self, role_id: int, privilege_id: int) -> None:
        rp = RolePrivilege(role_id=role_id, privilege_id=privilege_id)
        self.db.add(rp)
        self.db.commit()

    def check_user_privilege(self, user, privilege_name: str) -> bool:
        # For this demo, assume role names map to privileges directly.
        role = self.db.query(Role).filter(Role.name == user.role).first()
        if not role:
            return False
        privileges = self.db.query(Privilege).join(RolePrivilege).filter(RolePrivilege.role_id == role.id).all()
        return any(p.name == privilege_name for p in privileges)