# ALPHA-How to setup Gluu Cloud Native with ALB controller and Aurora serverless

## Overview

The Gluu Server has been optimized with several container strategies that allow scaling micro-services and orchestrating them using Kubernetes. This tutorial will walk through installation of Gluu on AWS EKS (Elastic Kuberentes service ) with ALB controller.

!!!warning
    In recent releases we have noticed that the ALB does not properly work with the oxtrust admin UI. Functions such as access and cache refresh do not work. There is an [issue](https://github.com/GluuFederation/oxTrust/issues/2130) open but the main issue is in the fact that ALB does not support rewrites.

## Installation

### Set up the cluster

#### Resources

-  Follow this [guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) to install a cluster with worker nodes. We used four nodes of  on all three available zones of instance type `t2.medium` instance type. Please make sure that you have all the `IAM` policies for the AWS user that will be creating the cluster and volumes.
 
   Create the Kubernetes cluster. We will be using EKS but GKE is also fine to use. Example `eksctl` command.

   ```bash
   eksctl create cluster --name gluualbcluster --version 1.19 --nodegroup-name standard-workers --node-type t2.medium --zones eu-central-1a,eu-central-1b,eu-central-1c --nodes 4 --nodes-min 1 --nodes-max 5 --region eu-central-1 --ssh-public-key "~/.ssh/id_rsa.pub"
   ```
   
#### Requirements

1. The above guide should also walk you through installing `kubectl` , `aws-iam-authenticator` and `aws cli` on the VM you will be managing your cluster and nodes from. Check to make sure.

        aws-iam-authenticator help
        aws-cli
        kubectl version

2. After setting up your EKS cluster start with installing the ALB controller following this [guide](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

3. [Amazon Aurora](https://aws.amazon.com/rds/aurora/?aurora-whats-new.sort-by=item.additionalFields.postDateTime&aurora-whats-new.sort-order=desc) is a MySQL and PostgreSQL-compatible relational database built for the cloud, that combines the performance and availability of traditional enterprise databases with the simplicity and cost-effectiveness of open source databases. Gluu fully supports Amazon Aurora, and recommends it in production.

4. Create an Amazon Aurora database with MySQL compatibility version >= `Aurora(MySQL 5.7) 2.07.1` and capacity type `Serverless`. Make sure the EKS cluster can reach the database endpoint. You may choose to use the same VPC as the EKS cluster. Save the master user, master password, and initial database name for use in Gluus helm chart.

5. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.2/README.md#build-pygluu-kubernetespyz-manually).

6. Run :

   ```bash
   ./pygluu-kubernetes.pyz helm-install
   ```

7. Once the installation has finished and you can access the GUI. Head to `Configuration > JSON Configuration > OxTrust Configuration`, then set `rptConnectionPoolUseConnectionPooling` to `false`.

8. Restart oxTrust.

   ```bash
   kubectl rollout restart statefulset <helm-name>-oxtrust -n <namespace>
   # kubectl rollout restart statefulset gluu-oxtrust -n gluu
   ```

!!!note
    Prompts will ask for the rest of the information needed. You may generate the manifests (yaml files) and continue to deployment or just generate the  manifests (yaml files) during the execution of `pygluu-kubernetes.pyz`. `pygluu-kubernetes.pyz` will output a file called `settings.json` holding all the parameters. More information about this file and the vars it holds is [here](../installation-guide/install-kubernetes.md#settingsjson-parameters-file-contents) but  please don't manually create this file as the script can generate it using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/cloud-native-edition/releases). 

