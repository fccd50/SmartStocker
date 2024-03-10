import communicator

if __name__ == '__main__':
  c = communicator.Communicator()
  a = c.getID()
  c.close_communicator()
  print(a)


  """
  b'\xf2%t#0-   0.003I1-   0.532I2-    47.6I9\xf3'

\F2%t#
0\s\s\s\s0.010M
1-\s\s\s0.532\s
2-\s\s\s\s47.7I
;\F3

5(+/-)+8(数字)+1(エラー)
16
27

11*n+5
"""