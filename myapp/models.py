from django.db import models
from base.models import BaseModel
import os
from django.core.validators import RegexValidator

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
# from django.contrib.auth.models import User
# from .validators import validate_pdf

# Create your models here.

class About_us(BaseModel):
    content=models.TextField(blank=True,null=True)


class Testimonials(BaseModel):
    message=models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to="testmomorials/image")
    
    def __str__(self):
        return self.message

# DCI Courses

class Courses(BaseModel):
    course_name=models.CharField(max_length=400,blank=True, null=True)
    course_duration=models.CharField(max_length=100,blank=True,null=True)
    course_detail=models.TextField(blank=True,null=True)
    course_fee=models.IntegerField()
    course_image=models.ImageField(upload_to="courses")
    
    def __str__(self):
        return self.course_name


# DCI Gallery

class GalleryItem(BaseModel):
    file = models.FileField(upload_to='gallery_files/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)


# Student Regestartion 

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(_('File must be a PDF.'), code='invalid')


class Student_Zone(BaseModel):
    name = models.CharField(max_length=50, null=True)
    enroll_no = models.CharField(max_length=22, unique=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pin = models.CharField(max_length=6, blank=True, null=True, validators=[RegexValidator(regex=r'^\d{6}$', message='Enter a valid 6-digit PIN.')])
    sex = models.CharField(max_length=10, blank=True, null=True)
    religion_category = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True, null=True)
    marksheet_last_year = models.FileField(upload_to='student/last_year_results/', validators=[validate_pdf], blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(regex=r'^\d{10}$', message='Enter a valid 10-digit mobile number.')])
    whatsapp_number = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(regex=r'^\d{10}$', message='Enter a valid 10-digit WhatsApp number.')])
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    signature = models.FileField(upload_to='student/signatures/', blank=True, null=True)
    image = models.ImageField(upload_to='student/images/', blank=True, null=True)
    thumb_fingerprint = models.ImageField(upload_to='student/thumbprints/', blank=True, null=True)
    student_result = models.FileField(upload_to='student_results/', validators=[validate_pdf],blank=True, null=True)

    def _validate_file_field(self, field, allowed_extensions, error_message):
        file_validator = FileExtensionValidator(allowed_extensions=allowed_extensions, message=error_message)
        file_validator(field.file)

    def clean(self):
        # Validate marksheet_last_year file format
        if self.marksheet_last_year:
            self._validate_file_field(
                self.marksheet_last_year,
                allowed_extensions=['pdf'],
                error_message='Invalid marksheet format. Accepted format: pdf.'
            )

        # Validate student_result file format
        if self.student_result:
            self._validate_file_field(
                self.student_result,
                allowed_extensions=['pdf'],
                error_message='Invalid student result format. Accepted format: pdf.'
            )

        # Validate image file format
        if self.image:
            self._validate_file_field(
                self.image,
                allowed_extensions=['jpg', 'jpeg', 'png'],
                error_message='Invalid image format. Accepted formats: jpg, jpeg, png.'
            )

        # Validate thumb_fingerprint file format
        if self.thumb_fingerprint:
            self._validate_file_field(
                self.thumb_fingerprint,
                allowed_extensions=['jpg', 'jpeg', 'png'],
                error_message='Invalid thumb fingerprint format. Accepted formats: jpg, jpeg, png.'
            )

        # Validate signature file format
        if self.signature:
            self._validate_file_field(
                self.signature,
                allowed_extensions=['jpg', 'jpeg', 'png'],
                error_message='Invalid signature format. Accepted formats: jpg, jpeg, png.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate on save
        super().save(*args, **kwargs)

    def __str__(self):
        return self.enroll_no
