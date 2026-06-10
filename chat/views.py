from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, Room
from .forms import RoomForm
from django.contrib.auth.decorators import login_required

@login_required
def chat(request, room_name:str):
    """Gestisce il crud dei messaggi in una room"""
    room = get_object_or_404(Room, name=room_name)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(room=room, user=request.user, text=text)
        return redirect('chat', room_name=room_name)

    elif request.method == 'DELETE':
        msg_id = request.GET.get('msg_id')
        if msg_id:
            get_object_or_404(Message, id=msg_id, room=room).delete()
        return redirect('chat', room_name=room_name)

    # GET
    messages = Message.objects.filter(room=room).order_by('created_at')

    return render(request, 'chat/chat.html', {
        'room': room,
        'messages': messages,
        'user': request.user,
    })

@login_required
def room_list(request):
    """Mostra tutte le room a cui l'utente può accedere"""
    filter_value = request.GET.get('filter', '')
    room_list = Room.objects.filter(users=request.user)
    
    if filter_value:
        room_list = room_list.filter(name__icontains=filter_value)

    return render(request, 'chat/room_list.html', {
        'room_list': room_list,
        'user': request.user,
        'filter_value': filter_value,
    })
    
@login_required
def room_create(request):
    """Crea una nuova room"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    
    return render(request, 'chat/room_form.html', {
        'form': form, 
        'title': 'Nuova Stanza',
        'submit_action_label': 'Crea Stanza'
    })

@login_required
def room_update(request, room_name:str):
    """Modifica una room esistente"""
    room = get_object_or_404(Room, name=room_name, users=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'chat/room_form.html', {'form': form, 'title': 'Modifica Stanza'})

@login_required
def room_delete(request, room_name:str):
    """Elimina una room"""
    room = get_object_or_404(Room, name=room_name, users=request.user)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    
    return render(request, 'chat/room_confirm_delete.html', {'room': room})
