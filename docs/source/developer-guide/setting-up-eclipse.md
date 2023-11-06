# Overview

This guide will detail how to set up Eclipse for developing [custom interception scripts](../admin-guide/custom-script.md).

## Prerequisites

Due to the vast array of development environments, Java runtimes and lack of documentation, a non-functional setup is very likely in many scenarios. As of this writing, the following environment has been successfully tested:

- OpenJDK >= 17 **AND** Amazon Corretto JDK 11
- Python 3.10
- Eclipse 2022-09 (4.25.0)
- PyDev 10.0.1
- Maven 3.8.6 (requires OpenJDK >= 17)
- Gluu source code

## Setup

1. Install [OpenJDK 17](https://openjdk.org/install/) and add it to your execution path.
    - Ensure you have the proper Java version installed by running `java --version` from your terminal of choice. The output should be:

        ```
        $ java --version
        openjdk 17.0.5 2022-10-18
        OpenJDK Runtime Environment (build 17.0.5+1)
        OpenJDK 64-Bit Server VM (build 17.0.5+1, mixed mode)
        ```
1. Download [Amazon Corretto 11](https://docs.aws.amazon.com/corretto/latest/corretto-11-ug/downloads-list.html) and extract it to your directory of choice. 
1. Install [Apache Maven](https://maven.apache.org/install.html) and add it to your execution path. On Linux, your distribution may have releases available on the package repository.
    - Ensure maven is functional by running `mvn --version` from the terminal.
1. Install [Eclipse IDE for Java Developers](https://www.eclipse.org/downloads/packages/). 
1. Open Eclipse, go through the setup. No special configuration is necessary for now.
1. Configure Eclipse to use Amazon Corretto JDK. Go to `Window -> Preferences -> Java -> Installed JREs` and add your Amazon Corretto root folder. Then, select it as the default JRE and Apply and Close.
1. Configure Eclipse to use the system-wide maven install. Go to `Window -> Preferences -> Maven -> Installations` and add your system-wide maven install if it's not already there. Then, check the tick mark, Apply and Close.
    - If you don't see maven configurations, make sure that Eclipse launched with the system-wide OpenJDK 17. Edit your `eclipse.ini` file (locations vary across operating systems) and ensure that the path following `-vm` is your OpenJDK 17's `bin` folder.
1. Install Pydev. Go to `Help -> Install New Software` and paste `https://www.pydev.org/updates/` into the "Work with" box, then hit Enter. Wait for Eclipse to fetch resources, then select PyDev, unselect "Contact all update sites during install to find required software" and click Finish. You may be asked to agree to License Agreements and trust signatures, accept these. Restart Eclipse when prompted.
1. Pydev should automatically find Python interpreters on your system. To ensure, go to `Window -> Preferences -> Pydev -> Interpeters -> Python Interpreters` and check.
1. Create a new Java Project by going to `File -> New -> Java Project`, fill out the name and location, and ensure Amazon Corretto JDK 11 is selcted as the Project JRE. Click Finish.
1. Inside the `src` folder of the newly created project, create a new file and name it `test.py`. Since the perspective is set to Java and the project is a Java project, PyDev won't be able to initialize it as a Python module.
1. In order to use Gluu classes, you will need the source code. For this example we will use [oxCore](https://github.com/GluuFederation/oxCore/). Clone the repository, and check out the version corresponding to the version of Gluu server you want.
1. To import the oxCore libraries, go to `File -> Import -> Maven -> Existing Maven Projects`, and select the oxCore directory and all subdirectories. Click finish.
1. If you have Java and maven properly configured, Eclipse will automatically fetch dependencies and build all the modules. Wait for it to finish.
1. Right-click the project you created and go to Properties. Click on Java Build Path, then Classpath. Click `Add...` and select all the oxCore modules. Click Apply and Close.
1. To test, open the `test.py` file and begin typing Java code. For example, you can use:

    ```python
    from org.gluu.model.custom.script.type.auth import PersonAuthenticationType
    from org.gluu.util import StringHelper
    ```
    If everything is configured correctly, Eclipse should start autofilling and allowing code completion. You can also test hyperlinking by holding Ctrl and clicking on `PersonAuthenticationType`, which will take you to the source code.

# Troubleshooting
TBI