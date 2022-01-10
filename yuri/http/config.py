def default():
    return {
        'address': '0.0.0.0',
        'port': 80,
        'timeout': 30,
        'require_auth': False,
        'realm': "esp8266",
        'user': "admin",
        'password': "99999990",
        'max_headers': 10,
        'max_content_length': 1024,
        # NB. SSL currently broken
        'use_ssl': False,
        'dev': True
    }