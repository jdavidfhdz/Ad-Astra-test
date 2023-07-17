from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from zones.models import Zone, Distribution



@api_view(['POST'])
def edit(request):
    zone_id = request.data.get('id')
    name = request.data.get('name')
    distributions = request.data.get('distributions')

    if len(name) == 0:
        return Response('The zone name cannot be empty', status=status.HTTP_400_BAD_REQUEST)
    
    zone = Zone.objects.filter(pk=zone_id).first()
    
    if not zone:
        return Response('', status=status.HTTP_400_BAD_REQUEST)

    # Check if zone name is unique (case-insensitive)
    if Zone.objects.filter(name__iexact = name).exclude(pk=zone_id).exists():
        return Response('The zone name cannot be repeated', status=status.HTTP_400_BAD_REQUEST)
    
    zone.name = name
    zone.save()
    
    # Remove all distributions from a specific zone
    Distribution.objects.filter(zone=zone).delete()
    
    # Add all distributions given from the zone
    for distribution in distributions:
        Distribution.objects.create(zone=zone, percentage=distribution['percentage'])
        
    return Response()
