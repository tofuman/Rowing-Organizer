
from .constans import BoatClubName

def createDefaultRenderArguments(request, rower=None, crews=None):
    dict = {'boatclub': {'name': BoatClubName}}
    dict['rower'] = rower
    dict['crews'] = crews
    return dict

