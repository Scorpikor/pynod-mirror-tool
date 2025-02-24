# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

def web_page_generator(data, only_table, file_path):
    
    html_table_content = f"""<div id="berta-nod32">\n\
    <table class="info_table" align="center" border="1">\n\
        <tr class="c_blue">\n\
            <th>Версия</th>\n\
            <th>Версия баз</th>\n\
            <th>Базы обновились</th>\n\
            <th>Последняя проверка</th>\n\
            <th>Файлов</th>\n\
            <th>Размер базы</th>\n\
        </tr>\n"""
    for a,b,c,d,e,f in data:
        if a =="" and b =="" and c == "" and d =="":
            html_table_content +=f"""\
        <tr class='c_back'>\n\
            <td colspan="4">\n\
            <td>{e}</td>\n\
            <td>{f}</td>\n\
        </tr>\n"""
        else:
            html_table_content +=f"""\
        <tr class='c_back'>\n\
            <td>{a}</td>\n\
            <td>{b}</td>\n\
            <td>{c}</td>\n\
            <td>{d}</td>\n\
            <td>{e}</td>\n\
            <td>{f}</td>\n\
        </tr>\n"""
                                        
            
    html_table_content += """\
    </table>\n\
    </div>\n"""
    if only_table == "1":
        html_content = html_table_content
    else:
        html_content = """<!DOCTYPE html>\n\
<html>\n\
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n\
<head>\n\
    <style>\n\
            body, html {\n\
                height: 100%;\n\
                margin: 0;\n\
                overflow:auto;\n\
                display: flex;\n\
                align-items: center;\n\
                justify-content: center;\n\
                font-family: Arial, helvetica;\n\
                font-weight: 400;\n\
                font-size: 10.56px;\n\
                background-color: #000000;\n\
                }\n\
            table {\n\
                color: #E6E6E6;\n\
                border-spacing: 0;\n\
                margin:3 auto;\n\
                }\n\
            td {\n\
                vertical-align:top;\n\
                padding: 3px 5px 3px 5px;\n\
                }\n\
            th {\n\
                vertical-align:top;\n\
                padding: 6px 5px 6px 5px;\n\
                }\n\
            .info_table {\n\
                vertical-align: 5px;\n\
                border: 3px solid #565759;\n\
                color: #E6E6E6;\n\
                text-indent: 0.5em;\n\
                }\n\
            .c_back {\n\
                background-color: #1C1C19;\n\
                }\n\
            .c_blue {\n\
                background-color: #0284ca;\n\
                color: #000;\n\
                }\n\
    </style>\n\
</head>\n\
<body>""" + html_table_content + """\
</body>\n\
</html>"""
                            
    
    file = open(file_path, "w")
    file.write(html_content)
    file.close()
    

