"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from product.views import ProductViewSet
from user.views import UserViewSet, RegisterView, VerifyEmailView, \
    RequestPasswordResetView, SetNewPasswordView, AuthFacebook, AuthGoogle, AuthGoogle2 
from order.views import OrderItemViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf.urls.static import static
# from django.views.static import serve


router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
router.register('orderitem', OrderItemViewSet, basename='orderitem')


TokenObtainPairView_swagger = swagger_auto_schema(method='post',    
    operation_summary='取得JWT Token和Refrech Token，可用於所有需要permission的api',
    operation_description='', security=[],)(TokenObtainPairView.as_view())
TokenRefreshView_swagger = swagger_auto_schema(method='post',
    operation_summary='更新JWT Token', security=[],)(TokenRefreshView.as_view())



urlpatterns = [
    path('admin/', admin.site.urls),
    # product, order, orderitem
    path('api/', include((router.urls, "shop_app"), namespace="shop")),
    # user
    path('api/user/session/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('api/user/register', RegisterView.as_view(), name='register'),
    path('api/user/verification/', VerifyEmailView.as_view(), name="email-verify"),
    path('api/user/passreset/request', RequestPasswordResetView.as_view(), name='passreset-request'),
    path('api/user/passreset/setpass/<token>',  SetNewPasswordView.as_view(), name='passreset-setpass'),
    # path('api/user/social-auth/facebook', AuthFacebook.as_view(), name='social-facebook'),    
    path('api/user/social-auth/google-oauth2', AuthGoogle.as_view(), name='social-google'),    
    path('api/user/social-auth/google-oauth2-front', AuthGoogle2.as_view(), name='social-google2'),  
    # token    
    path('api/token/', TokenObtainPairView_swagger, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView_swagger, name='token_refresh'),
]

# state is for cross site forge, will be returned back to the site with exact value
google_social_login_url = f'https://accounts.google.com/o/oauth2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}' \
    f'&redirect_uri={settings.SITE_URL}api/user/social-auth/google-oauth2' \
    '&state=lOpag66jEav7UINupALP5VBwhx1avuEe' \
    '&response_type=code&scope=openid+email+profile'

facebook_social_login_url = f'https://www.facebook.com/v2.10/dialog/oauth?client_id={settings.SOCIAL_AUTH_FACEBOOK_KEY}' \
    f'&redirect_uri={settings.SITE_URL}api/user/social-auth/facebook' \
    f'&state=EBpm2XAhCLxP6psD0KJQ2wYrBasdsfs7' \
    '&scope=email&response_type=code&return_scopes=true/'

# swagger
schema_view = get_schema_view(
   openapi.Info(
      title='Shop API',
      default_version='v1',
      description=f'Oauth2.0 social login \n Google \n {google_social_login_url}', 
        # Facebook \n {facebook_social_login_url}',
      contact=openapi.Contact(email='bright2227@gmail.com'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    # re_path(
    #    r'^swagger(?P<format>\.json|\.yaml)$',
    #    schema_view.without_ui(cache_timeout=0),
    #    name='schema-json'
    # ),
    # re_path(
    #     r'^redoc/$',
    #     schema_view.with_ui('redoc', cache_timeout=0),
    #     name='schema-redoc'
    # ),
    path(
        'swagger',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]

# # Debug tool
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     import debug_toolbar
#     urlpatterns = urlpatterns + [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
#     SHOW_TOOLBAR_CALLBACK = True
