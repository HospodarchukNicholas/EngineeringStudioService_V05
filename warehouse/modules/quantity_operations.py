class QuantityManager:

    @staticmethod
    def write_off(obj, outcome_quantity):
        """
        Perform a write-off operation on the given item_location.

        Args:
            obj (ItemLocation etc.): The Model instance with quantity field.
            outcome_quantity (int): The quantity to be written off.

        Returns:
            bool: True if the write-off operation was successful, False otherwise.
        """

        current_quantity = obj.quantity

        if outcome_quantity <= current_quantity:
            quantity = current_quantity - outcome_quantity
            obj.quantity = quantity
            obj.save()
            return True
        else:
            return False

    @staticmethod
    def add_quantity(item_location_obj, income_quantity):
        pass