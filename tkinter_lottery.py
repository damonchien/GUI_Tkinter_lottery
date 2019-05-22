import tkinter as tk
import pymysql
import json
import pandas as pd
from tkinter import messagebox

window = tk.Tk()
window.title('Lucky you~')
window.geometry('700x400')

image_file = tk.PhotoImage(file='.\coollogo_com-65251468.png')
lbl = tk.Label(image = image_file)
lbl.image = image_file
lbl.pack(side='top')

# tk.Label(window, text='# 獎項(未啟用) : ').place(x=440, y= 250)
# award = tk.Entry(window,width=4)
# award.place(x=550,y=237)

tk.Label(window, text='人數 : ').place(x=300, y= 260)
people = tk.Entry(window,width=4)
people.place(x=340,y=262)

tk.Label(window, text='Form ID : ').place(x=280, y= 210)
formid = tk.Entry(window,width=4)
formid.place(x=340,y=212)

# tk.Label(window, text='答案 : ').place(x=300, y= 250)
# answer = tk.Entry(window,width=13)
# answer.place(x=340,y=252)

# tk.Label(window, text='不重複的欄位 : ').place(x=310, y= 200)
# unduplicate = tk.Entry(window,width=15)
# unduplicate.place(x=400,y=202)

def lottery():
#     aw = award.get();
    pe = int(people.get());fo = formid.get()#;an = answer.get();
    un = '姓名 手機 郵箱'.split()
    conn = pymysql.connect()
    sql = 'SELECT * FROM formdata WHERE FormId="{}"'.format(fo)
    df = pd.read_sql(sql,conn)
    conn.close()
    df = df['Content'].apply(json.loads)

    columns_name = [df[0][i]['Title'] for i in range(len(df[0]))]
    ddf = pd.DataFrame(columns=columns_name)
    
    for i in range(len(df[0])):
        ddf.iloc[:,i] = df.apply(lambda x: x[i]['Content'])
    
    dup = [[i,ddf[ddf['姓名']==i].count()[0]] for i in ddf[ddf.duplicated(subset = ['姓名'])]['姓名'].unique()]
    dup = pd.DataFrame(dup,columns=['姓名','重複次數']).sort_values(by=['重複次數'],ascending=False)
    dup.to_csv('./輸出/重複抽獎_姓名.csv',encoding='utf-8-sig')
    
    dup1 = [[i,ddf[ddf['手機']==i].count()[0]] for i in ddf[ddf.duplicated(subset = ['手機'])]['手機'].unique()]
    dup1 = pd.DataFrame(dup1,columns=['手機','重複次數']).sort_values(by=['重複次數'],ascending=False)
    b =  [i[:4]+'-'+i[4:] for i in dup1['手機']]
    dup1['手機']=b
    dup1.to_csv('./輸出/重複抽獎_手機.csv',encoding='utf-8-sig')
    
    for j in dup[dup['重複次數']>99]['姓名']:
        ddf.drop([ddf[ddf['姓名']==j].index[0]],inplace=True)
        
    for i in range(len(un)):
        ddf = ddf.drop_duplicates([un[i]],keep='first')
#     for i in range(len(an)):
#         z = '答案'+str(i+1)
    ddf = ddf[ddf['答案選項']==ddf['答案選項'].max()]
    
    for i in ddf['姓名']:
        if 'test' in i.lower():
            ddf.drop([ddf[ddf['姓名']==i].index[0]],inplace=True)
            
    ddf = ddf.reset_index().drop(columns=['index'])
    df_pe = ddf.sample(n=pe)
    df_pe = df_pe.reset_index().drop(columns=['index'])
    c =  [i[:4]+'-'+i[4:] for i in df_pe['手機']]
    df_pe['手機']=c
    df_pe.to_csv('./輸出/{}people.csv'.format(pe),encoding='utf-8-sig')
    messagebox.showinfo(title='抽獎完成', message='檔案已下載至"輸出"資料夾 ')
tk.Button(window,text='開始抽獎',width=20, height=2, command=lottery).place(x=275,y=310)  

# tk.Entry(window,width=15).place(x=390,y=260)
# tk.Label(window, text='How Many People: ').place(x=120, y= 365)

window.mainloop()
