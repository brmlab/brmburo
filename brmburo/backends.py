import re
import logging
from passlib.hash import md5_crypt

from django.contrib.auth.models import User
from .settings.local import DOKUWIKI_USERS_FILE

logger = logging.getLogger(__name__)

class DokuwikiAuthBackend(object):

    def authenticate(self, username, password):
        username = username.encode("utf-8")
        password = password.encode("utf-8")

        try:
            with open(DOKUWIKI_USERS_FILE) as authfile:
                    for line in authfile:
                        line = line.rstrip()
                        if re.match("\\s*(?:#.*)", line): # skip comments and empty lines
                            continue

                        parts = line.split(":")
                        if len(parts) != 5: # skip badly formatted lines
                            continue

                        login = parts[0]
                        if login != username:
                            continue

                        hash = parts[1]
                        email = parts[3]
                        roles = parts[4].split(",")

                        is_member = "member" in roles
                        is_council = "council" in roles
                        is_admin = "admin" in roles

                        try:
                            if md5_crypt.verify(password, hash):
                                try:
                                    user = User.objects.get(username=username)
                                except User.DoesNotExist:
                                    user = User.objects.create(username=username, email=email, password="")

                                return user

                        except ValueError:
                            logging.exception("Cannot verify user")
                            continue
        except OSError, IOError:
            logging.exception("Cannot read dokuwiki users file, bailing.")

        # No user found, authenthication failed
        return None

    def get_user(self, user_id):
        if user_id is None:
            return None
        user = User.objects.get(pk=user_id)
        return user
