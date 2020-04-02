# Gluu Server Backup

The Gluu Server should be backed up frequently--**we recommend at least one daily and one weekly backup of Gluu's data and/or VM.** 

There are multiple methods for backing up the Gluu Server. A few recommended strategies are provided below.

## VM Snapshot Backup

In the event of a production outage, a proper snapshot of the last working condition will help rapidly restore service. 

Most platform virtualization software and cloud vendors have snapshot backup features. For instance, Digital Ocean has Live Snapshot and Droplet Snapshot; VMWare has Snapshot Manager, etc. 

Snaphots should be taken for all Gluu environments (e.g. Prod, Dev, QA, etc.) and tested periodically to confirm consistency and integrity. 
 

## Tarball Method
All Gluu Server files live in a single folder: `/opt`. The entire Gluu Server CE `chroot` folder can be archived using the `tar` command: 

1. Stop the server: `# service gluu-server-3.1.8 stop`
	
1. Use `tar` to take a backup: `# tar cvf gluu316-backup.tar /opt/gluu-server-3.1.8/`
	
1. Start the server again: `# service gluu-server-3.1.8 start`
	

## LDIF Data Backup
From time to time (daily or weekly), the LDAP database should be exported in a standard LDIF format. Having the data in plain text offers some options for recovery that are not possible with a binary backup. 

Instructions are provided below for exporting both OpenDJ and OpenLDAP data. The below instructions address situations where unused and expired cache and session related entries are piling and causing issues with functionality. Read more about this [issue](https://www.gluu.org/blog/managing-cache-in-the-gluu-server/).

### OpenDJ 

Errors that this may help fix include but are not restricted to: 

- Out of Memory

If your Gluu Server is backed by OpenDJ, follow these steps to backup your data:

1. Check cache entries

	First check your cache entries by running the following command:

	```bash
		/opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' -T 'oxAuthGrantId=*' dn | grep 'dn:' | wc –l
	```
1. Dump the data as LDIF

	- Log in to root:
		
		```bash
		sudo su -
		```

	- Log into Gluu-Server-3.1.x:   

		```bash
		service gluu-server-3.1.x login
		```

	- Stop Identity, oxAuth, and OpenDJ services:

		```bash
		service identity stop
		```

		```bash
		service oxauth stop
		```

		```bash
		/opt/opendj/bin/stop-ds
		```

	- If you are moving to a new LDAP, copy over your schema files from the following directory. Otherwise simply copy it for backup:

		```bash
		/opt/opendj/config/schema/
		```

	- Now export ldif and save it somewhere safe. You will not be importing this if you choose to apply any filters as below:

		```bash
		/opt/opendj/bin/export-ldif -n userRoot -l exactdatabackup_date.ldif
		```

	- Now exclude `oxAuthGrantId` so the command becomes:

		```bash
		/opt/opendj/bin/export-ldif -n userRoot -l yourdata_withoutoxAuthGrantId.ldif --includeFilter '(!(oxAuthGrantId=*))'
		```

	- You may also wish to exclude `oxMetric` so the command becomes:

		```bash
		/opt/opendj/bin/export-ldif -n userRoot -l yourdata_withoutGrantIdMetic.ldif --includeFilter '(&(!(oxAuthGrantId=*))(!			(objectClass=oxMetric)))'
		```

1. Rebuild indexes (as needed)

	Now, **only if needed**, rebuild indexes:

	- Check status of indexes: 

		```bash
		/opt/opendj/bin/backendstat show-index-status --backendID userRoot --baseDN o=gluu
		```

	Take note of all indexes that need to be rebuilt. **If no indexing is needed, move on to step 4.**

	- Start OpenDJ to build backend index :

		```bash
		/opt/opendj/bin/start-ds
		```

	- Build backend index for all indexes that need it accoring to previous status command, change passoword `-w` and index name accourdingly. This command has to be run for every index separately: 

		```bash
		/opt/opendj/bin/dsconfig create-backend-index --port 4444 --hostname localhost --bindDN "cn=directory manager" -w password --backend-name userRoot --index-name iname --set index-type:equality --set index-entry-limit:4000 --trustAll --no-prompt
		```

	- Stop OpenDJ:

		```bash
		/opt/opendj/bin/stop-ds
		```

	- Rebuild the indexes as needed, here are examples : 

		```bash
   		/opt/opendj/bin/rebuild-index --baseDN o=gluu --index iname
   		/opt/opendj/bin/rebuild-index --baseDN o=gluu --index uid
   		/opt/opendj/bin/rebuild-index --baseDN o=gluu --index mail
		```

	- Check status again :

		```bash
		/opt/opendj/bin/backendstat show-index-status --backendID userRoot --baseDN o=gluu
		```

	- Verify indexes: 

		```bash
		 /opt/opendj/bin/verify-index --baseDN o=gluu --countErrors
		```

1. Import previous ldif

	Next import your previously exported ldif. Here, we are importing without  `oxAuthGrantId` . 
	
	**Note : You may import the exact export of your ldap `exactdatabackup_date.ldif`.Do not import your exact copy of your ldif if you are following instructions to to clean your cache entries
	
	```bash
	/opt/opendj/bin/import-ldif -n userRoot -l yourdata_withoutoxAuthGrantId.ldif
	```
	If you moved to a new LDAP, copy back your schema files to this directory:

	```bash
	/opt/opendj/config/schema/
	```
1. Start services

	- Now start Identity, oxAuth, and OpenDJ services:

		```bash
		/opt/opendj/bin/start-ds
		```

		```bash
		service identity start
		```

		```bash
		service oxauth start
		```

1. Verify

	Finally, verify your cache entries have been removed:

	```bash
 	/opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' -T 		'oxAuthGrantId=*' dn | grep 'dn:' | wc –l
 	```

You should be done and everything should be working perfectly. You may notice your Gluu Server responding slower than before. That is expected -- your LDAP is adjusting to the new data, and indexing might be in process. Give it some time and it should be back to normal.

### OpenLDAP

Errors that this may help fix include but are not restricted to: 

- MDB_MAP_FULL: Environment mapsize limit reached (-30792)

If your Gluu Server is backed by OpenLDAP, follow these steps to backup your data:   

1. Check cache entries

	Check your cache entries by running the following command:

	```bash
	/opt/symas/bin/slapcat | grep oxAuthGrantId | wc -l
	```
	
1. Dump the db

	- Log in to root:
		
		```bash
		sudo su -
		```
	
	- Log into Gluu-Server-3.1.x: 

		```bash
		service gluu-server-3.1.x login
		```

	- Stop Identity, oxAuth, and solserver services :

		```bash
		service identity stop
		```

		```bash
		service oxauth stop
		```

		```bash
		service solserver stop
		```

	- Dump the data:
	
		```bash
		/opt/symas/bin/slapcat -a '(!(oxAuthGrantId=*))' > /root/yourdata.ldif
		```

	- The above command excludes `oxAuthGrantID`. If you wish to dump all your data, simply run:

		```bash
		/opt/symas/bin/slapcat > /root/allyourdata.ldif
		```

	- You may also wish to exclude `oxMetric` so the command becomes:
	
		```bash
		/opt/symas/bin/slapcat -a '(&(!(oxAuthGrantId=*))(!(objectClass=oxMetric)))' > /root/yourdata.ldif
		```
		
1. Move the current DB

	Now you need to move your current database so solsover loads an empty database when it starts. Even if you have a new installation of Gluu, you still need to follow this step so the db is no longer used:

	```bash
	mv /opt/gluu/data/main_db/data.mdb /opt/gluu/data/main_db/olddata.mdb.org
	```
	
1. Import previous ldif 

	Next import your previously exported ldif:
	
	```bash
	/opt/symas/bin/slapadd -l /root/yourdata.ldif
	```
	
	Wait for it to successfully load...

1. Chown data

	Next chown the data to LDAP:
	
	```bash
	chown ldap:ldap /opt/gluu/data/main_db/data.mdb
	```
	
1. Start services

	- Now start Identity, oxAuth, and solserver services:
	
		```bash
		service identity start
		```

		```bash
		service oxauth start
		```

		```bash
		service solserver start
		```

You should be done and everything should be working perfectly. You may notice your Gluu Server responding slower than before. That is expected -- your LDAP is adjusting to the new data, and indexing might be in process. Give it some time and it should be back to normal.




<!--
## Script Method

1. Log in to Gluu chroot
	a. # service gluu-server-3.1.8 login
2. Fetch export script from Gluu 
	b. wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py
3. Change permission of the script
	c. # chmod +x export24.py
4. run the script
	d. # ./export24.py

The export script will generate a directory called  backup_24  which will have all the data backed up from the 
current installation. Check the log file generated in the directory for any errors.
-->
