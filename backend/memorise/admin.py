from django.contrib import admin
from .models import Work, Section, Unit

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1  # how many blank sections to show

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 2  # blank units for quick entry

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    search_fields = ("title", "author")
    inlines = [SectionInline, UnitInline]  # ✅ nested forms

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "work", "order_index")
    list_filter = ("work",)
    search_fields = ("title",)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("text", "work", "section", "order_index")
    list_filter = ("work", "section")
    search_fields = ("text",)