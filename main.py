from flask import Flask, render_template, request
import requests
import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
TO = os.environ.get("TO")

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        subject = "New Contact Form Submission"
        body = f"""
                Dear [Recipient's Name],

                You have received a new message from your contact form:

                Name: {name}
                Email: {email}
                Phone: {phone}
                Message: {message}

                Best regards,
                [Your Name]
                [Your Position]
                [Your Company]
                """
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=TO,
                msg=f"Subject: {subject}\n\n{body}"
            )
        return render_template("contact.html", display="Successfully sent your message")
    return render_template("contact.html", display="Contact Me")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
