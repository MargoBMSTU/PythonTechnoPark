
import argparse
import sys
import re


def output(line):
    print(line)


# выводит before_context без linenumber
# n - количество линий выводимых До совпавшей
# lines - все линии
# current_line - номер текущей линии
# previous - номер предыдущего совпадения
def before_context(n, lines, current_line, previous):
    if current_line - n < 0: # если вылезли за левую границу
        start = 0
    elif previous >= current_line - n: # если было пересечение с предыдущем значением
        start = previous + 1 # начинаем со следуещего после него
    else:
        start = current_line - n # иначе текущая - n 
    for i in range(start, current_line):
        output(lines[i].strip())
    output(lines[current_line].strip())
    return current_line


#After_context без linenumber
def after_context(n, lines, current_line, previous):
    if previous + n >= current_line: # Если было пересечение с предыдущем значением
        start = previous
        end = current_line + n
    else:
        start = current_line
        end = current_line+n
    if current_line + n > len(lines): # если вылезли за правую границу
        end = len(lines)
    output(lines[start].strip()) 
    for i in range(start+1, end+1):
        output(lines[i].strip())
    return previous

# context без linenumber
def context(n, lines, current_line, previous):
    # Пересечение предыдущего вывода после, с текущем выводом до
    if previous >= current_line - 2*n and current_line-2*n >= 0: 
        start = previous + 1 + n
    elif current_line - n <= 0: #вылезли за левую грань
        start = 0
    else:
        start = current_line - n
    q = len(lines) # количество линий
    if current_line + n < q: 
        end = current_line + n + 1
    else:
        end = q # вылезли за правую грань
    for i in range(start, end):
        output(lines[i].strip())

    return current_line


#before_context если был установлен кулюч linenubmer
def before_context_with_linenumber(n, lines, current_line, previous):
    if current_line - n < 0: # вышли за левую грать
        k = 0
    elif previous >= current_line - n: # если было пересечение с предыдущем значением
        k = previous + 1 # начинаем со следуещего после него
    else:
        k = current_line - n #иначе просто -n от текущего
    for i in range(k, current_line - 1):
        output(str(i + 1) + '-' + lines[i].strip())
    output(str(current_line+1) + ':' + lines[current_line].strip()) # совпавшее значение
    return current_line


def after_context_with_linenumber(n, lines, current_line, previous):
    if previous + n <= current_line: # было пересечение предыдущего вывода
        k1 = previous + n + 1
    else:
        k1 = current_line
    output(str(previous+1) + ':' + lines[previous].strip())
    for i in range(previous + 1, k1):
        output(str(i+1) + '-' + lines[i].strip())
    return current_line


def context_With_linenumber(n, lines, current_line, previous):
    # Сначала выводится элементы после ПРЕДЫДУЩЕЙ совпавшей линии
    if previous > 0: 
        if previous + 2*n <= current_line:
            k1 = previous + n
        else:
            k1 = current_line - n
        output(str(previous+1) + ':' + lines[previous].strip())
        for i in range(previous + 1, k1):
            output(str(i+1) + '-' + lines[i].strip())
    # Элементы до текущей.         
    if current_line - n <= 0:
        k = 0
    elif previous + n > current_line - n and previous != 0:
        k = current_line + n
    else:
        k = current_line - n
    for i in range(k, current_line):
        output(str(i + 1) + '-' + lines[i].strip())
    return current_line


def case_1(params, lines, n, n1):
    if re.findall(params.pattern.lower(), lines[n].lower()) != []:
        return cont_with_linenumber(params, lines, n, n1)


def case_2(params, lines,n , n1):
    if re.findall(params.pattern.lower(), lines[n].lower()) != []:
        return cont(params, lines, n, n1)


def case_3(params, lines, n, n1):
    if re.findall(params.pattern, lines[n]) != []:
        return cont_with_linenumber(params, lines, n, n1)


def case_4(params, lines, n, n1):
    if re.findall(params.pattern, lines[n]) != []:
        return cont(params, lines, n, n1)


def case_5(params, lines, n, n1):
    if re.findall(params.pattern.lower(), lines[n].lower()) == []:
        return cont_with_linenumber(params, lines, n, n1)# output(str(n + 1) + ':' + lines[n].strip())  # output(num,':',line)


def case_6(params, lines, n, n1):
    if re.findall(params.pattern.lower(), lines[n].lower()) == []:
        return cont(params, lines, n, n1)#output(lines[n].strip())


def case_7(params, lines, n, n1):
    if re.findall(params.pattern, lines[n]) == []:
        return cont_with_linenumber(params, lines, n, n1)#output(str(n + 1) + ':' + lines[n].strip())


def case_8(params, lines, n, n1):
    if re.findall(params.pattern, lines[n]) == []:
        return cont(params, lines, n, n1)#output(lines[n].strip())

def case_9(params, lines, n, n1):
    if re.findall(params.pattern.lower(), lines[n].lower()) != []:
        return n1+1

def case_10(params, lines, n, n1):
    if re.findall(params.pattern, lines[n]) != []:
        return n1+1

def case_11(params, lines, n, n1):
    if re.findall(params.pattern.lower(), lines[n].lower()) == []:
        return n1+1

def case_12(params, lines, n, n1):
    if re.findall(params.pattern, lines[n]) == []:
        return n1+1


#Выбор вывода в зависимости от context/after_context/before_context для случая без linenumber
def cont(params, lines, n, n1):
    if (params.context != 0) or ((params.before_context != 0) and (params.after_context != 0)):
        return (context(params.context, lines, n, n1))
    elif params.before_context != 0:
        return (before_context(params.before_context, lines, n, n1))
    elif params.after_context != 0:
        return (after_context(params.after_context, lines, n, n1))
    else:
        return output(lines[n].strip())

#Выбор вывода в зависимости от context/after_context/before_context для случая с linenumber
def cont_with_linenumber(params, lines, n, n1):
    if (params.context != 0) or ((params.before_context != 0) and (params.after_context != 0)):
        return (context_With_linenumber(params.context, lines, n, n1))
    elif params.before_context != 0:
        return (before_context_with_linenumber(params.before_context, lines, n, n1))
    elif params.after_context != 0:
        return (after_context_with_linenumber(params.after_context, lines, n, n1))
    else:
        return output(str(n+1)+":"+lines[n].strip())


# Выбираем какая функция должна отработать и возвращаем её
def ChoiceExecuteFunc(params):
    if params.invert != True:
        if params.ignore_case == True:
            if params.count == True:
                return case_9 # Invert False; Ignore_Case True; Count True;
            else:
                if params.line_number == True:
                    return case_1 # Invert False; Ignore_Case True; Count False;line_number true
                else:
                    return case_2 # Invert False; Ignore_Case True; Count False;line_number false
        else:
            if params.count == True: 
                return case_10 # Invert False; Ignore_Case False; Count True;
            else:
                if params.line_number == True:
                    return case_3 # Invert False; Ignore_Case False;line_number True;
                else:
                    return case_4 # Invert False; Ignore_Case False;line_number False;
    else:
        if params.ignore_case == True: 
            if params.count == True:
                return case_11 # Invert True; Ignore_case True; Count True;
            else:
                if params.line_number == True:
                    return case_5 # Invert True; Ignore_case True; line_number True;
                else:
                    return case_6 # Invert True; Ignore_case True; line_number True;
        else:
            if params.count == True:
                return case_12 # Invert True; Ignore_case False; Count True;
            else:
                if params.line_number == True:
                    return case_7 # Invert True; Ignore_case False; Count False;line_number True;
                else:
                    return case_8 # Invert True; Ignore_case False; Count False;line_number False;


def grep(lines, params):
    # Замяем символы * и ? чтобы они удовлетворяли python re 
    params.pattern = params.pattern.replace('*', r'.*')
    params.pattern = params.pattern.replace('?', r'.')
    executor = ChoiceExecuteFunc(params) # исполнаяющая функция
    last = 0 # последнее совпадение(или счетчик с случае клуча -c)
    for i in range(len(lines)): 
        last_i = executor(params,lines, i, last) # номер последнего найденного элемента (или количество строк)
        if last_i != None:
            last = last_i
    if params.count == True:
        output (str(last))
    else:
        if params.line_number == True:
            # Выводим значения после последнего совпадения в случае context и after_context 
            # Так как в них мы выводим значения предидущей итерации(а не текущей) чтобы определить что ставить
            # ":" или "-"
            if params.after_context != 0:
                after_context_with_linenumber(params.after_context, lines, len(lines), last)
            if params.context != 0:
                after_context_with_linenumber(params.context, lines, len(lines), last)    

def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()