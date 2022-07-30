def add_comment_class(file):
    file_list = file.split("\n") # 先將原為 str 的 py 檔程式碼資料，以 \n 切割成每行並轉為 list
    for i in range(len(file_list)): # 走遍每行
        if "#" in file_list[i]: # 若此行有「#」註解
            comment_ind = file_list[i].find("#") # 儲存「#」的 index
            if file_list[i][comment_ind-1] != "\\": # 若非「\#」則開始更改，(因為\#為單純字元，非註解，故跳過)
                file_list[i] = f"{file_list[i][:comment_ind]}<span class='comment'>{file_list[i][comment_ind:]}</span>"
    file = "\n".join(file_list)
    # file = [file]
    file = divide_span(file)
    return file
def add_str_class(file):
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        LEN = len(file[i])
        quot_list = ["\"","\'"]
        dqi_list = [] # double quotation index list
        sqi_list = [] # single quotation index list
        for quot in quot_list:
            for j in range(LEN - 1, -1, -1):
                if file[i][j] == quot and file[i][j-1] != "\\":
                    if quot == "\"": dqi_list.append(j)
                    else: sqi_list.append(j)
        
        dqi_list = [[dqi_list[j], dqi_list[j+1], "\""] for j in range(0, len(dqi_list), 2)]
        sqi_list = [[sqi_list[j], sqi_list[j+1], "\'"] for j in range(0, len(sqi_list), 2)]
        
        for d in range(len(dqi_list)):
            for s in range(len(sqi_list)):
                compare = [dqi_list[d][0] , dqi_list[d][1], sqi_list[s][0], sqi_list[s][1]]
                if None not in compare:
                    if compare[1] < compare[3] < compare[2] < compare[0]:
                        sqi_list[s][0] = sqi_list[s][1] = None
                    elif compare[3] < compare[1] < compare[0] < compare[2]:
                        dqi_list[d][0] = dqi_list[d][1] = None

        for d in range(len(dqi_list)-1, -1, -1):
            if dqi_list[d][0] == None:
                del dqi_list[d]
        for s in range(len(sqi_list)-1, -1, -1):
            if sqi_list[s][0] == None:
                del sqi_list[s]

        qi_list = sorted(dqi_list + sqi_list)

        for j in range(len(qi_list)-1, -1, -1):
            file[i] = file[i][:qi_list[j][1]] + f"<span class='str'>" + file[i][qi_list[j][1]:qi_list[j][0]+1] + "</span>" + file[i][qi_list[j][0]+1:]

    file = divide_span(file)
    return file
def add_op_class(file):
    op_list = "=+-*/%&|^><!~,:"
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        LEN = len(file[i])
        for j in range(LEN - 1, -1, -1):
            if file[i][j] in op_list:
                file[i] = file[i][:j] + f"<span class='op'>{file[i][j]}</span>" + file[i][j + 1:]
    file = divide_span(file)
    return file
def add_method_class(file):
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        dot_ind_list = []
        # 處理.後的方法和屬性
        block = file[i][:]
        while "." in block:
            dot_ind = block.find(".")
            if not block[dot_ind+1].isdigit():
                dot_ind_list.append(dot_ind+1)
            block = block[dot_ind+1:]
        dot_ind_list = [sum(dot_ind_list[:j+1]) for j in range(len(dot_ind_list))][::-1]
        for d in dot_ind_list:
            j = 1
            while True:
                try:
                    tar = file[i][d+j]
                except IndexError:
                    break
                if not tar.isalpha() and tar!="_":
                    file[i] = file[i][:d] + f"<span class='func'>{file[i][d:d+j]}</span>" + file[i][d+j:]
                    break
                j += 1
        
    file = divide_span(file)
    return file
def add_class_and_def_class(file):
    for i in range(len(file)):
        if file[i].startswith("<span"): continue

        class_ind_list = []
        def_ind_list = []

        block = file[i][:]
        while "class" in block:
            class_ind = block.find("class")
            class_ind_list.append(class_ind+6)
            block = block[class_ind+6:]
        class_ind_list = [sum(class_ind_list[:j+1]) for j in range(len(class_ind_list))][::-1]
        for c in class_ind_list:
            j = 1
            while True:
                try:
                    tar = file[i][c+j]
                except IndexError:
                    break
                if not tar.isalpha() and tar!="_":
                    file[i] = file[i][:c] + f"<span class='func'>{file[i][c:c+j]}</span>" + file[i][c+j:]
                    break
                j += 1

        

        block = file[i][:]
        while "def" in block:
            def_ind = block.find("def")
            def_ind_list.append(def_ind+4)
            block = block[def_ind+4:]
        def_ind_list = [sum(def_ind_list[:j+1]) for j in range(len(def_ind_list))][::-1]
        for d in def_ind_list:
            j = 1
            while True:
                try:
                    tar = file[i][d+j]
                except IndexError:
                    break
                if not tar.isalpha() and tar!="_":
                    file[i] = file[i][:d] + f"<span class='func'>{file[i][d:d+j]}</span>" + file[i][d+j:]
                    break
                j += 1
        
    file = divide_span(file)
    return file
def add_func_class(file):
    func_list = ['staticmethod', 'classmethod', 'breakpoint', 'isinstance', 'issubclass', 'memoryview', 'bytearray', 'enumerate', 'frozenset', 'callable', 'property', 'reversed', 'compile', 'complex', 'delattr', 'getattr', 'globals', 'hasattr', 'setattr', 'divmod', 'filter', 'format', 'locals', 'object', 'sorted', 'aiter', 'anext', 'ascii', 'bytes', 'float', 'input', 'print', 'range', 'round', 'slice', 'super', 'tuple', 'bool', 'dict', 'eval', 'exec', 'hash', 'help', 'iter', 'list', 'next', 'open', 'repr', 'type', 'vars', 'abs', 'all', 'any', 'bin', 'chr', 'dir', 'hex', 'int', 'len', 'map', 'max', 'min', 'oct', 'ord', 'pow', 'set', 'str', 'sum', 'zip', 'id']
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        for func in func_list:
            for j in range(3):
                file[i] = file[i].replace(func + f"{' '*j}(", f"<span class='func'>{func}</span>{' '*j}(")
    file = divide_span(file)
    return file
def add_keyword_class(file):
    keyword_list1 = ["nonlocal", "global", "lambda", "class", "and", "def", "not", "is", "or", "@"]
    keyword_list2 = ["continue", "finally", "assert", "except", "import", "return", "except", "break", "raise", "while", "yield", "while", "elif", "else", "from", "pass", "with", "del", "for", "try", "as", "if", "in"]
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        fst_space = file[i].find(" ")
        if file[i][:fst_space] in keyword_list1:
            file[i] = f"<span class='keyword1'>{file[i][:fst_space]}</span>" + file[i][fst_space:]

        for keyword_list in [keyword_list1, keyword_list2]:
            for kw in keyword_list:
                if kw == "class": continue
                sign = ["\n", " "]
                for a in range(2):
                    for b in range(2):
                        if keyword_list == keyword_list1:
                            file[i] = file[i].replace(f"{sign[a]}{kw}{sign[b]}", f"{sign[a]}<span class='keyword1'>{kw}</span>{sign[b]}")
                        else:
                            file[i] = file[i].replace(f"{sign[a]}{kw}{sign[b]}", f"{sign[a]}<span class='keyword2'>{kw}</span>{sign[b]}")

        file[i] = file[i].replace("class ",f"<span class='keyword1'>class</span> ")
        # file[i] = file[i].replace("self",f"<span class='keyword2'>self</span>")
        file[i] = file[i].replace("else:", f"<span class='keyword2'>else</span>:")
        for j in ['False', 'True', 'None']:
            file[i] = file[i].replace(j, f"<span class='keyword1'>{j}</span>")
    file = divide_span(file)
    return file
def add_brackets_class(file):
    brackets_list = ["(", ")", "[", "]", "{", "}"]
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        for b in brackets_list:
            file[i] = file[i].replace(b, f"<span class='brackets'>{b}</span>")
    file = divide_span(file)
    return file
def change_start_space(file):
    file = "".join(file)
    file_list = file.split("\n")
    for i in range(len(file_list)):
        end = 0
        if file_list[i] == "" or set(file_list[i])=={" "}: continue # 若遇到 完全沒字""的行(長度為0) 或是 全為空格" "的行 就跳過
        while file_list[i][end] == " ":
            end += 1
            
        file_list[i] = "&nbsp"*end + file_list[i][end:]
    # file = "\n".join(file_list)
    return file_list[1:-1]
def divide_span(file):
    ori_file = file[:]
    if type(file)==str:
        file_list = []
        while True:
            if "<span" not in file:
                file_list.append(file)
                break

            start = file.find("<span")
            end = file.find("</span>")
            file_list.append(file[:start])
            file_list.append(file[start:end+7])
            file = file[end+7:]

        return file_list

    elif type(file)==list:
        new_file_list = []
        while file!=[]:
            while True:
                if "<span" not in file[0]:
                    new_file_list.append(file.pop(0))
                    break

                start = file[0].find("<span")
                end = file[0].find("</span>")
                new_file_list.append(file[0][:start])
                new_file_list.append(file[0][start:end+7])
                file[0] = file[0][end+7:]

        for i in range(len(new_file_list)-1, -1, -1):
            if new_file_list[i] == "":
                del new_file_list[i]

        return new_file_list
def to_html(file):
    HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {font-family: consolas;background-color: #37464a;color:black}
            table {border-collapse: collapse;color: #9acdedf8;background-color:#1a1b1c;width: 100%}
            .table_num {text-align: right;width: 40px;color: grey}
            .keyword1 {color: #2c7fd3}
            .keyword2 {color: #DA70D6}
            .op {color: white}
            .func {color: #d5d091}
            .str {color: #ef8652}
            .comment {color:#67a661}
            .brackets {color:gold}
        </style>
    </head>
    <body>
    """
    HTML += "<table>"
    for i in range(len(file)):
        HTML += "<tr>"
        HTML += f"<td class='table_num'>{i+1}</td>"
        HTML += f"<td width='10px'></td>"
        HTML += f"<td>{file[i]}</td>"
        HTML += "</tr>"
    HTML += "</table></body></html>"

    return HTML

with open("snake.py", "r", encoding="utf-8") as f:
    html = "\n"
    for line in f:
        html += line
    html += "\n"

html = add_comment_class(html)
html = add_str_class(html)
html = add_method_class(html)
html = add_class_and_def_class(html)
html = add_func_class(html)
html = add_keyword_class(html)
html = add_op_class(html)
html = add_brackets_class(html)
html = change_start_space(html)
html = to_html(html)
with open("out.html", "w", encoding="utf-8") as f:
    f.write(html)
