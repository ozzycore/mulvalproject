## Nessus Installation

1. **Log in to nessus01 instance:**
    - Go to 'vagrant' directory: `cd vagrant`.
    - Deploy 'nessus01' instance: `vagrant up nessus01`.
    - Login to 'nessus01' instance: `vagrant ssh nessus01`.
2. **Install Nessus [1.2]:**
    - Download the package 'Nessus-8.11.0-es7.x86_64.rpm' from [1.1].
    - Install: `yum install Nessus-8.11.0-es7.x86_64.rpm`.
    - Turn off the firewalld:
      - `systemctl stop firewalld`.
      - `systemctl disable firewalld`.
    - Turn on the 'nessusd' service:
      - `systemctl start nessusd`.
      - `systemctl enable nessusd`.
    - You should be able to access the Nessus portal on https://10.0.0.11:8834.
    - Follow the guided portal installation.
3. **Boot:** 
    - Boot the server.
    - Make sure that Nessus is up and running. 


#### Reference

**1 - Nessus**

1.1 - https://www.tenable.com/downloads/nessus?loginAttempted=true
1.2 - https://www.patrick-bareiss.com/install-nessus-on-centos-7/
