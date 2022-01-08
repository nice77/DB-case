from openpyxl import load_workbook
import sqlite3
import os
from pl_to_ru import pl_to_ru
from de_to_ru import de_to_ru
from cleaner import cleaner
from gc import collect


def func(way_to_file, way_to_save, object_o, file_name='results_database'):

    # loading excel file
    print(way_to_file, way_to_save)
    print('loading excel...')
    object_o.create.setText('loading excel...')
    rows = load_workbook(way_to_file).active.rows
    header = next(rows)

    # loading sql-database
    object_o.create.setText('loading db...')
    print('loading db...')

    count = 0
    total_way = way_to_save + '\\' + file_name
    while os.path.isfile(total_way + '.db'):
        count += 1
        total_way += str(count)
    del count

    # creating first table
    file_sql = sqlite3.connect(total_way + '.db')
    cur = file_sql.cursor()
    que = f'''CREATE TABLE Companies('''
    for i in header:
        que += f'{i.value} TINYTEXT,'
    que += 'ID int NOT NULL PRIMARY KEY)'
    que = que[:-1] + ')'
    cur.execute(que)

    # writing in sql-db all the values
    print('Processing...')
    for i, val in enumerate(rows):
        row = ', '.join(tuple(map(lambda x: '"' + str(x.value).replace('"', '\'') + '"', val)))
        row += f', {i}'
        que = f"""INSERT INTO Companies VALUES ({row})"""
        cur.execute(que)
        print(i)
    del rows

    # creating second table
    parents = set(cur.execute('''SELECT owner_title, owner_link FROM Companies''').fetchall())
    cur.execute('''CREATE TABLE Owners(owner_id int NOT NULL PRIMARY KEY, 
                owner_name TINYTEXT, owner_link TINYTEXT)''')
    for i, val in enumerate(parents):
        cur.execute(f'''INSERT INTO Owners
                    VALUES({i}, "{val[0]}", "{val[1]}")''')
    cur.execute(f'''UPDATE Companies
                SET owner_id = other.id
                FROM (SELECT owner_id as id, owner_name as name FROM Owners) as other
                WHERE Companies.owner_title = other.name''')
    cur.execute(f'''ALTER TABLE Companies DROP COLUMN owner_title''')
    cur.execute(f'''ALTER TABLE Companies DROP COLUMN owner_link''')
    file_sql.commit()

    # clearing the companies' names
    print('Change names')
    names = cur.execute('SELECT name FROM Companies').fetchall()
    for i, elem in enumerate(names):
        cur.execute(f'''UPDATE Companies
                    SET name = "{cleaner(elem[0])}"
                    WHERE ID = {i}''')
        print(i)

    # creating new column with name transliterations
    cur.execute(f'''ALTER TABLE Companies
                    ADD russian_transcription TINYTEXT''')
    file_sql.commit()
    pl = cur.execute('''SELECT name, ID FROM Companies WHERE country = "Poland" OR country LIKE "%Poland"''').fetchall()
    pl_tr = tuple(map(lambda x: (x[0].split(), x[1]), pl))
    pl_tr = tuple(map(lambda x: [' '.join(tuple(map(lambda y: pl_to_ru(y), x[0]))), x[1]], pl_tr))
    pl_tr = tuple(map(lambda x: [f'"{x[0]}"', x[1]], pl_tr))
    for i in pl_tr:
        cur.execute(f'''UPDATE Companies
                        SET russian_transcription = {i[0]}
                        WHERE country = "Poland" AND ID = {i[1]} ''')
    del pl
    del pl_tr
    print('PL done')
    collect()
    try:
        de = cur.execute('''SELECT name, ID FROM Companies WHERE country = "Germany" OR country LIKE "%Germany"''').fetchall()
        de_tr = tuple(map(lambda x: (x[0].split(), x[1]), de))
        de_tr = tuple(map(lambda x: [' '.join(tuple(map(lambda y: de_to_ru(y), x[0]))), x[1]], de_tr))
        de_tr = tuple(map(lambda x: [f'"{x[0]}"', x[1]], de_tr))
        for i in de_tr:
            cur.execute(f'''UPDATE Companies
                            SET russian_transcription = {i[0]}
                            WHERE country = "Germany" AND ID = {i[1]}''')
    except BaseException as e:
        print(e)

    del de
    del de_tr
    print('DE done')
    collect()

    file_sql.commit()
    file_sql.close()
    print('Ended')
    object_o.create.setText('Create the .db-file')
