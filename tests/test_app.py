import pytest

from note_book.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_add_contact_success(client):
    response = client.post('/create_contact', data={
        'name': 'Иван',
        'surname': 'Иванов',
        'phone_number': '+7 (999) 999-99-99',
        'comment': 'Друг с работы'
    })
    data = response.data.decode()
    assert 'Контакт Иван Иванов успешно добавлен.' in data
    assert response.status_code == 200


def test_add_contact_invalid_phone(client):
    response = client.post('/create_contact', data={
        'name': 'М',
        'surname': 'М',
        'phone_number': '99999999999'
    })
    assert response.status_code == 422
    json_data = response.data.decode()
    assert 'Неправильный формат номера телефона' in json_data


def test_add_contact_invalid_format(client):
    response = client.post('/create_contact', data={
        'name': 'Иван',
    })
    assert response.status_code == 400


def test_add_contact_duplicate_data(client):
    response = client.post('/create_contact', data={
        'name': 'Иван',
        'surname': 'Иванов',
        'phone_number': '+7(999)111-11-11',
        'comment': 'Друг с работы'
    })
    data = response.data.decode()
    assert 'Контакт Иван Иванов уже есть в телефонной книге.' in data
    assert response.status_code == 422


def test_view_contact_success(client):
    response = client.post('/find_contact', data={
        'name': 'Иван',
        'surname': 'Иванов',
    })
    data = response.data.decode()
    assert 'Иван' in data and 'Иванов' in data
    assert response.status_code == 200


def test_update_contact_not_found(client):
    response = client.post('/update_contact', data={
        'name': 'И',
        'surname': 'И',
    })
    data = response.data.decode()
    assert 'Контакт И И не найден' in data
    assert response.status_code == 400


def test_update_contact_wrong_format(client):
    response = client.post('update_contact', data={
        'name': 'Иван',
        'surname': 'Иванов',
        'phone_number': '1111111111'
    })
    data = response.data.decode()
    assert 'Неправильный формат номера телефона.' in data
    assert response.status_code == 422


def test_update_contact_success(client):
    response = client.post('/update_contact', data={
        'name': 'Иван',
        'surname': 'Иванов',
        'phone_number': '+7 (222) 222-22-22',
        'comment': 'Друг'
    })
    assert response.status_code == 200
    data = response.data.decode()
    assert 'Контакт Иван Иванов обновлён' in data


def test_view_all_contacts_success(client):
    response = client.get('/contacts')
    data = response.data.decode()
    assert all(word in data for word in ['Иван', 'Иванов', '+7 (222) 222-22-22', 'Друг'])
    assert response.status_code == 200


def test_view_contact_not_found(client):
    response = client.post('/find_contact', data={
        'name': 'Петр',
        'surname': 'Петров',
    })
    data = response.data.decode()
    assert 'Контакт Петр Петров не найден' in data
    assert response.status_code == 400


def test_delete_contact_not_found(client):
    response = client.post('/delete_contact', data={
        'name': 'Петр',
        'surname': 'Петров',
    })
    data = response.data.decode()
    assert 'Контакт Петр Петров не найден' in data
    assert response.status_code == 400


def test_delete_contact_success(client):
    response = client.post('/delete_contact', data={
        'name': 'Иван',
        'surname': 'Иванов',
    })
    data = response.data.decode()
    assert 'Контакт Иван Иванов удалён' in data
    assert response.status_code == 200