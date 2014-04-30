#!/usr/bin/env python
from CSHLDAP import CSHLDAP
from datetime import date, datetime
import argparse

def checkBirthday(ldap):
    today = date.today()
    for member in allMembersWithBirthdaysOnDate(ldap, today):
        name = member["displayName"]
        if len(name) < 1:
            continue
        displayName = name[0]

def allMembersWithBirthdays(ldap):
    activeMembers = ldap.search(active="1")
    members = []
    for memberTuple in activeMembers:
        if len(memberTuple) < 1:
            continue
        member = memberTuple[1]
        birthday = birthdateFromMember(member)
        if not birthday:
            continue
        members.append(member)
    return members

def allMembersWithBirthdaysOnDate(ldap, date):
    allMembers = allMembersWithBirthdays(ldap)
    birthdayMembers = []
    for member in allMembers:
        birthday = birthdateFromMember(member)
        if date.month != birthday.month or date.day != birthday.day:
            continue
        birthdayMembers.append(member)
    return birthdayMembers

def birthdateFromMember(member):
    if not "birthday" in member:
        return None
    birthday = member["birthday"]
    if len(birthday) < 1:
        return None
    birthdayString = birthday[0]
    memberMonthDay = birthdayString[:8]
    birthdate = datetime.strptime(memberMonthDay, "%Y%m%d")
    return date(year=birthdate.year, month=birthdate.month, day=birthdate.day)

def messageString(ldap):
    birthdays = allMembersWithBirthdaysOnDate(ldap, date.today())
    numberOfBirthdays = len(birthdays)
    if numberOfBirthdays == 0:
        return None
    plural = "s" if numberOfBirthdays > 1 else ""
    string = "Today's birthday" + plural + ":"
    for member in birthdays:
        birthdate = birthdateFromMember(member)
        age = date.today().year - birthdate.year
        name = member["displayName"]
        if len(name) < 1:
            continue
        nameString = name[0]
        memberString = "\n\t" + nameString + " is " + str(age) + " years old."
        string += memberString
    string += "\n\nShower on sight!"
    return string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find users with a birthday.')
    parser.add_argument("user", help="Specify a username.")
    parser.add_argument("password", help="Specify the password for the user.")
    args = parser.parse_args()
    ldap = CSHLDAP(args.user, args.password)
    message = messageString(ldap)
    if message:
        print(message)
