#!/usr/bin/env python3

def napply(func, arg, n):
  result = arg
  for i in range(n):
    result = func(result)
  return result

def Vplus(a, b):
  return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def Vminus(a, b):
  return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def Vrotx(a):
  return (a[0], a[2], -a[1])

def Vroty(a):
  return (-a[2], a[1], a[0])

def Vrotz(a):
  return (a[1], -a[0], a[2])

class Figure:
  def __init__(self, points):
    self._points = points[:]
    self._setpoints = set(self._points)

  def generatePositions(self, allowedCells):
    result = []
    minp = min(self._points)
    for cell in allowedCells:
      delta = Vminus(cell, minp)
      newFigure = self.translated(*delta)
      if all([p in allowedCells for p in newFigure._points]):
        result.append(newFigure)
    return result

  def generateRotations(self):
    figures = []
    for i in range(3):
      for j in range(3):
        for k in range(3):
          figures.append(self.rotatedX(i).rotatedY(j).rotatedZ(k))
    uniq = []
    for i in range(len(figures)):
      un = True
      for j in range(i+1, len(figures)):
        if figures[i].equals(figures[j]):
          un = False
          break
      if un:
        uniq.append(figures[i].normalized())
    return uniq

  def generateLocations(self, allowedCells):
    result = []
    for f in self.generateRotations():
      result.extend(f.generatePositions(allowedCells))
    return result

  def rotatedX(self, n):
    return Figure([napply(Vrotx, p, n) for p in self._points])
  
  def rotatedY(self, n):
    return Figure([napply(Vroty, p, n) for p in self._points])
  
  def rotatedZ(self, n):
    return Figure([napply(Vrotz, p, n) for p in self._points])

  def translated(self, dx, dy, dz):
    return Figure([Vplus(p, (dx, dy, dz)) for p in self._points])

  def normalized(self):
    minp = min(self._points)
    return Figure(sorted([Vminus(p, minp) for p in self._points]))

  def equals(self, other):
    if len(self._points) == len(other._points):
      p1 = sorted(self._points)
      p2 = sorted(other._points)
      dlt = Vminus(p2[0], p1[0])
      for i, p in enumerate(p1):
        if Vplus(p, dlt) != p2[i]:
          return False
    return True

def findDispositions(figures, allowedCells):
  if len(figures) == 0:
    return []
  f = figures[0]
  locations = f.generateLocations(allowedCells)
  for loc in locations:
    newCells = allowedCells.copy()
    for p in loc._points:
      newCells.remove(p)
    res = findDispositions(figures[1:], newCells)
    if res != None:
      return [loc] + res
  return None


def main():
  print('Blocked Box solver')

  allowedCells = []
  for i in range(3):
    for j in range(3):
      for k in range(3):
        if not(i == 0 and j == 0 and k == 1):
          allowedCells.append( (i, j, k) )
  allowedCells = set(allowedCells)

  figures = [
    Figure([(0, 0, 0), (0, 0, 1), (0, 0, 2)]), # Line
    Figure([(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1)]), # T-Bar
    Figure([(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1), (1, 1, 1)]), # Extended T-Bar
    Figure([(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)]),
    Figure([(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1), (1, 0, 0)]), # L-Bar with side block
    Figure([(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2), (1, 0, 1)]),
  ]
  variants = 1
  for f in figures:
    locations = f.generateLocations(allowedCells)
    print(len(locations))
    variants *= len(locations)
  print(variants) # Upper estimate. Backtracking is faster : )

  dispositions = findDispositions(figures, allowedCells)
  for d in dispositions:
    print(d._points)

if __name__ == '__main__':
  main()
