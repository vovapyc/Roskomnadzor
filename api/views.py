from .models import *
from .permissions import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class IPAddressViewSet(ModelViewSet):
    queryset = ProhibitedIP.objects.filter(approved=True)
    permission_classes = (IsAdminUserOrReadOnly, )
    serializer_class = IPAddresses


class IPRequestsViewSet(ModelViewSet):
    queryset = ProhibitedIP.objects.filter(approved=False)
    permission_classes = (IsAdminUserOrCreateOnly, )
    serializer_class = IPRequests

    @action(methods=['post'], detail=True)
    def approve(self, request, *args, **kwargs):
        self.get_object().approve()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['post'], detail=True)
    def refuse(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_202_ACCEPTED)
