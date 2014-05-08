#!/usr/bin/env python
from CSHLDAP import CSHLDAP
from datetime import date, datetime
from csh_webnews import Webnews
import argparse


def allMembersWithBirthdays(ldap):
    """
    Finds all active members in LDAP and strips those whose birthday is
    not today.
    Returns: The list of all active members whose birthday is today.
    """
    activeMembers = ldap.search(active="1", objects=True)
    members = [member for member in activeMembers if member.isBirthday()]
    return members

def message(ldap):
    """
    Finds all active members whos birthday is today and generates
    a subject and body for WebNews.
    Returns: The subject line, The body
    """
    birthdays = allMembersWithBirthdays(ldap)
    numberOfBirthdays = len(birthdays)
    if numberOfBirthdays == 0:
        return None, None
    plural = "s" if numberOfBirthdays > 1 else ""
    name = "Today" if numberOfBirthdays > 1 else "It's " + birthdays[0].fullName()
    subject = name + "'s Birthday" + plural
    string = ""
    for member in birthdays:
        memberString = (member.fullName() + " is " + 
                        str(member.age()) + " years old.\n")
        string += memberString
    string += ("\nShower on sight!\n\n" + 
               "(This post was automatically generated " +
               "by the WebNews Birthday Bot.)")
    return subject, string

def main(user=None, password=None, debug=False, apiKey=None, test=False):
    ldap = CSHLDAP(user, password, app=True)
    subject, post = message(ldap)
    if not post:
        print("No birthdays today.")
        return
    print(post)
    if debug:
        return
    newsgroup = "csh.test" if test else "csh.noise"
    webnews = Webnews(api_key=apiKey, api_agent="WebNews Birthday Bot")
    webnews.compose(newsgroup=newsgroup, subject=subject, body=post)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find users with a birthday.')
    parser.add_argument("user", help="Specify a username.")
    parser.add_argument("password", help="Specify the password for the user.")
    parser.add_argument("apikey", help="API key for posting to WebNews")
    parser.add_argument("--test", "-t",
                        action="store_true",
                        help="Posts to csh.test instead of csh.noise")
    parser.add_argument("--debug", "-d",
                        action="store_true",
                        help='Only prints to standard output.')
    args = parser.parse_args()

    if not args.apikey:
        print("No API key provided.")
        exit()

    main(user=args.user, password=args.password,
         apiKey=args.apikey, test=args.test,
         debug=args.debug)
