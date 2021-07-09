import drinks_info

class Ask():
    def __init__(self,choices=['y','n']):
        self.choices = choices
    def ask(self):
        if max([len(x) for x in self.choices])>1:
            for i,x in enumerate(self.choices):
                print("{0}. {1}".format(i,x))
            x = int(input())
            return self.choices[x]
        else:
            print("/".join(self.choices))
            return input()

class Content():
    def __init__(self,x):
        self.x=x
        
class If(Content):
    pass

class AND(Content):
    pass

class OR(Content):
    pass

rules = {
    'default': Ask(['y','n']),

    'крепость' : Ask(['<20','>20', '~20']),
    'ваш пол' : Ask(['мужской', 'женский']),
    'нрав. вкус' : Ask(['хмеля','ржаной', 'сладкий', 'пшенички', 'винограда', 'сливок', 'апельсина', 'травяной']),
    'здоровье' : Ask(['нормальное давление','повышенное давление', 'проблемы с желудком']),
###############################

    'Слабоалк' : If(OR(['крепость: <20', 'лучше сильно не напиваться'])),
    'Сильноалк' : If(OR(['крепость: >20', 'как насчет знатно напиться'])),
    'типа Пиво' : If(['Слабоалк', 'нап. газированный', OR(['ваш пол: мужской','нрав. вкус: хмеля'])]),
    'типа Вино' : If(['Слабоалк','нрав. вкус: винограда', OR(['пол: женский', 'хочется посмаковать напитком'])]),
    'типа Ликеры' : If(['крепость: ~20', AND(['нрав.вкус: сладкий', 'хочется посмаковать напитком'])]),

################################

    'напиток: Темное пиво' : If(['типа Пиво', 'нрав. вкус: ржаной']),
    'напиток: Пшеничное пиво' : If(['типа Пиво', 'нрав. вкус: пшенички']),
    'напиток: Красное вино' : If(['типа Вино', 'здоровье: нормальное давление']),
    'напиток: Белое вино' : If(['типа Вино', 'здоровье: повышенное давление']),
    'напиток: Шампанское' : If(['типа Вино', 'нап. газированный']),
    'напиток: Ликер Куантро' : If(['типа Ликеры', 'нрав. вкус: апельсина']),
    'напиток: Ликер Ягермейстер' : If(['типа Ликер', 'нрав. вкус: травяной']),
    'напиток: Ликер Белис' : If(['типа Ликер', 'нрав. вкус: сливки']),
    'напиток: Ром' : If(['Сильноалк', 'сигары', 'можно смешать']),
    'напиток: Виски' : If(['Сильноалк', 'есть лёд', 'можно смешать']),
    'напиток: Коньяк' : If(['Сильноалк', 'сигары', 'нужна закуска']),
    'напиток: Водка' : If(['Сильноалк', 'нужна закуска']),
    'напиток: Абсент' : If(['Сильноалк', 'нрав. анис']),

}

class KnowledgeBase():
    def __init__(self,rules):
        self.rules = rules
        self.memory = {}
        
    def get(self,name):
        if name in self.memory.keys():
            return self.memory[name]
        for fld in self.rules.keys():
            if fld==name or fld.startswith(name+":"):
                value = 'y' if fld==name else fld.split(':')[1]
                res = self.eval(self.rules[fld],field=name)
                if res=='y':
                    self.memory[name] = value
                    return value
        res = self.eval(self.rules['default'],field=name)
        self.memory[name]=res
        return res
                
    def eval(self,expr,field=None):
        if isinstance(expr,Ask):
            print(field)
            return expr.ask()
        elif isinstance(expr,If):
            return self.eval(expr.x)
        elif isinstance(expr,AND) or isinstance(expr,list):
            expr = expr.x if isinstance(expr,AND) else expr
            for x in expr:
                if self.eval(x)=='n':
                    return 'n'
            return 'y'
        elif isinstance(expr,OR):
            for x in expr.x:
                if self.eval(x)=='y':
                    return 'y'
            return 'n'
        elif isinstance(expr,str):
            return self.get(expr)
        else:
            print("Unknown expr: {}".format(expr))


kb = KnowledgeBase(rules)
answer = kb.get('напиток')
print("Предлагаем вам ",answer)
drinks_info.print_info(answer)

