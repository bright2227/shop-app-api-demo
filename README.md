# shop-app-api-demo

架設於AWS購物車的API，附有swagger文檔。

目前功能
  - 註冊
  - 產品搜尋
  - JWT驗證 (djangorestframework-simplejwt)
  - 加入產品到購物車內，並提交訂單
  - 提交訂單後，發送確認電子郵件給客戶 (Celery + Redis + Gmail)
  - 部署 (AWS + Docker + uWSGI + NGINX)

使用工具:
 - Djangorestframework
   - drf_yasg
   - Celery 
   - djangorestframework-simplejwt
   - uwsgi
 - Redis 
 - Docker
 - NGINX
 - AWS
 
