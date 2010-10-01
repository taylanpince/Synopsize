from django.contrib import admin

from synopses.models import Synopsis, Point, Fact, Journal


class PointInline(admin.StackedInline):
    model = Point


class FactInline(admin.StackedInline):
    model = Fact


class SynopsisAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ("title", "user", "created", "modified")
    inlines = [PointInline, FactInline]
    search_fields = ["user__email", "title", "journal__name", "points__content", "facts__content"]


class JournalAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


admin.site.register(Synopsis, SynopsisAdmin)
admin.site.register(Journal, JournalAdmin)
