class PlayerNotInRoomError(Exception):
    def __init__(self, players ,*args):
        super().__init__(*args)
        self.players = players


class PlayerIsNotLeaderError(Exception):

    def __init__(self, player_name, *args):
        super().__init__(*args)
        self.player_name = player_name
