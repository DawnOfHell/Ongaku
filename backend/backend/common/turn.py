class Turn:
    def __init__(self, genre: str, songs_limit: int, playback_time: int):
        self.genre = genre
        self.playback_time = playback_time
        self.songs_limit = songs_limit
        self.current_song = None

    def calculate_score(self, message):
        pass

