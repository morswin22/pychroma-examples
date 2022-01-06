import time
from multiprocessing import Process

from pychroma import Sketch, Controller

class MySketch(Sketch):
  config_path = "config.json"

  def setup(self):
    self.frame_rate = 60
    self.mouse.color_mode('hsv')
    self.hue = 120
    print("Hello from setup")

  def update(self):
    self.hue += 5
    if self.hue > 360:
      self.hue = 0

  def render(self):
    self.mouse.set_static((self.hue, 100, 100))

def sketchThread():
  with Controller(MySketch.config_path) as controller:
    controller.run_sketch(MySketch)

def otherThread():
  Controller.defined = True # Disable autorun of sketch in the other thread
  print("Hello from other thread")
  time.sleep(5)

if __name__ == '__main__':
  Controller.defined = True # Disable autorun of sketch in main thread
  sketch = Process(target=sketchThread)
  other = Process(target=otherThread)

  sketch.start()
  other.start()

  other.join()
  print("Other thread joined")

  sketch.terminate()
  print("Sketch terminated")