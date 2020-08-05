import json
from pychroma import Sketch

class Mapper(Sketch):
  config_path = 'config.json'

  def setup(self):
    self.interval = 1
    self.keys = {}
    self.position = [-1, 0]
    self.color = (0, 255, 0)
    self.current_map = self.controller.device_mapping['keyboard']
    print('This is a keyboard key mapping software')
    self.keyboard_name = input('Enter Your keyboard name: ')
    self.change = not self.keyboard_name in self.current_map['devices']
    if self.change is False:
      print('Only new key map will be generated (no layout)')
    self.next()

  def next(self, dir=1):
    self.position[0] += dir
    if dir == 1:
      if self.position[0] == self.keyboard.size[0]:
        self.position[0] = 0
        self.position[1] += dir
    else:
      if self.position[0] < 0:
        self.position[0] = self.keyboard.size[0] - 1
        self.position[1] += dir
        if self.position[1] < 0:
          self.position[1] = 0
    if self.position[1] == self.keyboard.size[1]:
      print('Generated mapping:')
      print(json.dumps(self.keys))
      if self.change:
        self.current_map['devices'][self.keyboard_name] = len(self.current_map['layouts'])
        self.current_map['layouts'].append(self.keys)
        with open('device_mapping.json', 'w') as file:
          json.dump(self.current_map, file)
          print('Dumped new layout into device_mapping.json')
      self.stop()
    else:
      self.keyboard.clear()
      self.keyboard.set_grid(self.position, self.color)
      self.keyboard.render()

  def previous(self):
    self.next(dir=-1)

  def on_key_press(self, key):
    if 'keyboard_name' in self.__dict__:
      self.keys[key] = (self.position[0], self.position[1])
      print(f"'{key}' set as {self.keys[key]}")
      self.next()

  def on_mouse_scroll(self, delta):
    if 'keyboard_name' in self.__dict__:
      if delta[1] > 0:
        self.next()
      elif delta[1] < 0:
        self.previous()