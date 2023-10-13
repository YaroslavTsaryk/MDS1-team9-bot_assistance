from  datetime import datetime, timedelta

users=[{"name": "Bill Gates", "birthday": datetime(1955, 10, 10)},
       {"name": "Mr Anderson", "birthday": datetime(1977, 10, 15)},
       {"name": "Morfeus", "birthday": datetime(1985, 10, 18)},
       {"name": "Neo", "birthday": datetime(1993, 10, 12)},
       {"name": "Trinity", "birthday": datetime(1966, 10, 7)},
       {"name": "Oraculus", "birthday": datetime(2000, 10, 14)},
       {"name": "Serafim", "birthday": datetime(2005, 10, 10)},
       {"name": "Architect", "birthday": datetime(1965, 10, 18)},
       {"name": "Agent Smith", "birthday": datetime(1953, 10, 12)}]
       
def get_birthdays_per_week(users,today=datetime.today().date()):
    res={}
    days={0:'Monday',
          1:'Tuesday',
          2:'Wednesday',
          3:'Thursday',
          4:'Friday'}
    
    #today=datetime.today().date() 
    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()  # Конвертуємо до типу date*
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year+1)
        delta_days = (birthday_this_year - today).days
        if delta_days<7:    
            set_day=0
            if birthday_this_year.weekday()>4:
                set_day=0
            else:
                set_day=birthday_this_year.weekday()
            if days[set_day] not in res.keys():
                res[days[set_day]]=[user["name"]]
            else:
                res[days[set_day]].append(user["name"])
       
    res2={}
    for i in range(7):
        sh=(today+timedelta(i)).weekday()
        if sh not in [5,6]:
            if days[sh] in res.keys():
                res2[days[sh]]=res[days[sh]]
                message=", ".join(res[days[sh]])
                print(f'{days[sh]}: {message}')
                
    return res2
            
#today=(datetime.today()-timedelta(1)).date() # set different date for testing 
today=datetime.today().date()
print(get_birthdays_per_week(users,today))
              