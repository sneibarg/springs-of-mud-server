cardinal_direction = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
    'u': 'up',
    'd': 'down'
}


def move_mobile(area_service, mobile, direction):
    if area_service is None:
        return None
    next_room = None
    room = area_service.get_room(mobile.room_id)

    if direction in cardinal_direction:
        if cardinal_direction[direction] == 'north':
            next_room = area_service.get_room(room.north)
            mobile.logger.info("Direction=" + direction + ", room=" + str(next_room))
        elif cardinal_direction[direction] == 'south':
            next_room = area_service.get_room(room.south)
            mobile.logger.info("Direction=" + direction + ", room=" + str(next_room))
        elif cardinal_direction[direction] == 'east':
            next_room = area_service.get_room(room.east)
            mobile.logger.info("Direction=" + direction + ", room=" + str(next_room))
        elif cardinal_direction[direction] == 'west':
            next_room = area_service.get_room(room.west)
            mobile.logger.info("Direction=" + direction + ", room=" + str(next_room))
        elif cardinal_direction[direction] == 'up':
            next_room = area_service.get_room(room.up)
            mobile.logger.info("Direction=" + direction + ", room=" + str(next_room))
        elif cardinal_direction[direction] == 'down':
            next_room = area_service.get_room(room.down)
            mobile.logger.info("Direction=" + direction + ", room=" + str(next_room))
    return next_room
