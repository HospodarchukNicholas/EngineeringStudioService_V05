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
