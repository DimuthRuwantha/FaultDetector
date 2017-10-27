# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Room
# from .utils import get_room_or_error, catch_client_error
#
# import json
# from channels import Group
# from channels import Channel
#
# @login_required
# def index(request):
#     """
#     Root page view. This is essentially a single-page app, if you ignore the
#     login and admin parts.
#     """
#     # Get a list of rooms, ordered alphabetically
#     rooms = Room.objects.order_by("title")
#     room = Room.objects.get(title="Room1")
#     user = request.user
#     payload= {'message': 'user logged in', 'command': 'send', 'room': '1'}
#     # Channel("chat.receive").send(payload)
#
#     # room = get_room_or_error(1, user)
#     # room.send_message("message", user)
#     # group = Group('room-1')
#     # message = {'room': str(1), 'message': "Hello", 'username': user.username, 'msg_type': 4}
#     # group.send({"text": json.dumps(message)})
#
#
#     # Render that in the index template
#     return render(request, "notification/index.html", {
#         # "rooms": rooms,
#         "room": room,
#     })
