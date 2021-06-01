from testmodel import connection
import numpy as np


def pyshine_process(age, gender, emotion):
    # while True:
    # tmp = get_value()
    # tmp = open_webcam()
    # with open('data.json','r') as f:
    #     json_read = json.load(f)
    # json_read = json_read[-1]
    # age = json_read['Age']
    # gender = json_read['Gender']
    # emotion = json_read['Emotion']
    print("Age: ", age)
    # for i in range(3):
    #     if i == 0:
    #         age = next(tmp)
    #     elif i == 1:
    #         gender = next(tmp)
    #     elif i == 2:
    #         emotion = next(tmp)
    # print("Age: ",age)
    # print("Gender: ",gender)
    # print("Emotion: ",emotion)

    list_movies = []
    c = connection()
    cursor = c.cursor()
    # print("Age: ",label_age_glob)
    age_mark = '0-12'
    if age_mark == 'Above 18':
        # if label_gender == 'Male':
        # age_mark
        cursor.execute(f"""select ads_path from movies where ads_age_from = '{age_mark}' 
                        order by ads_status desc
                        """)

        items = cursor.fetchall()
        # list_movies = items
        list_movies = items
        # age_mark = '16-17'

    # elif age_mark == '16-17':
    #     cursor.execute("""select ads_path from movies where ads_age_from = 'C16'
    #                     order by ads_status desc
    #                     """)
    #     items = cursor.fetchall()
    #     list_movies = items
    #
    #
    # elif age_mark == '13-15':
    #     cursor.execute("select ads_path from movies where ads_age_from = 'C13'")
    #     items = cursor.fetchall()
    #     list_movies = items
    #
    #
    # elif age_mark == '0-12':
    #     cursor.execute("select ads_path from movies where ads_age_from = 'P'")
    #     items = cursor.fetchall()
    #     list_movies = items
    #
    else:
        cursor.execute("select ads_path from movies order by ads_status desc, ads_id desc")
        items = cursor.fetchall()
        list_movies = items

    list_new = []
    # items = list(items)
    for item in items:
        item = list(item)
        tmp = item[0].split('/')
        list_new.append(tmp[-1])
    print('age_mark: ', age_mark)
    # list_movies = select(path)
    list_new = np.array(list_new)
    list_new = list_new.flatten()
    list_new = list(list_new)
    c.commit()
    # close connection
    c.close()

    return list_new
