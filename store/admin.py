from django.contrib import admin

class StorAdminSite(admin.AdminSite):
    site_header = 'Django Store Admin'
    site_title = 'Django Store'
    index_title = 'Store Management'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        # Add Analytics link at the top of the sidebar
        analytics_item = {
            'name': 'Analytics',
            'app_label': 'analytics',
            'app_url': '/admin/dashboard/',
            'has_module_perms': True,
            'models': [
                {
                    'name': 'Dashboard',
                    'object_name': 'Dashboard',
                    'admin_url': '/admin/dashboard/',
                    'view_only': True,
                    'perms': {'view': True},
                }
            ],
        }
        app_list.insert(0, analytics_item)
        return app_list