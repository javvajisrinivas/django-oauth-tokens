# Introduction

Application for getting, storing and refreshing OAuth access_tokens for
Django standalone applications without user manipulations.
Applications also can imitate authorized requests on behalf of user

# Providers

## Vkontakte

    OAUTH_TOKENS_VKONTAKTE_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_VKONTAKTE_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_VKONTAKTE_SCOPE = ['ads,wall,photos,friends,stats']    # application scopes
    OAUTH_TOKENS_VKONTAKTE_USERNAME = ''                                # user login
    OAUTH_TOKENS_VKONTAKTE_PASSWORD = ''                                # user password
    OAUTH_TOKENS_VKONTAKTE_PHONE_END = ''                               # last 4 digits of user mobile phone

## Facebook

    OAUTH_TOKENS_FACEBOOK_CLIENT_ID = ''                                # application ID
    OAUTH_TOKENS_FACEBOOK_CLIENT_SECRET = ''                            # application secret key
    OAUTH_TOKENS_FACEBOOK_SCOPE = ['offline_access']                    # application scopes
    OAUTH_TOKENS_FACEBOOK_USERNAME = ''                                 # user login
    OAUTH_TOKENS_FACEBOOK_PASSWORD = ''                                 # user password

# Settings

    OAUTH_TOKENS_HISTORY = True # to keep in DB expired access tokens

# Dependencies

* Django
* oauth2 service depends on http://github.com/ryanhorn/tyoiOAuth2.git
* requests (pip install requests)