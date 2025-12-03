
def validate_admin_action(action: str) -> bool:
    allowed_actions = ["create", "delete", "update", "read"]
    return action.lower() in allowed_actions
