from app.services.base_service import BaseService
from app.models.user_model import UserModel


class User(BaseService):

    def __init__(self):
        BaseService.__init__(self, UserModel)

    def create_user(self,
                    first_name,
                    last_name,
                    email_address,
                    password):
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            password=password)
        user.save()
        return user
