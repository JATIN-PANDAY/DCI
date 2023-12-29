from django.contrib import admin
from myapp.models import *

# Register your models here.
admin.site.register(About_us)
# admin.site.register(Gallery_images)
admin.site.register(Testimonials)
admin.site.register(Courses)

class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('file', 'video_link')

admin.site.register(GalleryItem, GalleryItemAdmin)


class StudentZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'enroll_no']

    
admin.site.register(Student_Zone, StudentZoneAdmin)