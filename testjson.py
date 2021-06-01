import json

data = [{'Gender':'Female', 'Age': 'Above 18', 'Emotion': 'Happy'},]
data1 = {'a':1,'b':2,'c':3}

# with open('data.json', 'w') as f:
#     json.dump(data,f)

# with open('data.json','r') as f:
#     json_read = json.load(f)
#
# json_read.update(data)

# with open('data.json', 'a') as f:
#     json.dump(data,f)
a_new = {'d':4}
with open('data.json', 'r+') as f:
    json_read = json.load(f)
    # json_read.update(a_new)
    # f.seek(0)
    # json.dump(json_read, f)

    # for i in json_read:
    #     del i['a']
# print(list(json_read.keys())[-1])
# for i in json_read:
    # del i
    # print(i)
print(type(json_read))
print(json_read[-1])
