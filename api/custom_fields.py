from django.core.exceptions import ValidationError
from django.db import models


class ListField(models.Field):
    SEPARATOR = "||"
    ALLOWED_CHOICES = None

    description = "Allow setting short options"
    __metaclass__ = models.SubfieldBase

    def __init__(self, help_text="Allows entering arrays of strings", *args, **kwargs):
        self.name = "ListField",
        self.through = None
        self.help_text = help_text
        self.blank = True
        self.editable = True
        self.creates_table = False
        self.db_column = None
        self.serialize = False
        self.null = True
        self.creation_counter = models.Field.creation_counter
        models.Field.creation_counter += 1
        # Custom stuff
        if 'choices' in kwargs:
            self.ALLOWED_CHOICES = map(lambda choice: choice[0], kwargs['choices'])
        super(ListField, self).__init__(*args, **kwargs)
        if 'blank' in kwargs:
            self.blank = kwargs['blank']
        if 'null' in kwargs:
            self.null = kwargs['null']

    def db_type(self, connection):
        return 'varchar(200)'

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

    def get_internal_type(self):
        return 'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
