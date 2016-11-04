# модуль с классами калькулятора
from tkinter import*
from tkinter import ttk
import math,sys,re
class Calculator:
    """методы калькулятора"""
    def __init__(self, exc):
        self.exc = exc
        self.signs = "^/*%-+"
        self.struck = ['sin', 'cos', 'atg', 'tg', 'sqrt', 'lg', 'log']
        self.do = True
        self.task = ""
        self.costas = []
    def replace(self,string,what,nawhat,ot=0):
        """собственный метод replace для замены с определенного места"""
        aga=string.find(what,ot)
        if aga!=-1:
            string =string[:aga]+nawhat+string[aga+len(what):]
        return string
    def find(self,string,what,ot=0):
        """собственный метод find для возвращения позиции последнего символа"""
        aga=string.find(what,ot)
        start=len(what)
        if aga!=-1:
            return aga+start
        return -1
    def masses(self,what):
        """разъединение выражения на знаки и числа(2+2->(2 2)+( + )), на вход простейшее выражение"""
        if self.do==False:
            return
        try:
            digits=""
            alpha=""
            all_digits="1234567890-+.e"
            for i in range(len(what)):
                need=all_digits.find(what[i])
                if need != -1:
                    if what[i]=="-"or what[i]=="+":
                        if len(digits)>0:
                            if digits[-1]=="e":
                                digits+=what[i]
                                alpha+=" "
                                continue
                        dsa=self.signs.find(what[i-1])
                        if i==0 or dsa!=-1:
                            pass
                        else:
                             need=self.signs.find(what[i])
                             if need!=-1:
                                digits+=" "
                                alpha+=what[i]
                                continue
                    digits+=what[i]
                    alpha+=" "
                else:
                    need=self.signs.find(what[i])
                    if need!=-1:
                        digits+=" "
                        alpha+=what[i]
            connect=[]
            connect.append(digits)
            connect.append(alpha)
            return connect
        except TypeError:
            self.error("Syntax error")
            return
    def make(self):
        """метод разделяет сложное выражение на простые и запиывает в массив
                    также ищет скобки для правильной последовательности счета"""
        if self.do==False:
            return
        gag=self.exc.find("(")
        ga=self.exc.find(")")
        if(gag!=-1 or ga!=-1):
            gig='1234567890.'
            stack=[]
            ch=0
            crack=""
            for i in range(len(self.exc)):
                if self.exc[i]=="(":
                    stack.append(i)
                    continue
                elif self.exc[i]==")":
                    if len(stack)==0:
                        self.error("So many brackets")
                        return
                    a=stack[-1]
                    for e in range(a+1,i):
                        crack+=self.exc[e]
                    costa = []
                    costa.append(crack)
                    crack="("+crack+")"
                    costa.append(("@"+str(ch))+(((len(crack)-1)-(len(str(ch))))*'_'))
                    ch+=1
                    costa.append(a)
                    self.costas.append(costa)
                    self.exc=self.exc.replace(crack,costa[1],1)
                    stack.pop()
                    crack=""
            if len(stack)>0:
                self.error("Lost brackets")
                return
            self.costas.sort(key=self.sada,reverse=True)
    def sada(self, a):
        """Корпоратор"""
        return a[2]
    def resh_func(self,what):
        """метод решает простейшее выражение и функцией, если она есть"""
        if self.do==False:
            return
        words='sincostgsqrtlgpie'
        dig='1234567890.-+'
        diga=self.find(what,".0")
        digan=what
        if diga!=-1:
            if diga==len(digan):
                digan=digan.replace(".0","",1)
        for i in range(len(self.struck)):
            a=self.find(digan,self.struck[i])
            if a!=-1:
                znak=''
                vira=''
                a1=digan.find(self.struck[i])
                for j in range(a1,a):
                    znak+=digan[j]
                for j in range(a,len(digan)):
                    mb=dig.find(digan[j])
                    if mb!=-1:
                        if (digan[j]=="+"or digan[j]=="-") and j!=a:
                            break
                        vira+=digan[j]
                    else:
                        break
                utu=znak+vira
                otvet=self.bobol(znak,vira)
                what=digan.replace(utu,str(otvet))
                digan=what
                i=i-1
        return what
    def bobol(self,znak,vira):
        """сама составляющая resh_func"""
        if self.do==False:
            return
        if vira=="" or vira==" ":
            self.error("No exception in brackets")
            return
        vira=float(vira)
        if znak=='lg'or znak=='log':
            if str(vira)[0]=="-":
                self.error("lg can't take minus exception")
                return
            extent=math.log10(vira)
        elif znak=='sqrt':
            if str(vira)[0]=="-":
                self.error("sqrt can't take minus exception")
                return
            extent=math.sqrt(vira)
        elif znak=='cos':
            vira=math.radians(vira)
            extent=math.cos(vira)
        elif znak=='sin':
            vira=math.radians(vira)
            extent=math.sin(vira)
        elif znak=='tg':
            vira=math.radians(vira)
            extent=math.tan(vira)
        elif znak == 'atg':
            extent = math.atan(vira)
            extent = math.degrees(extent)
        return extent
    def replacer(self,what):
        """заменяет в выражении несколько знаков подряд"""
        what=what.replace("--","+")
        what=what.replace("++","+")
        what=what.replace("+-","-")
        what=what.replace("-+","-")
        return what
    def kook(self,what):
        """главная фунция счета"""
        if self.do==False:
            return
        try:
                what=self.resh_func(what)#смотрим, есть ли в выражении функции, если есть то решаем
                what=self.replacer(what)
                connect=self.masses(what)
                digits=connect[0]
                alpha=connect[1]
                hack=alpha.split()#массив из всех знаков в выражении
                cch=len(hack)
                for k in range(cch):
                    for l in range(len(self.signs)):
                       cros=alpha.find(self.signs[l])
                       if cros!=-1:
                            sign=alpha[cros]
                            break
                    ll=''
                    rr=''
                    az=0
                    azm=len(alpha)
                    #находим операнды
                    for l in range(cros-1,-1,-1):
                        if digits[l]!=' ':
                            ll=digits[l]+ll
                        else:
                            az=l+1
                            break
                    for l in range(cros+1,len(digits)):
                        if digits[l]!=' ':
                            rr+=digits[l]
                        else:
                            azm=l
                            break

                    non=''
                    no=''
                    for i in range(az,azm):
                        non+=digits[i]
                        no+=alpha[i]
                    if ll[0]==".":
                        ll="0"+ll[:]
                    if rr[0]==".":
                        rr="0"+rr[:]
                    orl=0.0
                    try:#собственно, считаем
                        if sign=="+":
                            orl=float(ll)+float(rr)
                        elif sign=='-':
                            orl=float(ll)-float(rr)
                        elif sign=="*":
                            orl=float(ll)*float(rr)
                        elif sign=="/":
                            if float(rr)==0:
                                self.error("Zero error")
                                return
                            orl=float(ll)/float(rr)
                        elif sign=="^":
                            orl=float(ll)**float(rr)
                        elif sign=="%":
                            orl=float(ll)%float(rr)
                    except:
                        self.error("Syntax error")
                        return
                    afg=str(orl)
                    digits=self.replace(digits,non,afg,az)
                    alpha=self.replace(alpha,no,(len(afg)*' '),az)
                what=digits
                return what
        except:
            self.error("Syntax error")
            return
    def score(self):
        """метод решает массив из простейших выражений и подставляет в следующий элемент вместо сивола '__' """
        if self.do == False:
            return
        for i in range(len(self.costas)):
                jo=True
                self.costas[i][0]=self.kook(self.costas[i][0])
                if i!=len(self.costas)-1:
                    for j in range(i+1,len(self.costas)):
                        astd=self.costas[j][0].find(self.costas[i][1])
                        if astd!=-1:
                            self.costas[j][0]=self.replace(self.costas[j][0],self.costas[i][1],self.costas[i][0])
                            jo=False
                            break
                    if j==len(self.costas)-1:
                        if jo==True:
                            self.exc=self.replace(self.exc,self.costas[i][1],self.costas[i][0])
        for i in range(len(self.costas)-1,-1,-1):
            self.exc=self.replace(self.exc,self.costas[i][1],self.costas[i][0],self.costas[i][2])
        self.exc=self.resh_func(self.exc)
        self.exc=self.kook(self.exc)
    def error(self,mes):
        """метод вывода ошибки"""
        if self.do:
            self.task = mes
            self.do = False
    def is_correct(self):
        """Проверяем на правильность выражения"""
        all_what = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+', '-', '*', '^', '/', '%', '.', '(', ')', 'lg',
                    'sin', 'cos', 'atg', 'tg', 'sqrt', 'log']
        new = self.exc
        for i in all_what:
            new = new.replace(i, '')
        if len(new) != 0:
            self.error("Invalid character")
            return False
        del new
        return True
    def main(self):
        """main- главный метод программы, который вызывает все остальные методыи в уонце выводит ответ"""
        try:
            k = self.exc.find("=")
            if k != -1:
                self.exc = self.exc[:k]
            self.exc = self.exc.replace(" ", "")
            self.exc = self.exc.replace("\n", "")#удаляем переносы строк
            self.exc = self.exc.lower()
            #замена pi и e прямо в выражении
            self.exc = self.exc.replace("pi", str(math.pi))
            self.exc = self.exc.replace("e", str(math.e))
            self.exc = self.replacer(self.exc)
            self.exc = self.exc.replace(",", ".")
            #проверка на недопустимые символы
            if(self.is_correct()):
                self.make()#делим выражние на простые состовляющие
                self.score()#решаем и подставляем
                if self.exc == "-0.0" or self.exc == "-0":
                    self.exc = "0"
            else:
                self.error("Syntax error")
                return self.task
            self.exc = float(self.exc)
            self.exc = round(self.exc, 5)
            self.exc = str(self.exc)
            return self.exc
        except:
            self.error("Syntax error")
        return self.task
if __name__ == "__main__":
    print("It is a module. You can only import it")
    input()
