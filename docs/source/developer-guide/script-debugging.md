# Custom Script Debugging
The following guide will explain how to debug [custom interception scripts](../admin-guide/custom-script.md). 

=== "Community Edition - VM"
    
    ## Setup
    
    The following instructions assume Gluu Server is already installed and available. If not, perform a standard [Gluu Server installation](../installation-guide/index.md), then do the following: 
    
    1. Install `https://repo.gluu.org/tools/tools-install.sh`
    1. Log out of CE
    1. Run `/opt/gluu-server/opt/gluu/bin/prepare-dev-tools.py`
    1. Log in to CE
    1. Run `/opt/gluu/bin/eclipse.sh`
    
    Once complete, start the PyDev debug server:
    
    1. Open the Eclipse Debug perspective   
    1. Run this command from the menu: `Pydev` > `Start Debug Server`
    
    ## Development & Debugging
    
    Now we are ready to perform script development and debugging. Here is a quick overview:
    
    1. In order to simplify development, put the script into a shared folder like `/root/eclipse-workspace`
    1. Then instruct oxAuth to load the script from the file system *instead* of LDAP
    1. Add debug instructions to the script, as specified in the next section
    1. Execute the script
    
    ## Enable Remote Debug in Custom Script
    
    1. After the import section, add:   
      
        ```
        REMOTE_DEBUG = True
        
        if REMOTE_DEBUG:
            try:
                import sys
                sys.path.append('/opt/libs/pydevd')
                import pydevd
            except ImportError as ex:
                print "Failed to import pydevd: %s" % ex
                raise
        ```     
          
    1. Add the following lines wherever breakpoints are needed:   
      
        ```
        if REMOTE_DEBUG:
            pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
        ```
    
    ## Sample Scenario
    
    1. Log in to oxAuth 
    1. Navigate to `Manage Custom Script Section`  
    1. Expand `Basic` script section  
    1. Copy the script to `/root/eclipse-workspace/basic.py`  
    1. Change script `Location type` to `File`  
    1. Specify the `Script Path` location to: `/root/eclipse-workspace/basic.py`  
    1. Enable the script  
    1. Check the following log to verify that oxAuth loaded the script properly: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`. It should look like this:    
    
        ```
        ... (PythonService.java:239) - Basic. Initialization
    
        ... (PythonService.java:239) - Basic. Initialized successfully
       
        ```
    
    1. Open the following file in Eclipse: `/root/eclipse-workspace/basic.py` 
    1. When opening the Python file for the first time, we need to instruct Eclipse to use a specific interpreter. Follow these steps:
      
        - Press the "Manual Config" button in the dialog box after opening the Python file
        - Open "PyDev->Interpreters->Jython Interpreters"
        - Click the "New..." button in the right panel. Name it "Jython" and specify the interpreter executable "/opt/jython/jython.jar"
        - Click "OK", then confirm the settings by clicking "OK" again, then "Apply and Close"
        - In the final dialog, confirm the settings by clicking "OK"
    
    1. Open basic.py in a file editor. After the import section, add the following lines to load the PyDev libraries:
    
        ```  
        REMOTE_DEBUG = True  
      
        if REMOTE_DEBUG:  
            try:  
                import sys  
                sys.path.append('/opt/libs/pydevd')  
                import pydevd  
            except ImportError as ex:  
                print "Failed to import pydevd: %s" % ex  
                raise  
        ```    
    
    1. Add this break condition to the first line in the authenticate method:
    
        ```  
        if REMOTE_DEBUG:   
            pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)  
    
        ```
    
    1. Save `basic.py`   
    1. Within one minute, oxAuth should load the changed file. Check the following log file again to make sure there are no load errors: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`    
    1. To check if the script works, update the default authentication method to Basic Authentication. This can be performed in oxTrust by navigating to `Manage Authentication` > `Default Authentication Method`   
    1. Open another browser or session and try to log in. **Make sure** to keep the first session open in order to disable the Basic Authentication method in case the script doesn't work as expected.  
    1. After executing `pydevd.settrace` the script will transfer execution control to the PyDev server in Eclipse. You can use any debug commands. For example: Step Over (F6), Resume (F8), etc     
    1. After debugging is finished, resume script execution to transfer execution control back to oxAuth
    
    ## Additional Resources
    - [Remote debugger](http://www.pydev.org/manual_adv_remote_debugger.html)
    
    ## X Server troubleshooting
    Running `/opt/gluu-server/opt/gluu/bin/prepare-dev-tools.py` allows Eclipse to access X server. 
    
    It runs the following commands:
    
    ```
    # Only this one key is needed to access from chroot 
    xauth -f /root/.Xauthority-gluu generate :0 . trusted 2>1 >> /root/prepare-dev-tools.log
    
    # Generate our own key, xauth requires 128 bit hex encoding
    xauth -f /root/.Xauthority-gluu add ${HOST}:0 . $(xxd -l 16 -p /dev/urandom)
    
    # Copy result key to chroot
    cp -f /root/.Xauthority-gluu /opt/gluu-server/root/.Xauthority
    
    # Allow to access local server X11   
    sudo su $(logname) -c "xhost +local:
    ```
    
    ### Unable to access x11
    
    If Eclipse is unable to access X11, run the following command from the host to check if it has the necessary permissisons:
    
    ```
    user@u144:~$ xhost +local:
    non-network local connections being added to access control list
    user@u144:~$ xhost 
    access control enabled, only authorized clients can connect
    LOCAL:
    SI:localuser:user
    ```
    
    If the user is still unable to access X11, remove `.Xauthority` from user home and log out/log in again.

=== "Cloud Native Edition - Kubernetes"

    ## Setup
    
    For development the kubernetes setup must be local and accessible to the debug server address. The following steps will walk you trough a setup using Minikube with docker driver, and [ksync](https://ksync.github.io/ksync/) for syncing the files between local and the container. The following instructions assume a fresh ubuntu 20.04, however the setup can be done on a diffrrent operating systems such as macOS or Windows.  

    ### System Requirements
    
    The minimum system requirement for running all Gluu services are `8GB RAM`, `4 CPU`, and `50GB disk`. This can be dropped to `4GB RAM`, `4CPU` and `20GB` disk space if operating with required services oxTrust, oxAuth, Jackrabbit , and LDAP.
    
    ### Setup Minikube
    
    1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) 18.09 or higher. For other operating systems follow the appropriate [docs](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc).
    
    1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/) but do not start it yet.

    1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
    
    1. Once Minikube is installed start it with the docker driver.
    
        ```bash
        minikube start --driver=docker
        ```    
            
    1. If not automatically set configure `kubectl` to use the cluster:
    
        ```bash
        kubectl config use-context minikube
        ```
            
    1. Enable ingress on minikube
    
        ```bash
        minikube addons enable ingress
        ```
        
    ### Install Gluu

    1. Install [Helm3](https://helm.sh/docs/using_helm/)

    1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](installation-guide/install-kubernetes.md/#build-pygluu-kubernetespyz-manually).
    
    1. **Optional:** If using couchbase as the persistence backend. Download the couchbase [kubernetes](https://www.couchbase.com/downloads) operator package for linux and place it in the same directory as `pygluu-kubernetes.pyz`
    
    1. Run :
    
      ```bash
      ./pygluu-kubernetes.pyz helm-install
      ``` 
    
    ### Install Ksync
    
    Once Gluu is fully running we want to create an active sync between a local folder, and the folder that will hold the interception scripts inside the oxAuth server container.
    
    1. Create a folder that will hold the interception script inside the oxAuth container. Place the namespace where gluu is installed in the env `GLUU_NAMESPACE` and execute:
    
        ```bash
        GLUU_NAMESPACE=<gluu-namespace>
        for pod in $(kubectl get pods -n $GLUU_NAMESPACE --selector=app=oxauth --output=jsonpath={.items..metadata.name}); do
            kubectl exec -ti $pod -n $GLUU_NAMESPACE -- mkdir -p /opt/gluu/interception-scripts-ksync
        done        
        ```
        
    1. Install ksync
    
        ```bash
        curl https://ksync.github.io/gimme-that/gimme.sh | bash
        ```
        
    1. Initialize ksync
    
        ```bash
        ksync init -n <gluu-namespace>
        ```
        
    1. Start ksync.
    
        ```bash
        ksync watch -n <gluu-namespace> &
        ```
    
    1. Open a new terminal and create a folder called `interception-scripts-ksync`
    
        ```bash
        mkdir -p $(pwd)/interception-scripts-ksync
        ```
    
    1. Create a spec to start syncing folders between local and oxAuth container.
    
        ```bash
        ksync create --selector=app=oxauth $(pwd)/interception-scripts-ksync /opt/gluu/interception-scripts-ksync -n <gluu-namespace>
        ```
    
    1. Check the status. Also check the terminal where the `watch` command is running. 
    
        ```bash
        ksync get
        ```
    1. Move the interception script to the local folder `$(pwd)/interception-scripts-ksync`. In this example we logged in Gluu, `Configuration` -> `Person Authentication Scripts` -> `basic` and copied the script to the local folder.
    
    ### Install an IDE
    
    The IDE can be of choice but must contain PyDev. We chose [Liclipse](https://www.liclipse.com/download.html) for this demonstartion. 
    
    Once complete, start the PyDev debug server:
    
    1. Open Liclipse
    
    1. Download the jython jar for the interpreter. 
    
        ```
        wget https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar
        ```
    
    1. From the menu: go to `File` -> `Open File` and choose the interception script that will be debugged in `$(pwd)/interception-scripts-ksync`.
    
     
    1. When opening the Python file for the first time, we need to instruct Liclipse to use a specific interpreter. Follow these steps:
      
        - Press the "Manual Config" button in the dialog box after opening the Python file
        
        - Open "PyDev->Interpreters->Jython Interpreters"
        
        - Click the "New..." button in the right panel. Name it "Jython" and specify the interpreter executable that was downloaded previously "jython-standalone-2.7.2.jar"
        
        - Click "OK", then confirm the settings by clicking "OK" again, then "Apply and Close"
        
        - In the final dialog, confirm the settings by clicking "OK" 
    
    1. From the menu: go to `Window` -> `Perspective` -> `Open Perspective` -> `Other..` -> `Debug`
    
    1. From the menu: go to `Pydev` > `Start Debug Server`. Now the server should have started at port `5678`. Take a note of the ip of the computer running Liclipse and save it for later use. Remember that the oxAuth pod must be able to communicate with this ip. If you have followed the instructions above and installed minikube on your local computer which is the same computer Liclipse is operating on you should be able to reach it from within the pods.
    
    ### Development & Debugging
    
    Now we are ready to perform script development and debugging. Here is a quick overview:
    
    1. Instruct oxAuth to load the script from the file system *instead* of LDAP
    
    1. Add debug instructions to the script, as specified in the next section
    
    1. Execute the script
    
    ### Enable Remote Debug in Custom Script
    
    1. After the import section, add:   
      
        ```
        REMOTE_DEBUG = True
        
        if REMOTE_DEBUG:
            try:
                import sys
                import pydevd
            except ImportError as ex:
                print "Failed to import pydevd: %s" % ex
                raise
        ```     
          
    1. Add the following lines wherever breakpoints are needed:   
      
        ```
        if REMOTE_DEBUG:
            pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
        ```
    
    ### Sample Scenario
    
    1. Log in to Gluu
    
    1. Navigate to `Configuration` -> `Person Authentication Scripts` -> `basic`
    
    1. Expand `basic` script section  
    
    1. Copy the script to `$(pwd)/interception-scripts-ksync/basic.py`  
    
    1. Change script `Location type` to `File`  
    
    1. Specify the `Script Path` location to the location of the folder inside oxAuth pods: `/opt/gluu/interception-scripts-ksync/basic.py`
      
    1. Enable the script  
    
    1. Check the following log inside the the oxauth container to verify that oxAuth loaded the script properly: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`. It should look like this:    
    
        ```
        kubectl exec -ti <oxauth-pod-name> -n <gluu-namespace> -- tail -f /opt/gluu/jetty/oxauth/logs/oxauth_script.log
        
        ```
        
        You should find the following in the log:
        
        ```
        ... (PythonService.java:239) - Basic. Initialization
    
        ... (PythonService.java:239) - Basic. Initialized successfully
       
        ```
    
 
    1. Download the jython jar for the interpreter. 
    
        ```
        wget https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar
        ```
        
    1. From the IDE (Liclipse) menu: navigate  to `File` -> `Open File` and choose the interception script that will be debugged in `$(pwd)/interception-scripts-ksync/basic.py`
     
    1. When opening the Python file for the first time, we need to instruct Liclipse to use a specific interpreter. Follow these steps:
      
        - Press the "Manual Config" button in the dialog box after opening the Python file
        
        - Open "PyDev->Interpreters->Jython Interpreters"
        
        - Click the "New..." button in the right panel. Name it "Jython" and specify the interpreter executable that was downloaded previously "jython-standalone-2.7.2.jar"
        
        - Click "OK", then confirm the settings by clicking "OK" again, then "Apply and Close"
        
        - In the final dialog, confirm the settings by clicking "OK" 
    
    1. Open basic.py in a file editor. After the import section, add the following lines to load the PyDev libraries:
    
        ```bash
        REMOTE_DEBUG = True  
      
        if REMOTE_DEBUG:  
            try:  
                import sys  
                import pydevd  
            except ImportError as ex:  
                print "Failed to import pydevd: %s" % ex  
                raise  
        ```    
    
    1. Add this break condition to the first line in the authenticate method. Place the ip of the maching running the ide , here liclipse i.e `192.168.140.2`.
    
        ```bash
        if REMOTE_DEBUG:   
            pydevd.settrace('<ip-of-machine-running-ide>', port=5678, stdoutToServer=True, stderrToServer=True)  
    
        ```
    
    1. Save `basic.py`
    
    1. Within one minute, oxAuth should load the changed file. Check the following log file again to make sure there are no load errors: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`
        
    1. To check if the script works, update the default authentication method to Basic Authentication. This can be performed in oxTrust by navigating to `Configuration` -> `Manage Authentication` -> `Default Authentication Method`
       
    1. Open another browser or session and try to log in. **Make sure** to keep the first session open in order to disable the Basic Authentication method in case the script doesn't work as expected.
      
    1. After executing `pydevd.settrace` the script will transfer execution control to the PyDev server in Liclipse. You can use any debug commands. For example: Step Over (F6), Resume (F8), etc
         
    1. After debugging is finished, resume script execution to transfer execution control back to oxAuth    