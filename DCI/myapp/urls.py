from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
     path('', views.index,name='index'),
     path("gallery_photos",views.gallery_photos,name="gallery_photos"),
     path("courses",views.courses,name="courses"),
     path("course_detail/<uid>",views.course_detail,name="course_detail"),
     path("contact",views.contact,name="contact"),
     path("testimonial",views.testimonial,name='testimonial'),
     path("registration_no",views.registration_no,name="registration_no"),
     path('download_result/<str:enroll_no>/',views.download_result, name='download_result'),
     path('new_registration',views.new_registration,name='new_registration'),

     

]