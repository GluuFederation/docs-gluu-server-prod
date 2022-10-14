# Cleaning entries for auto-enrolled users

## Overview

If your environment supports inbound identity by means of Passport, users auto-create local accounts in the Gluu server when they authenticate through external identity providers, be they social sites, IDPs, etc.

With time, many unused entries can accumulate in your database, thus you can use the removal tool to delete or deactivate entries corresponding to users that have not logged-in after a specified date and were created in an setting of inbound identity (Passport usage or with [Casa accounts linking plugin](https://gluu.org/docs/casa/plugins/account-linking/)).

## Using the script 

Download the [script](https://github.com/GluuFederation/community-edition-setup/raw/master/static/scripts/remove_external_people.py) to your Gluu chroot.

You can type `python3 remove_external_people.py -h` to learn about script usage. The following summarizes key parameters: 

- `remove`: If removal of accounts should take place. When ommited, accounts will be only deactivated (by setting `status` database attribute to `inactive`).

- `provider-only`: Account only user entries that have been enrolled through the designated identity provider. Examples: "github", "my-OP-1", "Okta-1234". The value must match the identifier used in the Passport providers form in oxTrust. When this param is ommited, removal/deactivation applies for all providers found in `oxExternalUid` database attribute.

`last-logon`: Removal/deactivation will take place upon entries whose last logon time is earlier or equal than the provided value. Example: `2008-11-30`.

!!! Note
No user belonging to an administrative group will be considered in this process.

## Example

To remove auto-enrolled users that haven't logged in to any app after Dec 25th, 1998, you could do:

`python3 remove_external_people.py -remove last-logon 1998-12-25`

Output (in ldif format) will be sent to `remove.log` file.
