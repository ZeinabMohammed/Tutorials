from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialSeries
from tinymce.widgets import TinyMCE
from django.db import models

#to change fields ordering:
class tutorialAdmin(admin.ModelAdmin):
# 	fields= ["tutorial_title",
# 			 "tutorial_published",
# 			 "tutorial_content"]
	prepopulated_fields = {"tutorial_slug": ("tutorial_title",)}
	fieldsets = [
				("Title/date", {"fields": ["tutorial_title", "tutorial_published"]}),
					("content", {"fields": ["tutorial_content"]}),
					("URL", {"fields": ["tutorial_slug"]}),
					("series", {"fields": ["tutorial_series"]})
				]
	formfield_overrides = {
						models.TextField: {'widget':TinyMCE()}
							}
admin.site.register(Tutorial, tutorialAdmin)
admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)