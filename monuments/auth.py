import hashlib

from django.utils import timezone

from monuments.models import Token


def get_basic_auth(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split(' ')
        if len(auth) == 2 and auth[0] == 'Basic':
            return auth[1]
    return None


def get_or_create_token(user):
    token = Token.objects.filter(user=user)
    if token.count() >= 1:
        token = token[0]
        if not token.is_expired():
            return token
        token.delete()
    phrase = user.email + ':' + timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    hash_phrase = hashlib.sha256(bytes(phrase, 'ascii')).hexdigest()
    token = Token.objects.create(user=user, hash=hash_phrase)
    return token
