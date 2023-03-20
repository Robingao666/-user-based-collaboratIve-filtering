from flask import Flask,render_template,request,redirect,url_for
import pymysql
import pandas as pd
import json
app = Flask(__name__)
conn = pymysql.connect(host="47.97.175.255",port=3306,user="zz",
                       password="990506",database="movie",charset="utf8")

moviedata = pd.read_csv(r'C:/Users/zhuaba/Desktop/homework/movies.csv')
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.after_request(after_request)

def round1(x):
    return round(x,2)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/1')
def hello_world1():
    sql = "select * from count_between_score;"
    df = pd.read_sql(sql,conn)
    data = df['num'].reset_index(drop=True).to_numpy()
    return render_template('1.html',data1=list(data))


@app.route('/2')
def hello_world2():
    sql = "select * from counts_between_categories;"
    df = pd.read_sql(sql,conn)
    data2 = df['count'].reset_index(drop=True).to_list()
    data1 = df['categories'].reset_index(drop=True).to_list()
    return render_template('2.html',data1=data1,data2=data2)


@app.route('/3')
def hello_world3():
    sql = "select * from avgscore_between_categories;"
    df = pd.read_sql(sql,conn)
    data = list(map(round1,df['avgscore'].to_list()))
    return render_template('3.html',data2=data)


@app.route('/4')
def hello_world4():
    sql = "select * from avgscore_top100;"
    df = pd.read_sql(sql,conn)
    index = df['movieId'].tolist()

    data = moviedata[moviedata.movieId.isin(index)].title.tolist()
    # dataJson=json.dumps(data)
    return render_template('4.html',data1=data)


@app.route('/5')
def hello_world5():
    sql = "select * from top10;"
    df = pd.read_sql(sql,conn)
    dataDict = {}
    for col in df.columns[1:]:
        index = df[col].tolist()
        data = moviedata[moviedata.movieId.isin(index)].title.tolist()
        dataDict[col] = data
    return render_template('5.html',data1=dataDict)


@app.route('/6')
def hello_world6():
    return render_template('recommend.html')




@app.route('/recommend',methods=['GET'])
def hello_world7():
    userId = request.args.get("userId")
    print(userId)
    sql = f"select * from recommend_movie where userId={userId};"
    df = pd.read_sql(sql,conn)
    data = df['title'].tolist()
    # print(data)
    return {"data1": data}


if __name__ == '__main__':
    app.run()
    