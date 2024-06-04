from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Revenus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)

    def __init__(self, titre, montant):
        self.titre = titre
        self.montant = montant

class Depenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)

    def __init__(self, titre, montant):
        self.titre = titre
        self.montant = montant
    

@app.route("/")
def index():
    revenus = Revenus.query.all()
    depenses = Depenses.query.all()
    revenu_total = db.session.query(db.func.sum(Revenus.montant)).scalar()
    depense_total = db.session.query(db.func.sum(Depenses.montant)).scalar()
    mon_budget = revenu_total - depense_total
    return render_template('index.html', revenus=revenus, depenses=depenses, revenu_total=revenu_total, depense_total=depense_total, mon_budget=mon_budget)


@app.route("/recors_revenu/", methods=["GET", "POST"])
def recors_revenu():
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        nouvel_revenu = Revenus(titre=titre, montant=montant)
        try:
            db.session.add(nouvel_revenu)
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return "vous ne pouvez pas enregistrer les données"
    else:
        return render_template('revenu.html')
    

@app.route("/recors_depense/", methods=["GET", "POST"])
def recors_depense():
    if request.method == "POST":
        titre = request.form['titre']
        montant = request.form['montant']
        nouvel_depense = Depenses(titre=titre, montant=montant)
        try:
            db.session.add(nouvel_depense)
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return "vous ne pouvez pas enregistrer les données"
    else:
        return render_template('depense.html')

@app.route("/sup_revenus/<int:id>/")
def sup_revenus(id):
    revenu = Revenus.query.get_or_404(id)
    try:
        db.session.delete(revenu)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "une erreur s'est produit"

@app.route("/sup_depenses/<int:id>/")
def sup_depenses(id):
    depense = Depenses.query.get_or_404(id)
    try:
        db.session.delete(depense)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "une erreur s'est produit"


if __name__ == '__main__':
    app.run(debug=True)


with app.app_context():
    db.create_all()

