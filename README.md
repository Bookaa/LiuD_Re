# LiuD_Re
LiuD demo: Regular Expression

keywords: LiuD, re, regular expression

dependents:
  - Python 2.x
  - https://github.com/Bookaa/LiuD

intend to replace python re module.

how to run:
  - clone https://github.com/Bookaa/LiuD, and generate file Ast_Re.py by:
        python LiuD/MainGen.py Re.liud py > Ast_Re.py
  - cp LiuD/lib.py .
  - py.test Re2.py
