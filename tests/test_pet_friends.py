from api import PetFriends
from settings import valid_email, valid_password, valid_photo


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200, "Code error!"
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200, "Status error"
    assert len(result['pets']) > 0

def test_add_information_about_new_pet_with_valid_key(name="Jake", animal_type="cat", age='4', pet_photo=valid_photo):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200, "Status error"
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo=valid_photo, filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'],pet_photo)
        assert status == 200
    else:
        raise Exception("There is no my pets")

def test_add_information_about_new_pet_without_photo(name="Kennedy", animal_type="parrot", age=10):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    print(result)
    assert status == 200, "Code error!"
    # assert

def test_update_information_about_pet(name="Kesha", animal_type="parrot", age=20):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200, "Code error!"
        assert result['age'] == '20'
    else:
        raise Exception("There is no my pets")

def test_delete_pet_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key)

    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet_from_database(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
    else:
        raise Exception("There is no my pets")

    assert status == 200, "Code error!"

# Negative test-cases

def test_get_all_pets_with_not_valid_key(filter='my_pets'):
    """Введение кириллицы вместо апиключа"""

    auth_key = 'апиКЛЮЧ'
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200, "Status error"
    assert len(result['pets']) > 0

def test_get_all_pets_with_not_valid_key(filter='my_pets'):
    """Использование усиаревшего API-ключа"""

    auth_key = 'ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729'
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200, "Status error"
    assert len(result['pets']) > 0

def test_add_photo_of_pet_with_empty_path(pet_photo='', filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception("There is no my pets")

def test_add_file_text_instead_of_photo(pet_photo='images/text.txt', filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception("There is no my pets")

def test_delete_pet_from_the_database_with_incorrect_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key)
    my_pets['pets'][0]['id'] = '98383620-8129-4b8d-9377-ad5ae3a16936'

    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet_from_database(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
    else:
        raise Exception("There is no my pets")

    assert status == 200, "Code error!"

def test_delete_pet_from_the_database_with_id_string():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key)
    my_pets['pets'][0]['id'] = 'helloWORLD'

    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet_from_database(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
    else:
        raise Exception("There is no my pets")

    assert status == 200, "Code error!"

def test_add_information_about_new_pet_without_photo_with_str_in_field_age(name="Kennedy", animal_type="parrot", age='Kenedy'):
    """Создание карточки питомца с некорректными данными: добавление строки в поле 'возраст' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='')
    assert status == 200
    assert type(my_pets['pets'][0]['name']) == int,  "Incorrectly filling the 'age' field"

def test_update_information_about_pet_with_invalid_id(name="Kesha", animal_type="parrot", age=20):
    """Обновление информации о питомце с некорректным id(значение превышающее допустимое в несколько раз по количеству символов"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='')
    my_pets['pets'][0]['id'] = '98383620-8129-4b8d-9377-ad5ae3a1693698383620-8129-4b8d-9377-ad5ae3a1693698383620-8129-4b8d-9377-ad5ae3a16936'

    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400, "Icorrect ID"
    else:
        raise Exception("There is no my pets")