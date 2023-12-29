import re
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from myapp.models import *
from django.conf import settings
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import user_passes_test

from django.core.mail import send_mail
from django.contrib import messages

# from .forms import GalleryItemForm

# Additional
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator, FileExtensionValidator


# Create your views here.

def index(request):
    about_us=About_us.objects.all()
    photo=GalleryItem.objects.all()
    testimonials = Testimonials.objects.all()
    courses=Courses.objects.all()

    context={
        'about_us':about_us,
        "photo": photo,
        "testimonials": testimonials,
        "courses":courses
        }
    # print(context)
    return render(request,"index.html",context)

def gallery_photos(request):
    gallery_items = GalleryItem.objects.all()
    return render(request, 'gallery.html', {'gallery_items': gallery_items})
   
def courses(request):
    courses=Courses.objects.all()
    context={"courses":courses}
    return render(request,"courses.html",context)


def course_detail(request,uid):
    try:

        courses=Courses.objects.get(uid=uid)
        context={
                "courses":courses
                }
        return render(request,"course-detail.html",context) 

    except:
        return HttpResponse("Page not found")
    
   
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mb.no')
        address = request.POST.get('address')
        message = request.POST.get('message')

        # Validate email using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Please enter a valid email address !!")
            return HttpResponseRedirect(request.path_info)

        # Validate mobile number using regex
        mobile_number_regex = r'^\d{10}$'
        if not re.match(mobile_number_regex, mobile_number):
            messages.error(request, "Please enter a valid 10-digit mobile number !!")
            return HttpResponseRedirect(request.path_info)

        try:
            # Construct email message
            subject = 'New Contact Form Submission'
            email_message = f"Name: {name}\nEmail: {email}\nMobile Number: {mobile_number}\nAddress: {address}\nMessage: {message}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ["dcicourses@gmail.com"]

            send_mail(subject, email_message, email_from, recipient_list)

            messages.success(request, "Thank you for contacting us. We'll get back to you as soon as possible.")
            # return render(request, 'contact-success.html')
            return HttpResponseRedirect(request.path_info)
        
        except Exception as e:
            # Log the exception and provide an error message to the user
            print(f"Error sending email: {e}")
            messages.error(request, "An error occurred while processing your request. Please try again later.")
            return HttpResponseServerError("Internal Server Error")

    else:
        return render(request, 'index.html')


def testimonial(request):
    gallery_items = GalleryItem.objects.all()
    return render(request, 'video.html', {'gallery_items': gallery_items})



def registration_no(request):
    if request.method == 'POST':
        roll_no = request.POST.get('registration_number')
        student = Student_Zone.objects.filter(enroll_no=roll_no)
        print(student)
        context={'student':student,'enroll_no':roll_no}

        if student:
            return render(request, "registration_no.html", context)
        else:
            messages.warning(request, 'Incorrect Enrollment Number')
            return HttpResponseRedirect(request.path_info)
            return HttpResponse("Incorrect ro")


    return render(request, "registration_no.html")



def download_result(request, enroll_no):
    try:
        student_result = get_object_or_404(Student_Zone, enroll_no=enroll_no)
        
        # Assuming your result file is a PDF
        response = HttpResponse(student_result.student_result.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{enroll_no}_result.pdf"'

        return response
    except Exception as e:
        return HttpResponse("Something went wrong")

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)

def new_registration(request):
    if request.method == "POST":
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        address = request.POST.get('address')
        pin = str(request.POST.get('pin'))  # Treat PIN as a string
        sex = request.POST.get('sex')
        religion_category = request.POST.get('religion_category')
        dob = request.POST.get('dob')
        qualification = request.POST.get('qualification')
        marksheet_last_year = request.FILES.get('marksheet_last_year')
        mobile_number = request.POST.get('mobile_number')
        whatsapp_number = request.POST.get('whatsapp_number')
        marital_status = request.POST.get('marital_status')
        signature = request.FILES.get('signature')
        image = request.FILES.get('image')
        thumb_fingerprint = request.FILES.get('thumb_fingerprint')

        try:
            # Validate PIN
            pin_validator = [
                MinLengthValidator(limit_value=6, message='PIN must contain exactly 6 digits.'),
                MaxLengthValidator(limit_value=6, message='PIN must contain exactly 6 digits.'),
                RegexValidator(regex=r'^\d{6}$', message='PIN must be a 6-digit number.')
            ]
            for validator in pin_validator:
                validator(pin)

            # Validate mobile number and WhatsApp number
            mobile_number_validator = RegexValidator(regex=r'^\d{10}$', message='Enter a valid 10-digit mobile number.')
            mobile_number_validator(mobile_number)

            whatsapp_number_validator = RegexValidator(regex=r'^\d{10}$', message='Enter a valid 10-digit WhatsApp number.')
            whatsapp_number_validator(whatsapp_number)

            # Validate image, thumb_fingerprint, and signature file formats
            image_validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='Invalid image format. Accepted formats: jpg, jpeg, png.')
            image_validator(image)

            thumb_fingerprint_validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='Invalid thumb fingerprint format. Accepted formats: jpg, jpeg, png.')
            thumb_fingerprint_validator(thumb_fingerprint)

            signature_validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='Invalid signature format. Accepted formats: jpg, jpeg, png.')
            signature_validator(signature)

            # Validate marksheet_last_year file format
            marksheet_validator = FileExtensionValidator(allowed_extensions=['pdf'], message='Invalid marksheet format. Accepted format: pdf.')
            marksheet_validator(marksheet_last_year)

            # Create a new Student_Zone instance with all the required fields
            student = Student_Zone(
                name=name,
                enroll_no=generate_enroll_no(),
                father_name=father_name,
                mother_name=mother_name,
                address=address,
                pin=pin,
                sex=sex,
                religion_category=religion_category,
                dob=dob,
                qualification=qualification,
                marksheet_last_year=marksheet_last_year,
                mobile_number=mobile_number,
                whatsapp_number=whatsapp_number,
                marital_status=marital_status,
                signature=signature,
                image=image,
                thumb_fingerprint=thumb_fingerprint
            )

            # Save the instance to the database
            student.save()

            messages.success(request, 'Registration successful!')
            return HttpResponseRedirect(request.path_info)
        except ValidationError as e:
            # Handle validation errors
            messages.warning(request, f'Validation error: {e}')
        except Exception as e:
            # Handle other exceptions (e.g., file upload error)
            messages.warning(request, f'Error: {e}')

    return render(request, 'new_regestration.html')

def generate_enroll_no():
    # Retrieve the last student's enroll_no
    last_student = Student_Zone.objects.order_by('-uid').first()
    
    if last_student:
        last_enroll_no = last_student.enroll_no
        prefix = last_enroll_no[:13]  # Assuming the prefix is "UP123Y2022E"
        serial_number = int(last_enroll_no[13:]) + 1
        new_enroll_no = f"{prefix}{serial_number:04d}"
    else:
        # If no students exist yet, start with UP123Y2022E0001
        new_enroll_no = "UP123Y2022E0001"

    return new_enroll_no
