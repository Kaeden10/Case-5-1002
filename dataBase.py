# Андрей
import sqlite3
import remote


class City:
    def __init__(self, id, name, area_count, house_count, apartment_count):
        self.id = id
        self.name = name
        self.area_count = area_count
        self.house_count = house_count
        self.apartment_count = apartment_count


cursor = None
conn = None


def connect():
    global cursor, conn
    conn = sqlite3.connect("temp_data_full.db")
    cursor = conn.cursor()


def clearDtBs():
    cursor.execute('DELETE FROM APARTMENTS')
    cursor.execute('DELETE FROM HOUSES')
    cursor.execute('DELETE FROM CITIES')

    conn.commit()


def clearDtBs_temperature():
    cursor.execute('DELETE FROM APARTMENT_TEMPERATURE')
    cursor.execute('DELETE FROM CITIES_TEMPERATURE')


def add_city(city_id, city):
    # name, area_count, house_count, apartment_count
    cursor.execute('INSERT INTO CITIES VALUES (?,?,?,?,?)', (city_id,
                                                             city['city_name'], city['area_count'],
                                                             city['house_count'], city['apartment_count']))
    conn.commit()


def add_house(city_id, area_id, house):
    cursor.execute('''INSERT INTO HOUSES (city_id, area_id, house_number, apartment_count) 
                                   VALUES (?,?,?,?)''',
                                   (city_id, area_id, house['house_id'],
                                   house['apartment_count']))
    conn.commit()


def add_apartment(apartment_number, house):
    cursor.execute('''INSERT INTO APARTMENTS (apartment_number, house_id) 
                                        VALUES (?,?)''',
                   (apartment_number, house['house_id']))


def get_cities():
    return list(map(lambda x: City(x[0], x[1], x[2], x[3], x[4]),
                    cursor.execute("SELECT * FROM CITIES").fetchall()))


def get_houses():
    return list(cursor.execute('SELECT * from HOUSES'))


def add_apartments_city(city_id):
    for house in cursor.execute('SELECT * FROM HOUSES WHERE city_id=?', (city_id, )).fetchall():
        house_id, apartment_count = house[0], house[-1]
        for apartment_number in range(1, apartment_count + 1):
            cursor.execute('''INSERT INTO APARTMENTS (apartment_number, house_id) VALUES (?,?)''',
            (apartment_number, house_id))
    conn.commit()
    

def add_apartments():
    for house in get_houses():
        apartment_count, house_id = house[-1], house[0]
        for apartment_number in range(1, apartment_count + 1):
            cursor.execute('''INSERT INTO APARTMENTS (apartment_number, house_id) 
                                                    VALUES (?,?)''',
                           (apartment_number, house_id))
    conn.commit()


def get_cities():
    return list(map(lambda x: City(x[0], x[1], x[2], x[3], x[4]),
                    cursor.execute("SELECT * FROM CITIES").fetchall()))


def get_city(id) -> City:
    result = cursor.execute("SELECT * FROM CITIES WHERE id=?", (id, )).fetchone()
    return City(result[0], result[1], result[2], result[3], result[4])


def get_temperature_City_year():
    cursor.execute('SELECT APARTMENTS (apartment_number, house_id')


def get_names_citys():
    return [i[0] for i in cursor.execute('SELECT name FROM CITIES')]


def get_houses_city(city_id):
    return cursor.execute('SELECT * FROM HOUSES WHERE city_id=?', (city_id, )).fetchall()


def get_id_apartment(house_id, apartment_number):
    return cursor.execute('''SELECT a.id FROM APARTMENTS a INNER JOIN HOUSES h ON a.house_id = h.id
    WHERE h.id=? and a.apartment_number=?''', (house_id, apartment_number)).fetchone()[0]


def get_apartments_number1():
    return cursor.execute('''SELECT ct.id, h.area_id, h.house_number, a.apartment_number, a.id
    FROM APARTMENTS a INNER JOIN HOUSES h ON a.house_id = h.id INNER JOIN CITIES ct on ct.id = h.city_id
    WHERE h.area_id=? AND h.house_number=? AND a.apartment_number=? 
    ''', (1, 1, 1)).fetchall()


def add_temperature_city(time_id, city_id, temp):
    cursor.execute('INSERT INTO CITIES_TEMPERATURE (city_id, time_id, temperature) VALUES (?, ?, ?)',
                        (city_id, time_id, float(temp)))


def add_temperature_apartments(time_id, apartments, house_id):
    for apt in apartments:
        cursor.execute('INSERT INTO APARTMENT_TEMPERATURE (apartment_id, time_id, temperature) VALUES (?, ?, ?)',
                       (get_id_apartment(house_id, apt['apartment_id']), time_id, float(apt['temperature'])))
    conn.commit()


def add_temperature_citys_oneApp(apartment_id, time_id, temperature):
    cursor.execute('INSERT INTO APARTMENT_TEMPERATURE (apartment_id, time_id, temperature) VALUES (?, ?, ?)',
                   (apartment_id, time_id, float(temperature)))
    conn.commit()


def get_city_id(cityName):
    return cursor.execute('SELECT * FROM CITIES WHERE name=?', (cityName, )).fetchone()[0]


def get_city_area_count(city_id):
    return cursor.execute('SELECT area_count FROM CITIES WHERE id=?', (city_id, )).fetchone()[0]


def get_area_house_count(city_id, area_id):
    return cursor.execute('SELECT house_number FROM HOUSES WHERE city_id=? and area_id=?',
                          (city_id, area_id, )).fetchall()[-1][0]


def get_house_apartment_count(city_id, area_id, house_id):
    return cursor.execute('SELECT apartment_count FROM HOUSES WHERE city_\
id=? and area_id=? and house_number=?',
                          (city_id, area_id, house_id, )).fetchone()[0]


def get_cities_temperature_half_year(city_id):
    return cursor.execute('SELECT temperature FROM CITIES_TEMPERATURE WHERE time_id <= 180 and city_id=?', (city_id, )).fetchall()


def get_apartments_temperature_from_one_city(city_id):
    return cursor.execute('SELECT a.apartment_number, at.temperature FROM HOUSES \
h INNER JOIN APARTMENTS a on h.id = a.house_id INNER JOIN APARTMENT_TEMPERATURE at \
on a.id = at.apartment_id WHERE h.city_id=?', (city_id, )).fetchall()


def get_apartments_temperature_from_all_cities():
    apartments = [1, 14965, 60673, 107037, 121301, 137325, 148889, 159857, 167757, 180133,
                  189665,
                  197341,
                  241681,
                  252465,
                  265353]
    temp = list()
    for apartment_id in apartments:
        temp.append(cursor.execute('''SELECT c.name, at.temperature
                                          FROM CITIES c INNER JOIN HOUSES h ON c.id = h.city_id
                                          INNER JOIN APARTMENTS a on h.id = a.house_id
                                          INNER JOIN APARTMENT_TEMPERATURE at ON a.id = at.apartment_id
                                          WHERE at.apartment_id=?
                                          ORDER BY time_id''', (apartment_id,)).fetchall())
    return temp


def get_average_temperature(city_id):
    return list(map(lambda x: x[0], cursor.execute('''SELECT AVG(at.temperature) as AVERAGE FROM HOUSES h
                      INNER JOIN APARTMENTS a on h.id = a.house_id 
                      INNER JOIN APARTMENT_TEMPERATURE at on a.id = at.apartment_id
                      WHERE city_id=?
                      GROUP BY at.time_id''', (city_id, )).fetchall()))


def get_max_temperatures_from_areas(city_id):
    temp = list()
    for i in range(1, 5):
        temp.append(cursor.execute('''SELECT MAX(at.temperature) as MAX FROM HOUSES h
                             INNER JOIN APARTMENTS a on h.id = a.house_id
                             INNER JOIN APARTMENT_TEMPERATURE at ON a.id = at.apartment_id
                             WHERE city_id=? and area_id=?''', (city_id, i)).fetchone())
    return [i[0] for i in temp]


def help():
    return cursor.execute('''SELECT h.city_id, h.area_id, h.house_number, a.apartment_number, at.time_id
    FROM APARTMENT_TEMPERATURE at INNER JOIN APARTMENTS a on at.apartment_id=a.id INNER JOIN
    HOUSES h on a.house_id=h.id''').fetchall()
