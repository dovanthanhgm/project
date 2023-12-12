import sys,os
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
settings.configure(DEBUG=1,ROOT_URLCONF=__name__,SECRET_KEY='django', INSTALLED_APPS = ['project'],
	TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':['']}],
	DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': 'db.sqlite3',}},
)

def index(request):
	return render(request, 'index.html')

urlpatterns = [
	path('', index),
]


if __name__ == "__main__": execute_from_command_line(sys.argv)
