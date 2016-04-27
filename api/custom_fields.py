from django.core.exceptions import ValidationError
from django.db import models


class ListField(models.TextField):
    SEPARATOR = "||"
    ALLOWED_CHOICES = None

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        if 'choices' in kwargs:
            self.ALLOWED_CHOICES = map(lambda choice: choice[0], kwargs['choices'])

    def to_python(self, value):
        if value in (None, ''):
            return []
        else:
            if isinstance(value, list):
                return value
            else:
                split_values = value.split(self.SEPARATOR)
                if self.ALLOWED_CHOICES is not None:
                    for item in split_values:
                        if item not in self.ALLOWED_CHOICES:
                            raise ValidationError("Item " + item + " is not allowed here!")
                return split_values

    def get_prep_value(self, value):
        if isinstance(value, list):
            for item in value:
                self.validate_text(item)
            return self.SEPARATOR.join(value)
        elif isinstance(value, str):
            self.validate_text(value)
            return value

    def validate_text(self, value):
        if self.SEPARATOR in value:
            raise ValidationError(value + " contains non-allowed text.")

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
