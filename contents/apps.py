from django.contrib.admin.apps import AdminConfig

class ContentsAdminConfig(AdminConfig):

    default_site = 'contents.admin.ContentsAdminSite'
