#!/usr/bin/python
import argparse
import os
import pwd
import sys

#Get args
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", help="nfs share name", type=str)
    parser.add_argument("-l","--limit", help="nfs share size limit", type=str)
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    print(args.name)
    #Check if user exists
    try:
        p = pwd.getpwnam(args.name)
        print "User %s with %s founded. Exiting..." % (p.pw_name, p.pw_uid)
        exit()
    except KeyError:
        print "user %s not found, creating" % args.name
        #print "gid is %s" % p.pw_gid

        #Create user
        useradd_command = "useradd -U -M -s /sbin/nologin %s" % args.name
        os.system(useradd_command)
        #print gid/uid
        r = pwd.getpwnam(args.name)
        print "user %s created with uid %s" % (args.name, r.pw_uid)
        zfs_path="/opt/nfs/%s" % args.name
        add_zfs="zfs create -o mountpoint=%s -o sharenfs=off -o compression=off -o quota=%s zfs/%s" % (zfs_path, args.limit, args.name)
        os.system(add_zfs)
        chown_dir="chown -R %s:%s %s" % (args.name, args.name, zfs_path)
        os.system(chown_dir)

    os.chown(zfs_path, r.pw_uid, r.pw_gid)

main()
