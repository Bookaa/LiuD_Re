# Re2.py

from Ast_Re import *


class HowRe_liud:
    def __init__(self, s):
        #self.compiled = re.compile(s, re.VERBOSE)
        self.compiled = Test_Parse_Re(s)
    def howmatch(self, textsrc, pos):
        visit = RegularExpression()
        visit.input(textsrc, pos)
        self.compiled.walkabout(visit)
        return visit.matchtoken()

#import Ast_Re
#Ast_Re.HowRe = HowRe_liud

def Test_Parse_Re(srctxt):
    parser = Parser(srctxt)
    mod = parser.handle_Module()
    if mod is None:
        lastpos, lastlineno, lastcolumn, lastline = parser.GetLast()
        print 'parse error, last pos = %d' % lastpos
        print 'last lineno = %d, column = %d' % (lastlineno, lastcolumn)
        print 'last line :', lastline
    else:
        pass
        #print 'parse success'
    return mod

def match_compiled(lexre, lexdata, lexpos):
    m = lexre.match(lexdata, lexpos)
    if m:
        return (m.group(), m.end())
    return None

class REFLAGS(object):
    I = IGNORECASE = 2
    L = LOCALE = 4
    U = UNICODE = 32
    M = MULTILINE = 8
    S = DOTALL = 16
    X = VERBOSE = 64

class Re_sample_visitor_03(Re_sample_visitor_01):
    def visit_Module(self, node):
        assert False
        node.v.walkabout(self)
    def visit_stmt(self, node):
        assert False
        for v in node.vlst:
            v.walkabout(self)
    def visit_items(self, node):
        assert False
        for v in node.vlst:
            v.walkabout(self)
    def visit_NodeProceed(self, node):
        assert False
        node.v.walkabout(self)
    def visit_IfProceed(self, node):
        assert False
        node.v.walkabout(self)
    def visit_IfNext(self, node):
        assert False
        node.v.walkabout(self)
    def visit_IfNotNext(self, node):
        assert False
        node.v.walkabout(self)
    def visit_YesOrNo(self, node):
        assert False
        if node.v1q is not None:
            node.v1q.walkabout(self)
        if node.v2q is not None:
            node.v2q.walkabout(self)
    def visit_RefName(self, node):
        assert False
        pass
    def visit_SetFlags(self, node):
        assert False
        pass
    def visit_ZeroOrMoreNoGreedy(self, node):
        assert False
        node.v.walkabout(self)
    def visit_ZeroOrMore(self, node):
        assert False
        node.v.walkabout(self)
    def visit_OneOrMore(self, node):
        assert False
        node.v.walkabout(self)
    def visit_ZeroOrOne(self, node):
        assert False
        node.v.walkabout(self)
    def visit_NumCtlNoGreedy(self, node):
        assert False
        node.v1.walkabout(self)
        node.v2.walkabout(self)
    def visit_WithNumCtl(self, node):
        assert False
        node.v1.walkabout(self)
        node.v2.walkabout(self)
    def visit_OneChar(self, node):
        assert False
        pass
    def visit_Escape(self, node):
        assert False
        pass
    def visit_NonGroup(self, node):
        assert False
        node.v.walkabout(self)
    def visit_NamedGroup(self, node):
        assert False
        if node.vq is not None:
            node.vq.walkabout(self)
    def visit_Group(self, node):
        assert False
        node.v.walkabout(self)
    def visit_Set(self, node):
        assert False
        for v in node.vlst:
            v.walkabout(self)
    def visit_SetCompl(self, node):
        assert False
        for v in node.vlst:
            v.walkabout(self)
    def visit_AtoB(self, node):
        assert False
        pass
    def visit_CharItem(self, node):
        assert False
        pass
    def visit_Num11(self, node):
        assert False
        pass
    def visit_Num10(self, node):
        assert False
        pass
    def visit_Num01(self, node):
        assert False
        pass
    def visit_Num(self, node):
        assert False
        pass
    def visit_Escape(self, node):
        assert False
        pass

class RegularExpression(Re_sample_visitor_03):
    def input(self, s, pos, flags=0):
        self.sourcestr = s
        self.pos0 = self.pos = pos
        self.endpos = len(s)
        self.groupvalues = []
        self.namedvalues = {}
        self.walkback = []
        self.flags = flags
        self.fakecoloffset = 0

    def matchtoken(self):
        if self.pos == self.pos0:
            return None
        token = self.sourcestr[self.pos0:self.pos]
        return (token, self.pos)

    def visit_Module(self, node):
        node.v.walkabout(self)

    def visit_items(self, node):
        return self.sequence(node.vlst)

    def sequence(self, lst):
        savpos = self.pos
        if savpos == 61:
            pass
        savwb = len(self.walkback)
        sav = self.fakecoloffset

        n=0
        while True:
            n += 1
            for v in lst:
                if self.flags & REFLAGS.X:
                    if isinstance(v, ast_lex.Name0):
                        if v.nm in ' \t':
                            continue
                if not v.walkabout(self):
                    self.pos = savpos
                    break
            else:
                return True
            if savwb >= len(self.walkback):
                return False
            self.fakecoloffset = sav
            continue

    def visit_Set(self, node):
        savpos = self.pos
        for v in node.vlst:
            if v.walkabout(self):
                return True
            assert self.pos == savpos
        return False
    def visit_AtoB(self, node):
        if self.pos >= self.endpos:
            return False
        c1 = node.s1
        c2 = node.s2

        #print 'c1 c2', c1, c2
        assert len(c1) == len(c2) == 1
        c = self.sourcestr[self.pos]
        if ord(c1) <= ord(c) <= ord(c2):
            self.pos += 1
            return True
        return False

    def visit_OneOrMore(self, node):
        return self.NumberControl(node, 1, -1)

    def visit_ZeroOrMore(self, node):
        return self.NumberControl(node, 0, -1)

    def NumberControl(self, node, n1, n2):
        col_offset = self.fakecoloffset; self.fakecoloffset += 1
        if n1 == -1:
            n1 = 0
        if n2 != -1:
            assert n2 >= n1
        #print 'xxx', self.pos
        # use node.v, node.col_offset
        #print 'node.col_offset', node.col_offset
        flg_new = False
        if len(self.walkback) == 0 or self.walkback[-1][0] < col_offset:
            flg_new = True
        else:
            col, lst = self.walkback[-1]
            if col == node.col_offset:
                if self.pos > lst[0]:
                    flg_new = True
        if flg_new:
            lst = []

            savlen = len(self.walkback)
            n = 0
            while True:
                lst.append(self.pos)
                if n == n2:
                    break
                if not node.v.walkabout(self):
                    self.pos = lst[-1]
                    break
                n += 1
            assert n+1 == len(lst)
            if n < n1:
                self.pos = lst[0]
                return False
            #print 'add col', node.col_offset
            while len(self.walkback) > savlen:
                self.walkback.pop()
            self.walkback.append((col_offset, lst))
            return True
        col, lst = self.walkback[-1]
        if col == col_offset:
            #print 'lst', lst
            if self.pos != lst[0]:
                print self.pos, lst[0]
                print 'col', col

            assert self.pos == lst[0]
            n = len(lst)-1
            if n == n1:
                self.walkback.pop()
                return False
            lst.pop()
            self.pos = lst[-1]
            return True

        for col,lst in self.walkback:
            if col == col_offset:
                break
        else:
            assert False
        #print 'lst', lst

        assert self.pos == lst[0]
        self.pos = lst[-1]
        return True
    def NumberControlNoGreedy(self, node, n1, n2):
        col_offset = self.fakecoloffset; self.fakecoloffset += 1
        if n1 == -1:
            n1 = 0
        if n2 != -1:
            assert n2 >= n1
        #from dbgp.client import brk,brkOnExcept; brk(port=9000)
        #brk()
        flg_new = False
        if len(self.walkback) == 0 or self.walkback[-1][0] < col_offset:
            flg_new = True
        else:
            col, lst = self.walkback[-1]
            if col == col_offset:
                if self.pos > lst[0]:
                    flg_new = True

        if flg_new:
            lst = []
            n = 0
            while True:
                lst.append(self.pos)
                if n == n1:
                    break
                if not node.v.walkabout(self):
                    self.pos = lst[0]
                    return False
                n += 1
            assert n == n1 == len(lst)-1

            self.walkback.append((col_offset, lst))
            return True
        col, lst = self.walkback[-1]
        if col == col_offset:
            assert self.pos == lst[0]
            self.pos = lst[-1]
            n = len(lst)-1
            if (n2 == -1 or n < n2) and node.v.walkabout(self):
                lst.append(self.pos)    # this will update self.walkback
                return True
            self.walkback.pop()
            return False
        for col,lst in self.walkback:
            if col == col_offset:
                break
        else:
            assert False
        assert self.pos == lst[0]
        self.pos = lst[-1]
        return True
    def visit_OneChar(self, node):
        if self.pos >= len(self.sourcestr):
            return False
        c = self.sourcestr[self.pos]
        if c == node.c:
            self.pos += 1
            return True
        return False
    def visit_CharItem(self, node):
        if self.pos >= len(self.sourcestr):
            return False
        c = self.sourcestr[self.pos]
        if c == node.c:
            self.pos += 1
            return True
        return False
    def visit_Escape(self, node):
        #from dbgp.client import brk,brkOnExcept; brk(port=9000)
        #brk()

        c1 = node.c
        if c1 == 'A':
            return self.pos == 0
        if c1 == 'Z':
            return self.pos == self.endpos
        if c1 == 'b':
            return self.IsWordBegin() or self.IsWordEnd()
        if c1 == 'B':
            if 0 == self.pos == self.endpos:
                return True
            if self.pos > 0:
                c4 = self.sourcestr[self.pos-1]
                flg_left = IsWordChar(c4)
            if self.pos < self.endpos:
                c5 = self.sourcestr[self.pos]
                flg_right = IsWordChar(c5)

            if self.pos == 0:
                return not flg_right
            if self.pos == self.endpos:
                return not flg_left

            if flg_left and flg_right:
                return True
            return False

        if self.pos >= self.endpos:
            return False
        if '1' <= c1 <= '9':
            valuepos=ord(c1)-ord('1')
            _,value = self.groupvalues[valuepos]
            if True:
                if value is None:
                    return False
                assert isinstance(value, str)
                if self.sourcestr.startswith(value, self.pos):
                    self.pos += len(value)
                    return True
            return False

        c = self.sourcestr[self.pos]
        if self.Escape_inno(node, c):
            self.pos += 1
            return True
        return False
    def Escape_inno(self, node, c):
        c1 = node.c
        assert len(c1) == 1
        if c1 in r'''."'\.*^$[]()#?:+|{}''':
            pass
        elif c1 in 'bB':
            assert False # \b means word start or word end
        elif c1 == 'd':       # \d is 0-9
            return '0' <= c <= '9'
        elif c1 == 'D':
            if '0' <= c <= '9':
                return False
            return True
        elif c1 == 's':       # \s is [ \t\n\r\f\v]
            return c in ' \t\n\r\f\v'
        elif c1 == 'S':       # \S is [^ \t\n\r\f\v]
            return c not in ' \t\n\r\f\v'
        elif c1 in 'ntr':
            idx = 'ntr'.index(c1)
            c1 = '\n\t\r'[idx]
        elif c1 == 'w':
            return IsWordChar(c)
        elif c1 == 'W':
            return not IsWordChar(c)
        else:
            print 'c1 is', c1
            assert False

        return c1 == c

    def visit_ZeroOrMoreNoGreedy(self, node):
        return self.NumberControlNoGreedy(node, 0, -1)
    def visit_Dot(self, node):
        if self.pos >= self.endpos:
            return False
        c = self.sourcestr[self.pos]
        if self.flags & REFLAGS.DOTALL:
            self.pos += 1
            return True

        if c == '\n':
            return False
        self.pos += 1
        return True
    def visit_IfNext(self, node):
        savpos = self.pos
        if node.v.walkabout(self):
            self.pos = savpos
            return True
        return False
    def visit_IfNotNext(self, node):
        savpos = self.pos
        if node.v.walkabout(self):
            self.pos = savpos
            return False
        return True
    def visit_stmt(self, node):
        savpos = self.pos
        for v in node.vlst:
            if v.walkabout(self):
                return True
            assert savpos == self.pos
        return False
    def visit_Group(self, node):
        def func1(value):
            for i in range(len(self.groupvalues)):
                col, b = self.groupvalues[i]
                if col == id(node): #.col_offset:
                    self.groupvalues[i] = (col, value)
                    break
                #assert col < node.col_offset
            else:
                self.groupvalues.append((id(node), value))
        savpos = self.pos
        if node.v.walkabout(self):
            value = self.sourcestr[savpos:self.pos]
            func1(value)
            return True

        #func1(None)
        return False
    def visit_NonGroup(self, node):
        return node.v.walkabout(self)
    def visit_SetCompl(self, node):
        if self.pos >= self.endpos:
            return False
        #c = self.sourcestr[self.pos]
        #if c == '\n':   # anytime not include '\n'
        #    return False
        savpos = self.pos
        for v in node.vlst:
            if v.walkabout(self):
                self.pos = savpos
                return False
            assert savpos == self.pos
        self.pos += 1
        return True

class LexParser:
    def visit_Num11(self, node):
        return int(node.s1), int(node.s2)
    def visit_Num10(self, node):
        return int(node.s), -1
    def visit_Num(self, node):
        return int(node.s), int(node.s)
    def visit_Num01(self, node):
        return -1, int(node.s)
    def visit_WithNumCtl(self, node):
        n1, n2 = node.n.walkabout(self)
        #print 'n1,n2', n1, n2
        return self.NumberControl(node, n1, n2)
    def visit_NumCtlNoGreedy(self, node):
        n1, n2 = node.n.walkabout(self)
        #print 'n1,n2', n1, n2
        return self.NumberControlNoGreedy(node, n1, n2)

    def visit_ZeroOrOne(self, node):
        #from dbgp.client import brk,brkOnExcept; brk(port=9000)
        #brk()
        return self.NumberControl(node, 0, 1)
        node.v.walkabout(self)
        return True
    def visit_Opt(self, node):
        savpos = self.pos
        for v in node.v:
            if v.walkabout(self):
                return True
            assert self.pos == savpos
        return False

    def visit_Name0(self, node):
        if self.pos >= self.endpos:
            return False
        c = self.sourcestr[self.pos]
        if c == node.nm:
            self.pos+=1
            return True
        assert len(node.nm) == 1
        c = ord(c)
        c2 = ord(node.nm)
        if self.flags & REFLAGS.I:
            if ord('a') <= c <= ord('z'):
                c = c - ord('a') + ord('A')
            if ord('a') <= c2 <= ord('z'):
                c2 = c2 - ord('a') + ord('A')
            if c == c2:
                self.pos += 1
                return True
        return False
    def IsWordBegin(self):
        if self.pos == self.endpos == 0:
            return False
        if self.pos == 0:
            return IsWordChar(self.sourcestr[self.pos])
        if self.pos == self.endpos:
            return False
        f1 = IsWordChar(self.sourcestr[self.pos-1])
        f2 = IsWordChar(self.sourcestr[self.pos])
        return (f1, f2) == (False, True)
    def IsWordEnd(self):
        if self.pos == 0:
            return False
        if self.pos == self.endpos:
            return IsWordChar(self.sourcestr[self.pos-1])
        f1 = IsWordChar(self.sourcestr[self.pos-1])
        f2 = IsWordChar(self.sourcestr[self.pos])
        return (f1, f2) == (True, False)

    def visit_NamedGroup(self, node):
        #print node.nm, node.v
        #assert False
        # refer visit_Group(self, node)
        savpos = self.pos
        if node.v.walkabout(self):
            value = self.sourcestr[savpos:self.pos]
            for i in range(len(self.groupvalues)):
                col, b = self.groupvalues[i]
                if col == node.col_offset:
                    self.groupvalues[i] = (col, value)
                    self.namedvalues[node.nm] = value
                    break
                #assert col < node.col_offset
            else:
                self.groupvalues.append((node.col_offset, value))
                self.namedvalues[node.nm] = value
            return True
        return False

    def visit_CharAsIs(self, node):
        if self.pos >= self.endpos:
            return False
        c = self.sourcestr[self.pos]
        if c == node.s:
            self.pos += 1
            return True
        return False
    def visit_LineLead(self, node):
        if self.pos == 0:
            return True
        if self.sourcestr[self.pos-1] == '\n':
            return True
        return False

    def visit_LineTail(self, node):
        if self.pos == self.endpos:
            return True
        if self.sourcestr[self.pos] == '\n':
            return True
        return False
    def visit_IfProceed(self, node):
        assert isinstance(node.v, ast_lex.Stmt)
        lst = node.v.v + []
        flgIsProceed = self.IsProceedLst(lst, self.pos)
        return flgIsProceed
    def visit_NotProceed(self, node):
        assert isinstance(node.v, ast_lex.Stmt)
        lst = node.v.v + []
        pos = self.pos
        #from dbgp.client import brk,brkOnExcept; brk(port=9000)
        #brk()
        flgIsProceed = self.IsProceedLst(lst, pos)
        if flgIsProceed:
            return False
        return True
    def IsProceedLst(self, lst, pos):
        while lst:
            v = lst.pop()
            flg, newpos = self.IsProceed(v,pos)
            if not flg:
                return False
            pos = newpos
        return True

    def IsProceed(self, node, pos):
        if pos == 0:
            return False,0
        if isinstance(node, ast_lex.Name0):
            c = self.sourcestr[pos-1]
            if c == node.nm:
                return True, pos-1
            return False,0
        if isinstance(node, ast_lex.Escape):
            c = self.sourcestr[pos-1]
            if self.Escape_inno(node, c):
                return True, pos-1
            return False,0

        assert False, type(node)

    def visit_SetFlags(self, node):
        for v in node.v:
            assert isinstance(v, ast_lex.Name0)
            if v.nm == 'i':
                self.flags |= REFLAGS.I
            elif v.nm == 'L':
                self.flags |= REFLAGS.L
            elif v.nm == 'm':
                self.flags |= REFLAGS.M
            elif v.nm == 's':
                self.flags |= REFLAGS.S
            elif v.nm == 'u':
                self.flags |= REFLAGS.U
            elif v.nm == 'x':
                self.flags |= REFLAGS.X
            else:
                assert False
        return True
    def visit_YesOrNo(self, node):
        node.nm
        node.v
        n = TryToNum(node.nm)
        if n > 0:
            _,value = self.groupvalues[n-1]
        elif node.nm in self.namedvalues:
            value = self.namedvalues[node.nm]
        else:
            assert False

        if value:
            if node.v.v1:
                return node.v.v1.walkabout(self)
        else:
            if node.v.v2:
                return node.v.v2.walkabout(self)
        return True
    def visit_RefName(self, node):
        assert False

#---- Some unit tests ----#

import unittest, re

class TestRegularExpression(unittest.TestCase):

    def test_1(self):
        s_sample = r"hello 'string\n\'STRING' world"
        redef = r"'([^'\\]*(?:\\.[^'\\]*)*)'"

        mod = Test_Parse_Re(redef)
        visit = RegularExpression()
        visit.input(s_sample, 6)
        mod.walkabout(visit)
        mt = visit.matchtoken()
        if not mt:
            self.fail('error')
        word, pos = mt
        self.assertEqual(word, r"'string\n\'STRING'")
        self.assertEqual(pos, 24)
        self.assertEqual(len(visit.groupvalues), 1)
        self.assertEqual(visit.groupvalues[0][1], r"string\n\'STRING")

    def test_2(self):
        lexed = re.compile(r'[^\]+\-<>.,]+', re.VERBOSE)
        s = 'A mandelbrot set fractal viewer in brainfuck2 wri,tten] by'
        m = lexed.match(s, 0)
        self.assertEqual(m.end(), 49)
        lexed2 = re.compile(r'[^\]+-<>.,]+', re.VERBOSE)
        m = lexed2.match(s, 0)
        self.assertEqual(m.end(), 44)

        redef = r'[^\]+\-<>.,]+'
        mod = Test_Parse_Re(redef)
        visit = RegularExpression()
        visit.input(s, 0)
        mod.walkabout(visit)
        mt = visit.matchtoken()
        if not mt:
            self.fail('error')
        word, pos = mt
        self.assertEqual(word, r"A mandelbrot set fractal viewer in brainfuck2 wri")
        self.assertEqual(pos, 49)

        redef = r'[^\]+-<>.,]+'
        mod = Test_Parse_Re(redef)
        visit = RegularExpression()
        visit.input(s, 0)
        mod.walkabout(visit)
        mt = visit.matchtoken()
        if not mt:
            self.fail('error')
        word, pos = mt
        self.assertEqual(word, r"A mandelbrot set fractal viewer in brainfuck")
        self.assertEqual(pos, 44)


if __name__ == '__main__':
    pass
