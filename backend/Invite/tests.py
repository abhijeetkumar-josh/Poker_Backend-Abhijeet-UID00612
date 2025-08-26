from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from gamecreation.models import pokermember,PokerBoard
from django.contrib.auth import get_user_model

User = get_user_model()



class AcceptInvitationViewTest(APITestCase):
    def setUp(self):
        user=User.objects.create(username='somerandomname',email='testing@examplesome.com',is_active=True)
        user.set_password('someStrng@123')
        user.save()
        poker=PokerBoard.objects.create(game_name='random game summary',game_description='random description')
        self.poker_member = pokermember.objects.create(
            member=user,
            poker=poker,
            accept=False
        )
        self.valid_url = reverse("Invite:invite", args=[self.poker_member.id])
        self.invalid_url = reverse("Invite:invite", args=[9999])

    def test_accept_valid_invitation(self):
        """ Accepts a valid invitation """
        response = self.client.get(self.valid_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Invitation Accepted")

        # Refresh from DB to check if accept was updated
        self.poker_member.refresh_from_db()
        self.assertTrue(self.poker_member.accept)

    def test_accept_invalid_invitation(self):
        """Trying to accept an invalid invitation ID should fail """
        response = self.client.get(self.invalid_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Wrong Invitation")
