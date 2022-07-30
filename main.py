def divide_span(file): # 將 py 檔以 <span></span> 為基準分割
    new_file_list = []
    while file!=[]: # 重複執行到全部切分完
        while True:
            if "<span" not in file[0]: # 若此區塊無 <span (或已切分完)則直接 pop 到 new_file_list
                new_file_list.append(file.pop(0))
                break
            start = file[0].find("<span") # 抓取最前面的 <span
            end = file[0].find("</span>") # 抓取最前面的 </span>
            new_file_list.append(file[0][:start]) # 將 <span 前的區塊切分進 new_file_list
            new_file_list.append(file[0][start:end+7]) # 將 <span></span> 切分進 new_file_list
            file[0] = file[0][end+7:] # 將以上處理完的區塊刪除，往下輪 while 處理
    # 刪除切分多餘的空元素
    for i in range(len(new_file_list)-1, -1, -1):
        if new_file_list[i] == "":
            del new_file_list[i]
    return new_file_list
def add_comment_class(file): # 處理註解區塊
    file_list = file.split("\n") # 先將原為 str 的 py 檔程式碼資料，以 \n 切割成每行並轉為 list
    for i in range(len(file_list)): # 走遍每行
        if "#" in file_list[i]: # 若此行有「#」註解
            comment_ind = file_list[i].find("#") # 儲存「#」的 index
            if file_list[i][comment_ind-1] != "\\": # 若非「\#」則開始更改，(因為\#為單純字元，非註解，故跳過)
                file_list[i] = f"{file_list[i][:comment_ind]}<span class='comment'>{file_list[i][comment_ind:]}</span>"
    file = "\n".join(file_list) # 以 \n 組合回 str
    file = [file] # 將 file 型別從 str 改成 [str]，以便做 divide_span() 處理
    file = divide_span(file) # 以 span 切分
    return file
def add_str_class(file): # 處理字串區塊
    quot_list = ["\"","\'"]
    for i in range(len(file)):
        if file[i].startswith("<span"): continue # 若該區塊以"<span"開頭，說明此區塊已有標籤，故跳過
        LEN = len(file[i]) # 儲存此區塊的 str 長度
        dqi_list = list() # double quotation index list (記錄雙引號位置)
        sqi_list = list() # single quotation index list (記錄單引號位置)
        # 紀錄引號位置
        for quot in quot_list:
            for j in range(LEN - 1, -1, -1): # 反向讀取此區塊
                if file[i][j] == quot and file[i][j-1] != "\\": # 跳過「\'」、「\"」字元
                    if quot == "\"": dqi_list.append(j) # 紀錄雙引號位置
                    else: sqi_list.append(j) # 紀錄單引號位置
        # 因引號為兩兩一組出現，故把 list 分割為兩兩一組
        # (因註解與「\'」、「\"」已處理完，在程式碼無 SyntaxError 前提下，可直接分兩兩一組)
        dqi_list = [[dqi_list[j], dqi_list[j+1]] for j in range(0, len(dqi_list), 2)]
        sqi_list = [[sqi_list[j], sqi_list[j+1]] for j in range(0, len(sqi_list), 2)]
        # 若某單引號包裹著雙引號，或者反之，則必須把被包裹的引號對刪除，只保留外部的引號對
        for d in range(len(dqi_list)):
            for s in range(len(sqi_list)):
                compare = [dqi_list[d][0] , dqi_list[d][1], sqi_list[s][0], sqi_list[s][1]]
                # 若某對引號被包裹，則此區塊會將它們的值改為 [None, None]
                # 若無兩對比較引號皆不為 None，且無互相包裹情況，則不做任何處理
                if None not in compare: 
                    if compare[1] < compare[3] < compare[2] < compare[0]:
                        sqi_list[s][0] = sqi_list[s][1] = None
                    elif compare[3] < compare[1] < compare[0] < compare[2]:
                        dqi_list[d][0] = dqi_list[d][1] = None
        # 將為 [None, None] 的引號對刪除
        # (因屬於 for 迴圈，要走訪並刪除就必須反向讀取，避免 IndexError)
        for d in range(len(dqi_list)-1, -1, -1):
            if dqi_list[d][0] == None:
                del dqi_list[d]
        for s in range(len(sqi_list)-1, -1, -1):
            if sqi_list[s][0] == None:
                del sqi_list[s]
        qi_list = sorted(dqi_list + sqi_list) # 將兩組引號對位置合併並排序
        # 反向讀取並開始更改為span
        for j in range(len(qi_list)-1, -1, -1):
            file[i] = file[i][:qi_list[j][1]] + f"<span class='str'>" + file[i][qi_list[j][1]:qi_list[j][0]+1] + "</span>" + file[i][qi_list[j][0]+1:]
    file = divide_span(file) # 以 span 切分
    return file
def add_type_class(file): # 處理型別區塊
    type_list = ["type", "int", "float", "str", "tuple", "list", "dict", "set", "bool"]
    for i in range(len(file)):
        if file[i].startswith("<span"): continue # 若該區塊以"<span"開頭，說明此區塊已有標籤，故跳過
        for md in type_list:
            sign = ["\n", " ", ",", "(", ")", "[", "]", "{", "}"]
            for a in range(len(sign)):
                for b in range(len(sign)):
                    file[i] = file[i].replace(f"{sign[a]}{md}{sign[b]}", f"{sign[a]}<span class='module'>{md}</span>{sign[b]}")

    file = divide_span(file)
    return file
def add_module_class(file): # 處理模組區塊
    
    file_copy = "".join(file)
    file_copy = file_copy.split("\n")
    file_copy = [line for line in file_copy if "import" in line]
    file_copy = [item for line in file_copy for item in line.split()]

    for i in range(len(file_copy)-1, -1, -1):
        if "." in file_copy[i]:
            file_copy.extend(file_copy[i].split("."))
            del file_copy[i]

    module_list = list()
    for f in file_copy:
        m = ""
        for s in f:
            if s.isalpha() or s.isdigit() or s == "_": m += s
        module_list.append(m)
    module_list = [m for m in list(set(module_list)) if m not in ["import", "from", "as", "*", ""]]

    for i in range(len(file)):
        if file[i].startswith("<span"): continue # 若該區塊以"<span"開頭，說明此區塊已有標籤，故跳過
        for md in module_list:
            sign = ["\n", " ", ".", ",", "(", ")"]
            for a in range(len(sign)):
                for b in range(len(sign)):
                    file[i] = file[i].replace(f"{sign[a]}{md}{sign[b]}", f"{sign[a]}<span class='module'>{md}</span>{sign[b]}")

    file = divide_span(file)
    return file
def add_method_class(file): # 處理方法區塊(以.開頭)
    for i in range(len(file)):
        if file[i].startswith("<span"): continue # 若該區塊以"<span"開頭，說明此區塊已有標籤，故跳過
        dot_ind_list = []
        # 處理.後的方法和屬性
        block = file[i][:]
        while "." in block:
            dot_ind = block.find(".")
            try:
                if not block[dot_ind+1].isdigit():
                    dot_ind_list.append(dot_ind+1)
            except IndexError:
                break
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
def add_class_and_def_class(file): # 處理 class 和 def 後的區塊
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
                    file[i] = file[i][:c] + f"<span class='module'>{file[i][c:c+j]}</span>" + file[i][c+j:]
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
                if not tar.isalpha() and tar.isdigit() and tar!="_":
                    file[i] = file[i][:d] + f"<span class='func'>{file[i][d:d+j]}</span>" + file[i][d+j:]
                    break
                j += 1
        
    file = divide_span(file)
    return file
def add_func_class(file): # 處理 python 內建函式區塊
    func_list = ['staticmethod', 'classmethod', 'breakpoint', 'isinstance', 'issubclass', 'memoryview', 'bytearray', 'enumerate', 'frozenset', 'callable', 'property', 'reversed', 'compile', 'complex', 'delattr', 'getattr', 'globals', 'hasattr', 'setattr', 'divmod', 'filter', 'format', 'locals', 'object', 'sorted', 'aiter', 'anext', 'ascii', 'bytes', 'input', 'print', 'range', 'round', 'slice', 'super', 'eval', 'exec', 'hash', 'help', 'iter', 'next', 'open', 'repr', 'vars', 'abs', 'all', 'any', 'bin', 'chr', 'dir', 'hex', 'len', 'map', 'max', 'min', 'oct', 'ord', 'pow', 'sum', 'zip', 'id']
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        for func in func_list:
            for j in range(3):
                file[i] = file[i].replace(func + f"{' '*j}(", f"<span class='func'>{func}</span>{' '*j}(")
    file = divide_span(file)
    return file
def add_keyword_class(file): # 處理 python 關鍵字(2種顏色)
    keyword_list1 = ["nonlocal", "global", "lambda", "class", "and", "def", "not", "is", "or", "@"]
    keyword_list2 = ["continue", "finally", "assert", "except", "import", "return", "except", "break", "raise", "while", "yield", "while", "elif", "else", "from", "pass", "with", "del", "for", "try", "as", "if", "in"]
    for i in range(len(file)):
        if file[i].startswith("<span"): continue
        for keyword_list in [keyword_list1, keyword_list2]:
            for kw in keyword_list:
                sign = ["\n", " ", ":"]
                for a in range(len(sign)):
                    for b in range(len(sign)):
                        if keyword_list == keyword_list1:
                            file[i] = file[i].replace(f"{sign[a]}{kw}{sign[b]}", f"{sign[a]}<span class='keyword1'>{kw}</span>{sign[b]}")
                        else:
                            file[i] = file[i].replace(f"{sign[a]}{kw}{sign[b]}", f"{sign[a]}<span class='keyword2'>{kw}</span>{sign[b]}")
        # file[i] = file[i].replace("class ",f"<span class='keyword1'>class</span> ")
        # file[i] = file[i].replace("self",f"<span class='keyword2'>self</span>")
        # file[i] = file[i].replace("else:", f"<span class='keyword2'>else</span>:")
        for j in ['False', 'True', 'None']:
            file[i] = file[i].replace(j, f"<span class='keyword1'>{j}</span>")
    file = divide_span(file)
    return file
def add_op_class(file): # 處理運算符號區塊
    op_list = "=+-*/%&|^><!~,:"
    for i in range(len(file)):
        if file[i].startswith("<span"): continue # 若該區塊以"<span"開頭，說明此區塊已有標籤，故跳過
        LEN = len(file[i])
        for j in range(LEN - 1, -1, -1): # 因<>會與<span>標籤衝突，故需使用反向讀取並更改才不會有錯誤
            if file[i][j] in op_list: # 更改所有的運算符號
                file[i] = file[i][:j] + f"<span class='op'>{file[i][j]}</span>" + file[i][j + 1:]
    file = divide_span(file) # 以 span 切分
    return file
def add_brackets_class(file): # 處理括號區塊
    brackets_list = ["(", ")", "[", "]", "{", "}"]
    for i in range(len(file)):
        if file[i].startswith("<span"): continue # 若該區塊以"<span"開頭，說明此區塊已有標籤，故跳過
        for b in brackets_list: # 更改所有的括號
            file[i] = file[i].replace(b, f"<span class='brackets'>{b}</span>")
    file = divide_span(file) # 以 span 切分
    return file
def change_start_space(file): # 將空白開頭的行轉換為 html 格式
    file = "".join(file) # 將切分好的 html list 合併成 str
    file_list = file.split("\n") # 再以 \n 切分為 list
    for i in range(len(file_list)):
        space = 0
        # 若遇到「完全沒字""的行(長度為0)」或「全為空格" "」的行就跳過
        if file_list[i] == "" or set(file_list[i])=={" "}: continue
        # 計算此行開頭有幾個空格，若無空格亦不影響後續
        while file_list[i][space] == " ": space += 1
        # 將開頭為空格的行，開頭空格以 &nbsp 代替(html空格開頭要求格式)
        file_list[i] = "&nbsp"*space + file_list[i][space:]
    return file_list[1:-1] # 因讀取檔案時在檔案頭尾都有加 \n 方便處理，故現在要刪掉頭尾的 \n
def to_html(file): # 轉為 HTML
    HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {font-family: consolas;background-color: #37464a;color:black}
            .code {border-collapse: collapse;color: #9acdedf8;background-color:#1a1b1c;width: 100%}
            .table_num {text-align: right;width: 40px;color: grey}
            .keyword1 {color: #2c7fd3}
            .keyword2 {color: #DA70D6}
            .op {color: white}
            .func {color: #d5d091}
            .str {color: #ef8652}
            .comment {color:#67a661}
            .brackets {color:gold}
            .module {color:turquoise}
        </style>
    </head>
    <body>
    """
    HTML += "<table class='code'>"
    for i in range(len(file)):
        HTML += "<tr>"
        HTML += f"<td class='table_num'>{i+1}</td>"
        HTML += f"<td width='10px'></td>"
        HTML += f"<td>{file[i]}</td>"
        HTML += "</tr>"
    HTML += "</table></body></html>"

    return HTML
def main(in_file, out_file):
    with open(in_file, "r", encoding="utf-8") as f:
        html = "\n"
        for line in f:
            html += line
        html += "\n"
    html = add_comment_class(html)
    html = add_str_class(html)
    html = add_module_class(html)
    html = add_type_class(html)
    html = add_method_class(html)
    html = add_class_and_def_class(html)
    html = add_func_class(html)
    html = add_keyword_class(html)
    html = add_op_class(html)
    html = add_brackets_class(html)
    html = change_start_space(html)
    html = to_html(html)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)

main("in.py", "out.html")
