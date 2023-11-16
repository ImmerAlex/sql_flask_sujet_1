from flask import Flask, render_template, redirect, request, flash, g
import pymysql.cursors
app = Flask(__name__)
app.secret_key = "azerty123"


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="flask_sujet_1",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route("/")
def show_layout():
    return render_template("layout.html")

# ------------------------------------------------
# ---------------- Departement -------------------
# ------------------------------------------------


@app.route("/departement/show")
def show_departement():
    cursor = get_db().cursor()
    sql = ''' SELECT d.id_departement as id, d.nomDepartement, COUNT(e.id_employe) as nombre_employes
            FROM departement d
            LEFT JOIN employe e ON d.id_departement = e.departement_id
            GROUP BY d.id_departement, d.nomDepartement; '''
    cursor.execute(sql)
    departements = cursor.fetchall()
    return render_template("show_departement.html", departement=departements)


@app.route("/departement/add", methods=["GET"])
def add_departement():
    return render_template("add_departement.html")


@app.route("/departement/add", methods=["POST"])
def valid_add_departement():
    if request.method == "POST":
        form = request.form
        nom_department = form.get('nomDepartement')

        cursor = get_db().cursor()
        sql = ''' INSERT INTO departement (id_departement, nomDepartement) 
                VALUES
                (NULL, %s);  '''
        cursor.execute(sql, (nom_department,))
        get_db().commit()
    return redirect("/departement/show")


@app.route("/departement/delete/<id>")
def delete_departement(id):
    cursor = get_db().cursor()
    sql = ''' SELECT departement_id FROM employe WHERE departement_id = %s '''
    cursor.execute(sql, (id,))
    employe_associer = cursor.fetchone()

    if employe_associer:
        message = "Le departement est associer a un employe, il est impossible de le supprimer"
        flash(message, "error")
        return redirect("/departement/show")

    cursor = get_db().cursor()
    sql = ''' DELETE FROM departement WHERE id_departement = %s  '''
    cursor.execute(sql, (id,))
    get_db().commit()
    return redirect("/departement/show")


@app.route("/departement/edit/<id>", methods=["GET"])
def edit_departement(id):
    cursor = get_db().cursor()
    sql = ''' SELECT id_departement as id, nomDepartement FROM departement WHERE id_departement = %s '''
    cursor.execute(sql, (id,))
    departements = cursor.fetchone()
    return render_template("edit_departement.html", departement=departements)


@app.route("/departement/edit", methods=["POST"])
def valid_edit_departement():
    if request.method == "POST":
        form = request.form
        cursor = get_db().cursor()
        sql = ''' UPDATE departement SET nomDepartement = %s WHERE id_departement = %s  '''
        tup_departement_edit = (form.get('nomDepartement'), form.get('id'))
        cursor.execute(sql, tup_departement_edit)
        get_db().commit()
        message = f"Edit departement : id = {form.get('id')}, nom department = {form.get('nomDepartement')}"
    return redirect("/departement/show")


# ------------------------------------------------
# ------------------ Employe ---------------------
# ------------------------------------------------

@app.route("/employe/show")
def show_employe():
    cursor = get_db().cursor()
    sql = ''' SELECT e.id_employe as id, e.nom_employe as nomEmploye,
                    e.ville_dept as villeDept, e.date_embauche as dateEmbauche,
                    e.indice, e.salaire, e.photo, e.departement_id,
                    d.id_departement as idDepartement, d.nomDepartement
            FROM employe e
            JOIN departement d ON e.departement_id = d.id_departement
            ORDER BY e.id_employe ASC; '''
    cursor.execute(sql)
    employes = cursor.fetchall()
    return render_template("show_employe.html", employe=employes)


@app.route("/employe/add", methods=["GET"])
def add_employe():
    cursor = get_db().cursor()
    sql = ''' SELECT id_departement as id, nomDepartement FROM departement '''
    cursor.execute(sql)
    departements = cursor.fetchall()
    return render_template("add_employe.html", departement=departements)


@app.route("/employe/add", methods=["POST"])
def valid_add_employe():
    if request.method == "POST":
        form = request.form

        cursor = get_db().cursor()
        sql = ''' INSERT INTO employe(id_employe, nom_employe, ville_dept, date_embauche, indice, salaire, photo, departement_id) 
                VALUES (NULL, %s, %s, %s, %s, %s ,%s, %s);  '''
        tup_employe = (form.get('nomEmploye'), form.get('villeDept'), form.get('dateEmbauche'), form.get(
            'indice'), form.get('salaire'), form.get('photo'), form.get('departement_id'))
        cursor.execute(sql, tup_employe)
        get_db().commit()

    return redirect("/employe/show")


@app.route("/employe/delete/<id>")
def delete_employe(id):
    cursor = get_db().cursor()
    sql = ''' DELETE FROM employe WHERE id_employe = %s  '''
    cursor.execute(sql, (id,))
    get_db().commit()
    return redirect("/employe/show")


@app.route("/employe/edit/<id>", methods=["GET"])
def edit_employe(id):
    cursor = get_db().cursor()
    sql = ''' SELECT id_employe as id, nom_employe as nomEmploye,
                    ville_dept as villeDept, date_embauche as dateEmbauche,
                    indice, salaire, photo, departement_id
            FROM employe
            WHERE id_employe = %s'''
    cursor.execute(sql, (id,))
    employes = cursor.fetchone()

    sql = ''' SELECT id_departement as id, nomDepartement FROM departement '''
    cursor.execute(sql)
    departements = cursor.fetchall()

    return render_template("edit_employe.html", employe=employes, departement=departements)


@app.route("/employe/edit", methods=["POST"])
def valid_edit_employe():
    print("Pass to post edit employe")
    if request.method == "POST":
        form = request.form

        cursor = get_db().cursor()
        sql = ''' UPDATE employe 
                SET nom_employe = %s, ville_dept = %s, date_embauche = %s, indice = %s, salaire = %s, photo = %s, departement_id = %s 
                WHERE id_employe = %s  '''
        tup_departement_edit = (form.get('nomEmploye'), form.get('villeDept'), form.get('dateEmbauche'), form.get(
            'indice'), form.get('salaire'), form.get('photo'), form.get('departement_id'), form.get('id'))
        cursor.execute(sql, tup_departement_edit)
        get_db().commit()

    return redirect("/employe/show")


@app.route("/employe/filtre", methods=["GET"])
def filtre_employe():
    cursor = get_db().cursor()
    sql = '''
        SELECT e.id_employe as id, e.nom_employe as nomEmploye,
            e.ville_dept as villeDept, e.date_embauche as dateEmbauche,
            e.indice, e.salaire, e.photo, e.departement_id, d.nomDepartement
        FROM employe e
        JOIN departement d ON e.departement_id = d.id_departement
    '''
    cursor.execute(sql)
    employes = cursor.fetchall()

    sql = ''' SELECT id_departement as id, nomDepartement FROM departement '''
    cursor.execute(sql)
    departements = cursor.fetchall()

    return render_template("front_employe_filtre_show.html", employe=employes, departement=departements)


@app.route("/employe/filtre", methods=["POST"])
def valid_filtre_employe():
    if request.method == "POST":
        form = request.form
        nom_employe = form.get("nomEmploye")
        liste_departement = form.getlist("departement")
        salaire_min = form.get("salaire_min")
        salaire_max = form.get("salaire_max")

        tup_filtre = ()
        sql = '''
            SELECT e.photo, e.nom_employe as nomEmploye, e.date_embauche as dateEmbauche, e.salaire, d.nomDepartement
            FROM employe e
            JOIN departement d ON e.departement_id = d.id_departement
            WHERE 1=1
        '''

        if nom_employe:
            sql += "AND LOWER(e.nom_employe) LIKE LOWER(%s) "
            tup_filtre += (f"%{nom_employe}%",)

        if salaire_min and salaire_max:
            if int(salaire_min) > int(salaire_max):
                message = "Le salaire min ne peut pas être supérieur au salaire max"
                flash(message, "error")
                return redirect("/employe/filtre")
            sql += "AND e.salaire BETWEEN %s AND %s "
            tup_filtre += (salaire_min, salaire_max)

        if salaire_min and not salaire_max:
            sql += "AND e.salaire >= %s "
            tup_filtre += (salaire_min,)

        if salaire_max and not salaire_min:
            sql += "AND e.salaire <= %s "
            tup_filtre += (salaire_max,)
            
        if liste_departement:
            for i in range (len(liste_departement)):
                if i == 0:
                    sql += "AND e.departement_id = %s "
                else:
                    sql += "OR e.departement_id = %s "
                tup_filtre += (liste_departement[i],)

        cursor = get_db().cursor()
        cursor.execute(sql, tup_filtre)
        employes = cursor.fetchall()

        print(sql, tup_filtre, employes)

        sql = ''' SELECT id_departement as id, nomDepartement FROM departement '''
        cursor.execute(sql)
        departements = cursor.fetchall()

    return render_template("front_employe_filtre_show.html", employe=employes, departement=departements)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
