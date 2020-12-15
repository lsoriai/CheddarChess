# -*- coding: utf-8 -*-
from channels.db import database_sync_to_async
from .exceptions import ClientError
from .models import *

# decorador síncrono para consumidor asíncrono
@database_sync_to_async
def get_room_or_error(room_id, user):
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    if room.staff_only and not user.is_staff:
        raise ClientError("ROOM_ACCESS_DENIED")
    return room
