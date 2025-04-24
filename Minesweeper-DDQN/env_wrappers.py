# env_wrappers.py
import numpy as np

class MineCountWrapper:
    """
    Adds one extra feature to every observation:
        mine_ratio = mine_count / (rows * cols)
    Does not alter the underlying env.
    """
    def __init__(self, env):
        self.env         = env
        self.mine_ratio  = env.mine_count / (env.rowdim * env.coldim)

    # ---------- Gym-style API ----------
    def reset(self):
        state = self.env.reset()
        return self._augment(state)

    def step(self, action):
        next_state, reward, done = self.env.step(action)
        return self._augment(next_state), reward, done

    # -----------------------------------
    def _augment(self, state):
        """
        state is a 2‑D array (rowdim × coldim).
        We add a 3rd dimension of size 1 that carries the same mine_ratio
        value for every cell.  The resulting shape is (rowdim, coldim, 2).
        reshape_state_for_net() flattens this anyway, but np.where still
        sees a 2‑D grid.
        """
        mine_layer = np.full_like(state, fill_value=self.mine_ratio, dtype=np.float32)
        stacked    = np.dstack([state.astype(np.float32), mine_layer])   # (R,C,2)
        return stacked
    # proxy everything else (render, seed, etc.)
    def __getattr__(self, name):
        return getattr(self.env, name)
