import re

def convert_sql_to_python():
    with open('../insert_pizzas.sql', 'r', encoding='utf-8') as sql_file:
        sql_content = sql_file.read()
    
    # Extraer los valores usando expresiones regulares
    pattern = r"\('([^']*)', '([^']*)', '([^']*)', ([0-9.]*), ([^)]*)\)"
    matches = re.findall(pattern, sql_content)
    
    with open('pizzas_data.py', 'w', encoding='utf-8') as py_file:
        py_file.write("pizzas_data = [\n")
        for match in matches:
            name, description, size, price, _ = match
            py_file.write(f"    {{'name': '{name}', 'description': '{description}', "
                         f"'size': '{size}', 'price': {price}}},\n")
        py_file.write("]\n")

if __name__ == '__main__':
    convert_sql_to_python()
