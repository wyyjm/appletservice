from django.urls import path

from .views import weather, menu, images, service

urlpatterns = [
    # path('', weather.helloworld)
    # path('', weather.weather)
    # path('weather', weather.weather),
    path('menu', menu.get_menu),
    # path('image', images.image),
    # path('imagetext', images.image_text),
    path('image', images.ImageView.as_view()),
    path('image/list', images.ImageListView.as_view()),
    path('weather', weather.WeatherView.as_view()),
    path('stock', service.StockView.as_view()),
    path('star', service.StarView.as_view())
]
