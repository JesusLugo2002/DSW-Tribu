import datetime
from functools import partial

import pytest
from django.conf import settings
from django.template.defaultfilters import truncatewords
from django.test import Client
from faker import Faker
from model_bakery import baker
from model_bakery.utils import seq
from pytest_django.asserts import assertContains, assertRedirects

from echos.models import Echo
from waves.models import Wave


@pytest.fixture
def user(django_user_model):
    return baker.make(django_user_model, _fill_optional=True)


@pytest.fixture
def echo(fake):
    return baker.make(Echo, content=partial(fake.paragraph, nb_sentences=10))


@pytest.fixture
def wave(fake):
    return baker.make(Wave, content=partial(fake.paragraph, nb_sentences=10))


@pytest.fixture
def fake():
    return Faker()


@pytest.mark.django_db
def test_echo_model_has_proper_fields(client: Client, echo):
    PROPER_FIELDS = ('content', 'created_at', 'updated_at', 'user')
    for field in PROPER_FIELDS:
        assert getattr(echo, field) is not None


@pytest.mark.django_db
def test_wave_model_has_proper_fields(client: Client, wave):
    PROPER_FIELDS = ('content', 'created_at', 'updated_at', 'user', 'echo')
    for field in PROPER_FIELDS:
        assert getattr(wave, field) is not None


def test_required_apps_are_installed():
    PROPER_APPS = ('shared', 'echos', 'waves', 'accounts', 'users')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    assert len(custom_apps) == len(PROPER_APPS)
    for app in PROPER_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps


@pytest.mark.django_db
def test_login(client: Client, django_user_model):
    USERNAME = 'pytest'
    PASSWORD = 'pwtest'

    user = django_user_model.objects.create_user(username=USERNAME, password=PASSWORD)

    response = client.get('/login/')
    assert response.status_code == 200
    # wrong login
    response = client.post('/login/', dict(username=user.username, password=USERNAME))
    assert response.status_code == 200
    assertContains(response, 'username')
    assertContains(response, 'password')
    # right login
    response = client.post(
        '/login/', dict(username=user.username, password=PASSWORD, next='/echos/')
    )
    assertRedirects(response, '/echos/')


@pytest.mark.django_db
def test_logout(client: Client, user):
    client.force_login(user)
    client.get('/logout/')
    # https://stackoverflow.com/a/6013115
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_signup(client: Client, fake, user):
    SIGNUP_DATA = {
        'username': fake.user_name(),
        'password': fake.password(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
    }
    response = client.get('/signup/')
    assert response.status_code == 200
    for field in SIGNUP_DATA.keys():
        assertContains(response, field)

    # wrong signup (no username provided)
    payload = SIGNUP_DATA.copy()
    payload.pop('username')
    response = client.post('/signup/', payload)
    assert response.status_code == 200
    assertContains(response, 'error')
    for field in SIGNUP_DATA.keys():
        assertContains(response, field)

    # wrong signup (no password provided)
    payload = SIGNUP_DATA.copy()
    payload.pop('password')
    response = client.post('/signup/', payload)
    assert response.status_code == 200
    assertContains(response, 'error')
    for field in SIGNUP_DATA.keys():
        assertContains(response, field)

    # wrong signup (user already exists)
    payload = SIGNUP_DATA.copy()
    payload['username'] = user.username
    response = client.post('/signup/', payload)
    assert response.status_code == 200
    assertContains(response, 'error')
    for field in SIGNUP_DATA.keys():
        assertContains(response, field)

    # right signup
    response = client.post('/signup/', SIGNUP_DATA)
    assertRedirects(response, '/echos/')


@pytest.mark.django_db
def test_root_url_redirects_to_echo_list(client: Client, user):
    response = client.get('/', follow=True)
    assertRedirects(response, '/login/?next=/echos/')
    client.force_login(user)
    response = client.get('/')
    assertRedirects(response, '/echos/')


@pytest.mark.django_db
def test_echo_list(client: Client, user, fake):
    TARGET_URL = '/echos/'
    DETAIL_URL = '/echos/{pk}/'

    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')
    client.force_login(user)
    echos = baker.make(
        Echo,
        _quantity=10,
        content=partial(fake.paragraph, nb_sentences=10),
        _fill_optional=True,
    )
    response = client.get(TARGET_URL)
    assert response.status_code == 200
    for echo in echos:
        assertContains(response, truncatewords(echo.content, 20), count=1)
        assertContains(response, echo.user.username)
        assertContains(response, DETAIL_URL.format(pk=echo.pk))


@pytest.mark.django_db
def test_echo_detail(client: Client, echo, user, fake):
    TARGET_URL = f'/echos/{echo.pk}/'

    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')
    client.force_login(user)
    waves = baker.make(
        Wave,
        _quantity=10,
        echo=echo,
        content=partial(fake.paragraph, nb_sentences=10),
        created_at=seq(datetime.datetime.now(), increment_by=datetime.timedelta(days=-1)),
        _fill_optional=True,
    )
    response = client.get(TARGET_URL)
    assert response.status_code == 200
    assertContains(response, echo.content, count=1)
    assertContains(response, echo.user.username)
    for wave in waves[:5]:
        assertContains(response, wave.content, count=1)
        assertContains(response, wave.user.username)


@pytest.mark.django_db
def test_add_echo(client: Client, user):
    TARGET_URL = '/echos/add/'
    ECHO_CONTENT = 'pytest'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test GET request
    client.force_login(user)
    response = client.get(TARGET_URL)
    assert response.status_code == 200
    assertContains(response, 'form')
    assertContains(response, 'content')

    # Test POST request
    payload = dict(content=ECHO_CONTENT)
    response = client.post(TARGET_URL, payload, follow=True)
    assert response.status_code == 200
    echo = Echo.objects.latest('pk')
    assert echo.user == user
    assert echo.content == ECHO_CONTENT
    assert echo.updated_at >= echo.created_at


@pytest.mark.django_db
def test_edit_echo(client: Client, echo, django_user_model):
    TARGET_URL = f'/echos/{echo.pk}/edit/'
    ECHO_CONTENT = 'pytest'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test edit echo with no echo owner
    user = baker.make(django_user_model)
    client.force_login(user)
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 403

    # Test GET request
    client.force_login(echo.user)
    response = client.get(TARGET_URL)
    assertContains(response, echo.content, 1, 200)

    # Test POST request
    payload = dict(content=ECHO_CONTENT)
    response = client.post(TARGET_URL, payload, follow=True)
    assert response.status_code == 200
    edited_echo = Echo.objects.get(pk=echo.pk)
    assert edited_echo.user == echo.user
    assert edited_echo.content == ECHO_CONTENT
    assert edited_echo.updated_at >= echo.created_at


@pytest.mark.django_db
def test_delete_echo(client: Client, echo, django_user_model):
    TARGET_URL = f'/echos/{echo.pk}/delete/'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test delete echo with no echo owner
    user = baker.make(django_user_model)
    client.force_login(user)
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 403
    echo = Echo.objects.get(pk=echo.pk)
    assert echo is not None

    # Test delete echo with echo owner
    client.force_login(echo.user)
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 200
    with pytest.raises(Echo.DoesNotExist):
        Echo.objects.get(pk=echo.pk)


@pytest.mark.django_db
def test_add_wave(client: Client, echo, user):
    TARGET_URL = f'/echos/{echo.pk}/waves/add/'
    WAVE_CONTENT = 'pytest'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test GET request
    client.force_login(user)
    response = client.get(TARGET_URL)
    assert response.status_code == 200
    assertContains(response, 'form')
    assertContains(response, 'content')

    # Test POST request
    payload = dict(content=WAVE_CONTENT)
    response = client.post(TARGET_URL, payload, follow=True)
    assert response.status_code == 200
    wave = Wave.objects.latest('pk')
    assert wave.echo == echo
    assert wave.user == user
    assert wave.content == WAVE_CONTENT
    assert wave.updated_at >= wave.created_at


@pytest.mark.django_db
def test_edit_wave(client: Client, wave, django_user_model):
    TARGET_URL = f'/waves/{wave.pk}/edit/'
    WAVE_CONTENT = 'pytest'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test edit wave with no wave owner
    user = baker.make(django_user_model)
    client.force_login(user)
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 403

    # Test GET request
    client.force_login(wave.user)
    response = client.get(TARGET_URL)
    assertContains(response, wave.content, 1, 200)

    # Test POST request
    payload = dict(content=WAVE_CONTENT)
    response = client.post(TARGET_URL, payload, follow=True)
    assert response.status_code == 200
    edited_wave = Wave.objects.get(pk=wave.pk)
    assert edited_wave.echo == wave.echo
    assert edited_wave.user == wave.user
    assert edited_wave.content == WAVE_CONTENT
    assert edited_wave.updated_at >= edited_wave.created_at


@pytest.mark.django_db
def test_delete_wave(client: Client, wave, django_user_model):
    TARGET_URL = f'/waves/{wave.pk}/delete/'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test delete wave with no wave owner
    user = baker.make(django_user_model)
    client.force_login(user)
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 403
    echo = Wave.objects.get(pk=wave.pk)
    assert echo is not None

    # Test delete echo with echo owner
    client.force_login(wave.user)
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 200
    with pytest.raises(Wave.DoesNotExist):
        Wave.objects.get(pk=wave.pk)


@pytest.mark.django_db
def test_user_list(client: Client, user, django_user_model):
    TARGET_URL = '/users/'
    USER_DETAIL_URL = '/{username}/'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test AUTH request
    users = baker.make(django_user_model, _quantity=10)
    client.force_login(user)
    response = client.get(TARGET_URL)
    assert response.status_code == 200
    for user in users:
        assertContains(response, user)
        assertContains(response, USER_DETAIL_URL.format(username=user.username))


@pytest.mark.django_db
def test_user_detail(client: Client, user, django_user_model):
    another_user = baker.make(django_user_model)
    TARGET_URL = f'/users/{another_user}/'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    # Test AUTH request
    client.force_login(user)
    echos = baker.make(
        Echo,
        user=another_user,
        created_at=seq(datetime.datetime.now(), increment_by=datetime.timedelta(days=-1)),
        _quantity=10,
    )
    response = client.get(TARGET_URL, follow=True)
    assert response.status_code == 200
    assertContains(response, another_user.username)
    assertContains(response, another_user.first_name)
    assertContains(response, another_user.last_name)
    assertContains(response, another_user.email)
    for echo in echos[:5]:
        assertContains(response, echo.content, count=1)

    # Test user detail with ALL echos
    response = client.get(TARGET_URL + 'echos/', follow=True)
    assert response.status_code == 200
    for echo in echos:
        assertContains(response, echo.content, count=1)


@pytest.mark.django_db
def test_my_user_detail(client: Client, user):
    TARGET_URL = '/users/@me/'

    # Test NO AUTH request
    response = client.get(TARGET_URL, follow=True)
    assertRedirects(response, f'/login/?next={TARGET_URL}')

    client.force_login(user)
    response = client.get(TARGET_URL)
    assertRedirects(response, f'/users/{user}/')


@pytest.mark.django_db
def test_models_are_available_on_admin(admin_client: Client):
    ADMIN_URLS = ['/admin/echos/echo/', '/admin/waves/wave/']

    for url in ADMIN_URLS:
        response = admin_client.get(url)
        assert response.status_code == 200
