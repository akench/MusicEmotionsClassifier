from flask import render_template, Blueprint, session, redirect, url_for, flash
import pymysql
from app.views.db_manager import get_songs_for_user

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

        email = session.get('user', None)

        if email is not None:
            rows, errno = get_songs_for_user(email)

            # check if there was an error
            if errno != 0:
                flash("There was an unknown error getting your song library", "error")
                return render_template('dashboard.html', songs={})
            else:
                organized_songs = organize_songs_by_emot(rows)
                return render_template('dashboard.html', songs=organized_songs)
        else:
            return redirect(url_for('pages.home_page'))
    # otherwise not logged in, redirect to the login page
    else:
        flash("Access unauthorized. Please login first.", "error")
        return redirect(url_for('pages.home_page'))


def organize_songs_by_emot(rows):
    '''
    Takes the raw database output, of list of dictionaries and organizes
    them by emotion, to be displayed on the page

    Args:
        rows (list of dicts): raw database output

    Returns:
        dict : songs sorted by emotion
    '''
    songs = {}

    for row in rows:
        emot = row['emotion']
        vid_id = row['vid_id']
        title = row['title']

        if emot not in songs:
            songs[emot] = []

        songs[emot].append(
            {
                'url': 'https://www.youtube.com/embed/%s' % vid_id,
                'title': title
            }
        )

    return songs