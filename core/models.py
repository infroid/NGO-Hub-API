from django.db import models
from cuser.fields import CurrentUserField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_isalphaspace(value):
    """
    Vaildates if the value is alphabet and space
    """
    if all(x.isalpha() or x.isspace() for x in value):
        raise ValidationError(
            _('%(value)s : cannot contain anything other than alphabet, space'),
            params={'value': value},
        )


def validate_minlength(value, min):
    """
    Vaildates the minimum length of the value
    """
    if len(value)<min:
        raise ValidationError(
            _('%(value)s : length is less than %(constraint)s'),
            params={'value': value, 'constraint': min},
        )

# NGO Class
class NGO(models.Model):
    """
    The class is responsible to hold an NGO. 
    Class attributes to be taken from NGO upon first interaction:
    + name
    + purpose
    + description
    + location_city
    + location_state
    + location_country
    + mobile_p
    + mobile_s
    + email
    + website
    """
    # Date and Time of creation of record for this NGO
    created_at = models.DateTimeField(auto_now_add=True)
    # This NGO record was created by <User>
    # Use User.created_ngos.all() to see all NGOs they created
    created_by = CurrentUserField(add_only=True, related_name="created_ngos")
    # This NGO record was modified by <User>
    # Use User.modified_ngos.all() to see all NGOs they modified
    modified_by = CurrentUserField(related_name="modified_ngos")
    # Name of the NGO | 2,000 characters max | 2 characters min
    name = models.TextField(max_length=2000,blank=False,null=False)
    # Purpose of the NGO | 5,000 characters max | 50 characters min
    purpose = models.TextField(max_length=5000,blank=False,null=False)
    # Description of the NGO | 10,000 characters max | 300 characters min
    description = models.TextField(max_length=10000,blank=False,null=False)
    # Location of the NGO | 255 characters max | City
    location_city = models.CharField(max_length=255)
    # Location of the NGO | 255 characters max | State
    location_state = models.CharField(max_length=255)
    # Location of the NGO | 255 characters max | Country
    location_country = models.CharField(max_length=255)
    # Phone Number of the NGO | 50 characters max | Primary Phone Number
    phone_p = models.CharField(max_length=50)
    # Phone Number of the NGO | 50 characters max | Secondary Phone Number
    phone_s = models.CharField(max_length=50)
    # Email of the NGO | 254 characters max (RFC 2821)
    email = models.EmailField(max_length=254)
    # Website of the NGO | 200 characters max
    website = models.URLField(max_length=200)


    def save(self, *args, **kwargs):
        """
        Overrides save method to perform validations and standardizations.
        """
        validate_minlength(self.name,2)
        validate_minlength(self.purpose,50)
        validate_minlength(self.description,300)
        self.location_city = self.location_city.upper()
        self.location_state = self.location_state.upper()
        self.location_country = self.location_country.upper()
        validate_isalphaspace(self.name)
        validate_isalphaspace(self.location_city)
        validate_isalphaspace(self.location_state)
        validate_isalphaspace(self.location_country)  
        # Initiate NGO Verification
        NGO_Verification(self).save()
        super().save(*args, **kwargs)  # Call the "real" save() method.


# NGO Verification Class
class NGO_Verification(models.Model):
    """
    The class is responsible to perform NGO Verification. 
    Class attributes to be updated upon second interaction:
    + primary phone number verification status
    + secondary phone number verification status
    + email verification status
    """
    # The NGO 
    # Use <NGO>.verification.all() to see the NGO's verification status
    ngo = models.OneToOneField(NGO, on_delete=models.CASCADE, related_name="verification")
    # This NGO was verified by <User>
    # Use User.verified_ngos.all() to see all NGOs they verified
    modified_by = CurrentUserField(related_name="verified_ngos")
    # Verification Status of Primary Phone Number
    v_mobile_p = models.BooleanField(default=False)
    # Verification Status of Secondary Phone Number
    v_mobile_s = models.BooleanField(default=False)
    # Verification Status of Email
    v_email = models.BooleanField(default=False)
    # Verification Status of Website
    v_website = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        """
        Overrides save method to check if verification finished.
        """
        if self.v_mobile_p and self.v_mobile_s and self.v_email and self.v_website:
            NGO_Detail(self.ngo).save()
        super().save(*args, **kwargs)  # Call the "real" save() method.



# NGO Detail Class
class NGO_Detail(models.Model):
    """
    The class is responsible to hold details of an NGO. 
    Class attributes to be filled by NGO (to activate donation):
    + orientation
    + level (level of operation / scale)
    + activity
    + staffing
    + funding
    + funding_acceptance_from
    + overhead_cost
    + legal_status
    """

    # Orientation choices
    ORIENTATION = (
        ('C', 'Charitable'),
        ('S', 'Service'),
        ('P', 'Participatory'),
        ('E', 'Empowering'),
    )

    # Level choices
    LEVEL = (
        ('COM', 'Community based'),
        ('CIT', 'City wide'),
        ('STA', 'State NGO'),
        ('NAT', 'National Ngo'),
        ('INT', 'International Ngo'),
    )

    # The NGO
    # Use <NGO>.detail.all() to see the NGO's detail
    ngo = models.OneToOneField(NGO, on_delete=models.CASCADE, related_name="detail")
    # Orientation of the NGO | Choice
    # Choices: charitable, service, participatory, empowering
    scale = models.CharField(max_length=1,choices=ORIENTATION,blank=False,null=False)
    # Level of the NGO | Choice
    # Choices: community-based, city-wide, state-ngo, national-ngo, international-ngo
    scale = models.CharField(max_length=1,choices=LEVEL,blank=False,null=False)
