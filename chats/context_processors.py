def user_profile(request):
    return {
        'user_profile_id': request.user.profile.id if request.user.is_authenticated else None,
        'user_profile_name': request.user.profile.name if request.user.is_authenticated else None,
        'user_profile_pic': request.user.profile.user_pic if request.user.is_authenticated else None
    }
