import os
import sys

cwd = os.path.split(os.path.abspath(__name__))[0]
ALLDIRS = ['lib/python%s/site-packages' % sys.version[:3]]
import site 

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(os.path.join(cwd, directory))

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(cwd)
sys.path.insert(0, os.path.join(cwd, 'django_eggproxy'))
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

