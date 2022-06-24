from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Main
from .forms import AddMainForm
def about(request):
    return render(request, 'about.html', {})
def delete(request, pk):
    item = Main.objects.get(id=pk)
    print('test')
    if request.method=="GET":
        item.delete()
    return redirect('index')
def update(request):
    qs = Main.objects.all()
    for item in qs:
        item.save()
    return redirect('index')


def index(request):
    discount_count = 0
    error = None
    form = AddMainForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return redirect('index')

        except AttributeError:
            error = "couldn't get the name of the price"
        except:
            error = "something went wrong"
    form = AddMainForm()

    qs = Main.objects.all()
    item_count = qs.count()
    if item_count > 0:
        for item in qs:
            if item.current_price < item.previous_price:
                discount_count += 1
    content = {
        'qs': qs,
        'item_count': item_count,
        'discount_count': discount_count,
        'form': form,
        'error': error,
    }
    return render(request, 'index.html', content)