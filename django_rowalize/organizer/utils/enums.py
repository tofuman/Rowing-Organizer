
GENDER_MALE = 'm'
GENDER_FEMALE = 'f'
GENDER_CHOICES = (
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
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
    (SIDE_STROKE, "Strokeside Only"),
    (SIDE_UNDECIDED, "No Preference yet"),
    (SIDE_BOW_STROKE, "Mainly Bowside"),
    (SIDE_STROKE_BOW, "Mainly Strokeside")
)