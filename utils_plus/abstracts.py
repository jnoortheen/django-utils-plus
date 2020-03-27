# Copied from this [gist](https://gist.github.com/freewayz/69d1b8bcb3c225bea57bd70ee1e765f8)
from django.db.models import Model


class CheckDeletableModelMixin:
    def is_deletable(self: Model):  # type: ignore
        # get all the related object
        for rel in self._meta.get_fields():
            try:
                # check if there is a relationship with at least one related object
                if rel.related_model:
                    related = rel.related_model.objects.filter(**{rel.field.name: self})  # type: ignore
                    if related.exists():
                        # if there is return a Tuple of flag = False the related_model object
                        return False, related
            except AttributeError:  # an attribute error for field occurs when checking for AutoField
                pass  # just pass as we dont need to check for AutoField
        return True, None
