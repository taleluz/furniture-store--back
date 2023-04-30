from django.contrib import admin
from .models import Product
# from .models import Gallery
from .models import Category
from .models import Subcategory
from .models import Image

# from .models import Profile

# Register your models here.


admin.site.register(Product)

admin.site.register(Category)

admin.site.register(Subcategory)

admin.site.register(Image)


# admin.site.register(Profile)

# admin.site.register(Gallery)

# admin.site.register(Albums)

# admin.site.register(AlbumsType)

