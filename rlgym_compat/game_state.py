import numpy as np
from typing import List

from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket, PlayerInfo

from .physics_object import PhysicsObject
from .player_data import PlayerData


class GameState:
    def __init__(self, game_info: FieldInfoPacket):
        self.blue_score = 0
        self.orange_score = 0
        self.players: List[PlayerData] = []

        self.ball: PhysicsObject = PhysicsObject()
        self.inverted_ball: PhysicsObject = PhysicsObject()

        # List of "booleans" (1 or 0)
        self.boost_pads: np.ndarray = np.zeros(game_info.num_boosts, dtype=np.float32)
        self.inverted_boost_pads: np.ndarray = np.zeros_like(self.boost_pads, dtype=np.float32)

    def decode(self, packet: GameTickPacket):
        self.blue_score = packet.teams[0].score
        self.orange_score = packet.teams[1].score

        for i in range(packet.num_boost):
            self.boost_pads[i] = packet.game_boosts[i].is_active
        self.inverted_boost_pads[:] = self.boost_pads[::-1]

        self.ball.decode_ball_data(packet.game_ball.physics)
        self.inverted_ball.invert(self.ball)

        self.players = []
        for i in range(packet.num_cars):
            player = self._decode_player(packet.game_cars[i])
            self.players.append(player)

            if player.ball_touched:
                self.last_touch = player.car_id

    def _decode_player(self, player_info: PlayerInfo) -> PlayerData:
        player_data = PlayerData()

        player_data.car_data.decode_car_data(player_info.physics)
        player_data.inverted_car_data.invert(player_data.car_data)

        player_data.car_id = player_info.spawn_id
        player_data.team_num = player_info.team
        player_data.is_demoed = player_info.is_demolished
        player_data.on_ground = not player_info.jumped and player_info.has_wheel_contact
        player_data.ball_touched = False
        player_data.has_flip = not player_info.double_jumped  # RLGym does consider the timer/unlimited flip, but i'm to lazy to track that in rlbot
        player_data.boost_amount = player_info.boost / 100

        return player_data
