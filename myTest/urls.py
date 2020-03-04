"""myTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""



from django.conf.urls import url, include
from django.contrib import admin
import todo.views

info_list = [{'PORT': '2002', 'TYPE': 'AP230', 'VERSION': '6.5r3', 'SERIER': '83752057024'},
            {'PORT': '2003', 'TYPE': 'AP240', 'VERSION': '6.5r4', 'SERIER': '83752057025'},
            {'PORT': '2004', 'TYPE': 'AP250', 'VERSION': '6.5r5', 'SERIER': '83752057027'}]

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^refresh$', todo.views.Query_AP_refresh),
    url(r'.*', todo.views.Query_AP),
]

