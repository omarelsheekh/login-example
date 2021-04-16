from flask import Blueprint, url_for, request, flash, session, redirect
from models import UserModel
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.oauth2.credentials, google_auth_oauthlib.flow, os, string, random
from googleapiclient.discovery import build

CREDS_FILE='/tmp/google_creds.json'
REDIRECT_URI=os.getenv('domain_name', 'http://localhost:8000')

def google_auth_blueprint(db):
    google_auth = Blueprint('google_auth', __name__)
    
    @google_auth.route('/login')
    def login():
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CREDS_FILE,
            # all scopes: https://developers.google.com/identity/protocols/oauth2/scopes
            scopes=['openid',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'])

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = url_for('google_auth.callback', _external=True)

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, session['state'] = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        return redirect(authorization_url)

    @google_auth.route('/callback')
    def callback():
        state = session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CREDS_FILE,
            # all scopes: https://developers.google.com/identity/protocols/oauth2/scopes
            scopes=['openid',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'],
            state=state)
        flow.redirect_uri = url_for('google_auth.callback', _external=True)
        authorization_response = request.url
        # to allow insecure connection
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        flow.fetch_token(authorization_response=authorization_response, )
        credentials = flow.credentials
        # services list: https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
        user_info_service = build(
            serviceName='oauth2', version='v2',credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        user = UserModel.query.filter_by(email=user_info['email']).first() 
        if not user:
            random_password=''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user = UserModel(email=user_info['email'], name=user_info['name'], password=generate_password_hash(random_password, method='sha256'))
            # add the new user to the database
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('index'))

    return google_auth
# reference: https://developers.google.com/identity/protocols/oauth2/web-server