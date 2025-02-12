from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel, select

from .models import Session, engine
from .models.admin import Permission, Role, RolePermission


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed_roles_and_permissions(session)

    yield

    pass


def seed_roles_and_permissions(session: Session):
    roles = ["super_admin", "user_manager", "product_manager", "category_manager"]
    permissions = [
        "create_admin",
        "delete_admin",
        "view_admin",
        "update_admin",
        "disable_user",
        "create_product",
        "update_product",
        "delete_product",
        "view_product",
        "create_category",
        "update_category",
        "delete_category",
        "view_roles",
    ]

    role_permissions = {
        "super_admin": permissions,
        "user_manager": [
            "disable_user",
        ],
        "product_manager": [
            "create_product",
            "update_product",
            "delete_product",
            "view_product",
        ],
        "category_manager": ["create_category", "update_category", "delete_category"],
    }

    # add new roles
    existing_roles = [role.name for role in session.exec(select(Role)).all()]
    new_roles = [Role(name=role) for role in roles if role not in existing_roles]
    if new_roles:
        session.add_all(new_roles)
        session.commit()

    # add new permissions
    existing_permissions_names = [
        perm.name for perm in session.exec(select(Permission)).all()
    ]
    new_permissions = [
        Permission(name=perm)
        for perm in permissions
        if perm not in existing_permissions_names
    ]

    if new_permissions:
        session.add_all(new_permissions)
        session.commit()

    # add new role_permissions
    existing_roles = session.exec(select(Role)).all()
    existing_perms_dict = {
        perm.name: perm.id for perm in session.exec(select(Permission)).all()
    }

    for role in existing_roles:
        existing_role_perms_name = [perm.permission.name for perm in role.permissions]

        for perm_name in role_permissions[role.name]:
            if perm_name not in existing_role_perms_name:
                session.add(
                    RolePermission(
                        role_id=role.id, permission_id=existing_perms_dict[perm_name]
                    )
                )

    session.commit()
