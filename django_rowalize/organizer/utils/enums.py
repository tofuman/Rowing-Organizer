
GENDER_MALE = 'm'
GENDER_FEMALE = 'f'
GENDER_UNICORN = 'u'
GENDER_OTHER = 'o'
GENDER_CHOICES = (
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
    (GENDER_UNICORN, 'Unicorn'),
    (GENDER_OTHER, 'Other')
)

BOAT_SWEEP = 'w'
BOAT_SKULL = 'k'

BOAT_CHOICES = (
    (BOAT_SWEEP, 'Sweep'),
    (BOAT_SKULL, 'Skull'),
)

LOCATION_CLAIRE = 'c'
LOCATION_CRA = 'r'

LOCATION_CHOICES = (
    (LOCATION_CLAIRE, 'Claire Boat House'),
    (LOCATION_CRA, 'Cambridge Rowing Assosiation'),
)

SIDE_BOW = 'b'
SIDE_STROKE = 's'
SIDE_UNDECIDED = 'u'
SIDE_BOW_STROKE = 'bs'
SIDE_STROKE_BOW = 'sb'
SIDE_CHOICES = (
    (SIDE_BOW,"Bowside Only"),
    (SIDE_BOW_STROKE, "Mainly Bowside"),
    (SIDE_UNDECIDED, "No Preference"),
    (SIDE_STROKE_BOW, "Mainly Strokeside"),
    (SIDE_STROKE, "Strokeside Only")
)