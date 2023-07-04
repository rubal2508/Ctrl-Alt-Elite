from . import web, api


urlpatterns = \
    web.urlpatterns + \
    api.urlpatterns
