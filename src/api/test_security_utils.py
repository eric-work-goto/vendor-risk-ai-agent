print('Test script started')
try:
    import web_app
    print('Imported web_app')
except Exception as import_exc:
    print('Import Exception:', import_exc)
    import sys; sys.exit(1)

try:
    print('SQLi:', web_app.detect_sql_injection("'; DROP TABLE assessments; --"))
except Exception as e:
    print('SQLi Exception:', e)

try:
    print('Sanitize:', web_app.sanitize_input('test.com'))
except Exception as e:
    print('Sanitize Exception:', e)
