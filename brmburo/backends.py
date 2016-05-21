import re
import logging
from passlib.hash import md5_crypt
from models import Buddy

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
                                    user.email = email
                                    # user invalidation
                                    if not is_member:
                                        user.is_superuser = False
                                        user.is_staff = False
                                    user.save()
                                    # TODO we could update email here if it changed, but it's not used for anything
                                except User.DoesNotExist:
                                    if is_member:
                                        try:
                                            buddy = Buddy.objects.get(nickname__iexact=username)
                                            user = User.objects.create(username=username, email=email, password="")
                                            buddy.user = user
                                            buddy.save()
                                        except Buddy.DoesNotExist:
                                            logging.info("Buddy %s does not exist", username)
                                            return None
                                    else:
                                        return None


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
