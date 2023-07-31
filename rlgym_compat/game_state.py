import numpy as np
from typing import List, Optional

from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket, PlayerInfo

from .physics_object import PhysicsObject
from .player_data import PlayerData


class GameState:
    def __init__(self, game_info: FieldInfoPacket):
        self.game_type: int = 0 # TODO: perhaps update this according to match settings
        self.blue_score = 0
        self.orange_score = 0
        self.last_touch: Optional[int] = -1
        
        self.players: List[PlayerData] = []
        self._on_ground_ticks = np.zeros(64)
        self._air_time_since_jump = np.zeros(64)

        self.ball: PhysicsObject = PhysicsObject()
        self.inverted_ball: PhysicsObject = PhysicsObject()

        # List of "booleans" (1 or 0)
        self.boost_pads: np.ndarray = np.zeros(game_info.num_boosts, dtype=np.float32)
        self.inverted_boost_pads: np.ndarray = np.zeros_like(self.boost_pads, dtype=np.float32)

    def decode(self, packet: GameTickPacket, ticks_elapsed=1, tick_skip=8):
        self.blue_score = packet.teams[0].score
        self.orange_score = packet.teams[1].score

        for i in range(packet.num_boost):
            self.boost_pads[i] = packet.game_boosts[i].is_active
        self.inverted_boost_pads[:] = self.boost_pads[::-1]

        self.ball.decode_ball_data(packet.game_ball.physics)
        self.inverted_ball.invert(self.ball)

        self.players = []
        latest_touch = packet.game_ball.latest_touch
        for i in range(packet.num_cars):
            player = self._decode_player(packet.game_cars[i], i, ticks_elapsed)
            if latest_touch.time_seconds > 0 and i == latest_touch.player_index and packet.game_info.seconds_elapsed - latest_touch.time_seconds < tick_skip / 120:
                player.ball_touched = True
            
            self.players.append(player)
        
        if latest_touch.time_seconds > 0:
            self.last_touch = latest_touch.player_index
        

    def _decode_player(self, player_info: PlayerInfo, index: int, ticks_elapsed: int) -> PlayerData:
        player_data = PlayerData()

        player_data.car_data.decode_car_data(player_info.physics)
        player_data.inverted_car_data.invert(player_data.car_data)

        if player_info.has_wheel_contact:
            self._on_ground_ticks[index] = 0
            self._air_time_since_jump[index] = 0
        else:
            self._on_ground_ticks[index] += ticks_elapsed
            if player_info.jumped: # Technically this should only start when you stop holding jump
                self._air_time_since_jump[index] += ticks_elapsed

        player_data.car_id = index
        player_data.team_num = player_info.team
        player_data.match_goals = player_info.score_info.goals
        player_data.match_saves = player_info.score_info.saves
        player_data.match_shots = player_info.score_info.shots
        player_data.match_demolishes = player_info.score_info.demolitions
        if player_data.boost_amount < player_info.boost / 100: # This isn't perfect but with decent fps it'll work
            if player_data.boost_pickups == -1:
                player_data.boost_pickups = 1
            else:
                player_data.boost_pickups += 1
        player_data.is_demoed = player_info.is_demolished
        player_data.on_ground = player_info.has_wheel_contact or self._on_ground_ticks[index] <= 6
        player_data.ball_touched = False
        player_data.has_jump = not player_info.jumped
        player_data.has_flip = self._air_time_since_jump[index] < 150 and not player_info.double_jumped
        player_data.boost_amount = player_info.boost / 100

        return player_data