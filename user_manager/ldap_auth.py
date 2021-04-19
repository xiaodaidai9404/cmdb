import ldap3
import re
from django.conf import settings

class LdapAuthAPI(object):
    def __init__(self, username, password,):

        self.ldapserver = settings.LDAP_SERVER
        self.ldapadmin = settings.LDAP_ADMIN
        self.admin_password = settings.LDAP_ADMIN_PASSWORD
        self.ldapscbase = settings.LDAP_SCBASE
        self.username = str(username)
        self.password = str(password)


    def get_username_ou(self):
        server = ldap3.Server(self.ldapserver, get_info=all)
        conn = ldap3.Connection(server, self.ldapadmin, self.admin_password,auto_bind=True)
        search_dc = ','.join(self.ldapscbase.split(',')[1:])
        conn.search(search_dc, '(objectclass=person)')
        ldap_list = conn.entries
        ou = str([item for item in ldap_list if re.search(self.username, str(item))][0]).split(',')[1]
        return ou

    def auth(self):
        ou = self.get_username_ou()
        user = "uid=%s,%s,%s" % (self.username, ou, self.ldapscbase)
        c = ldap3.Connection(
            ldap3.Server(self.ldapserver, get_info=ldap3.ALL),
            user=user,
            password=self.password)
        ret = c.bind()
        if ret:
            c.unbind()
            return True
        else:
            return False
