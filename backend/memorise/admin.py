from django.contrib import admin
from .models import Work, Section, Unit, UserWorkProgress, UserHistory, UserUnitProgress
from django.utils.html import format_html
from django.urls import reverse

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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.raw_text:
            structured = obj.split_into_sections_and_units()

            Section.objects.filter(work=obj).delete()
            Unit.objects.filter(work=obj).delete()

            for sec_data in structured:
                section = Section.objects.create(
                    work=obj,
                    title=f"Section {sec_data['order']}",
                    order_index=sec_data['order']
                )
                for line in sec_data["lines"]:
                    Unit.objects.create(
                        work=obj,
                        section=section,
                        text=line["text"],
                        order_index=line["order"]
                    )

            obj.raw_text=""
            obj.save()

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



@admin.register(UserWorkProgress)
class UserWorkProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "work", "mastery_score", "last_practiced_at", "view_unit_progress_link")

    def view_unit_progress_link(self, obj):
        url = (
            reverse("admin:memorise_userunitprogress_changelist")
            + f"?user__id__exact={obj.user.id}"
        )
        return format_html('<a href="{}">View Unit Progress</a>', url)
    view_unit_progress_link.short_description = "Unit Progress"

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "work", "mode", "score", "cap", "timestamp")
    list_filter = ("mode", "timestamp")
    search_fields = ("user__username", "work__title")


@admin.register(UserUnitProgress)
class UserUnitProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "unit", "mastery_score", "last_practiced_at", "times_practiced")
    list_filter = ("user", "unit")
    search_fields = ("user__username", "unit__title")