from django.apps import apps

def get_app_name(model_instance):
    """
    Get the app name for a given model instance.

    Args:
        model_instance: An instance of a Django model.

    Returns:
        str: The app name for the model instance.
    """
    app_config = apps.get_containing_app_config(type(model_instance))
    return app_config.name if app_config else None


class ModelMethods:
    @staticmethod
    def is_update(obj):
        """
        Determines whether the given object is being updated.

        Checks if the object has a primary key (`pk`). If it does, the object is considered to be
        in update mode, as it already exists in the database.

        Args:
            obj: The object for which to check the update status.

        Returns:
            bool: True if the object is being updated, False otherwise.
        """
        update = False
        if obj.pk:
            update = True
        return update

