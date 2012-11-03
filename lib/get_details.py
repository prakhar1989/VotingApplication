from ldap_helper import ldap_fetch_detail
detail_list = ["displayName", "mobile", "hostel", "roomNumber"]
f = open("listorders")
userlist = []
for line in f.readlines():
    if len(line) > 2:
        userlist.append(line[:line.find('@')])
f.close()
f = open("user_details2", "w")
for u in set(userlist):
    detail = ldap_fetch_detail(u, detail_list)
    if detail:
        f.write(str(ldap_fetch_detail(u, detail_list)))
    else:
        f.write(u)
    f.write("\n")
f.close()
