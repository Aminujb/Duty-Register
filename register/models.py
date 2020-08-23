from django.db import models


SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
        ('Unknown', 'Unknown'),
    )

RELIGION_CHOICES = (
    ('Christianity', 'Christianity'),
    ('Islam', 'Islam'),
    ('Others', 'Others'),
)

BLOOD_GROUP_CHOICES = (
    ('A', 'A'),
    ('AB', 'AB'),
    ('B', 'B'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

GENOTYPE_CHOICES = (
    ('AA', 'AA'),
    ('AS', 'AS'),
    ('SS', 'SS'),
)

SINGLE = 'Single'
MARRIED = 'Married'
WIDOWED = 'Widowed'
DIVORCED = 'Divorced'

MARITAL_STATUS_CHOICES = (
    (SINGLE, SINGLE),
    (MARRIED, MARRIED),
    (WIDOWED, WIDOWED),
    (DIVORCED, DIVORCED),
)

class Country(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = u'Countries'

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1, null=False)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Nigerian State'
        verbose_name_plural = 'Nigerian States'

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(State, related_name='local_govt_areas', on_delete= models.CASCADE, null=True)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['state', 'name']
        verbose_name = 'Nigerian Local Government Area'
        verbose_name_plural = 'Nigerian Local Government Areas'

    def __str__(self):
        return self.name


class Rank(models.Model):
    reports_to = models.ForeignKey('self', null=True, blank=True, related_name='reports', on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_head = models.BooleanField(verbose_name='Unit head', default=False)

    class Meta:
        verbose_name = 'Rank'
        verbose_name_plural = u'Ranks'
        ordering = ('name',)

    fields = ['reports_to', 'name', 'description', 'is_head', ]

    def __str__(self):
        return self.name

class UnitType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Unit type'
        verbose_name_plural = u'Unit types'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Unit(models.Model):
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(
        UnitType, related_name='units', on_delete=models.CASCADE)
    head_count = models.IntegerField(
        verbose_name='Head count', null=True, blank=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ('name', 'type',)

    def __str__(self):
        return self.name


class Employee(models.Model):
    last_name = models.CharField(verbose_name='Surname', max_length=50)
    first_name = models.CharField(verbose_name='First name', max_length=50)
    middle_name = models.CharField(verbose_name='Middle name', max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=SEX_CHOICES, default='Female')
    birth_date = models.DateField(blank=True, null=True, db_index=True)
    photo = models.ImageField(upload_to='register/photos/%Y/%m/', blank=True, null=True)
    rank = models.ForeignKey(Rank, related_name='employees', on_delete=models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Unit, related_name='employees', on_delete=models.SET_NULL, blank=True, null=True,
                             help_text= "The department or division this employee is being assigned to")
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=2, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    genotype = models.CharField(max_length=2, choices=GENOTYPE_CHOICES, blank=True, null=True)
    national_id_number = models.CharField(verbose_name="National ID Number", max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    state_of_residence = models.ForeignKey(State, related_name='employees_residence', null=True, blank=False,
                                           on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, related_name='country_of_residence', null=True, blank=True,
                                on_delete=models.SET_NULL)
    state_of_origin = models.ForeignKey(State, related_name='employees_origin', blank=True, null=True,
                                        on_delete=models.SET_NULL)
    lga = models.ForeignKey(LGA, verbose_name= 'LGA', related_name='employees', blank=True, null=True,
                            on_delete=models.SET_NULL)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    last_pass = models.DateTimeField('Last Pass')

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ('first_name', 'last_name',)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """Returns this employee's full name."""
        names = [self.first_name]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.last_name)
        return u' '.join(names)
