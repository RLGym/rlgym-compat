"""
    Object to contain all relevant information about the game state.
"""

import numpy as np
from typing import List, Optional
from rlgym_compat.gamestates import PlayerData, PhysicsObject


class GameState(object):
    BOOST_PADS_LENGTH = 34
    BALL_STATE_LENGTH = 18
    PLAYER_INFO_LENGTH = 38
    PLAYER_CAR_STATE_LENGTH = 13
    PLAYER_TERTIARY_INFO_LENGTH = 10

    def __init__(self, state_floats: List[float] = None):
        self.game_type: int = 0
        self.blue_score: int = -1
        self.orange_score: int = -1
        self.last_touch: Optional[int] = -1

        self.players: List[PlayerData] = []

        self.ball: PhysicsObject = PhysicsObject()
        self.inverted_ball: PhysicsObject = PhysicsObject()

        # List of "booleans" (1 or 0)
        self.boost_pads: np.ndarray = np.zeros(GameState.BOOST_PADS_LENGTH, dtype=np.float32)
        self.inverted_boost_pads: np.ndarray = np.zeros_like(self.boost_pads, dtype=np.float32)

        if state_floats is not None:
            self.decode(state_floats)

    def __str__(self):
        output = "{}GAME STATE OBJECT{}\n" \
                 "Game Type: {}\n" \
                 "Orange Score: {}\n" \
                 "Blue Score: {}\n" \
                 "PLAYERS: {}\n" \
                 "BALL: {}\n" \
                 "INV_BALL: {}\n" \
                 "".format("*" * 8, "*" * 8,
                           self.game_type,
                           self.orange_score,
                           self.blue_score,
                           self.players,
                           self.ball,
                           self.inverted_ball)

        return output

