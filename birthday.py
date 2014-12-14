#!/usr/bin/env python
from creds import *
from csh import ldapapi
from datetime import date, datetime
import argparse


def allMembersWithBirthdays():
    """
    Finds all active members in LDAP and strips those whose birthday is
    not today.
    Returns: The list of all active members whose birthday is today.
    """
    activeMembers = ldap.search(active="1")
    members = [member for member in activeMembers if member.isBirthday()]
    return members

def message():
    """
    Finds all active members whos birthday is today and generates
    a subject and body for WebNews.
    Returns: The subject line, The body
    """
    birthdays = allMembersWithBirthdays()
    numberOfBirthdays = len(birthdays)
    if numberOfBirthdays == 0:
        return None, None
    oneBirthday = (numberOfBirthdays == 1)
    plural = "" if oneBirthday else "s"
    name = "It's " + birthdays[0].fullName() if oneBirthday else "Today"
    subject = name + "'s Birthday" + plural
    body = ""
    for member in birthdays:
        memberString = (member.fullName() + " is " + 
                        str(member.age()) + " years old.\n")
        body += memberString
    body += ("\nShower on sight!\n\n" + 
               "(This post was automatically generated " +
               "by the WebNews Birthday Bot.)")
    return subject, body

def main(debug=False, test=False):
    subject, post = message()
    if not post:
        print("No birthdays today.")
        return
    print("Subject: \n" + subject + "\n")
    print("Body:\n" + post)
    if debug:
        return
    newsgroup = "csh.test" if test else "csh.noise"
    webnews.compose(newsgroup=newsgroup, subject=subject, body=post)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find users with a birthday.')
    parser.add_argument("--test", "-t",
                        action="store_true",
                        help="Posts to csh.test instead of csh.noise")
    parser.add_argument("--debug", "-d",
                        action="store_true",
                        help='Only prints to standard output.')
    args = parser.parse_args()

    main(test=args.test,
         debug=args.debug)
