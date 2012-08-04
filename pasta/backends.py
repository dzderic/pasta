from guardian.backends import ObjectPermissionBackend
from guardian.utils import get_anonymous_user

class FallbackObjectPermissionBackend(ObjectPermissionBackend):
    """
    Identical to :class:`guardian.backends.ObjectPermissionBackend`, except it
    falls back to the anonymous user before returning `False`.
    """
    def has_perm(self, user_obj, perm, obj=None):
        parent = super(FallbackObjectPermissionBackend, self).has_perm
        return parent(user_obj, perm, obj) or parent(get_anonymous_user(), perm, obj)
