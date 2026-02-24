from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.auth.hashing import hash_password

def seed_data():
    db: Session = SessionLocal()
    
    # For Admin Role
    admin_role = db.query(Role).filter(Role.name == "Admin").first()

    if not admin_role:

        # Create Permissions
        assign_permission = Permission(name="ASSIGN_ROLE")
        read_permission = Permission(name="READ_DATA")
        delete_permission = Permission(name="DELETE_DATA")

        db.add_all([read_permission, assign_permission, delete_permission])
        db.commit()

        # Create Roles
        admin_role = Role(name="Admin")
        user_role = Role(name="User")

        db.add_all([admin_role, user_role])
        db.commit()

        # Assign permissions to admin roles(Admin gets all, User gets read only)
        admin_role.permissions.append(read_permission)
        admin_role.permissions.append(assign_permission)
        admin_role.permissions.append(delete_permission)

        # Assign permissions to user role
        user_role.permissions.append(read_permission)

        db.commit()

    # For Admin User
    admin_user = db.query(User).filter(User.username == "admin").first()

    if not admin_user:

        admin_user = User(
            username="admin",
            password=hash_password("admin123")
        )

        admin_user.roles.append(admin_role)

        db.add(admin_user)
        db.commit()

    if admin_role not in admin_user.roles:
        admin_user.roles.append(admin_role)
        db.commit()

    db.close()