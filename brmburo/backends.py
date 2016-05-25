import re
import logging
from passlib.hash import md5_crypt
from django.contrib.auth.backends import ModelBackend
from models import Buddy

from django.contrib.auth.models import User
from .settings.local import DOKUWIKI_USERS_FILE

from collections import namedtuple

logger = logging.getLogger(__name__)


class DokuwikiAuthBackend(ModelBackend):

    AuthStruct = namedtuple('MyStruct', ('login', 'hash', 'email', 'roles', 'is_member', 'is_council', 'is_admin'))

    def _load_docuwiki_authfile(self):
        try:
            with open(DOKUWIKI_USERS_FILE) as authfile:
                for line in authfile:
                    line = line.rstrip()
                    if re.match(r"\s*(?:#.*)", line):  # skip comments and empty lines
                        continue

                    parts = line.split(":")
                    if len(parts) != 5:  # skip badly formatted lines
                        continue

                    roles = parts[4].split(",")
                    is_member = "member" in roles
                    is_council = "council" in roles
                    is_admin = "admin" in roles

                    yield self.AuthStruct(
                        parts[0],
                        parts[1],
                        parts[3],
                        roles,
                        is_member,
                        is_council,
                        is_admin,
                    )

        except (OSError, IOError):
            logging.exception("Cannot read dokuwiki users file, bailing.")

    def authenticate(self, username=None, password=None, **kw):
        username = username.encode("utf-8")
        password = password.encode("utf-8")

        for auth in self._load_docuwiki_authfile():

            if auth.login != username:  # skip username mismatch
                continue

            try:
                if md5_crypt.verify(password, auth.hash):
                    try:
                        user = User.objects.get(username=username)

                        # if user is superuser authenticate using django password
                        if user.is_superuser or user.is_staff:
                            return super(DokuwikiAuthBackend,self).authenticate(username, password, **kw)

                        # update user
                        user.email = auth.email
                        # user invalidation
                        if not auth.is_member:
                            user.is_superuser = False
                            user.is_staff = False
                        user.save()

                    except User.DoesNotExist:
                        if auth.is_member:
                            try:
                                buddy = Buddy.objects.get(nickname__iexact=username)
                                user = User.objects.create(username=username, email=auth.email, password="")
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

        # No user found, authenthication failed
        return None

