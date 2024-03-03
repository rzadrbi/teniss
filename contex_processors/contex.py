from reservation.models import texts


def get_texts(request):
    return {'text': texts.objects.get(id=1), }
