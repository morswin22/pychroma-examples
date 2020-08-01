from collections import deque
from random import randint

from pychroma import Sketch, parse_key


class Snake(Sketch):
  config_path = 'config.json'

  def setup(self):
    self.frame_rate = 4
    self.constraints = ((3, 12), (1, 4))
    self.pos = [(self.constraints[0][1] - self.constraints[0][0]) // 2 + self.constraints[0][0], (self.constraints[1][1] - self.constraints[1][0]) // 2 + self.constraints[1][0]]
    self.dir = [1, 0]
    self.size = 1
    self.history = deque(maxlen=self.size)
    self.history.append((self.pos[0]-1, self.pos[1]))
    self.spawn_fruit()

  def on_key_press(self, key):
    key = parse_key(key)
    if key == 'up':
      self.dir = [0, -1]
    elif key == 'down':
      self.dir = [0, 1]
    elif key == 'left':
      self.dir = [-1, 0]
    elif key == 'right':
      self.dir = [1, 0]
    elif key == 'esc':
      self.stop()

  def spawn_fruit(self):
    self.fruit = self.history[0]
    while self.is_in_tail(self.fruit) or self.is_in_head(self.fruit):
      self.fruit = [randint(self.constraints[0][0],self.constraints[0][1]), randint(self.constraints[1][0],self.constraints[1][1])]

  def increase_size(self):
    self.spawn_fruit()
    temp = list(self.history)
    self.size += 1
    self.history = deque(maxlen=self.size)
    for pos in temp:
      self.history.append(pos)

  def is_in_head(self, pos):
    return self.pos[0] == pos[0] and self.pos[1] == pos[1]

  def is_in_tail(self, pos):
    for tail_pos in self.history:
      if pos[0] == tail_pos[0] and pos[1] == tail_pos[1]:
        return True
    return False

  def is_out_of_bounds(self):
    return self.pos[0] < self.constraints[0][0] or self.pos[0] > self.constraints[0][1] or self.pos[1] < self.constraints[1][0] or self.pos[1] > self.constraints[1][1]

  def update(self):
    self.history.append(tuple(self.pos))

    self.pos[0] += self.dir[0]
    self.pos[1] += self.dir[1]

    if self.is_out_of_bounds() or self.is_in_tail(self.pos):
      print(f"Game Over: {self.size + 1}")
      self.setup()

    if self.is_in_head(self.fruit):
      self.increase_size()

  def render(self):
    for i in range(self.constraints[1][0], self.constraints[1][1] + 1):
      for j in range(self.constraints[0][0], self.constraints[0][1] + 1):
        self.keyboard.set_grid((j, i), (10, 10, 10))

    for pos in self.history:
      self.keyboard.set_grid(pos, (0, 127, 0))
    self.keyboard.set_grid(self.pos, (0, 255, 0))

    self.keyboard.set_grid(self.fruit, (255, 0, 0))
