from fastapi import HTTPException, Depends, status
from app.auth.dependencies import get_current_user

def get_user_permissions(user):
    return {
        permission.name
        for role in user.roles
        for permission in role.permissions
    }

def require_permission(permission_name: str):
    def permission_checker(current_user = Depends(get_current_user)):

        # print("User:", current_user.username)
        # print("Roles:", current_user.roles)

        user_permission = get_user_permissions(current_user)

        # for role in current_user.roles:
        #     # print("Role:", role.name)
        #     # print("Role Permissions:", role.permissions)

        #     for permission in role.permissions:
        #         user_permission.add(permission.name)

        # print("Collected Permissions:", user_permission)
        # print("Required Permission:", permission_name)

        if permission_name not in user_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user

    return permission_checker
