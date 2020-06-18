class Square:
    def __init__(self, length, width):
      self.length = length
      self.width = width

    def area(self):
        return self.length * self.width

  
r = Square(2,3)
print("Area is %d" %r.area())