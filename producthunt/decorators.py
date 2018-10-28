import time
from django.shortcuts import get_object_or_404
from products.models import Product
from django.http import Http404

# Show script execution time
def timeit(method):
   def timed(*args, **kwargs):
       ts = time.time()
       result = method(*args, **kwargs)
       te = time.time()
       print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kwargs, te - ts))
       return result

   return timed

# Check that particular product belongs to authenticated user, else raise 404 page
def user_is_product_hunter(method):
    def wrapper(*args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs.get('pk'))
        if obj.hunter == args[0].user:
            return method(*args, **kwargs)
        else:
            raise Http404
    return wrapper
