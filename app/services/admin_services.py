from app.models.user import User
from app.models.role import Role
from fastapi import HTTPException

def assign_role_to_user_service(db, username: str, role_name: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role in user.roles:
        raise HTTPException(status_code=400, detail="User already has this role")

    user.roles.append(role)
    db.commit()

    return {"message": f"Role '{role_name}' assigned to user '{username}' successfully"}

def list_users_with_roles_service(db):
    users = db.query(User).all()
    
    return [
        {
            "username": user.username,
            "roles": [role.name for role in user.roles]
        }
        for user in users
    ]