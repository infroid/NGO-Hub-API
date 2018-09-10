from rest_framework import serializers
from core.models import Ngo, Ngo_Verification, Ngo_Detail

class NgoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Class Ngo
    """
    class Meta:
        model = Ngo
        fields = (
            'name',
            'purpose',
            'description',
            'location_city',
            'location_state',
            'location_country',
            'phone_primary',
            'phone_secondary',
            'email',
            'website'
            )


class Ngo_VerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Class Ngo_Verification
    """
    class Meta:
        model = Ngo_Verification
        fields = (
            'verified_phone_primary',
            'verified_phone_secondary',
            'v_email',
            'v_website'
            )


class Ngo_DetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Class Ngo_Detail
    """
    class Meta:
        model = Ngo_Detail
        fields = (
            'orientation',
            'level',
            'activity',
            'staffing',
            'fund',
            'fund_acceptance_from',
            'legal_status',
            'overhead_cost',
            )
