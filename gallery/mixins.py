from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerOrAdminMixin(UserPassesTestMixin):
    """
    Grants access only if the current user is the object owner
    or is a staff member / superuser (album administrator).
    
    Subclasses must define `owner_field` to specify which attribute
    on the model object holds the owner User instance.
    Default is 'created_by' (used by Album).
    """
    owner_field = 'created_by'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        owner = getattr(obj, self.owner_field)
        return user == owner or user.is_staff or user.is_superuser
