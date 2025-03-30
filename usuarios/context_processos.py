def user_type(request):
    # Verificar se o usuário está autenticado
    if not request.user.is_authenticated:
        return {}

    # Verificar se o usuário tem um perfil de aluno ou empresa
    user_type = None
    if hasattr(request.user, 'alunoprofile'):
        user_type = 'aluno'
    elif hasattr(request.user, 'anuncianteprofile'):
        user_type = 'anunciante'

    # Retornar o user_type para ser incluído no contexto
    return {'user_type': user_type}


