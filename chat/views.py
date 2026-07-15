from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, Room
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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


# API
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_room_list(request):
    # LISTA CHAT ROOMS
    if request.method == 'GET':
        room_list = Room.objects.all()
        return JsonResponse({
            'rooms': [
                {
                    'id': room.id,
                    'name': room.name,
                    'created_at': room.created_at.isoformat(),
                }
                for room in room_list
            ]
        })
        
    # CREA CHAT ROOM
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            if Room.objects.filter(name=name).exists():
                return JsonResponse({'error': 'A room with this name already exists'}, status=400)
            
            room = Room.objects.create(name=name)
            if request.user.is_authenticated:
                room.users.add(request.user)
                
            return JsonResponse({
                'id': room.id,
                'name': room.name,
                'created_at': room.created_at.isoformat(),
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def api_room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # MODIFICA CHAT ROOM
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            if Room.objects.filter(name=name).exclude(id=room.id).exists():
                return JsonResponse({'error': 'A room with this name already exists'}, status=400)
            room.name = name
            room.save()
            return JsonResponse({
                'id': room.id,
                'name': room.name,
                'created_at': room.created_at.isoformat(),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    # ELIMINA CHAT ROOM
    elif request.method == 'DELETE':
        room.delete()
        return JsonResponse({'message': 'Room deleted successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)