
'''
Allauth configuration, see also:
http://rdmo.readthedocs.io/en/latest/configuration/authentication/allauth.html
'''

ACCOUNT = True
ACCOUNT_SIGNUP = True
SOCIALACCOUNT = True

INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.dummy',
#     'allauth.socialaccount.providers.github',
#     'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.orcid',
#     'allauth.socialaccount.providers.twitter',
]

SOCIALACCOUNT_PROVIDERS = {
    'orcid': {
        # Base domain of the API. Default value: 'orcid.org', for the production API
        'BASE_DOMAIN': 'sandbox.orcid.org',  # for the sandbox API
        # Member API or Public API? Default: False (for the public API)
        'MEMBER_API': True,  # for the member API
        'APP' : {
            "client_id" : "APP-XXXXXXXXXXXXXXXX",
            "secret" : "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        }
    },
}

AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')
MIDDLEWARE.append('allauth.account.middleware.AccountMiddleware')
