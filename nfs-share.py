#!/usr/bin/python
import argparse
import os
import pwd


#Get args
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name", help="nfs share name", type=str)
    parser.add_argument("-l","--limit", help="nfs share size limit", type=int)


    args = parser.parse_args()

    print(args.name)

    #Check if user exists
    try:
        p = pwd.getpwnam(args.name)
        print "User %s with %s founded. Exiting..." % (p.pw_name, p.pw_uid)
        exit()
    except KeyError:
        print "user %s not found" % args.name
        print "gid is %s" % p.pw_gid

        #Create user
        useradd_command = "useradd -U -M -s /sbin/nologin %s" % args.name
        os.system(useradd_command)

        p = pwd.getpwnam(args.name)
        zfs_path="/mnt/nfs/msed"
        add_zfs="zfs create -o mountpoint=%s -o sharenfs=on -o compression=off -o quota=%s nfs/%s" % (zfs_path, args.limit, args.name)
        os.system(add_zfs)
        chown_dir="chown -R %s:%s %s" % (args.name, args.name, zfs_path)
        os.system(chown_dir)

    os.chown(zfs_path, p.pw_uid, p.pw_gid)

main()
