from api import PetFriends
from settings import valid_email, valid_password


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

def test_add_information_about_new_pet_with_valid_key(name="Jake", animal_type="cat", age='4', pet_photo="images/catt.jpeg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200, "Status error"
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo="images/catt.jpeg", filter=''):
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