""" A little helper that provides a few methods to work with IIMC's LDAP Server

Connect to IIM Calcutta's LDAP Server. Exposes two helper methods - ldap_authenticate and
ldap_fetch_detail. See their respective documentation for help
"""
__author__ = "Prakhar Srivastav"
__date__ = "$Date: 2012/06/18"
__license__ = "Python"

import ldap, sys
base_dn = "ou=Student,ou=Person,dc=iimcal,dc=ac,dc=in"
searchScope = ldap.SCOPE_SUBTREE

def connect_ldap():
    """Connects to the IIM Calcutta's LDAP Server. Returns None if connection
    successful
    """
    try:
        l = ldap.open(hostname)
        return l
    except ldap.LDAPERROR, e:
        print e
        sys.exit()

def ldap_authenticate(username, password):
    """Authenticate a user against the LDAP Server

    Keyword Arguments:
    username: string
    password: string

    Returns True if authentication successful and False otherwise
    """
    l = connect_ldap()
    retAttr = ['sn']
    searchFilter = "cn=%s" % username

    if l:
        try:
            ldap_result_id = l.search(base_dn, searchScope, searchFilter, retAttr)
            returned_result = l.result(ldap_result_id)
            if returned_result[1]:
                user_dn = returned_result[1][0][0]
                if l.result(l.bind(user_dn, password, ldap.AUTH_SIMPLE))[0] == 97:
                    return True
            else: return False
        except ldap.LDAPError, e:
            return False
        finally:
            l.unbind()

def ldap_fetch_detail(username, attr_list):
    """Fetch details about a list of attributes of a user

    Keyword arguments:
    username: string
    attr_list: list of attrs. Example ['sn', 'batch']

    Returns a dict with keys as attr passed and values as results
    retrived from LDAP. Invalid attrs are not added in dict
    """
    l = connect_ldap()
    retAttr = []
    res = {}
    if l:
        for a in attr_list:
            retAttr.append(a)
        searchFilter = "cn=%s" % username

        try:
            ldap_result_id = l.search(base_dn, searchScope, searchFilter, retAttr)
            returned_result = l.result(ldap_result_id)
            if returned_result[1]:
                user_dict = returned_result[1][0][1]
                for attr in attr_list:
                    if attr in user_dict:
                        res[attr] = user_dict[attr][0]
                return res
            else: return None
        except ldap.LDAPError, e:
            return None
        finally:
            l.unbind()
