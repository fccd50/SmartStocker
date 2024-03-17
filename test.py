import threading, queue
import time

class Test():
  def __init__(self, q) -> None:
    self.qu = q

  def printNum(self, num, q):
    for i in num:
      print("Num:",i)
      time.sleep(1)
      q.put(i)
  def addX(self):
    while True:
      _num = self.qu.get()
      _num += 10
      print("Num(add10):",_num)
      time.sleep(3)
      self.qu.task_done()

if __name__ == "__main__":
  q = queue.Queue()
  t = Test(q)
  thread = threading.Thread(target=t.addX, daemon=True)
  # thread = threading.Thread(target=t.addX, args=(q,), daemon=True)
  thread.start()
  num = [1,2,3,4,5,6,7,8,9]
  t.printNum(num, q)
  q.join()


"""

'6t5    0.025 -   0.543I-    48.7IE10       E10       g'
'    0.025 -', '   0.543I- ', '   48.7IE10', '       E10 '

4(+/-)+8(数字)+1(エラー)
16
27
i*11+5:i*11+5+9

11*n+5
"""