from django.shortcuts import render
from parsing.parser import parsing_one_page, parse_links
# Create your views here.

def parse_view(request):
    if request.method == 'POST':
        p = parse_links()
        return render(request, 'parse.html')
    return render(request, 'parse.html')