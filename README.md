# shop-app-api-demo

架設於AWS購物車的API，附有swagger文檔。

目前功能
  - 發信功能 (Celery + Redis + Gmail)
  - 註冊，發送驗證信，點擊信中地址啟動帳號
  - 請求修改密碼功能，請求後發送修改地址信，點擊信中地址來到修改密碼頁面 
  - google社群登入
  - 產品搜尋以及分頁
  - JWT驗證 (djangorestframework-simplejwt)
  - 加入產品到購物車內，並提交訂單
  - 提交訂單後，發送確認電子郵件給客戶
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
 
