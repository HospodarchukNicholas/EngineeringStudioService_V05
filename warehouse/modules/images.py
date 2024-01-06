from django.utils.html import format_html, mark_safe

class ImageWizard:

    @staticmethod
    def image_tag(obj, width=250):
        """
        Generate an HTML image tag for the 'image' field.

        Args:
            obj: The model object with an 'image' field.
            width (int): The desired width for the image (default is 250).

        Returns:
            str: An HTML image tag with the specified width and automatic height.
                 If the object has no image, 'No preview image available' is displayed.
        """
        if obj.image:
            return format_html('<img src="{}" width="{}" height="auto"/>'.format(obj.image.url, width))
        else:
            return 'No preview image available'