from flask import Flask, render_template,flash, redirect, url_for, request, session, jsonify
import psycopg2
from forms import add_hospital, update_hospital, add_vaccinecenter, add_testcenter , add_personnel, add_patient, update_testcenter,update_vaccinecenter,update_patient,update_personnel
from datetime import datetime
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f5b9ac4eddb1942feeb7d826b76b4a3a'
#session['username'] = 'admin'


hospital_CREATE = """CREATE TABLE IF NOT EXISTS Hospital(
                    hospital_id SERIAL PRIMARY KEY,
                    city_id INT NOT NULL,
                    name VARCHAR(300) NOT NULL,
                    telephone VARCHAR(13),
                    capacity INT NOT NULL,
                    for_pandemic BOOL DEFAULT FALSE
                    )"""
             
patient_CREATE = """CREATE TABLE IF NOT EXISTS Patient(
                    patient_id SERIAL PRIMARY KEY,
                    test_center_id INT NOT NULL REFERENCES TestCenter(test_center_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                    vaccine_center_id INT NOT NULL REFERENCES VaccineCenter(vaccine_center_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                    name VARCHAR(30) NOT NULL,
                    surname VARCHAR(30) NOT NULL,
                    age INT NOT NULL,
                    sex VARCHAR(1) NOT NULL,
                    test_status BOOLEAN DEFAULT TRUE,
                    vaccine_status BOOLEAN DEFAULT TRUE
                    )"""

testcenter_CREATE = """CREATE TABLE IF NOT EXISTS TestCenter(
                    test_center_id SERIAL PRIMARY KEY,
                    hospital_id INT NOT NULL REFERENCES Hospital(hospital_id) ON DELETE CASCADE ON UPDATE CASCADE,
                    test_stock INT DEFAULT 0,
                    personnel_number INT DEFAULT 0
                    )"""

vaccinecenter_CREATE = """CREATE TABLE IF NOT EXISTS VaccineCenter(
                    vaccine_center_id SERIAL PRIMARY KEY,
                    hospital_id INT NOT NULL REFERENCES Hospital(hospital_id) ON DELETE CASCADE ON UPDATE CASCADE,
                    vaccine_stock INT DEFAULT 0,
                    personnel_number INT DEFAULT 0
                    )"""

personnel_CREATE = """CREATE TABLE IF NOT EXISTS Personnel(
                    personnel_id SERIAL PRIMARY KEY,
                    test_center_id INT NOT NULL REFERENCES TestCenter(test_center_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                    vaccine_center_id INT NOT NULL REFERENCES VaccineCenter(vaccine_center_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                    name VARCHAR(30) NOT NULL,
                    surname VARCHAR(30) NOT NULL,
                    age INT NOT NULL,
                    sex VARCHAR(1) NOT NULL,
                    telephone VARCHAR(13) 
                    )"""

def connect_to_DB():
    try: 
        db = psycopg2.connect(user = "postgres",
                      password = "bomonti44",
                      host = "localhost",
                      port = "5432",
                      database = "covidb")
        cursor = db.cursor()  #imlec
        print( db.get_dsn_parameters())
        return db
    except: 
        print("Connection failed.")
        pass

def initialize():
    try:
        db = connect_to_DB()
        cursor = db.cursor()
        cursor.execute(hospital_CREATE)
        cursor.execute(vaccinecenter_CREATE)
        cursor.execute(testcenter_CREATE)
        cursor.execute(personnel_CREATE)
        cursor.execute(patient_CREATE)
        db.commit()
        cursor.close()
        db.close()
        print("Tables created.")
    except:
        print("Tables cannot created.")

initialize()


# @app.route('/home/login', methods = ['GET', 'POST'])
# def login():
#    if request.method == 'POST':
#       session['username'] = request.form['username']
#       return redirect(url_for('index'))
#    return '''
	
#    <form action = "" method = "post">
#       <p><input type = text name = username/></p>
#       <p<<input type = submit value = Login/></p>
#    </form>	
# '''

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
   # remove the username from the session if it is there
    today = datetime.today()
    day_name = today.strftime("%A")
    session.pop('username', None)
    result = index()
    return render_template("logout.html", day = day_name, userinfo = result)

def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username
    return "You are not logged in."

def join_h_t():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT city_id, name, test_stock, personnel_number from Hospital inner join TestCenter on Hospital.hospital_id = TestCenter.hospital_id "
        cursor.execute(statement,)
        result = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return result  

def join_h_v():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT city_id, name, vaccine_stock, personnel_number from Hospital inner join VaccineCenter on Hospital.hospital_id = VaccineCenter.hospital_id "
        cursor.execute(statement,)
        result = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return result  

def join_h_t_p():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT Hospital.name, TestCenter.test_center_id, Personnel.name,surname from (Hospital inner join TestCenter on Hospital.hospital_id = TestCenter.hospital_id) inner join Personnel on TestCenter.test_center_id = Personnel.test_center_id "
        cursor.execute(statement,)
        resultf = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return resultf  

def join_h_v_p():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT Hospital.name, VaccineCenter.vaccine_center_id, Personnel.name,surname from (Hospital inner join VaccineCenter on Hospital.hospital_id = VaccineCenter.hospital_id) inner join Personnel on VaccineCenter.vaccine_center_id = Personnel.vaccine_center_id "
        cursor.execute(statement,)
        resultf = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return resultf  

def intersect_h_t_v():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT x.city_id , x.name from ((select distinct hospital_id from testcenter) intersect (select distinct hospital_id from vaccinecenter)) y inner join Hospital x on x.hospital_id = y.hospital_id "
        cursor.execute(statement,)
        resultf = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return resultf 

def except_h_t_v():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT x.city_id , x.name from ((select distinct hospital_id from testcenter) except (select distinct hospital_id from vaccinecenter)) y inner join Hospital x on x.hospital_id = y.hospital_id "
        cursor.execute(statement,)
        resultt = cursor.fetchall()
        statement = "SELECT x.city_id , x.name from ((select distinct hospital_id from vaccinecenter) except (select distinct hospital_id from testcenter)) y inner join Hospital x on x.hospital_id = y.hospital_id "
        cursor.execute(statement,)
        resultv = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return resultt, resultv 


@app.route("/" , methods = ['GET', 'POST'])
def entrance():
    today = datetime.today()
    day_name = today.strftime("%A")
    #result = "Bakalim gorelim"
    if request.method == 'POST':
        session['username'] = request.form['username']
        result = index()
        return render_template("home.html", day = day_name, userinfo = result)   #home_main
    return render_template("entrance.html", day = day_name) 


@app.route("/home", methods = ['GET', 'POST'])
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    userinfo = session['username']
    #result = "Bakalim gorelim"
    return render_template("home.html", day = day_name, userinfo = userinfo) 


@app.route("/hospital", methods=['GET'])
def hospital_page():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT * FROM Hospital"
        cursor.execute(statement,)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        htvs = intersect_h_t_v()
        ehtvs, ehvts = except_h_t_v()
    except psycopg2.Error as error:
        print(error)
    return render_template("hospital_page.html", hospitals = result, htvs = htvs, ehvts = ehvts, ehtvs=ehtvs)   #hospital_page

@app.route("/personnel", methods=['GET'])
def personnel_page():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT * FROM Personnel"
        cursor.execute(statement,)
        result = cursor.fetchall()
        statement_test = "SELECT * FROM TestCenter"
        cursor.execute(statement_test,)
        result_test = cursor.fetchall()
        statement_vaccine = "SELECT * FROM VaccineCenter"
        cursor.execute(statement_vaccine,)
        result_vaccine = cursor.fetchall()
        for test in result_test:
            counter_state = "SELECT COUNT(*) FROM Personnel WHERE test_center_id = %s GROUP BY test_center_id"
            test_id = str(test[0])
            cursor.execute(counter_state, (test_id),)
            personnel_num = cursor.fetchone()
            print("Selam")
            print(personnel_num)
            if personnel_num:
                new_num = int(personnel_num[0])
                new_pers_num = str(new_num)
                solution_state = "UPDATE TestCenter SET personnel_number = %s WHERE test_center_id = %s"
                cursor.execute(solution_state,( new_pers_num, test_id),)
                db.commit()
        for vaccine in result_vaccine:
            counter_state = "SELECT COUNT(*) FROM Personnel WHERE vaccine_center_id = %s GROUP BY vaccine_center_id"
            vaccine_id = str(vaccine[0])
            cursor.execute(counter_state, (vaccine_id),)
            personnel_num = cursor.fetchone()
            if personnel_num:
                new_num = int(personnel_num[0])
                new_pers_num = str(new_num)
                solution_state = "UPDATE VaccineCenter SET personnel_number = %s WHERE vaccine_center_id = %s"
                cursor.execute(solution_state,( new_pers_num, vaccine_id),)
                db.commit()
        cursor.close()
        db.close()
        htp = join_h_t_p()
        hvp = join_h_v_p()
    except psycopg2.Error as error:
        print(error)
    return render_template("personnel_page.html", personnels = result, htps = htp, hvps = hvp)  

@app.route("/patient", methods=['GET'])
def patient_page():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT * FROM Patient"
        cursor.execute(statement,)
        result = cursor.fetchall()
        cursor.close()
        db.close()
    except psycopg2.Error as error:
        print(error)
    return render_template("patient_page.html", patients = result)    

@app.route("/testcenter", methods=['GET'])
def test_page():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT * FROM TestCenter"
        cursor.execute(statement,)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        test_hospital = join_h_t()
    except psycopg2.Error as error:
        print(error)
    return render_template("test_page.html", tests = result, test_hospital = test_hospital)   

@app.route("/vaccinecenter", methods=['GET'])
def vaccine_page():
    try:            
        db = connect_to_DB()
        cursor = db.cursor()
        statement = "SELECT * FROM VaccineCenter"
        cursor.execute(statement,)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        vaccine_hospital = join_h_v()
    except psycopg2.Error as error:
        print(error)
    return render_template("vaccine_page.html", vaccines = result, vaccine_hospital= vaccine_hospital)    

@app.route("/hospital/update/<update>", methods=['GET','POST'])
def hospital_update(update):       
    form = update_hospital()
    try:        
        db = connect_to_DB()
        cursor = db.cursor()       
        statement = "SELECT * FROM Hospital WHERE hospital_id = %s"
        cursor.execute(statement,(update,))        
        result = cursor.fetchone()
        #gender = "Female" if result[3] == "F" else "Male"
        if request.method == 'POST':
            city_id = request.form['city_id']
            name = request.form['name']
            telephone = request.form['telephone']   
            capacity = request.form['capacity']  
            for_pandemic = request.form['for_pandemic']     
            try:
                if city_id:
                    statement = "UPDATE Hospital SET city_id = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(city_id,update,))                
                if name:
                    statement = "UPDATE Hospital SET name = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(name,update,))
                if telephone:
                    statement = "UPDATE Hospital SET telephone = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(telephone,update,))
                if capacity:
                    statement = "UPDATE Hospital SET capacity = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(capacity,update,))
                if for_pandemic:
                    statement = "UPDATE Hospital SET for_pandemic = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(for_pandemic,update,))
                db.commit()
                cursor.close()
                db.close()
                flash('Hospital updated.', 'success')
                return redirect(url_for("hospital_update", update = update))     
            except psycopg2.Error as error:
                print(error)
                db.rollback()
                cursor.close()
                db.close()
                flash('An error occured.', 'danger')
                return redirect(url_for('hospital_page'))
    except psycopg2.Error as error:
        print(error)
        db.rollback()
        cursor.close()
        db.close()
        flash('An error occured.', 'danger')
        return redirect(url_for('hospital_page'))
    return render_template("hospital_update.html", form = form,result = result
                        # city_id = result[1],
                        # name = result[2],
                        # telephone = result[3],
                        # capacity = result[4],
                        # for_pandemic = result[5],
                        # form = form
                        )

@app.route("/patient/update/<update>", methods=['GET','POST'])
def patient_update(update):       
    form = update_patient()
    try:        
        db = connect_to_DB()
        cursor = db.cursor()       
        statement = "SELECT * FROM Patient WHERE patient_id = %s"
        cursor.execute(statement,(update,))        
        result = cursor.fetchone()
        previous_test = result[7]
        previous_vaccine = result[8]
        print(previous_test)
        #gender = "Female" if result[3] == "F" else "Male"
        if request.method == 'POST':
            test_center_id = request.form['test_center_id']
            vaccine_center_id = request.form['vaccine_center_id']
            name = request.form['name']
            surname = request.form['surname']
            age = request.form['age']
            sex = request.form['sex']
            test_status = request.form['test_status']   
            vaccine_status = request.form['vaccine_status']     
            try:
                
                
                if test_center_id:
                    statement = "UPDATE Patient SET test_center_id = %s WHERE patient_id = %s"
                    cursor.execute(statement,(test_center_id,update,))                
                if vaccine_center_id:
                    statement = "UPDATE Patient SET vaccine_center_id = %s WHERE patient_id = %s"
                    cursor.execute(statement,(vaccine_center_id,update,))
                if name:
                    statement = "UPDATE Patient SET name = %s WHERE patient_id = %s"
                    cursor.execute(statement,(name,update,))
                if surname:
                    statement = "UPDATE Patient SET surname = %s WHERE patient_id = %s"
                    cursor.execute(statement,(surname,update,))
                if age:
                    statement = "UPDATE Patient SET age = %s WHERE patient_id = %s"
                    cursor.execute(statement,(age,update,))
                if sex:
                    statement = "UPDATE Patient SET sex = %s WHERE patient_id = %s"
                    cursor.execute(statement,(sex,update,))
                if test_status:
                    if(previous_test == False and test_status == 'true'):
                        test_center_state = "SELECT test_center_id FROM Patient where patient_id = %s"
                        cursor.execute(test_center_state,(update,))
                        test_center = cursor.fetchone()
                        teststatement = "UPDATE TestCenter SET test_stock = test_stock - 1 WHERE test_center_id = %s"
                        cursor.execute(teststatement,(test_center,))
                        db.commit()
                    statement = "UPDATE Patient SET test_status = %s WHERE patient_id = %s"
                    cursor.execute(statement,(test_status,update,))
                if vaccine_status:
                    if(previous_vaccine == False and vaccine_status == 'true'):
                        vaccine_center_state = "SELECT vaccine_center_id FROM Patient where patient_id = %s"
                        cursor.execute(vaccine_center_state,(update,))
                        vaccine_center = cursor.fetchone()
                        vaccinestatement = "UPDATE VaccineCenter SET vaccine_stock = vaccine_stock - 1 WHERE vaccine_center_id = %s"
                        cursor.execute(vaccinestatement,(vaccine_center,))
                        db.commit()
                    statement = "UPDATE Patient SET vaccine_status = %s WHERE patient_id = %s"
                    cursor.execute(statement,(vaccine_status,update,))
                db.commit()
                cursor.close()
                db.close()
                flash('Patient updated.', 'success')
                return redirect(url_for("patient_page"))    # , update = update
            except psycopg2.Error as error:
                print(error)
                db.rollback()
                cursor.close()
                db.close()
                flash('An error occured.', 'danger')
                return redirect(url_for('patient_page'))
    except psycopg2.Error as error:
        print(error)
        db.rollback()
        cursor.close()
        db.close()
        flash('An error occured.', 'danger')
        return redirect(url_for('patient_page'))
    return render_template("patient_update.html", form = form,result = result)

@app.route("/personnel/update/<update>", methods=['GET','POST'])
def personnel_update(update):       
    form = update_personnel()
    try:        
        db = connect_to_DB()
        cursor = db.cursor()       
        statement = "SELECT * FROM Personnel WHERE personnel_id = %s"
        cursor.execute(statement,(update,))        
        result = cursor.fetchone()
        #gender = "Female" if result[3] == "F" else "Male"
        if request.method == 'POST':
            test_center_id = request.form['test_center_id']
            vaccine_center_id = request.form['vaccine_center_id']
            name = request.form['name']
            surname = request.form['surname']
            age = request.form['age']
            sex = request.form['sex']
            telephone = request.form['telephone']    
            try:
                if test_center_id:
                    statement = "UPDATE Personnel SET test_center_id = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(test_center_id,update,))                
                if vaccine_center_id:
                    statement = "UPDATE Personnel SET vaccine_center_id = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(vaccine_center_id,update,))
                if name:
                    statement = "UPDATE Personnel SET name = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(name,update,))
                if surname:
                    statement = "UPDATE Personnel SET surname = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(surname,update,))
                if age:
                    statement = "UPDATE Personnel SET age = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(age,update,))
                if sex:
                    statement = "UPDATE Personnel SET sex = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(sex,update,))
                if telephone:
                    statement = "UPDATE Personnel SET telephone = %s WHERE personnel_id = %s"
                    cursor.execute(statement,(telephone,update,))
                db.commit()
                cursor.close()
                db.close()
                flash('Personnel updated.', 'success')
                return redirect(url_for("personnel_update", update = update))     
            except psycopg2.Error as error:
                print(error)
                db.rollback()
                cursor.close()
                db.close()
                flash('An error occured.', 'danger')
                return redirect(url_for('personnel_page'))
    except psycopg2.Error as error:
        print(error)
        db.rollback()
        cursor.close()
        db.close()
        flash('An error occured.', 'danger')
        return redirect(url_for('personnel_page'))
    return render_template("personnel_update.html", form = form,result = result)

@app.route("/testcenter/update/<update>", methods=['GET','POST'])
def test_update(update):       
    form = update_testcenter()
    try:        
        db = connect_to_DB()
        cursor = db.cursor()       
        statement = "SELECT * FROM TestCenter WHERE test_center_id = %s"
        cursor.execute(statement,(update,))        
        result = cursor.fetchone()
        #gender = "Female" if result[3] == "F" else "Male"
        if request.method == 'POST':
            hospital_id = request.form['hospital_id']
            test_stock = request.form['test_stock']
            personnel_number = request.form['personnel_number']    
            try:
                if hospital_id:
                    statement = "UPDATE TestCenter SET hospital_id = %s WHERE test_center_id = %s"
                    cursor.execute(statement,(hospital_id,update,))                
                if test_stock:
                    statement = "UPDATE TestCenter SET test_stock = %s WHERE test_center_id = %s"
                    cursor.execute(statement,(test_stock,update,))
                if personnel_number:
                    statement = "UPDATE TestCenter SET personnel_number = %s WHERE test_center_id = %s"
                    cursor.execute(statement,(personnel_number,update,))
                db.commit()
                cursor.close()
                db.close()
                flash('Test Center updated.', 'success')
                return redirect(url_for("test_update", update = update))     
            except psycopg2.Error as error:
                print(error)
                db.rollback()
                cursor.close()
                db.close()
                flash('An error occured.', 'danger')
                return redirect(url_for('test_page'))
    except psycopg2.Error as error:
        print(error)
        db.rollback()
        cursor.close()
        db.close()
        flash('An error occured.', 'danger')
        return redirect(url_for('test_page'))
    return render_template("test_update.html", form = form,result = result )

@app.route("/vaccinecenter/update/<update>", methods=['GET','POST'])
def vaccine_update(update):       
    form = update_vaccinecenter()
    try:        
        db = connect_to_DB()
        cursor = db.cursor()       
        statement = "SELECT * FROM VaccineCenter WHERE vaccine_center_id = %s"
        cursor.execute(statement,(update,))        
        result = cursor.fetchone()
        #gender = "Female" if result[3] == "F" else "Male"
        if request.method == 'POST':
            hospital_id = request.form['hospital_id']
            test_stock = request.form['test_stock']
            personnel_number = request.form['personnel_number']    
            try:
                if hospital_id:
                    statement = "UPDATE VaccineCenter SET hospital_id = %s WHERE vaccine_center_id = %s"
                    cursor.execute(statement,(hospital_id,update,))                
                if test_stock:
                    statement = "UPDATE VaccineCenter SET vaccine_stock = %s WHERE vaccine_center_id = %s"
                    cursor.execute(statement,(test_stock,update,))
                if personnel_number:
                    statement = "UPDATE VaccineCenter SET personnel_number = %s WHERE vaccine_center_id = %s"
                    cursor.execute(statement,(personnel_number,update,))
                db.commit()
                cursor.close()
                db.close()
                flash('Vaccine Center updated.', 'success')
                return redirect(url_for("vaccine_update", update = update))     
            except psycopg2.Error as error:
                print(error)
                db.rollback()
                cursor.close()
                db.close()
                flash('An error occured.', 'danger')
                return redirect(url_for('vaccine_page'))
    except psycopg2.Error as error:
        print(error)
        db.rollback()
        cursor.close()
        db.close()
        flash('An error occured.', 'danger')
        return redirect(url_for('vaccine_page'))
    return render_template("vaccine_update.html", form = form,result = result
                        # city_id = result[1],
                        # name = result[2],
                        # telephone = result[3],
                        # capacity = result[4],
                        # for_pandemic = result[5],
                        # form = form
                        )

@app.route("/hospital/add", methods=['GET','POST'])
def hospital_add():
    form = add_hospital()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                db = connect_to_DB()
                cursor = db.cursor()            
                statement = "INSERT INTO Hospital (city_id,name,telephone,capacity,for_pandemic) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(statement,(request.form['city_id'],request.form['name'],request.form['telephone'],request.form['capacity'],request.form['for_pandemic'],)) #request.form['for_pandemic']
                db.commit()
                cursor.close()
                db.close()
                flash('Hospital added successful.', 'success')
                return redirect(url_for('hospital_page'))
            except psycopg2.Error as error:
                print(error)                    
                flash('An error occured.', 'danger')
                return redirect(url_for('hospital_add'))
        
    return render_template("hospital_add.html", form = form)

@app.route("/patient/add", methods=['GET','POST'])
def patient_add():
    form = add_patient()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                db = connect_to_DB()
                cursor = db.cursor()            
                statement = "INSERT INTO Patient (test_center_id,vaccine_center_id, name, surname, age, sex, test_status, vaccine_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(statement,(request.form['test_center_id'],request.form['vaccine_center_id'],request.form['name'],request.form['surname'],request.form['age'],request.form['sex'],request.form['test_status'],request.form['vaccine_status'],)) #request.form['for_pandemic']
                db.commit()
                cursor.close()
                db.close()
                flash('Patient added successfully.', 'success')
                return redirect(url_for('patient_page'))
            except psycopg2.Error as error:
                print(error)                    
                flash('An error occured.', 'danger')
                return redirect(url_for('patient_page'))
        
    return render_template("patient_add.html", form = form)

@app.route("/personnel/add", methods=['GET','POST'])
def personnel_add():
    form = add_personnel()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                db = connect_to_DB()
                cursor = db.cursor()            
                statement = "INSERT INTO Personnel (test_center_id,vaccine_center_id, name, surname, age, sex, telephone) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(statement,(request.form['test_center_id'],request.form['vaccine_center_id'],request.form['name'],request.form['surname'],request.form['age'],request.form['sex'],request.form['telephone'],)) #request.form['for_pandemic']
                db.commit()
                cursor.close()
                db.close()
                flash('Personnel added successfully.', 'success')

                return redirect(url_for('personnel_page'))
            except psycopg2.Error as error:
                print(error)                    
                flash('An error occured.', 'danger')
                return redirect(url_for('personnel_add'))
        
    return render_template("personnel_add.html", form = form)

@app.route("/vaccinecenter/add", methods=['GET','POST'])
def vaccine_add():
    form = add_vaccinecenter()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                db = connect_to_DB()
                cursor = db.cursor()            
                statement = "INSERT INTO VaccineCenter (hospital_id,vaccine_stock, personnel_number) VALUES (%s,%s,%s)"
                cursor.execute(statement,(request.form['hospital_id'],request.form['vaccine_stock'],request.form['personnel_number'],)) #request.form['for_pandemic']
                db.commit()
                cursor.close()
                db.close()
                flash('Vaccine Center added successfully.', 'success')
                return redirect(url_for('vaccine_page'))
            except psycopg2.Error as error:
                print(error)                    
                flash('An error occured.', 'danger')
                return redirect(url_for('vaccine_add'))
        
    return render_template("vaccine_add.html", form = form)

@app.route("/testcenter/add", methods=['GET','POST'])
def test_add():
    form = add_testcenter()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                db = connect_to_DB()
                cursor = db.cursor()            
                statement = "INSERT INTO TestCenter (hospital_id,test_stock, personnel_number) VALUES (%s,%s,%s)"
                cursor.execute(statement,(request.form['hospital_id'],request.form['test_stock'],request.form['personnel_number'],)) #request.form['for_pandemic']
                db.commit()
                cursor.close()
                db.close()
                flash('Test Center added successfully.', 'success')
                return redirect(url_for('test_page'))
            except psycopg2.Error as error:
                print(error)                    
                flash('An error occured.', 'danger')
                return redirect(url_for('test_add'))
        
    return render_template("test_add.html", form = form)

@app.route("/hospital/delete/<delete>", methods=['GET'])
def hospital_delete(delete):
        try:
            db = connect_to_DB()
            cursor = db.cursor() 
            statement = "DELETE FROM Hospital WHERE hospital_id=%s"
            cursor.execute(statement, (delete,))
            db.commit()
            cursor.close()
            db.close()
        except psycopg2.Error as error:
            print(error)
            db.rollback()
            cursor.close()
            db.close()
            flash('An error occured.', 'danger')
            #return redirect(url_for('hospital_page'))
        return redirect(url_for("hospital_page"))

@app.route("/patient/delete/<delete>", methods=['GET'])
def patient_delete(delete):
        try:
            db = connect_to_DB()
            cursor = db.cursor() 
            statement = "DELETE FROM Patient WHERE patient_id=%s"
            cursor.execute(statement, (delete,))
            db.commit()
            cursor.close()
            db.close()
        except psycopg2.Error as error:
            print(error)
            db.rollback()
            cursor.close()
            db.close()
            flash('An error occured.', 'danger')
            #return redirect(url_for('hospital_page'))
        return redirect(url_for("patient_page"))

@app.route("/personnel/delete/<delete>", methods=['GET'])
def personnel_delete(delete):
        try:
            db = connect_to_DB()
            cursor = db.cursor() 
            statement = "DELETE FROM Personnel WHERE personnel_id=%s"
            cursor.execute(statement, (delete,))
            db.commit()
            cursor.close()
            db.close()
        except psycopg2.Error as error:
            print(error)
            db.rollback()
            cursor.close()
            db.close()
            flash('An error occured.', 'danger')
            #return redirect(url_for('hospital_page'))
        return redirect(url_for("personnel_page"))

@app.route("/testcenter/delete/<delete>", methods=['GET'])
def test_delete(delete):
        try:
            db = connect_to_DB()
            cursor = db.cursor() 
            statement = "DELETE FROM TestCenter WHERE test_center_id=%s"
            cursor.execute(statement, (delete,))
            db.commit()
            cursor.close()
            db.close()
        except psycopg2.Error as error:
            print(error)
            db.rollback()
            cursor.close()
            db.close()
            flash('An error occured.', 'danger')
            #return redirect(url_for('hospital_page'))
        return redirect(url_for("test_page"))

@app.route("/vaccinecenter/delete/<delete>", methods=['GET'])
def vaccine_delete(delete):
        try:
            db = connect_to_DB()
            cursor = db.cursor() 
            statement = "DELETE FROM VaccineCenter WHERE vaccine_center_id=%s"
            cursor.execute(statement, (delete,))
            db.commit()
            cursor.close()
            db.close()
        except psycopg2.Error as error:
            print(error)
            db.rollback()
            cursor.close()
            db.close()
            flash('An error occured.', 'danger')
            #return redirect(url_for('hospital_page'))
        return redirect(url_for("vaccine_page"))

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object("settings")

#     app.add_url_rule("/",view_func=views.home_page)
#     app.add_url_rule("/movies",view_func=views.movies_page)
#     app.add_url_rule("/movies/<int:movie_key>", view_func = views.movie_page)
#     app.add_url_rule("/new-movie", view_func=views.movie_add_page, methods=["GET", "POST"])
#     app.add_url_rule("/hospital", view_func=views.hospital_page, methods=["GET", "POST"])
#     db = connect_to_DB()
#     #db.add_movie(Movie("Slaughterhouse-Five", year=1972))
#     #db.add_movie(Movie("The Shining"))
#     app.config["db"] = db
#     return app

# if __name__ == "__main__" : 
#     app = Flask(__name__)
#     app.config.from_object("settings")
#     #app = create_app()
#     app.run(host = "127.0.0.1", port = 8080)     #browser and local ip every 

           
if __name__ == '__main__':
    # app.run(host = "127.0.0.1", port = process.env.PORT or 8080, debug=True)
    #app.run(host = "127.0.0.1", port = process.env.PORT or 8080, debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    #process.env.PORT || 3000