# Add 'file_handler' to INSTALLED_APPS

INSTALLED_APPS = [
    # ...
    'file_handler',
]

# Add media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

