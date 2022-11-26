import mysql.connector
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Sameonu07@"
app.config["MYSQL_DB"] = "IBM"
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/report',methods=['POST','GET'])
def report():
    nitrogen = int(request.form['nvalue'])
    phosphorous = int(request.form['pvalue'])
    potassium = int(request.form['Kvalue'])
    sqrt = int(request.form['sqft'])//1000
    crop = request.form['cropname']
    # summary = reportSummary()
    # summary.getReport(nitrogen, phosphorous, potassium, sqrt, crop)
    mes = True
    u = 0
    d = 0
    m = 0
    matched = False
    urea = 60
    dap = [18, 46]
    mop = 60
    mycursor = mysql.connection.cursor()
    mycursor.execute('select * from plants where plant_name = "%s"' % crop)
    users = mycursor.fetchall()
    mycursor.close()
    n = users[0][2]
    p = users[0][3]
    k = users[0][4]
    print(nitrogen,phosphorous,potassium)
    n = int(sqrt * n)
    p = int(sqrt * p)
    k = int(sqrt * k)
    print(n, p, k)
    if (phosphorous not in range(p - 5, p + 5) and nitrogen not in range(n-5, n+5) and potassium not in range(k-5, k+5)):
        print(potassium) #25
        if (potassium < k):
            diff = abs(potassium - k)
            print(diff)
            fertilzer = diff / mop
            print(fertilzer)
            m = int(fertilzer * 100)
            print(m)
        elif (potassium == k):
            print("MOP is not required")
        else:
            mes = False
        print("Phosphorous")
        if (phosphorous < p):
            diffPhos = abs(phosphorous - p)
            print(diffPhos)
            diffNitro = abs(nitrogen - n)
            print(diffNitro)
            fertilzerPhos = diffPhos /dap[1]
            d = int(fertilzerPhos * 100)
            nitro = dap[0] * fertilzerPhos
            n1 = n
            n = int(n - nitro)
            if (n > 0):
                print(n)
                if (nitrogen not in (n - 5, n + 5)):
                    print("Nitrogen")
                    if (nitrogen < n):
                        diff = abs(nitrogen - n)
                        print(diff)
                        fertilzer = diff / urea
                        print(int(fertilzer * 100))
                    else:
                        mes = False
                        print("This crop is not suited for this soil")

                else:
                    print(nitrogen)
            elif (n == 0):
                print(n)
                print("Urea useage doesnot needed")
            else:
                mes = False
                print("This crop is not suitable for this land nitrogen dap")
        else:
            mes = False
            print("This crop is not suited for this soil phosphorosus dap")
        if (nitrogen < n):
            diff = abs(nitrogen - n)
            print(diff)
            fertilzer = diff / urea
            u = int(fertilzer * 100)
        else:
            mes = False
            print("This crop is not suited for this soil")
    if(u==0 and d==0 and m==0):
        matched = True
    mycursor = mysql.connection.cursor()
    mycursor.execute('select plant_name from plants where  (nitrogen between "%d" and "%d") and (phosphorous between "%d" and "%d") and (potassium between "%d" and "%d") and plant_name != "%s" limit 2' %(n1-5,n1+5,p-5,p+5,k-5,k+5,crop))
    recommended = mycursor.fetchall()
    mycursor.close()
    if(mes==True and len(recommended)==0):
        return render_template('report.html', cropname = crop, n = u,p = d,k=m)
    elif((mes==True and len(recommended)==0)):
        return render_template('report1.html', cropname=crop, n=u, p=d, k=m,r1=recommended[0],r2=recommended[1])
    elif(matched):
        return render_template('report2.html', mes = "Good to go")
    else:
        return render_template('report2.html',mes = "This crop's npk is not suitable for the soil's npk")
if __name__ == '__main__':
    app.run(debug=True)