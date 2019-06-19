from .models import *
from rest_framework import serializers


class IPAddresses(serializers.ModelSerializer):
    approved = serializers.HiddenField(default=True)

    class Meta:
        model = ProhibitedIP
        fields = ('address', 'approved', )


class IPRequests(serializers.ModelSerializer):
    class Meta:
        model = ProhibitedIP
        fields = ('address', )
