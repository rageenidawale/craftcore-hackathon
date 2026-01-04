def is_onboarding_complete(user):
    return bool(user.first_name and user.last_name)