from django.core.exceptions import ValidationError


def validate_image_size(file):
    max_size_kb = 5
    if file.size > max_size_kb * 1024 * 1024:
        raise ValidationError(f"image cannot be larger than {max_size_kb} MB")
