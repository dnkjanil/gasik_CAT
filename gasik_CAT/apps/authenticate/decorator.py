import sweetify
from django.shortcuts import HttpResponseRedirect, reverse

# Decorator mahasiswa
def mahasiswa_required(function):
    def wrap(request, *args, **kwargs):
        # Pastikan bukan admin
        if (not request.user.is_superuser) and request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            sweetify.error(request, 'Harap masuk terlebih dahulu')
            return HttpResponseRedirect(reverse('user_login'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# Decorator admin
def admin_required(function):
    def wrap(request, *args, **kwargs):
        # Pastikan kalau admin
        if request.user.is_superuser and request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            sweetify.error(request, 'Harap masuk terlebih dahulu')
            return HttpResponseRedirect(reverse('admin_login'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# # Decorator post
# def post_required(function):
#     def wrap(request, *args, **kwargs):
#         if request.method == 'POST':
#             return function(request, *args, **kwargs)
#         else:
#             sweetify.error(request, 'Metode Request Tidak Valid')
#             return HttpResponseRedirect(reverse('user_login'))
#
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
#
#
# # Decorator post
# def get_required(function):
#     def wrap(request, *args, **kwargs):
#         if request.method == 'POST':
#             return function(request, *args, **kwargs)
#         else:
#             sweetify.error(request, 'Metode Request Tidak Valid')
#             return HttpResponseRedirect(reverse('user_login'))
#
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
#
