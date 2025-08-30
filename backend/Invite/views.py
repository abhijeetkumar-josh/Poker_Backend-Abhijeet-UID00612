from rest_framework.views import APIView
from gamecreation.models import pokermember
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class IsInvitedUser(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.member == request.user


class AcceptInvitationView(APIView):

    permission_classes = [IsAuthenticated, IsInvitedUser]

    def post(self, request, pkuid):
        
        poker = get_object_or_404(pokermember, id=pkuid)
        self.check_object_permissions(request, poker)

        if poker.accept:
            return Response(
                {"detail": "Invitation already accepted."},
                status=status.HTTP_200_OK,
            )

        poker.accept = True
        poker.save()

        return Response(
            {
                "detail": "Invitation accepted successfully.",
                "pokerboard_id": poker.poker.pokerid,
                "role": poker.get_role_display(),
                "member": poker.member.email,
            },
            status=status.HTTP_200_OK,
        )

        
