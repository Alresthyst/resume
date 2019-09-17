import airplane_frontend_variables as a_val


def airplane_behavior(mode, pos):

    if mode == '' or None:
        pass

    if mode == 'up':
        pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'down':
        pos[1] += a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'left':
        pos[0] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'right':
        pos[0] += a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'up&right':
        pos[0] += a_val.AIRPLANE_MOVEMENT_MODIFIER
        pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'down&right':
        pos[0] += a_val.AIRPLANE_MOVEMENT_MODIFIER
        pos[1] += a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'up&left':
        pos[0] -= a_val.AIRPLANE_MOVEMENT_MODIFIER
        pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'down&left':
        pos[0] -= a_val.AIRPLANE_MOVEMENT_MODIFIER
        pos[1] += a_val.AIRPLANE_MOVEMENT_MODIFIER

    elif mode == 'normal':
        self.generate_bullet("player", 'normal')

    elif mode == 'multi':
        self.generate_bullet("player", 'multi')

    elif mode == 'bomb':
        self.generate_bullet("player", 'bomb')

    elif mode == 'spread':
        self.generate_bullet("player", mode)

    elif mode == 'charge&up':
        pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER
        self.generate_bullet("player", "charge")


def action_controller(start_time, present_time, time_threshold, previous_action, new_action):
    if present_time - start_time < time_threshold:
        for action in previous_action:
            airplane_behavior(action)
    else:
        return new_action
