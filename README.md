LoyaltyOne challenge
Break down of Major tasks
A: Set up Python environment for application in virtual container to localize all dependencies in virtualenv 
B: Set up apache virtual server with WSGI to enable use of python code to be presented as web pages
C: Secure Web server at network level and service level
D: Test webservice to make sure it does the job
E: Put code in Version controle repository
F: Setup some autodeploy mechanism' so that when there are code changes committed code is deployed automaticlly
G: Propose a monitoring solution



A: Set up Python environment for application in virtual container to localize all dependencies in virtualenv
1: install python-pip apache2 libapache2-mod-wsgi using command below
	apt-get install python-pip apache2 libapache2-mod-wsgi
2: Install python virtual environment for this project using
	 pip install virtualenv
3: Make dir where project code will reside using command
	mkdir ~/myproject
4: Within ~/myproject create virtual environment for the project using command
	virtualenv myprojectenv
5: Activate the virtual environment using command below; while you are in mkdir ~/myproject
	source myprojectenv/bin/activate
6: Copy the the directories with Django settings and application to the project directory
    i-e copy anagrams and apps directories to ~/myproject
7: Make sure manage.py, requirements.txt, db.sqlite3 and dictionary.txt reside in ~/myproject
8: Using following command instll required software and dependencies
	pip install -r requirements
9: Edit file settings.py in ~/myproject/nagrams to make sure it has following; we are using wild character settings here Ec2 host names keep changing.
	ALLOWED_HOSTS = ['.us-west-2.compute.amazonaws.com']

B: Set up apache virtual server with WSGI to enable use of python code to be presented as web pages
1: Make sure WSGI module is enabled on apache by issuing following command
	a2enmod wsgi
2: Create Virtual Host configuration file in apache2 configuration under sites-available with following contents
	<VirtualHost *:80>
		Alias /static/ "/home/ubuntu/anagrams/static"
		<Directory "/home/ubuntu/anagrams/static">
		Options Indexes FollowSymLinks
		AllowOverride None
		Require all granted
		</Directory>
		 <Directory /home/ubuntu/anagrams/anagrams>
		  <Files wsgi.py>
		  Require all granted
		  </Files>
		</Directory>
		WSGIDaemonProcess anagrams python-path=/home/ubuntu/anagrams python-home=/home/ubuntu/anagrams/anagramsenv
		WSGIProcessGroup anagrams
		WSGIScriptAlias / /home/ubuntu/anagrams/anagrams/wsgi.py
		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined
		</VirtualHost>
# vim: syntax=apache ts=4 sw=4 sts=4 sr noet

3: Make sure site is enabled 
	a2ensite anagrams
4: Tweak file ownership and permission in ~/myproject directory; this is to facilitate for apache to be able to read and write.
	chmod 664 ~/myproject/db.sqlite3
	chown :www-data ~/myproject/db.sqlite3
	chown :www-data ~/myproject
5: Finally start apache service

C: Secure Web server at network level and service level
1: Create SSL key and Cert pair 
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
2: Create strong Diffie-Hellman group
	openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
3: Create ssl-param.conf in apache2 conf-available directory; with following Directives
	# from https://cipherli.st/
	# and https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html

	SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
	SSLProtocol All -SSLv2 -SSLv3
	SSLHonorCipherOrder On
	# Disable preloading HSTS for now.  You can use the commented out header line that includes
	# the "preload" directive if you understand the implications.
	#Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains; preload"
	Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains"
	Header always set X-Frame-Options DENY
	Header always set X-Content-Type-Options nosniff
	# Requires Apache >= 2.4
	SSLCompression off 
	SSLSessionTickets Off
	SSLUseStapling on 
	SSLStaplingCache "shmcb:logs/stapling-cache(150000)"

	SSLOpenSSLConfCmd DHParameters "/etc/ssl/certs/dhparam.pem"
4: Modify default unencrypted site to redirect traffic to SSL site
   <VirtualHost *:80>
        . . .

        Redirect "/" "https://your_domain_or_IP/"

        . . .
	</VirtualHost>
5: Add following Configuration parameters to your virtual host file
	<VirtualHost *:443>
	# Following Defines SSL self signed Cert param
        SSLEngine on
        SSLCertificateFile      /etc/ssl/certs/apache-selfsigned.crt
        SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key

        <FilesMatch "\.(cgi|shtml|phtml|php)$">
                        SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
                        SSLOptions +StdEnvVars
         </Directory>
        BrowserMatch "MSIE [2-6]" \
        nokeepalive ssl-unclean-shutdown \
        downgrade-1.0 force-response-1.0

5: Adjust any firewalls rules to make sure port 443 is allowed
6: Enable changes in Apache 
	a2enmod ssl 
	a2enmod headers
	a2ensite default-ssl
	a2enconf ssl-param
7: Perform a configuration test to make sure apache will not fail to reload
	apache2ctl configtest
8: restart apache
	service apache2 restart
9: you can use https://www.ssllabs.com/ to test your cert and ssl setup

#######
Installing Jenkins
1: Add jenkin key 
	wget -q -O — https://jenkins-ci.org/debian/jenkins-ci.org.key
	wget -q -O — https://jenkins-io.org/debian/jenkins-io.org.key
2: Add the jenkin repository under /etc/apt/souorces.list in new file with	
	deb http://pkg.jenkins-ci.org/debian binary/
	deb https://pkg.jenkins.io/debian binary/
3: update the repositories; install java and jenkins
	apt-get update
	apt-get install openjdk-8-jdk
	apt-get install jenkins
4: Start jenkins server
	service jenkins start
