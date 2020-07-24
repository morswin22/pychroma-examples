from pychroma import Sketch

class MySketch(Sketch):
  config_path = 'config.json'

  def setup(self):
    self.frame_rate = 30
    self.hue = 0
    self.keyboard.color_mode('hsv')
    
  def update(self):
    self.hue += 1
    if self.hue == 360:
      self.stop()
    
  def render(self):
    self.keyboard.set_static((self.hue, 100, 100))