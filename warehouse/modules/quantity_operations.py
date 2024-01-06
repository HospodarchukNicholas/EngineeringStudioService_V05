class QuantityManager:

    @staticmethod
    def write_off(item_location_obj, write_off_quantity):
        """
        Perform a write-off operation on the given item_location.

        Args:
            item_location_obj (ItemLocation etc.): The ItemLocation instance.
            write_off_quantity (int): The quantity to be written off.

        Returns:
            bool: True if the write-off operation was successful, False otherwise.
        """

        current_quantity = item_location_obj.quantity

        if write_off_quantity <= current_quantity:
            quantity = current_quantity - write_off_quantity
            item_location_obj.quantity = quantity
            item_location_obj.save()
            return True
        else:
            return False