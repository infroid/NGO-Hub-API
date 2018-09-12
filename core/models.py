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


def validate_isnumeric(value):
    """
    Vaildates if the value is alphabet and space
    """
    if all(x.isnumeric() for x in value):
        raise ValidationError(
            _('%(value)s : cannot contain anything other than number'),
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


def validate_choice(selection, choice):
    """
    Vaildates if selection in choices
    """
    values = [item[0] for item in choice]
    if selection not in values:
        raise ValidationError(
            _('%(selection)s : selection is not in %(values)s'),
            params={'selection': selection, 'values': values},
        )


# Ngo Class
class Ngo(models.Model):
    """
    The class is responsible to hold an Ngo. 
    Class attributes to be taken from Ngo upon first interaction:
    + name
    + purpose
    + description
    + location_city
    + location_state
    + location_country
    + phone_primary
    + phone_secondary
    + email
    + website
    """
    
    # Date and Time of creation of record for this Ngo
    created_at = models.DateTimeField(auto_now_add=True)
    
    # This Ngo record was created by <User>
    # Use User.created_Ngos.all() to see all Ngos they created
    created_by = CurrentUserField(add_only=True, related_name="CreatedNgo",blank=False,null=False,on_delete=models.DO_NOTHING)
    
    # This Ngo record was modified by <User>
    # Use User.modified_Ngos.all() to see all Ngos they modified
    modified_by = CurrentUserField(related_name="ModifiedNgo",blank=False,null=False,on_delete=models.DO_NOTHING)
    
    name = models.TextField(
        help_text='Name of the Ngo | 2,000 characters max | 2 characters min',
        max_length=2000,blank=False,null=False)
        
    purpose = models.TextField(
        help_text='Purpose of the Ngo | 5,000 characters max | 50 characters min',
        max_length=5000,blank=False,null=False)
        
    description = models.TextField(
        help_text='Description of the Ngo | 10,000 characters max | 300 characters min',
        max_length=10000,blank=False,null=False)
        
    location_city = models.CharField(
        help_text='Location of the Ngo | 255 characters max | City',
        max_length=255,blank=False,null=False)
        
    location_state = models.CharField(
        help_text='Location of the Ngo | 255 characters max | State',
        max_length=255,blank=False,null=False)
        
    location_country = models.CharField(
        help_text='Location of the Ngo | 255 characters max | Country',
        max_length=255,blank=False,null=False)

    phone_primary = models.CharField(
        help_text='Phone Number of the Ngo | 50 characters max | Primary Phone Number',
        max_length=50,blank=False,null=False)

    phone_secondary = models.CharField(
        help_text='Phone Number of the Ngo | 50 characters max | Secondary Phone Number',
        max_length=50,blank=False,null=False)

    email = models.EmailField(
        help_text='Email of the Ngo | 254 characters max (RFC 2821)',
        max_length=254,blank=False,null=False)

    website = models.URLField(
        help_text='Website of the Ngo | 200 characters max',
        max_length=200,blank=False,null=False)


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
        validate_isnumeric(self.phone_p)
        validate_isnumeric(self.phone_s)
        # Initiate Ngo Verification
        Ngo_Verification(Ngo=self).save()
        super().save(*args, **kwargs)  # Call the "real" save() method.


# Ngo Verification Class
class Ngo_Verification(models.Model):
    """
    The class is responsible to perform Ngo Verification. 
    Class attributes to be updated upon second interaction:
    + primary phone number verification status
    + secondary phone number verification status
    + email verification status
    + website verification status
    """
    # The Ngo 
    # Use <Ngo>.verification.all() to see the Ngo's verification status
    ngo = models.OneToOneField(Ngo, on_delete=models.CASCADE, related_name="Verification",blank=False,null=False)
    # This Ngo was verified by <User>
    # Use User.verified_Ngos.all() to see all Ngos they verified
    modified_by = CurrentUserField(related_name="VerifiedNgo",blank=False,null=False,on_delete=models.DO_NOTHING)
    # Verification Status of Primary Phone Number
    verified_phone_primary = models.BooleanField(default=False)
    # Verification Status of Secondary Phone Number
    verified_phone_secondary = models.BooleanField(default=False)
    # Verification Status of Email
    v_email = models.BooleanField(default=False)
    # Verification Status of Website
    v_website = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        """
        Overrides save method to check if verification finished.
        """
        if self.verified_phone_primary and self.verified_phone_secondary and self.v_email and self.v_website:
            Ngo_Detail(Ngo=self.Ngo).save()
        super().save(*args, **kwargs)  # Call the "real" save() method.



# Ngo Detail Class
class Ngo_Detail(models.Model):
    """
    The class is responsible to hold details of an Ngo.
    These details could only be changed by the Ngo's manager. 
    Class attributes to be filled by Ngo (to activate donation):
    + orientation
    + level (level of operation / scale)
    + activity
    + staffing
    + fund
    + fund_acceptance_from
    + legal_status
    + overhead_cost
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
        ('STA', 'State Ngo'),
        ('NAT', 'National Ngo'),
        ('INT', 'International Ngo'),
    )

    # Activity choices
    ACTIVITY = (
        ('O', 'Operational'),
        ('C', 'Campaigning'),
        ('OC', 'Both Operational & Campaigning'),
        ('PR', 'Public Relations'),
        ('PM', 'Project Management'),
    )

    # Staffing choices
    STAFFING = (
        ('V', 'Volunteers'),
        ('P', 'Paid Staff'),
        ('VP', 'Both Volunteers & Paid Staff'),
    )

    # FUND choices
    FUND = (
        ('H', 'High (>= US $ 1 Billion)'),
        ('M', 'Medium (>= US $ 1 Million)'),
        ('L', 'Low (< US $ 1 Million)'),
    )

    # FUND_ACCEPTANCE_FROM choices
    FUND_ACCEPTANCE_FROM = (
        ('G', 'Government'),
        ('C', 'Firms / Companies / Organizations'),
        ('I', 'Individual'),
        ('N', 'Other Ngos'),
    )

    # LEGAL_STATUS choices
    LEGAL_STATUS = (
        ('UVA', 'Unincorporated & Voluntary Association'),
        ('TCF', 'Trust, Charities & Foundations'),
        ('CNF', 'Companies not just for profit'),
        ('NPL', 'Entities formed or registered under special Ngo or Non Profit Laws'),
    )

    # The Ngo
    # Use <Ngo>.detail.all() to see the Ngo's detail
    ngo = models.OneToOneField(Ngo, on_delete=models.CASCADE, related_name="detail")
    # Orientation of the Ngo | Choice
    # Choices: charitable, service, participatory, empowering
    orientation = models.CharField(max_length=1,choices=ORIENTATION)
    # Level of the Ngo | Choice
    # Choices: community-based, city-wide, state-Ngo, national-Ngo, international-Ngo
    level = models.CharField(max_length=3,choices=LEVEL)
    # Activity of the Ngo | Choice
    # Operational, Campaigning, Both Operational & Campaigning, Public Relations, Project Management
    activity = models.CharField(max_length=2,choices=ACTIVITY)
    # Staffing of the Ngo | Choice
    # Volunteers, Paid Staff, Both Volunteers & Paid Staff
    staffing = models.CharField(max_length=2,choices=STAFFING)
    # Fund of the Ngo | Choice
    # High (>= US $ 1 Billion), Medium (>= US $ 1 Million), Low (< US $ 1 Million)
    fund = models.CharField(max_length=1,choices=FUND)
    # Fund Acceptance of the Ngo | Choice
    # Government, Firms / Companies / Organizations, Individual, Other Ngos
    fund_acceptance_from = models.CharField(max_length=1,choices=FUND_ACCEPTANCE_FROM)
    # Legal Status of the Ngo | Choice
    # Unincorporated & Voluntary Association
    # Trust, Charities & Foundations
    # Companies not just for profit
    # Entities formed or registered under special Ngo or Non Profit Laws
    legal_status = models.CharField(max_length=3,choices=LEGAL_STATUS)
    # Overhead Cost of the Ngo | Choice
    # % of funding spent on overheads
    overhead_cost = models.PositiveSmallIntegerField()


    def save(self, *args, **kwargs):
        """
        Overrides save method to check if verification finished.
        """
        if self.orientation:
            validate_choice(self.orientation, self.ORIENTATION)
        if self.level:
            validate_choice(self.level, self.LEVEL)
        if self.activity:
            validate_choice(self.activity, self.ACTIVITY)
        if self.staffing:
            validate_choice(self.staffing, self.STAFFING)
        if self.fund:
            validate_choice(self.fund, self.FUND)
        if self.fund_acceptance_from:
            validate_choice(self.fund_acceptance_from, self.FUND_ACCEPTANCE_FROM)
        if self.legal_status:
            validate_choice(self.legal_status, self.LEGAL_STATUS)
        super().save(*args, **kwargs)  # Call the "real" save() method.
    overhead_cost = models.PositiveSmallIntegerField(blank=False,null=False)
