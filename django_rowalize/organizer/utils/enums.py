from django.db import models

class EnumField(models.Field):

    def __init__(self, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        if not self.choices:
            raise AttributeError('EnumField requires `choices` attribute.')

    def db_type(self):
        return "enum(%s)" % ','.join("'%s'" % k for (k, _) in self.choices)

GENDER_MALE = 'm'
GENDER_FEMALE = 'f'
GENDER_CHOICES = (
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
)

BOAT_SWEEP = 1
BOAT_SKULL = 2

BOAT_CHOICES = (
    (BOAT_SWEEP, 'Sweep'),
    (BOAT_SKULL, 'Skull'),
)

LOCATION_CLAIRE = 1
LOCATION_CRA = 2

LOCATION_CHOICES = (
    (LOCATION_CLAIRE, 'Claire Boat House'),
    (LOCATION_CRA, 'Cambridge Rowing Assosiation'),
)

SIDE_BOW = 'b'
SIDE_STROKE = 's'
SIDE_UNDECIDED = 'u'
SIDE_BOW_STROKE = 'b_s'
SIDE_STROKE_BOW = 's_b'
SIDE_CHOICES = (
    (SIDE_BOW,"Bowside Only"),
    (SIDE_STROKE, "Strokeside Only"),
    (SIDE_UNDECIDED, "No Preference yet"),
    (SIDE_BOW_STROKE, "Mainly Bowside"),
    (SIDE_STROKE_BOW, "Mainly Strokeside")
)