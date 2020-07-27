from random import randint
from pychroma import Sketch

class HelloWorld(Sketch):
  config_path = 'config.json'

  def setup(self):
    self.interval = 0.35
    self.keyboard.color_mode('hsv')
    self.letters = "helloworld"
    self.index = 0

  def update(self):
    self.index += 1
    if self.index == len(self.letters):
      self.stop()
    
  def render(self):
    self.keyboard.clear()
    self.keyboard.set_mapped(self.letters[self.index-1], (randint(0, 360), 100, 100))