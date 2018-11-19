from flask import render_template, Blueprint, session, redirect, url_for, flash
import pymysql

mod = Blueprint('pages', __name__)


@mod.route('/', methods=['GET'])
def home_page():
    # if user logged in, go to dashboard, otherwise go to login page
    if 'user' in session:
        return redirect(url_for('pages.dashboard_page'))
    else:
        return render_template('home.html')


@mod.route('/about', methods=['GET'])
def about_page():
    # render the about page
    return render_template('about.html')


@mod.route('/dashboard', methods=['GET'])
def dashboard_page():
    # if the user's session exists, render the dashboard
    if 'user' in session:
        flash("Successfully logged in as %s!" % session['user'], "success")

        songs = {
            "angry": [],
            "happy": [],
            "motivational": [],
            "relaxing": [],
            "sad": []
        }

        email = session.get('user', None)
        query = "SELECT songemotions.* FROM usersongs INNER JOIN songemotions ON usersongs.songurl=songemotions.songurl WHERE email='%s'" % email


        conn = pymysql.connect(
            host="localhost",
            user="testuser",
            password="password",
            db="musicemotions"
        )

        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(query)

        user_songs = cur.fetchall()
        for row in user_songs:
            songs[row['emotion']].append(row['songurl'])

        return render_template('dashboard.html', songs=songs)
    # otherwise redirect to the login page and flash an error
    else:
        flash("Access unauthorized. Please login first.", "error")
        return redirect(url_for('pages.home_page'))
