# NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG NG

class User:
    def __init__(
        self, id: int,
        name: str,
        permissions: list[str] | None = None
    ) -> None:
        self.id = id
        self.name = name
        self.permissions = permissions if permissions else []

    def add_permission(self, permission: str) -> None:
        self.permissions.append(permission)


alice = User(0, "alice", ["read"])
print(alice.permissions)    # ['read']

bob = User(1, "bob", alice.permissions)

bob.add_permission("write")

print(bob.permissions)  # ['read', 'write']
print(alice.permissions)    # ['read', 'write'] <- ?!?!?!

# `bob.permissions` and `alice.permissions` refer to the same object.
print(id(bob.permissions))  # 139846030651520
print(id(alice.permissions))    # 139846030651520
