from flask import Flask, abort, render_template, g, redirect, url_for, request, flash, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email
import smtplib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap(app)


class ContactMe(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()], render_kw={"placeholder": "Your Name"})
    mail = EmailField(" Your E-Mail Address", validators=[DataRequired(), Email()],
                      render_kw={"placeholder": "Your E-Mail"})
    phone = StringField("Your Phone Number (optional)", render_kw={"placeholder": "Your Phone Number"})
    message = TextAreaField("Your Message...", validators=[DataRequired()],
                            render_kw={"placeholder": "Your Message..."})
    submit = SubmitField("Send Message")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactMe()
    if form.validate_on_submit():
        name = form.name.data
        email = form.mail.data
        telephone = form.phone.data
        message = form.message.data
        my_email = "oibrasil2510@gmail.com"
        second_email = "luise.schwenkee@gmail.com"
        password = "fpjohbmnwgbrbqpk"
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=second_email,
                                msg=f"New message from {name}:\n {message} \n E-Mail: {email}\n phone:{telephone}")
            flash('Your Message got send successfully!')
            return redirect(url_for('home'))
    else:
        return render_template("index.html", msg_send=False, form=form)


@app.route('/download')
def download():
    return send_from_directory('static', path="files/CV-L.Schwenke.pdf")


@app.route('/bachelor')
def bachelor():
    return send_from_directory('static', path="files/bachelor.pdf")


@app.route('/android')
def android():
    return send_from_directory('static', path="files/udemy_java.pdf")


@app.route('/language')
def language():
    return send_from_directory('static', path="files/Abitur.pdf")


@app.route('/about_me')
def about_me():
    numbers = [55, 20, 10, 17, 3]
    labels = ['Work And Code', 'Spend Time With My Horse', 'Read', 'Meet Friends', 'Drink Coffee']
    fig1, ax1 = plt.subplots()
    ax1.pie(numbers, labels=labels)
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return render_template("about_me.html", image_base64=image_base64)

@app.route('/projects')
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run(debug=True)
