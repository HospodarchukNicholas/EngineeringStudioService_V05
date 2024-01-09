from django.db.models import Sum

class QuantityManager:

    @staticmethod
    def write_off(obj, outcome_quantity):
        """
        Perform a write-off operation on the given obj (model instance).

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
    def add_quantity(obj, income_quantity):
        quantity = obj.quantity + income_quantity
        # income_quantity += obj.quantity
        obj.quantity = quantity
        obj.save()

    def get_total_quantity(obj):
        """
        A function to calculate the total quantity associated with a given object.

        'obj': The model instance for which the total quantity is calculated.

        It uses the Django ORM to query and aggregate the 'quantity' field for related items,
        returning the sum of quantities associated with the specified object.
        """

        # метод get_total_quantity дозволяє отримати кількість всіх Item в одному місці
        return obj.objects.filter(item=obj).aggregate(Sum('quantity'))['quantity__sum']