# Remove Admin Visibility in Frontend and Related Files

## Tasks
- [ ] Remove admin URL from Donotech/urls.py
- [ ] Remove 'django.contrib.admin' and 'jazzmin' from INSTALLED_APPS in settings.py
- [ ] Remove JAZZMIN_SETTINGS from settings.py
- [ ] Delete Donotechapp/admin.py
- [ ] Update views.py to replace @staff_member_required with role-based access control
