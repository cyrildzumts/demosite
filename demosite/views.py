from django.shortcuts import render


def not_found_404(request):
    template_name = '404.html'
    return render(request, template_name)


def server_error_500(request):
    template_name = '500.html'
    return render(request, template_name)
