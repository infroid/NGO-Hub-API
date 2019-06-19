from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Ngo, Ngo_Verification, Ngo_Detail
from core.serializers import NgoSerializer,Ngo_VerificationSerializer,Ngo_DetailSerializer


class NgoViewSet(viewsets.ModelViewSet):
    """
    Kindly fill all the details in order to register the NGO in NGO-Hub.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Ngo.objects.all()
    serializer_class = NgoSerializer


class Ngo_VerificationViewSet(viewsets.ModelViewSet):
    """
    Update the verification status of the NGO. These steps are to be taken upon manual verification.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Ngo_Verification.objects.all()
    serializer_class = Ngo_VerificationSerializer


class Ngo_DetailViewSet(viewsets.ModelViewSet):
    """
    These are optional details which could be updated by the NGO.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Ngo_Detail.objects.all()
    serializer_class = Ngo_DetailSerializer