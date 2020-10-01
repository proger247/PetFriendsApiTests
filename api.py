import json

from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests


class PetFriends:

    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:
        """This method allows to get API key which should be used for other API methods."""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result


    def get_list_of_pets(self, auth_key: json, filter: str) -> json:

        """This method allows to get the list of pets."""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_information_about_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """This method allows to add information about new pet."""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_information_about_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """This method allows to add information about new pet without photo."""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + f'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_photo_of_pet(self,auth_key: json, pet_id: str, pet_photo: str) -> json:
        """This method allows to add photo of a pet."""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def update_information_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """This method allows to update information about pet."""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str) -> json:
        """This method allows to delete information about pet from database."""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text

        return status, result
