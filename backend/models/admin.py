from sqlmodel import Field, Relationship, SQLModel


# admins
class AdminBase(SQLModel):
    username: str = Field(min_length=1, max_length=50, unique=True)


class Admin(AdminBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=1)

    roles: list["AdminRole"] = Relationship(
        back_populates="admin", sa_relationship_kwargs={"cascade": "delete"}
    )


class AdminInput(AdminBase):
    password: str = Field(min_length=8, max_length=16)
    role_id: int


class AdminUpdate(SQLModel):
    username: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=16)
    role_id: int | None = None


class AdminOutput(AdminBase):
    id: int
    roles: list["RoleOutput"] = []

    @classmethod
    def from_orm(cls, admin):
        return cls(
            id=admin.id,
            username=admin.username,
            roles=[
                RoleOutput(
                    id=ar.role.id,
                    name=ar.role.name,
                    permissions=[
                        PermissionOutput(id=rp.permission.id, name=rp.permission.name)
                        for rp in ar.role.permissions
                    ],
                )
                for ar in admin.roles
            ],
        )


# roles
class Role(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=3, max_length=50, unique=True)

    admin_roles: list["AdminRole"] = Relationship(
        back_populates="role", sa_relationship_kwargs={"cascade": "delete"}
    )
    permissions: list["RolePermission"] = Relationship(back_populates="role")


class RoleOutput(SQLModel):
    id: int
    name: str
    permissions: list["PermissionOutput"] = []


# permissions
class Permission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=3, max_length=50, unique=True)

    role_permissions: list["RolePermission"] = Relationship(
        back_populates="permission", sa_relationship_kwargs={"cascade": "delete"}
    )


class PermissionOutput(SQLModel):
    id: int
    name: str


# admin_roles
class AdminRole(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    admin_id: int = Field(..., foreign_key="admin.id")
    role_id: int = Field(..., foreign_key="role.id")

    admin: Admin = Relationship(back_populates="roles")
    role: Role = Relationship(back_populates="admin_roles")


class AdminRoleOutput(SQLModel):
    role: RoleOutput


# role_permissions
class RolePermission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role_id: int = Field(..., foreign_key="role.id")
    permission_id: int = Field(..., foreign_key="permission.id")

    role: Role = Relationship(back_populates="permissions")
    permission: Permission = Relationship(back_populates="role_permissions")


class RolePermissionOutput(SQLModel):
    permission: Permission
