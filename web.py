import os
import cgi
from flask import Flask, render_template, abort, \
        url_for, request, flash, session, redirect, jsonify, json
from flaskext.markdown import Markdown
from mdx_github_gists import GitHubGistExtension
from mdx_strike import StrikeExtension
from mdx_quote import QuoteExtension
from mdx_code_multiline import MultilineCodeExtension
from werkzeug.contrib.atom import AtomFeed
import post
import user
import pagination
import settings
from helper_functions import *
import csv


app = Flask('IncidentDB')
md = Markdown(app)
md.register_extension(GitHubGistExtension)
md.register_extension(StrikeExtension)
md.register_extension(QuoteExtension)
md.register_extension(MultilineCodeExtension)
app.config.from_object('config')


@app.route('/', defaults={'page': 1})
@app.route('/page-<int:page>')
@login_required()
def index(page):
    # Use posts view 
    # print(session['user'])
    return redirect(url_for('posts'))

    # original index view

    # skip = (page - 1) * int(app.config['PER_PAGE'])
    # posts = postClass.get_posts(int(app.config['PER_PAGE']), skip)
    # count = postClass.get_total_count()
    # pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    # return render_template('index.html',
    #                        posts=posts['data'],
    #                        pagination=pag,
    #                        meta_title=app.config['BLOG_TITLE'])


# TODO create api key system for authenticated users to access
@app.route('/data')
@login_required()
def data():
    """
    JSON API output for database data for external development use
    """
    # set 999999 as limit to change once if this is actually reached
    posts = postClass.get_posts_date_reported(999999, 0, 1)
    jsonified = jsonify(posts['data'])
    return jsonified


@app.route('/analytics')
@login_required()
def analytics():
    """
    Analytics for database
    """
    posts = postClass.get_posts_date_reported(999999, 0, 1)

    # Note we use flask json here not python inbuilt json
    json_file = json.dumps(posts['data'], ensure_ascii=True)
    return render_template('analytics.html', post=json_file)


@app.route('/tag/<tag>', defaults={'page': 1})
@app.route('/tag/<tag>/page-<int:page>')
@login_required()
def posts_by_tag(tag, page):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts(int(app.config['PER_PAGE']), skip, tag=tag)
    count = postClass.get_total_count(tag=tag)
    if not posts['data']:
        abort(404)
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts by tag: ' + tag)


@app.route('/incident/<permalink>')
@login_required()
def single_post(permalink):
    post = postClass.get_post_by_permalink(permalink)
    if not post['data']:
        abort(404)
    return render_template('single_incident.html', post=post['data'],
                           meta_title=app.config['BLOG_TITLE'] + '::' +
                           post['data']['incident_title'])


@app.route('/q/<query>', defaults={'page': 1})
@app.route('/q/<query>/page-<int:page>')
@login_required()
def search_results(page, query):
    skip = (page - 1) * int(app.config['PER_PAGE'])
    if query:
        posts = postClass.get_posts(
            int(app.config['PER_PAGE']), skip, search=query)
    else:
        posts = []
        posts['data'] = []
    count = postClass.get_total_count(search=query)
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)
    return render_template('index.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Search results')


@app.route('/search', methods=['GET', 'POST'])
@login_required()
def search():
    if request.method != 'POST':
        return redirect(url_for('index'))

    query = request.form.get('query', None)
    if query:
        return redirect(url_for('search_results', query=query))
    else:
        return redirect(url_for('index'))


@app.route('/new_incident', methods=['GET', 'POST'])
@login_required()
def new_post():
    """
    Stores the post data from /new_incident into MongoDB
    """
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        title = request.form.get('incident_title').strip()
        description = request.form.get('incident_description')

        if not title \
           or not description:
            error = True

        else:
            # Sanitize data
            try:
                incident_categories = \
                    request.form.get('incident_categories').strip()
            except:
                incident_categories = None

            try:
                victim_targetting = \
                    request.form.get('victim_targetting').strip()
            except:
                victim_targetting = None

            try:
                attack_pattern_type_capec_id = \
                    request.form.get('attack_pattern_type_capec_id').strip()
            except:
                attack_pattern_type_capec_id = None

            try:
                attack_pattern_type = \
                    request.form.get('attack_pattern_type').strip()
            except:
                attack_pattern_type = None

            try:
                exploit_targets = \
                    request.form.get('exploit_targets').strip()
            except:
                exploit_targets = None

            try:
                initial_compromise = \
                    request.form.get('initial_compromise').strip()
            except:
                initial_compromise = None

            try:
                incident_reported = \
                        request.form.get('incident_reported').strip()
            except:
                incident_reported = None

            try:
                loss_crypto = request.form.get('loss_crypto').strip()
            except:
                loss_crypto = None

            try:
                loss_usd = request.form.get('loss_usd').strip()
            except:
                loss_usd = None

            try:
                description_geographical = \
                    request.form.get('description_geographical').strip(),

                # request.form.get gives tuple we take the first value
                description_geographical = description_geographical[0]
            except:
                description_geographical = None

            try:
                references = request.form.get('references').strip()
            except:
                references = None

            try:
                advanced = request.form.get('advanced').strip()
            except:
                advanced = None

            # Data dictionary to input into MongoDB 
            post_data = {
                'incident_title': title,
                'incident_description': description,
                'incident_categories': incident_categories,
                'victim_targetting': victim_targetting,
                'attack_pattern_type_capec_id': attack_pattern_type_capec_id,
                'attack_pattern_type': attack_pattern_type,
                'exploit_targets': exploit_targets,
                'initial_compromise': initial_compromise,
                'incident_reported': incident_reported,
                'loss_crypto': loss_crypto,
                'loss_usd': loss_usd,
                'description_geographical': description_geographical,
                'references': references,
                'advanced': advanced,

                'author': session['user']['username']}

            # Check for escape
            # print("Part A")
            # print(post_data)
            # print()
            # print()
            # print("Part B")
            post = postClass.validate_post_data(post_data)

            # Temporarily remove post preview this function is unavailble on
            # front-end
            if request.form.get('post-preview') == '1':
                session['post-preview'] = post
                session['post-preview']['action'] = 'edit' \
                    if request.form.get('post-id') else 'add'
                if request.form.get('post-id'):
                    session['post-preview']['redirect'] = \
                            url_for('post_edit',
                                    id=request.form.get('post-id'))
                else:
                    session['post-preview']['redirect'] = url_for('new_post')
                return redirect(url_for('post_preview'))
            else:
                session.pop('post-preview', None)

                # if post-id == True, the post exists, we edit the post instead
                if request.form.get('post-id'):
                    response = postClass.edit_post(
                        request.form['post-id'], post)
                    if not response['error']:
                        flash('Incident updated!', 'success')
                    else:
                        flash(response['error'], 'error')
                    return redirect(url_for('posts'))

                # if post-id == False, the post doesn't exist, we create a new
                # post
                else:
                    response = postClass.create_new_post(post)
                    if response['error']:
                        error = True
                        error_type = 'post'
                        flash(response['error'], 'error')
                    else:
                        flash('New incident created!', 'success')
    else:
        if session.get('post-preview') \
           and session['post-preview']['action'] == 'edit':
            session.pop('post-preview', None)
    return render_template('new_incident.html',
                           meta_title='New Incident',
                           error=error,
                           error_type=error_type)


@app.route('/incident_preview')
@login_required()
def post_preview():
    post = session.get('post-preview')
    return render_template('preview.html',
                           post=post,
                           meta_title='Preview post::'
                           + post['incident_title'])


@app.route('/incidents_list', defaults={'page': 1})
@app.route('/incidents_list/page-<int:page>')
@login_required()
def posts(page):
    """
    List incidents based on time created
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts(int(app.config['PER_PAGE']), skip)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/usd/ascending', defaults={'page': 1})
@app.route('/incidents_list/usd/ascending/page-<int:page>')
@login_required()
def posts_usd_ascending(page):
    """
    List incidents based on the amount of USD lost
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_usd(int(app.config['PER_PAGE']), skip, 1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/usd/descending', defaults={'page': 1})
@app.route('/incidents_list/usd/descending/page-<int:page>')
@login_required()
def posts_usd_descending(page):
    """
    List incidents based on the amount of USD lost
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_usd(int(app.config['PER_PAGE']), skip, -1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/title/ascending', defaults={'page': 1})
@app.route('/incidents_list/title/ascending/page-<int:page>')
@login_required()
def posts_title_ascending(page):
    """
    List incidents based on name
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_title(int(app.config['PER_PAGE']), skip, 1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/title/descending', defaults={'page': 1})
@app.route('/incidents_list/title/descending/page-<int:page>')
@login_required()
def posts_title_descending(page):
    """
    List incidents based on name
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_title(int(app.config['PER_PAGE']), skip, -1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/category/ascending', defaults={'page': 1})
@app.route('/incidents_list/category/ascending/page-<int:page>')
@login_required()
def posts_category_ascending(page):
    """
    List incidents based on name
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_category(int(app.config['PER_PAGE']), skip, 1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/category/descending', defaults={'page': 1})
@app.route('/incidents_list/category/descending/page-<int:page>')
@login_required()
def posts_category_descending(page):
    """
    List incidents based on name
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_category(int(app.config['PER_PAGE']), skip, -1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/date_reported/ascending', defaults={'page': 1})
@app.route('/incidents_list/date_reported/ascending/page-<int:page>')
@login_required()
def posts_date_reported_ascending(page):
    """
    List incidents based on name
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_date_reported(int(app.config['PER_PAGE']), skip, 1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incidents_list/date_reported/descending', defaults={'page': 1})
@app.route('/incidents_list/date_reported/descending/page-<int:page>')
@login_required()
def posts_date_reported_descending(page):
    """
    List incidents based on name
    """
    session.pop('post-preview', None)
    skip = (page - 1) * int(app.config['PER_PAGE'])
    posts = postClass.get_posts_date_reported(int(app.config['PER_PAGE']), skip, -1)
    count = postClass.get_total_count()
    pag = pagination.Pagination(page, app.config['PER_PAGE'], count)

    if not posts['data']:
        abort(404)

    return render_template('incidents.html',
                           posts=posts['data'],
                           pagination=pag,
                           meta_title='Posts')


@app.route('/incident_edit?id=<id>')
@login_required()
def post_edit(id):
    post = postClass.get_post_by_id(id)
    if post['error']:
        flash(post['error'], 'error')
        return redirect(url_for('posts'))

    if session.get('post-preview') and \
       session['post-preview']['action'] == 'add':
        session.pop('post-preview', None)
    return render_template('edit_incident.html',
                           meta_title='Edit post::' + \
                            post['data']['incident_title'],
                           post=post['data'],
                           error=False,
                           error_type=False)


@app.route('/incident_delete?id=<id>')
@login_required()
def post_del(id):
    response = postClass.delete_post(id)
    if response['data'] is True:
        flash('Incident removed!', 'success')
    else:
        flash(response['error'], 'error')

    return redirect(url_for('posts'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    error_type = 'validate'
    if request.method == 'POST':
        username = request.form.get('login-username')
        password = request.form.get('login-password')
        if not username or not password:
            error = True
        else:
            user_data = userClass.login(username.lower().strip(), password)
            if user_data['error']:
                error = True
                error_type = 'login'
                flash(user_data['error'], 'error')
            else:
                userClass.start_session(user_data['data'])
                flash('You are logged in!', 'success')
                return redirect(url_for('posts'))
    else:
        if session.get('user'):
            return redirect(url_for('posts'))

    return render_template('login.html',
                           meta_title='Login',
                           error=error,
                           error_type=error_type)


@app.route('/logout')
def logout():
    if userClass.logout():
        flash('You are logged out!', 'success')
    return redirect(url_for('login'))


@app.route('/users')
@login_required()
def users_list():
    users = userClass.get_users()
    return render_template('users.html',
                           users=users['data'],
                           meta_title='Users')


@app.route('/add_user')
@login_required()
@superuser()
def add_user():
    gravatar_url = userClass.get_gravatar_link()
    return render_template('add_user.html',
                           gravatar_url=gravatar_url,
                           meta_title='Add user')


@app.route('/edit_user?id=<id>')
@login_required()
def edit_user(id):
    user = userClass.get_user(id)
    return render_template('edit_user.html',
                           user=user['data'],
                           meta_title='Edit user')


@app.route('/delete_user?id=<id>')
@login_required()
@superuser()
def delete_user(id):
    if id != session['user']['username']:
        user = userClass.delete_user(id)
        if user['error']:
            flash(user['error'], 'error')
        else:
            flash('User deleted!', 'success')
    return redirect(url_for('users_list'))


@app.route('/save_user', methods=['POST'])
@login_required()
@superuser()
def save_user():
    post_data = {
        '_id': request.form.get('user-id', None).lower().strip(),
        'email': request.form.get('user-email', None),
        'old_pass': request.form.get('user-old-password', None),
        'new_pass': request.form.get('user-new-password', None),
        'new_pass_again': request.form.get('user-new-password-again', None),
        'super': request.form.get('user-super', False) == "True" or \
            request.form.get('user-super', False) == "true",
        'update': request.form.get('user-update', False)
    }

    print(post_data)

    if not post_data['email'] or not post_data['_id']:
        flash('Username and Email are required..', 'error')
        if post_data['update']:
                return redirect(url_for('edit_user', id=post_data['_id']))
        else:
            return redirect(url_for('add_user'))

    else:
        user = userClass.save_user(post_data)
        if user['error']:
            flash(user['error'], 'error')
            if post_data['update']:
                return redirect(url_for('edit_user', id=post_data['_id']))
            else:
                return redirect(url_for('add_user'))
        else:
            message = 'User updated!' if post_data['update'] else 'User added!'
            flash(message, 'success')

    return redirect(url_for('edit_user', id=post_data['_id']))


@app.route('/recent_feed')
@login_required()
def recent_feed():
    feed = AtomFeed('TNO Blockchain Incident Database::Recent Incidents',
                    feed_url=request.url, url=request.url_root)
    posts = postClass.get_posts(int(app.config['PER_PAGE']), 0)
    for _post in posts['data']:
        _post_entry = _post['incident_description']
        feed.add(_post['incident_title'], md(_post_entry),
                 content_type='html',
                 url=make_external(
                     url_for('single_post', permalink=_post['permalink'])),
                 updated=_post['date'])
    return feed.get_response()


@app.route('/settings', methods=['GET', 'POST'])
@login_required()
@superuser()
def blog_settings():
    error = None
    error_type = 'validate'
    if request.method == 'POST':
        blog_data = {
            'title': request.form.get('blog-title', None),
            'description': request.form.get('blog-description', None),
            'per_page': request.form.get('blog-perpage', None),
            'text_search': request.form.get('blog-text-search', None)
        }
        blog_data['text_search'] = 1 if blog_data['text_search'] else 0

        try:
            print("reading file")
            # Settle file upload
            f = request.files['file-upload'].read()

            # Decode f take as utf-8
            f = f.decode('utf-8')

            # Split lines 
            f = f.splitlines()

            # Read the file
            csvreader = csv.reader(f, delimiter=',')

            # Clear database
            print("deleting posts")
            postClass.delete_all_posts()
            print("all posts deleted")

            # skip header and description of headers
            next(csvreader)
            next(csvreader)


            user_data = session.get('user')

            # upload data to database
            for lines in csvreader:
                post_data = {'incident_title': lines[1],
                             'incident_description': lines[2],
                             'incident_categories': lines[3],
                             'victim_targetting': lines[4],
                             'attack_pattern_type_capec_id': lines[5],
                             'attack_pattern_type': lines[6],
                             'exploit_targets': lines[7],
                             'initial_compromise': lines[9],
                             'incident_reported': lines[11],
                             'loss_crypto': lines[12],
                             'loss_usd': lines[13],
                             'description_geographical': lines[14],
                             'references': lines[15],
                             'advanced': '{"misc": "' + lines[16] + '"}',
                             'author': user_data['username']}

                post = postClass.validate_post_data(post_data)
                post_create = postClass.create_new_post(post)

        except Exception as e:
            print(e)
            pass

        for key, value in blog_data.items():
            if not value and key != 'text_search' and key != 'description':
                error = True
                break
        if not error:
            update_result = settingsClass.update_settings(blog_data)
            if update_result['error']:
                flash(update_result['error'], 'error')
            else:
                flash('Settings updated!', 'success')
                return redirect(url_for('blog_settings'))

    return render_template('settings.html',
                           default_settings=app.config,
                           meta_title='Settings',
                           error=error,
                           error_type=error_type)


@app.route('/install', methods=['GET', 'POST'])
def install():
    if session.get('installed', None):
        return redirect(url_for('index'))

    error = False
    error_type = 'validate'
    if request.method == 'POST':
        user_error = False
        blog_error = False

        user_data = {
            '_id': request.form.get('user-id', None).lower().strip(),
            'email': request.form.get('user-email', None),
            'new_pass': request.form.get('user-new-password', None),
            'new_pass_again': request.form.get('user-new-password-again',
                                               None),
            'super': True,
            'update': False
        }

        blog_data = {
            'title': request.form.get('blog-title', None),
            'description': request.form.get('blog-description', None),
            'per_page': request.form.get('blog-perpage', None),
            'text_search': request.form.get('blog-text-search', None)
        }
        blog_data['text_search'] = 1 if blog_data['text_search'] else 0

        for key, value in user_data.items():
            if not value and key != 'update':
                user_error = True
                break
        for key, value in blog_data.items():
            if not value and key != 'text_search' and key != 'description':
                blog_error = True
                break

        if user_error or blog_error:
            error = True
        else:
            install_result = settingsClass.install(blog_data, user_data)

            # Settle file upload
            f = request.files['file-upload'].read()

            # Decode f take as utf-8
            f = f.decode('utf-8')

            # Split lines 
            f = f.splitlines()

            # Read the file
            csvreader = csv.reader(f, delimiter=',')

            # skip header and description of headers
            next(csvreader)
            next(csvreader)

            # upload data to database
            for lines in csvreader:
                post_data = {'incident_title': lines[1],
                             'incident_description': lines[2],
                             'incident_categories': lines[3],
                             'victim_targetting': lines[4],
                             'attack_pattern_type_capec_id': lines[5],
                             'attack_pattern_type': lines[6],
                             'exploit_targets': lines[7],
                             'initial_compromise': lines[9],
                             'incident_reported': lines[11],
                             'loss_crypto': lines[12],
                             'loss_usd': lines[13],
                             'description_geographical': lines[14],
                             'references': lines[15],
                             'advanced': '{"misc": "' + lines[16] + '"}',
                             'author': user_data['_id']}

                post = postClass.validate_post_data(post_data)
                post_create = postClass.create_new_post(post)

            if install_result['error']:
                for i in install_result['error']:
                    if i is not None:
                        flash(i, 'error')
            else:
                session['installed'] = True
                flash('Successfully installed!', 'success')
                user_login = userClass.login(
                    user_data['_id'], user_data['new_pass'])
                if user_login['error']:
                    flash(user_login['error'], 'error')
                else:
                    userClass.start_session(user_login['data'])
                    flash('You are logged in!', 'success')
                    return redirect(url_for('posts'))
    else:
        if settingsClass.is_installed():
            return redirect(url_for('index'))

    return render_template('install.html',
                           default_settings=app.config,
                           error=error,
                           error_type=error_type,
                           meta_title='Install')


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(400)


@app.before_request
def is_installed():
    app.config = settingsClass.get_config()
    app.jinja_env.globals['meta_description'] = app.config['BLOG_DESCRIPTION']
    if not settingsClass.is_installed():
        session['installed'] = False
        if url_for('static', filename='') not in request.path and request.path != url_for('install'):
            return redirect(url_for('install'))


@app.before_request
def set_globals():
    app.jinja_env.globals['csrf_token'] = generate_csrf_token
    app.jinja_env.globals['recent_posts'] = postClass.get_posts(10, 0)['data']
    app.jinja_env.globals['tags'] = postClass.get_tags()['data']


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', meta_title='404'), 404


@app.template_filter('formatdate')
def format_datetime_filter(input_value, format_="%Y-%m-%d"):
    try:
        return input_value.strftime(format_)
    except:
        return None


settingsClass = settings.Settings(app.config)
postClass = post.Post(app.config)
userClass = user.User(app.config)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['meta_description'] = app.config['BLOG_DESCRIPTION']

if not app.config['DEBUG']:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            debug=app.config['DEBUG'])

