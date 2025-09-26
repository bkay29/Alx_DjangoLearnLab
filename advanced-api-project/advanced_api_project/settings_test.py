from .settings import *   # import all normal settings

# Use a dedicated test DB name (Postgres example)
DATABASES['default'].update({
    'TEST': {
        'NAME': 'test_advanced_api_db',
    }
})
