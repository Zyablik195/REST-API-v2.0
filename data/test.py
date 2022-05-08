from requests import get, post, delete, put

print(get('http://localhost:5000/api/v2/jobs').json())

print(get('http://localhost:5000/api/v2/jobs/1').json())

print(get('http://localhost:5000/api/v2/jobs/999').json())


# нет json
print(post('http://localhost:5000/api/v2/jobs').json())

# нехватка аргументов
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 1}).json())


# неверный аргумент
print(post('http://localhost:5000/api/v2/jobs',
           json={'id': 1, 'name': 'baba', 'surname': 'boy', 'age': 15, 'position': '4543543', 'speciality': '432432', 'address': 'module_2', 'city_from': 'New-York', 'email': 'fls[fls@akpe.ru', 'hashed_password': '1234'}).json())

# всё верно
print(post('http://localhost:5000/api/v2/jobs',
           json={'id': 5, 'team_leader': 1, 'job': 'test', 'work_size': 15, 'collaborators': '3, 4', 'hazard': 2, 'is_finished': False}).json())

# проверка добавки
print(get('http://localhost:5000/api/v2/jobs').json())

print(delete('http://localhost:5000/api/v2/jobs/999').json())

print(delete('http://localhost:5000/api/v2/jobs/5').json())

print(get('http://localhost:5000/api/v2/jobs').json())