from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from pyppp.django.models import UserPPP

#@login_required
def card(request, card=None):
    ppp = UserPPP.objects.get_or_create(user=request.user)[0]
    if card == None:
        card = ppp.get_current_sequence_info()['card']
    else:
        card = int(card)
    
    chunk = lambda l, s, c: [l[i * c : (i + 1) * c] for i in range(s)]
    
    card_list = []
    for i in range(3):
        card_list.append(chunk(ppp.retrieve_card(card+i), ppp.lines_per_card, ppp.row_per_card))
    
    return render_to_response('pyppp/card.html', {
        'name': request.get_host(),
        'card_list': card_list,
        'columns_on_card': ppp.columns_on_card,
        'lines_per_card': range(ppp.lines_per_card + 1)[1:]
    })
card = login_required(card)