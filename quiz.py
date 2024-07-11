import requests as r
import json
import ctypes

while True:
    TOK =input("enter token:")
    head={
        "Authorization": f"Bearer {TOK}",
        "Referer": "https://tesseractonline.com/"
    }
    l=r.get(url="https://api.tesseractonline.com/studentmaster/subjects/1/2",headers=head).text
    l=json.loads(l)
    if l['Error']==False:
        break
    else:
        print('the given token is expired or may be wrong.')


def getQuiz(i):
    url=f"https://api.tesseractonline.com/quizattempts/create-quiz/{i}"
    res=r.get(url=url,headers=head).text
    return json.loads(res)

def saveQ(Zid,Qid,Opt):
    url="https://api.tesseractonline.com/quizquestionattempts/save-user-quiz-answer"
    payload={
        "quizId": f'{Zid}',
        "questionId": f'{Qid}',
        "userAnswer": f'{Opt}'
    }
    save=r.post(url=url,json=payload,headers=head).text
    return save

def submit(a):
    url="https://api.tesseractonline.com/quizattempts/submit-quiz"
    payload={
        "branchCode": "CSE",
        "sectionName": "CSE-PS1",
        "quizId": f'{a}'
    }
    submit=r.post(url=url,json=payload,headers=head).text
    submit=json.loads(submit)
    return submit

def write_quiz(i):
    try:
        rc=getQuiz(i)
        quizId=rc["payload"]['quizId']
        questions=rc["payload"]["questions"]
        opt=['a','b','c','d']
        prev=submit(quizId)["payload"]["score"]
        print("work in progress Please wait")
        for i in range(5):
            for j in opt:
                saveQ(quizId,rc["payload"]["questions"][i]['questionId'],j)
                scr=submit(quizId)["payload"]["score"]
                if(scr==5):
                    print('test compleated refresh the page')
                if(scr>prev):
                    prev=scr
                    break
                else:
                    pass
    except KeyError:
        print('This subject or topic is inactive')

def dashbord():
    url="https://api.tesseractonline.com/studentmaster/subjects/1/2"
    l=r.get(url=url,headers=head).text
    l=json.loads(l)

    l=l['payload']
    subjects={}
    for i in l:
        subjects[i['subject_id']]=i['subject_name']
    return subjects

def units(i):
    url=f"https://api.tesseractonline.com/studentmaster/get-subject-units/{i}"
    l=r.get(url=url,headers=head).text
    l=json.loads(l)
    l=l['payload']
    units={}
    for i in l:
        units[i['unitId']]=i['unitName']
    return units

def topics(a):
    url = f"https://api.tesseractonline.com/studentmaster/get-topics-unit/{a}"
    l=r.get(url=url,headers=head).text
    l=json.loads(l)
    l=l['payload']['topics']
    pdf={}
    top={}
    for i in l:
        top[f"{i['id']}. {i['name']}  {i['learningFlag']}"]={'pdf':f'"https://api.tesseractonline.com"{i["pdf"]}','video': i['videourl']}
    return top


sub=dashbord()
for i in sub:
    print(f'{i}. {sub[i]}')
subc=input('Enter the key to select subject:')
units=units(subc)
for i in units:
    print(f'{i}.{units[i]}')
unitc=input('Enter the key to select unit:')
topics=topics(unitc)
for i in topics:
    print(i)
ip=input('Enter the key to select topic:').split()
for x in ip:
    write_quiz(x)



