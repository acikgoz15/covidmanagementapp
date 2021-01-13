from flask import Flask, render_template
import views
import psycopg2
# from database import Database 
# from movie import Movie 


# db = psycopg2.connect(user = "postgres",
#                       password = "bomonti44",
#                       host = "localhost",
#                       port = "5432",
#                       database = "dbcovid")

# cursor = db.cursor()  #imlec
# print( db.get_dsn_parameters())


hospital_CREATE = """CREATE TABLE IF NOT EXISTS Hospital(
                    hospital_id SERIAL PRIMARY KEY,
                    city_id INT NOT NULL,
                    name VARCHAR(300) NOT NULL,
                    telephone VARCHAR(13)
                    capacity INT NOT NULL,
                    for_pandemic BOOLEAN DEFAULT FALSE
                    )"""
             
patient_CREATE = """CREATE TABLE IF NOT EXISTS Patient(
    patient_id SERIAL PRIMARY KEY,
    test_center_id 
    vaccine_center_id
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR(1) NOT NULL,
    test_status BOOLEAN DEFAULT FALSE,
    vaccine_status BOOLEAN DEFAULT FALSE
)"""

testcenter_CREATE = """CREATE TABLE IF NOT EXISTS TestCenter(
test_center_id SERIAL PRIMARY KEY,
test_stock INT DEFAULT 0,
personnel_number INT DEFAULT 0
)"""

vaccinecenter_CREATE = """CREATE TABLE IF NOT EXISTS VaccineCenter(
vaccine_center_id SERIAL PRIMARY KEY,
vaccine_stock INT DEFAULT 0,
personnel_number INT DEFAULT 0
)"""

personnel_CREATE = """CREATE TABLE IF NOT EXISTS Personnel(
personnel_id SERIAL PRIMARY KEY,
test_center_id
vaccine_center_id
name VARCHAR(30) NOT NULL,
surname VARCHAR(30) NOT NULL,
age INT NOT NULL,
sex VARCHAR(1) NOT NULL,
telephone VARCHAR(13) 
)"""

# cursor.execute(hospital_CREATE)
# db.commit()



def connect_to_DB():
    try: 
        db = psycopg2.connect(user = "postgres",
                      password = "bomonti44",
                      host = "localhost",
                      port = "5432",
                      database = "dbcovid")
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
        # cursor.execute(vaccinecenter_CREATE)
        # cursor.execute(testcenter_CREATE)
        # cursor.execute(personnel_CREATE)
        # cursor.execute(patient_CREATE)
        cursor.close()
        db.close()
        print("Tables created.")
    except:
        print("Tables cannot created.")


initialize()


# komut_INSERT = "INSERT INTO Hospital_new(city_id, name, telephone) VALUES(7,'Antalya Eğitim Araştırma Hastanesi','+902422494400');"

# cursor.execute(komut_INSERT)
# db.commit()

@app.route("/")
@app.route("/home")
def home():
    return render_template("home_main.html")

@app.route("/hospital", methods=['GET'])
def hospital_page():
    return render_template("hospital_page.html")   

@app.route("/personnel", methods=['GET'])
def personnel_page():
    return render_template("personnel_page.html")  

@app.route("/patient", methods=['GET'])
def patient_page():
    return render_template("patient_page.html")  

@app.route("/testcenter", methods=['GET'])
def test_page():
    return render_template("test_page.html")  

@app.route("/vaccinecenter", methods=['GET'])
def vaccine_page():
    return render_template("vaccine_page.html")  

@app.route("/hospital/update", methods=['GET','POST'])
def hospital_update():       
    form = update_hospital()
    try:        
        db = connect_to_DB()
        cursor = db.cursor()       
        statement = "SELECT * FROM hospital WHERE hospital_id = %s"
        cursor.execute(statement,(session['hospital_id'],))        
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
                    cursor.execute(statement,(city_id,session['hospital_id'],))                
                if name:
                    statement = "UPDATE Hospital SET name = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(name,session['hospital_id'],))
                if telephone:
                    statement = "UPDATE Hospital SET telephone = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(telephone,session['hospital_id'],))
                if capacity:
                    statement = "UPDATE Hospital SET capacity = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(capacity,session['hospital_id'],))
                if for_pandemic:
                    statement = "UPDATE Hospital SET for_pandemic = %s WHERE hospital_id = %s"
                    cursor.execute(statement,(for_pandemic,session['hospital_id'],))
                db.commit()
                cursor.close()
                db.close()
                flash('Hospital updated.', 'success')
                return redirect(url_for("hospital_page"))
                
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
    return render_template("hospital_update.html",
                        city_id = result[1],
                        name = result[2],
                        telephone = result[3],
                        capacity = result[4],
                        for_pandemic = result[5],
                        form = form
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
                cursor.execute(statement,(request.form['city_id'],request.form['name'],request.form['telephone'],request.form['capacity'],request.form['for_pandemic'],))
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


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/",view_func=views.home_page)
    app.add_url_rule("/movies",view_func=views.movies_page)
    app.add_url_rule("/movies/<int:movie_key>", view_func = views.movie_page)
    app.add_url_rule("/new-movie", view_func=views.movie_add_page, methods=["GET", "POST"])
    app.add_url_rule("/hospital", view_func=views.hospital_page, methods=["GET", "POST"])
    db = connect_to_DB()
    #db.add_movie(Movie("Slaughterhouse-Five", year=1972))
    #db.add_movie(Movie("The Shining"))
    app.config["db"] = db
    return app

if __name__ == "__main__" : 
    app = create_app()
    app.run(host = "127.0.0.1", port = 8080)     #browser and local ip every 