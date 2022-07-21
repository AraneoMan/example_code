from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, full_name: str, **kwargs):
        if not (email and password and full_name):
            raise TypeError('Users must have an email address, full name and password.')

        user = self.model(email=self.normalize_email(email), full_name=full_name)
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str):
        if password is None:
            raise TypeError('Superusers must have an email and password.')

        user = self.create_user(email, password, 'Admin')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
