from django.urls import path
from . import views
from store.accounts import authviews
from store.cart import cartviews
from store.wishlist import wishlistview
from store.checkout import checkoutviews
from store.orders import orderviews
from store.comments import comment_views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>/', views.collection_products, name='collection_products'),
    path('collections/<str:cat_name>/<str:prod_name>/<int:pk>', views.product_details, name='prod_details'),

    path('product-list/', views.product_list_ajax),
    path('search-product', views.search_product, name="search-product"),

    path('register/', authviews.register, name='register'),
    path('login/', authviews.loginpage, name='login'),
    path('logout/', authviews.logout_user, name='logout'),

    path("password_reset/", authviews.password_reset_request, name="password_reset"),      

    path('add-to-cart/', cartviews.add_to_cart, name='add_to_cart'),
    path('cart', cartviews.viewcart, name='cart'),
    path('update-cart', cartviews.update_cart, name='update_cart'),
    path('delete-cart-item', cartviews.delete_cart_item, name='delete_cart_item'),

    path('wishlist/', wishlistview.index, name='wishlist'),
    path('add-to-wishlist/', wishlistview.add_to_wishlist, name='add_to_wishlist'),
    path('delete-wishlist-item', wishlistview.delete_wishlist_item, name='delete_wishlist_item'),

    path('checkout', checkoutviews.index, name='checkout'),
    path('place-order', checkoutviews.place_order, name='place_order'),
    path('place-order/<str:ref>', checkoutviews.verify_payment, name='verify-payment'),

    path('my-orders', orderviews.index, name='orders'),
    path('view-order/<str:t_no>', orderviews.view_order, name='view_order'),

    path('add-comment/', comment_views.add_to_comments, name='add-comment'),
    path('delete-comment/', comment_views.delete_comment, name='delete-comment')
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)