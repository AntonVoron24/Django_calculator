from django.http import HttpResponse
from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def serving(dish_name, num):
    result = {}
    for ingredient, amount in DATA.get(dish_name).items():
        result[ingredient] = amount * num
    return result


def main(request):
    template_name = 'calculator/main.html'
    pages = {
        'Главная страница': reverse('main'),
        'Кулинарная книга': reverse('cook_book'),
        f'Скоро здесь будет список всех блюд. А пока посмотри мемасик :)': 'https://media.tenor.com/SZfxhxkCn1cAAAAC/where-lost.gif'
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def recipe(request, dish_name=None):

    try:
        if not dish_name:
            return HttpResponse(
                'Пока что я знаю не много блюд. Но я учусь.'
                'Ты можешь выбрать следующие блюда: ' +
                str([name for name in DATA.keys()])
            )
        if dish_name in DATA.keys():
            serv_num = request.GET.get('servings', 1)
            context = {
                'recipe': serving(dish_name, int(serv_num)),
                'dish_name': dish_name
            }
            return render(request, 'calculator/index.html', context)
        else:
            return render(request, 'calculator/404.html')
    except ValueError:
        return render(request, 'calculator/404.html')
