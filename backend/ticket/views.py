from rest_framework.views import APIView
from rest_framework import status
from ticket.serializers import TicketFilterSerializer
from ticket.models  import estimate
from ticket.serializers import EstimateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
    

class FilterTicketView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
         
        filter_serializer = TicketFilterSerializer(data=request.data)
        filter_serializer.is_valid(raise_exception=True)

        ticket_type = filter_serializer.validated_data.get('filterType')
        estimate_date = filter_serializer.validated_data.get('estimateDate')
        
        queryset = estimate.objects.select_related('ticket').filter(
            user_id=request.user.id
        )

        if ticket_type:
            queryset = queryset.filter(ticket__type=ticket_type)
        if estimate_date:
            queryset = queryset.filter(estimate_date=estimate_date)

        tickets = EstimateSerializer(queryset, many=True)
        return Response(tickets.data, status=status.HTTP_200_OK)
