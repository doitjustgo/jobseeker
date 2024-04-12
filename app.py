from flask import Flask, render_template, request, redirect, send_file
from scraper import get_pages, save_to_file

app = Flask("job_seeker")

db = {}

@app.route('/')
def main():
    return render_template("home.html")

@app.route('/search')
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs= db[keyword]
    else:
        jobs = get_pages("JAVA")
        db[keyword] =jobs
        return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route('/export')
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?={keyword}")
    else:
        save_to_file(keyword, db[keyword])
        return send_file(f"{keyword}.csv", as_attachment=True,mimetype='text/csv')