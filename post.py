import datetime
from dateutil.parser import isoparse
import cgi
from bson.objectid import ObjectId
from helper_functions import *


class Post:

    def __init__(self, default_config):
        self.collection = default_config['POSTS_COLLECTION']
        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']


    def delete_all_posts(self):
        """
        Deletes posts. I used 999999 as a limit, to change if the
        team actually hits that amount.
        """
        cursor = self.collection.find({}).limit(999999)

        for post in cursor:
            self.delete_post(post['_id'])


    def get_posts(self, limit, skip, tag=None, search=None, direction=-1):
        """
        Returns post sorted by date created

        :type limit: int
        :type skip: int
        :type tag: str
        :type search: str

        :rtype: dict
        :example:
            {'error': None,
             'data': [{
                        # data schema
                        'date':,
                        'attack_pattern_type':,
                        ...
                        },]
        """
        self.response['error'] = None
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'incident_title': {'$regex': search, '$options': 'i'}},
                    {'incident_description': {'$regex': search, '$options': 'i'}}]}
        try:
            cursor = self.collection.find(cond).sort(
                'date', direction=direction).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'comments' not in post:
                    post['comments'] = []

                self.response['data'].append({
                    'id': post['_id'],
                    'incident_title': post['incident_title'],
                    'incident_preview': post['incident_preview'],
                    'incident_description': post['incident_description'],
                    'incident_categories': post['incident_categories'],
                    'victim_targetting': post['victim_targetting'],
                    'attack_pattern_type_capec_id': \
                        post['attack_pattern_type_capec_id'],
                    'attack_pattern_type': post['attack_pattern_type'],
                    'exploit_targets': post['exploit_targets'],
                    'initial_compromise': post['initial_compromise'],
                    'incident_reported': post['incident_reported'],
                    'loss_crypto': post['loss_crypto'],
                    'loss_usd': post['loss_usd'],
                    'description_geographical': post['description_geographical'],
                    'references': post['references'],
                    'advanced': post['advanced'],

                    'date': post['date'],
                    'permalink': post['permalink'],
                    'author': post['author'],
                    'comments': post['comments']})

        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response

    def get_posts_usd(self, limit, skip, direction=-1):
        """
        This is intended for
        /incident_list/usd/ascending
        /incident_list/usd/descending

        :type limit: int
        :type skip: int
        :type direction: int (-1 or 1) default = -1

        :rtype: dict
        :example:
            {'error': None,
             'data': [{
                        # data schema
                        'date':,
                        'attack_pattern_type':,
                        ...
                        },]
        """
        self.response['error'] = None

        try:
            cursor = self.collection.find({}).sort(
                'loss_usd', direction=direction).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'comments' not in post:
                    post['comments'] = []

                self.response['data'].append({
                    'id': post['_id'],
                    'incident_title': post['incident_title'],
                    'incident_preview': post['incident_preview'],
                    'incident_description': post['incident_description'],
                    'incident_categories': post['incident_categories'],
                    'victim_targetting': post['victim_targetting'],
                    'attack_pattern_type_capec_id': \
                        post['attack_pattern_type_capec_id'],
                    'attack_pattern_type': post['attack_pattern_type'],
                    'exploit_targets': post['exploit_targets'],
                    'initial_compromise': post['initial_compromise'],
                    'incident_reported': post['incident_reported'],
                    'loss_crypto': post['loss_crypto'],
                    'loss_usd': post['loss_usd'],
                    'description_geographical': post['description_geographical'],
                    'references': post['references'],
                    'advanced': post['advanced'],

                    'date': post['date'],
                    'permalink': post['permalink'],
                    'author': post['author'],
                    'comments': post['comments']})

        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response

    def get_posts_title(self, limit, skip, direction=-1):
        """
        This is intended for
        /incident_list/title/ascending
        /incident_list/title/descending

        :type limit: int
        :type skip: int
        :type direction: int (-1 or 1) default = -1

        :rtype: dict
        :example:
            {'error': None,
             'data': [{
                        # data schema
                        'date':,
                        'attack_pattern_type':,
                        ...
                        },]
        """
        self.response['error'] = None

        try:
            cursor = self.collection.find().sort(
                'incident_title', direction=direction
            ).skip(skip).limit(limit)

            self.response['data'] = []
            for post in cursor:
                if 'comments' not in post:
                    post['comments'] = []

                self.response['data'].append({
                    'id': post['_id'],
                    'incident_title': post['incident_title'],
                    'incident_preview': post['incident_preview'],
                    'incident_description': post['incident_description'],
                    'incident_categories': post['incident_categories'],
                    'victim_targetting': post['victim_targetting'],
                    'attack_pattern_type_capec_id': \
                        post['attack_pattern_type_capec_id'],
                    'attack_pattern_type': post['attack_pattern_type'],
                    'exploit_targets': post['exploit_targets'],
                    'initial_compromise': post['initial_compromise'],
                    'incident_reported': post['incident_reported'],
                    'loss_crypto': post['loss_crypto'],
                    'loss_usd': post['loss_usd'],
                    'description_geographical': post['description_geographical'],
                    'references': post['references'],
                    'advanced': post['advanced'],

                    'date': post['date'],
                    'permalink': post['permalink'],
                    'author': post['author'],
                    'comments': post['comments']})

        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response

    def get_posts_category(self, limit, skip, direction=-1):
        """
        This is intended for
        /incident_list/category/ascending
        /incident_list/category/descending

        :type limit: int
        :type skip: int
        :type direction: int (-1 or 1) default = -1

        :rtype: dict
        :example:
            {'error': None,
             'data': [{
                        # data schema
                        'date':,
                        'attack_pattern_type':,
                        ...
                        },]
        """
        self.response['error'] = None

        try:
            cursor = self.collection.find({}).sort(
                'incident_categories', direction=direction).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'comments' not in post:
                    post['comments'] = []

                self.response['data'].append({
                    'id': post['_id'],
                    'incident_title': post['incident_title'],
                    'incident_preview': post['incident_preview'],
                    'incident_description': post['incident_description'],
                    'incident_categories': post['incident_categories'],
                    'victim_targetting': post['victim_targetting'],
                    'attack_pattern_type_capec_id': \
                        post['attack_pattern_type_capec_id'],
                    'attack_pattern_type': post['attack_pattern_type'],
                    'exploit_targets': post['exploit_targets'],
                    'initial_compromise': post['initial_compromise'],
                    'incident_reported': post['incident_reported'],
                    'loss_crypto': post['loss_crypto'],
                    'loss_usd': post['loss_usd'],
                    'description_geographical': post['description_geographical'],
                    'references': post['references'],
                    'advanced': post['advanced'],

                    'date': post['date'],
                    'permalink': post['permalink'],
                    'author': post['author'],
                    'comments': post['comments']})

        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response

    def get_posts_date_reported(self, limit, skip, direction=-1):
        """
        This is intended for
        /incident_list/date_reported/ascending
        /incident_list/date_reported/descending

        :type limit: int
        :type skip: int
        :type direction: int (-1 or 1) default = -1

        :rtype: dict
        :example:
            {'error': None,
             'data': [{
                        # data schema
                        'date':,
                        'attack_pattern_type':,
                        ...
                        },]
        """
        self.response['error'] = None

        try:
            cursor = self.collection.find({}).sort(
                'incident_reported', direction=direction).skip(skip).limit(limit)
            self.response['data'] = []
            for post in cursor:
                if 'comments' not in post:
                    post['comments'] = []

                self.response['data'].append({
                    'id': str(post['_id']),
                    'incident_title': post['incident_title'],
                    'incident_preview': post['incident_preview'],
                    'incident_description': post['incident_description'],
                    'incident_categories': post['incident_categories'],
                    'victim_targetting': post['victim_targetting'],
                    'attack_pattern_type_capec_id': \
                        post['attack_pattern_type_capec_id'],
                    'attack_pattern_type': post['attack_pattern_type'],
                    'exploit_targets': post['exploit_targets'],
                    'initial_compromise': post['initial_compromise'],
                    'incident_reported': post['incident_reported'],
                    'loss_crypto': post['loss_crypto'],
                    'loss_usd': post['loss_usd'],
                    'description_geographical': post['description_geographical'],
                    'references': post['references'],
                    'advanced': post['advanced'],

                    'date': post['date'],
                    'permalink': post['permalink'],
                    'author': post['author'],
                    'comments': post['comments']})

        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Posts not found..'

        return self.response
    def get_post_by_permalink(self, permalink):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.find_one(
                {'permalink': permalink})
        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Post not found..'

        return self.response

    def get_post_by_id(self, post_id):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.find_one(
                {'_id': ObjectId(post_id)})
            if self.response['data']:
                if 'tags' not in self.response['data']:
                    self.response['data']['tags'] = ''
                else:
                    self.response['data']['tags'] = ','.join(
                        self.response['data']['tags'])
        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Post not found..'

        return self.response

    def get_total_count(self, tag=None, search=None):
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'incident_title': {'$regex': search, '$options': 'i'}},
                    {'incident_description': {'$regex': search, '$options': 'i'}}]}

        return self.collection.find(cond).count()

    def get_tags(self):
        self.response['error'] = None
        try:
            self.response['data'] = list(self.collection.aggregate([
                {'$unwind': '$tags'},
                {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10},
                {'$project': {'title': '$_id', 'count': 1, '_id': 0}}
            ]))
        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Get tags error..'

        return self.response

    def create_new_post(self, post_data):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.insert(post_data)
        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Adding post error..'

        return self.response

    def edit_post(self, post_id, post_data):
        self.response['error'] = None

        del post_data['date']
        #del post_data['permalink']

        try:
            self.collection.update(
                {'_id': ObjectId(post_id)}, {"$set": post_data}, upsert=False)
            self.response['data'] = True

        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Post update error..'

        return self.response

    def delete_post(self, post_id):
        self.response['error'] = None
        try:
            if self.get_post_by_id(post_id) and self.collection.remove({'_id': ObjectId(post_id)}):
                self.response['data'] = True
            else:
                self.response['data'] = False
        except Exception as e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Deleting post error..'

        return self.response

    @staticmethod
    def validate_post_data(post_data):
        """
        Validates post data by converting &, <, > into
        HTML safe sequences. Appends permalink to the post_data

        :param post_data:
            Dictionary of post data consists of the following string keys:
                'id'
                'incident_title'
                'incident_description'
                'incident_categories'
                'victim_targetting'
                'attack_pattern_type_capec_id'
                'attack_pattern_type'
                'exploit_targets'
                'initial_compromise'
                'incident_reported'
                'loss_crypto'
                'loss_usd'
                'description_geographical'
                'references'
                'advanced'
                'author'
                'comments'

        :type post_data: dictionary

        :return: post_data with escaped fields + permalink + date
            Dictionary of out post data consists of the following string keys:
                'id'
                'incident_title'
                'incident_description'
                'incident_categories'
                'victim_targetting'
                'attack_pattern_type_capec_id'
                'attack_pattern_type'
                'exploit_targets'
                'initial_compromise'
                'incident_reported'
                'loss_crypto'
                'loss_usd'
                'description_geographical'
                'references'
                'advanced'
                'author'
                'comments'
            ADDED by this method
            +   'date'
            +   'permalink'

        :rtype: dictionary
        """
        # 26 ascii_uppercase + 10 digit
        # 12 characters 
        # 4.7383813e+18 possible combinations 
        # Quite unlikely for a collision to happen
        permalink = random_string(12)


        # Escape user input fields
        post_data['incident_title'] = \
            str(cgi.escape(post_data['incident_title']))
        post_data['incident_description'] = cgi.escape(post_data['incident_description'], quote=True)
        description = post_data['incident_description']

        # get an incident_preview
        post_data['incident_preview'] = (description[:150] + "...") if \
                                            len(description) > 150 \
                                            else description


        try:
            post_data['incident_categories'] = \
                cgi.escape(post_data['incident_categories'])
        except:
            post_data['incident_categories'] = None

        try:
            post_data['victim_targetting'] = \
                cgi.escape(post_data['victim_targetting'])
        except:
            post_data['victim_targetting'] = None

        try:
            post_data['attack_pattern_type_capec_id'] = \
                cgi.escape(post_data['attack_pattern_type_capec_id'])
        except:
            post_data['attack_pattern_type_capec_id'] = None

        try:
            post_data['attack_pattern_type'] = \
                cgi.escape(post_data['attack_pattern_type'])
        except:
            post_data['attack_pattern_type'] = None

        try:
            post_data['exploit_targets'] = \
                cgi.escape(post_data['exploit_targets'])
        except:
            post_data['exploit_targets'] = None

        try:
            post_data['initial_compromise'] = \
                isoparse(cgi.escape(post_data['initial_compromise']))
        except:
            post_data['initial_compromise'] = None

        try:
            post_data['incident_reported'] = \
                isoparse(cgi.escape(post_data['incident_reported']))
        except:
            post_data['incident_reported'] = None

        try:
            post_data['loss_crypto'] = cgi.escape(post_data['loss_crypto'])
        except:
            post_data['loss_crypto'] = None

        try:
            # Convert to Float
            post_data['loss_usd'] = float(cgi.escape(post_data['loss_usd']))
        except:
            post_data['loss_usd'] = None

        try:
            post_data['description_geographical'] = \
                cgi.escape(post_data['description_geographical'])
        except:
            post_data['description_geographical'] = None

        try:
            post_data['references'] = cgi.escape(post_data['references'])
        except:
            post_data['references'] = None

        try:
            post_data['advanced'] = cgi.escape(post_data['advanced'])
        except:
            post_data['advanced'] = None

        # append to to post_data
        post_data['date'] = datetime.datetime.utcnow()
        post_data['permalink'] = permalink

        print(post_data)

        return post_data

    @staticmethod
    def print_debug_info(msg, show=False):
        if show:
            import sys
            import os

            error_color = '\033[32m'
            error_end = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                     'line': sys.exc_info()[2].tb_lineno,
                     'details': str(msg)}

            print(error_color)
            print('\n\n---\nError type: %s in file: %s on line: %s\nError \
                  details: %s\n---\n\n'\
                  % (error['type'], error['file'], error['line'],
                     error['details']))
            print(error_end)
