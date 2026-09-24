from django.contrib import admin
from .models import Resume, Education, Experience, Project, Skill, Certificate, Language, Hobby, SiteVisitor

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'profession', 'user', 'template', 'created_at']
    list_filter = ['template', 'created_at']
    search_fields = ['full_name', 'profession', 'user__username']

@admin.register(SiteVisitor)
class SiteVisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'page', 'user', 'visited_at']
    list_filter = ['visited_at']

admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Language)
admin.site.register(Hobby)
