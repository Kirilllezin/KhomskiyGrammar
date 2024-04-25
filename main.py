# Регулярная грамматика
# 1) A -> Bγ или A -> γ, где γ ∈ VT*, A, B ∈ VN (для леволинейных грамматик)
# 2) A -> γB; или A -> γ, где γ ∈ VT*, A, B ∈ VN (для праволинейных грамматик)

# Контекстно-свободная
# A -> β, где β ∈ V+ (для неукорачивающих КС-грамматик) или β ∈ V* (для укорачивающих), A ∈ VN
# То есть грамматика допускает появление в левой части правила только нетерминального символа.

# Контекстно-зависимая
# 1) αAβ -> αγβ, где α, β ∈ V*, γ ∈ V+, A ∈ VN.
#    Такие грамматики относят к контекстно-зависимым
# 2) α -> β, где α, β ∈ V+, 1 ≤ |α| ≤ |β|.
#    Такие грамматики относят к неукорачивающим

# Грамматика тип 0
# Не подходит под остальные типы грамматики


# Функция для создания замыкания множества
def kleene_star(G, parent, symbol):
    # Начинаем с пустой строки в качестве начального замыкания
    closure = {''}
    if parent in "T":
        # Добавляем все элементы из исходного множества
        for element in G["T"]:
            closure.update(element)

        # Пока замыкание продолжает расширяться и счётчик < 1000 итераций
        iterations = 0
        while True and iterations < 2:
            iterations += 1
            new_elements = set()
            # Для каждой пары элементов из замыкания и исходного множества
            for element in closure:
                for t in G["T"]:
                    # Добавляем конкатенацию элемента из замыкания и элемента из исходного множества
                    new_elements.add(element + t)
            # Если не было добавлено новых элементов, значит замыкание завершено
            if not new_elements:
                break
            # Обновляем замыкание
            closure.update(new_elements)

    elif parent in "NT":
        # Добавляем все элементы из исходного множества
        for element in G["T"]:
            closure.update(element)
        for element in G["N"]:
            closure.update(element)

        # Пока замыкание продолжает расширяться и счётчик < 1000 итераций
        iterations = 0
        while True and iterations < 2:
            iterations += 1
            new_elements = set()
            # Для каждой пары элементов из замыкания и исходного множества
            for element in closure:
                for t in G["T"]:
                    # Добавляем конкатенацию элемента из замыкания и элемента из исходного множества
                    new_elements.add(element + t)

            for element in closure:
                for t in G["N"]:
                    # Добавляем конкатенацию элемента из замыкания и элемента из исходного множества
                    new_elements.add(element + t)

            # Если не было добавлено новых элементов, значит замыкание завершено
            if not new_elements:
                break
            # Обновляем замыкание
            closure.update(new_elements)

    if symbol == "*":
        # print("T*:",closure)
        return sorted(list(closure))

    elif symbol == "+":
        # print("T+:", closure)
        return sorted(list(closure)[1:])


def check_grammar_class(G):
    is_regular_type1 = True
    is_regular_type2 = True
    is_context_free = True
    is_context_sensitive_type1 = False
    is_context_sensitive_type2 = True
    is_unrestricted = True

    # Добавить проверку  A → r или A → Br ; r in Vt*

    # Задаем r
    Vt_star = kleene_star(G, "T", "*")
    V_star = kleene_star(G, "NT", "*")
    V_plus = kleene_star(G, "NT", "+")
    for rule in G["P"]:
        # Разделяем левую и правую части по знаку ->
        left_side, right_side = rule.split("->")
        left_side = left_side.strip()
        right_side = right_side.strip()
        # print("left",left_side)
        # print("right",right_side)

        #                                                                                                           Проверка на класс регулярности
        if (is_regular_type1 or is_regular_type2) and (len(right_side) > 0 and len(left_side) > 0):
            # Проверка на класс 1: A -> Br или A -> r, где r ∈ VT*, A, B ∈ VN (для леволинейных грамматик)
            # Проверка левой части на принадлежность VN
            for A in left_side:
                if A in G["N"]:
                    continue
                else:
                    is_regular = False
                    break

            # Проверка правой части на принадлежность VN
            for symbol in right_side:
                if symbol in G["N"]:

                    # Проверка: A -> Br
                    # Проверка: A -> r
                    flag_Br = False
                    flag_rB = False
                    flag_r = False
                    for r in Vt_star:
                        if r in right_side:
                            # Проверка, что r Именно справа Br
                            right_side_check = right_side.replace(r, '')
                            if (right_side_check + r) == right_side:
                                flag_Br = True
                            elif (r + right_side_check) == right_side:
                                flag_rB == True
                        else:
                            continue

                        # A -> r
                        if right_side == r:
                            flag_r = True
                        else:
                            continue

                        if flag_Br or (flag_Br and flag_r):
                            is_regular_type2 = False

                        elif flag_rB or (flag_rB and flag_r):
                            is_regular_type1 = False


                else:
                    is_regular_type1 = False
                    is_regular_type2 = False
                    break


        else:
            continue

    #                                                                                                Проверка на класс контекстно-свободных грамматик
    # alpha -> beta, где beta ∈ V+  β ∈ V + (для неукорачивающих КС-грамматик) или β ∈ V∗ (для укорачивающих), A∈Vn 1 ≤ |alpha| ≤ |beta|.Такие грамматики относят к неукорачивающим
    # Проверка beta ∈ V+
    beta = right_side
    flag_beta = False
    flag_beta2 = False
    if beta in V_plus:
        flag_beta = True

    # Проверка beta ∈ V*
    elif beta in V_star:
        flag_beta2 = True

    if (flag_beta == False) and (flag_beta2 == False):
        is_context_free = False

    # Проверка A ∈ VN
    for A in left_side:
        if A in G["N"]:
            continue
        else:
            is_context_free = False
            break

    #                                                                                               Проверка на класс контекстно-зависимых грамматик
    # Проверка типа 1: α -> β, где α, β ∈ V+, 1 ≤ |α| ≤ |β| (Такие грамматики относят к неукорачивающим.)
    # Проверка α, β ∈ V+
    alpha, beta = left_side, right_side
    flag_alpha = False, False
    if alpha in V_plus:
        flag_alpha = True
    else:
        is_context_sensitive_type1 = False

    if beta in V_plus:
        flag_beta = True
    else:
        is_context_sensitive_type1 = False
    # Проверка 1 ≤ |α| ≤ |β|
    if flag_alpha and flag_beta:
        if 1 <= len(alpha) <= len(beta):
            ...
        else:
            is_context_sensitive_type1 = False
    else:
        is_context_sensitive_type1 = False

    # Проверка типа 2: αAβ -> αγβ, где α, β ∈ V*, γ ∈ V+, A ∈ VN. Такие грамматики относят к контекстно-зависимым.
    if len(left_side) > 2 and len(right_side) > 2:
        alpha2 = left_side[0]
        beta2 = left_side[-1]
        A = left_side.replace(alpha, "")
        A = left_side.replace(beta, "")
        # Проверка αAβ -> αγβ
        # Проверка, что нет пустых множетсв
        if right_side != '' and left_side != '':
            if right_side[0] == alpha2 and right_side[-1] == beta2:
                y = right_side.replace(alpha2, "")
                y = right_side.replace(beta2, "")
            else:
                y = "Epsilon"
                is_context_sensitive_type2 = False
        else:
            y = "Epsilon"
            is_context_sensitive_type2 = False
    else:
        alpha2 = "Epsilon"
        beta2 = "Epsilon"
        y = "Epsilon"
        is_context_sensitive_type2 = False

    # Проверка A ∈ VN
    for symbol in range(len(A)):
        if symbol in G["N"]:
            continue
        else:
            is_context_sensitive_type2 = False

    # Проверка α, β ∈ V*
    if alpha2 not in V_star:
        is_context_sensitive_type2 = False
    if beta2 not in V_star:
        is_context_sensitive_type2 = False

    # Проверка γ ∈ V+
    if y != "Epsilon":
        if y not in V_plus:
            is_context_sensitive_type2 = False

        else:
            ...
    else:
        is_context_sensitive_type2 = False


    # Проверка завершения вычислений и вывод результата
    if rule == G["P"][-1]:
        flag_print = False
        while not flag_print:
            if (is_context_sensitive_type2 or is_context_sensitive_type1):
                print("Тип грамматики: контекстно-зависимые ")
                if is_context_sensitive_type1:
                    print("Тип контекстно-зависимой грамматики: Такие грамматики относят к неукорачивающим")
                    flag_print = True

                else:
                    print("Тип контекстно-зависимой грамматики: Контекстно-зависимая")
                    flag_print = True

            if (is_context_free):
                print("Тип грамматики: контекстно-свободный")
                flag_print = True

            if (is_regular_type2 or is_regular_type1):
                print("Тип грамматики: регулярный:", end='')
                if is_regular_type1:
                    print("Тип регулярной грамматики: 1")
                    flag_print = True
                else:
                    print("Тип регулярной грамматики: 2")
                    flag_print = True

            if (flag_print == False):
                is_unrestricted == True
                print("Тип грамматики 0")
            exit()


# Классная работа
# G = {
#     "T": {'0', '1'},
#     "N": {'A', 'S'},
#     "P": ['S -> 0A1', '0A -> 00A1', 'A -> '],
#     "S": 'S'
# }
# Вариант 1
# G = {
#     "T": {'a', 'b', 'c'},
#     "N": {'A', 'B', 'C', 'S'},
#     "P": ['S -> aAbBcC', 'A -> aA', 'A -> ', 'B -> bB','B -> ', 'C -> cC', 'C -> '],
#     "S": 'S'
# }
#Вариант 10
# G = {
#     "T": {'0','1'},
#     "N": {'S', 'a'},
#     "P": ['S -> 0S1', 'S -> 1S0', 'S -> ', 'a -> 0a','a -> 1a', 'a -> '],
#     "S": 'S'
# }
# Пример из видео 2. Контекстно-свободная ОШИБКА
# G = {
#     "N": {'Q', 'S'},
#     "T": {'a', 'b', 'c'},
#     "P": ['S -> aQb', 'S -> accb', 'Q -> cSc'],
#     "S": 'S'
# }
# Пример из видео 3. Контекстно-зависимая ОШИБКА
# G = {
#     "N": {'S', 'B', 'C', },
#     "T": {'a', 'b', 'c'},
#     "P": ['S -> aSBC', 'S -> abc', 'bC -> bc', 'CB -> BC', 'cC -> cc', 'BB -> bb'],
#     "S": 'S'
# }
# Пример из видео 4. Тип грамматики 0
# G = {
#     "N": {'S', 'B', 'C', },
#     "T": {'a', '2', 'b'},
#     "P": ['S -> aaCFD', 'AD -> D', 'F -> AFB', 'F -> AB', 'Cb -> bC', 'AB -> bBA', 'CB -> C', 'Ab -> bA', 'bCD -> '],
#     "S": 'S'
# }
print("G = ", G)
result = check_grammar_class(G)
print(result)
