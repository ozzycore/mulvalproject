## MulVAL Installation

1. **Log in to mulval01 instance:**
    - Go to 'vagrant' directory: `cd vagrant`.
    - Deploy 'mulval01' instance: `vagrant up mulval01`.
    - Login to 'mulval01' instance: `vagrant ssh mulval01`.
2. **Install Graphviz [1.1]:**
    - Verify that the 'base' repository is enabled: `yum repolist enabled`.
    - Install: `yum install graphviz`.
3. **Install XSB [2.1]:**
    - Install 'C compiler' and all the required dependecies: `yum groupinstall "Development Tools"`.
    - Define XSB environment variable: `echo "export XSB_DIR=/opt/XSB/bin" >> /etc/profile.d/xsb.sh`.
    - Download the 'XSB.tar' file from [2.2]:   
    `wget http://xsb.sourceforge.net/downloads/XSB.tar.gz -P /opt`.
    - Untar the file: `tar xvfz /opt/XSB.tar`.
    - Go into 'build' directory: `cd /opt/XSB/build`.
    - Run the following commands: `./configure` , `./makexsb`.
    - Now you can verify the installation by running: `/opt/XSB/bin/xsb`
4. **Install MulVAL:**
    - Install the following packages:
        - `yum install java-1.8.0-openjdk-devel`
        - `yum install texlive-epstopdf-bin`
        - `yum install ghostscript`
    - Define MulVAL environment variables: 
        - `echo "export PATH=$PATH:/opt/XSB/bin:/opt/mulval/utils" >> /etc/profile.d/mulval.sh`.
        - `echo "export MULVALROOT=/opt/mulval" >> /etc/profile.d/mulval.sh`.
        - `echo "export CLASSPATH=$MULVALROOT/lib/dom4j-1.6.1.jar:$MULVALROOT/lib/jaxen-1.1.1.jar:$MULVALROOT/bin/adapter" >> /etc/profile.d/mulval.sh`
    - Download the 'mulval_1_1.tar' file from [3.1]: 
    `wget http://people.cs.ksu.edu/~xou/argus/software/mulval/mulval_1_1.tar.gz -P /opt`
    - Untar the file: `tar xvfz /opt/mulval_1_1.tar`.
    - Run make from '/opt/mulval': `make`.
    - To test Attack graph generation, run: `graph_gen.sh testcases/3host/input.P -v -p`.
5. **Boot:** 
    - Boot the server.
    - Make sure that everything works by running the 3host example again.


#### Reference

**1 - Graphviz**

1.1 - http://www.graphviz.org/download/. 

**2 - XSB**

2.1 - http://xsb.sourceforge.net.  
2.2 - http://xsb.sourceforge.net/downloads/downloads.html. 

**3 - MulVAL**
3.1 - http://people.cs.ksu.edu/~xou/argus/software/mulval/readme.html. 
