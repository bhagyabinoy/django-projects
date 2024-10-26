from django.db import models

# Create your models here.

RELATIONSHIP_CHOICES= (('Father','Father'),('Mother', 'Mother'),('GrandParent', 'Grand Parent'))  
GENDER_CHOICES= (('Male','Male'),('Female', 'Female')) 
#_CHOICES= (('Male','Male'),('Female', 'Female')) 
STANDARD_CHOICES= (('1','I'),('2','II'),('3','III'),('4','IV'),('5','V'),('6','VI'),('7','VII'),('8','VIII'),('9','IX'),('10','X')) 
DIVISION_CHOICES= (('A','A'),('B','B'),('C','C'),('D','D'),('E','E'))
BLOODGROUP_CHOICES= (('Apositive ','A+'),('Anegative', 'A-'),('Bpositive', 'B+'),('Bnegative', 'B-'),('Opositive', 'O+'),('Onegative', 'O-'),('ABpositive', 'AB+'),('ABnegative', 'AB-'),) 
STATE_CHOICES = (
    ('AndhraPradesh','Andhra Pradesh'),
    ('AndamanandNicobarIslands', 'Andaman and Nicobar Islands'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Delhi','Delhi'),
    ('Lakshadweep','Lakshadweep'),
    ('Puducherry','Puducherry'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('HimachalPradesh','Himachal Pradesh'),
    ('JammuandKashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('MadhyaPradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('TamilNadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura '),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),  
)

ACTIVE_CHOICES= (('1','1'),('2', '2')) 

class Student(models.Model):
    student_ID = models.CharField(max_length=40, primary_key=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    guardian_name = models.CharField(max_length=40, null=True, blank=True)
    guardian_relationship = models.CharField(choices=RELATIONSHIP_CHOICES,max_length=40, null=True, blank=True)
    guardian_phone = models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=40, null=True, blank=True)
    address = models.TextField(max_length=40, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    district = models.CharField(max_length=40, null=True, blank=True)
    state = models.CharField(max_length=40, choices=STATE_CHOICES, default='Kerala')
    standard = models.CharField(choices=STANDARD_CHOICES, max_length=10, null=True, blank=True)
    division = models.CharField(choices=DIVISION_CHOICES,max_length=10,null=True, blank=True)
    date_of_birth = models.DateField(max_length=40, null=True, blank=True)
    blood_group = models.CharField(choices=BLOODGROUP_CHOICES,max_length=40,null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    bus_no = models.IntegerField(null=True, blank=True)
    isactive = models.CharField(max_length=10,choices=ACTIVE_CHOICES, default='1')

    def __str__(self):
        return self.first_name


ATTENDANCE_CHOICES= (('Fulldaypresent','P'),('Fulldayabsent', 'A'),('Halfdayleave', 'H'))  

class Attendance(models.Model):
    date = models.DateField(max_length=40, null=True, blank=True)
    markattendance= models.CharField(choices=ATTENDANCE_CHOICES, max_length=40, null=False,default='P')
    student=models.ForeignKey(Student,null=True,blank=True, on_delete=models.CASCADE,related_name='stud_id')
   