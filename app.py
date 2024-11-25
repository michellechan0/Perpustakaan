from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="perpustakaan",
    password="")

userAdmin = {
    "username" : "admin",
    "password" : "54321"
}

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = md5(%s) ")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    password = request.form['password']
    if username == userAdmin["username"]and password == userAdmin["password"]:
        session["user"] = username
        return redirect(url_for("home"))
    else:
        return f"salah cuy .."
    
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

    
@app.route('/home')
def home():
        return render_template("home.html")

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    cursor = mydb.cursor()
    nama = request.form["nama"]
    kelas = request.form["kelas"]
    tanggal = request.form["tanggal"]
    judul = request.form["judul"]

    query = ("insert into peminjaman values( %s, %s, %s, %s, %s)")
    data = ( "", nama, kelas, tanggal, judul )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect("/tampil")

@app.route('/tampil')
def tampil():
    cursor = mydb.cursor()
    cursor.execute("select * from peminjaman")
    data = cursor.fetchall()
    return render_template('tampil.html',data=data) 

@app.route('/hapus/<id>')
def hapus(id):
    cursor = mydb.cursor()
    query = ("delete from peminjaman where id = %s")
    data = (id,)
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect('/tampil')

    

@app.route('/update/<id>')
def update(id):
    cursor = mydb.cursor()
    query = ("select * from peminjaman where id = %s")
    data = (id,)
    cursor.execute( query, data )
    value = cursor.fetchone()
    return render_template('update.html',value=value) 

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    cursor = mydb.cursor()
    id = request.form["id"]
    nama = request.form["nama"]
    kelas = request.form["kelas"]
    tanggal = request.form["tanggal"]
    judul = request.form["judul"]

    query = ("update peminjaman set nama = %s, kelas = %s, tanggal = %s, judul = %s where id = %s")
    data = ( nama, kelas, tanggal, judul, id, )
    cursor.execute( query, data )
    mydb.commit()
    cursor.close()
    return redirect('/tampil')
if __name__ == "__main__":
    app.run(debug=True)