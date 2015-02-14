# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
# from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', include("search.urls", namespace="search")),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),

    # Your stuff: custom urls go here
    url(r'^contacts/', include("contacts.urls", namespace="contacts")),
    url(r'^promotions/', include("promotions.urls", namespace="promotions")),
    url(r'^contributions/', include("contributions.urls",
                                    namespace="contributions")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
