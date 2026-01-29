# Containerization and DevOps Lab

Name: Mayank Thakur

Roll no: R2142230924

Sap-ID: 500123412


# Installation and Configuration of Windows Subsystem for Linux (WSL)

# Aim

To install and configure Windows Subsystem for Linux (WSL) on a Windows machine and set up an Ubuntu Linux distribution for running Linux commands and DevOps tools on Windows.

# Theory

Windows Subsystem for Linux (WSL) is a compatibility layer developed by Microsoft that allows users to run a Linux environment directly on Windows without the need for a virtual machine or dual boot system.

WSL enables developers to:

- Run Linux command-line tools directly on Windows  
- Use Linux-based development tools like Git, Docker, Podman, and Vagrant  
Integrate Linux workflows with Windows applications

There are two versions of WSL:

WSL 1: Uses a translation layer between Linux and Windows kernel  
- WSL 2: Uses a real Linux kernel with better performance and full system call compatibility

WSL 2 is recommended for containerization and DevOps workflows.

# System Requirements

Windows 10 (Version 2004 or later) or Windows 11  
- Administrator access  
Virtualization enabled in BIOS  
- Internet connection

Procedure / Steps to Perform the Experiment

Step 1: Install WSL and Ubuntu Distribution

1. Open PowerShell as Administrator

# 2. Run the following command:

wsl --install -d Ubuntu  
```txt
PS C:\WINDOWS\system32> wsl --install -d Ubuntu  
Downloading: Ubuntu  
Installing: Ubuntu  
Distribution successfully installed. It can be launched via 'wsl.exe -d Ubuntu'  
Launching Ubuntu...  
Provisioning the new WSL instance Ubuntu  
This might take a while...  
Create a default Unix user account: mayank  
New password:  
Retype new password:  
passwd: password updated successfully  
To run a command as administrator (user "root"), use "sudo <command>".  
See "man sudo root" for details.
```

# This command performs:

• Enables required Windows features  
• Installs WSL  
- Installs Ubuntu as the default Linux distribution

![](images/9f45b9e5171d7fc4b9080cc3fe6a73a80c7d7f565502dfb39932a7ca0329e767.jpg)

Restart the system after installation completes.

# Step 2: Verify WSL Installation

After restart, open PowerShell and execute:

ws1 --list --verbose

OR

ws1 -l -v

This displays:

- Installed Linux distributions  
WSL version (WSL 1 or WSL 2)  
Running status

```batch
PS C:\WINDOWS\system32> wsl -l -v  
NAME STATE VERSION  
* docker desktop Running 2  
Ubuntu Running 2
```

# Step 3: Check and Change WSL Version

To convert Ubuntu to WSL 2:

wsl --set-version Ubuntu 2

To convert Ubuntu to WSL 1 (if needed):

wsl --set-version Ubuntu 1

To set WSL 2 as default for future installations:

wsl --set-default-version 2

```txt
PS C:\WINDOWS\system32> wsl --set-default Ubuntu  
The operation completed successfully.
```

# Step 4: Check Installed Linux Distributions

To list all available and installed distributions:

wsl --list --all

To install another distribution (example: Debian):

wsl --install -d Debian

```batch
PS C:\WINDOWS\system32> wsl --list --all Windows Subsystem for Linux Distributions: Ubuntu (Default) docker-osktop PS C:\WINDOWS\system32>
```

# Step 5: Set Default Linux Distribution

To set Ubuntu as default:

wsl --set-default Ubuntu

OR simply launch Ubuntu using:

Ws1

PS C:\WINDOWS\system32> wsl --set-default Ubuntu  
The operation completed successfully.

# Step 6: Fix WSL 2 Kernel Update Issue (If Occurs)

If error appears:

"WSL 2 requires an update to its kernel"

Run:

wsl --set-version Ubuntu 2

If still unresolved, install the latest WSL kernel update from Microsoft and restart.

# Step 7: Common Errors and Solutions

Error: 'wsl' is not recognized as a command

Run in PowerShell (Admin):

dism.exe /online /enable-feature /featurename: Microsoft-Windows-Subsystem-Linux/all/norestart

Enable Virtual Machine Platform:

dism.exe /online /enable-feature / featurename: VirtualMachine Platform/all/norestart

Restart the system.

# Step 8: Virtualization Disabled Error (0x80370102)

If virtualization is disabled:

Restart PC  
. Enter BIOS/UEFI (F2 / F10 / DEL / ESC)  
Enable Intel VT-x / AMD-V  
Save & Restart

# Step 9: Useful WSL Commands

# Command

# Description

wsl Start default Linux

wsl -d Ubuntu Start Ubuntu

wsl --terminate Ubuntu Stop Ubuntu

ws1 --shutdown Stop all WSL instances

wsl --unregister Ubuntu Remove Ubuntu completely

# Result

Windows Subsystem for Linux (WSL) was successfully installed and configured. Ubuntu Linux distribution was setup and verified with WSL 2, enabling Linux command-line and DevOps tool usage on Windows.

# Conclusion

WSL provides a powerful Linux development environment on Windows. It allows seamless execution of Linux tools and is highly suitable for cloud computing, DevOps, and container-based workflows.

# EXPERIMENT - 1

# Comparison of Virtual Machines (VMs) and Containers using Ubuntu and Nginx

# Aim

To study, implement, and compare Virtual Machines (VMs) and Containers by deploying an Ubuntu-based Nginx web server in both environments and analyzing their resource utilization, performance, and operational characteristics.

# Objectives

1. To understand the conceptual difference between Virtual Machines and Containers.  
2. To install and configure a Virtual Machine using Virtual Box and Vagrant.  
3. To install and configure Containers using Docker inside WSL.  
4. To deploy Nginx web server on both VM and Container.

5. To compare performance, startup time, and resource usage of VMs and Containers.

# System Requirements

# Hardware Requirements

64-bit system with virtualization enabled in BIOS  
Minimum 8 GB RAM (4 GB acceptable)  
- Stable internet connection

# Software Requirements (Windows Host)

Oracle VirtualBox  
Vagrant  
Windows Subsystem for Linux (WSL 2)  
- Ubuntu (WSL distribution)  
Docker Engine (Docker CLI)

# Theory

# Virtual Machine (VM)

A Virtual Machine emulates a complete physical computer, including its own operating system, kernel, libraries, and hardware drivers. Each VM runs on top of a hypervisor such as VirtualBox.

# Characteristics:

Full OS per VM  
• Strong isolation  
High resource usage  
• Slower startup time

# Container

Containers virtualize at the operating system level. They share the host OS kernel while isolating applications and dependencies in user space.

# Characteristics:

- Shared kernel  
Lightweight  
- Fast startup  
Efficient resource utilization

# Experiment Setup

# PART A: Virtual Machine Setup (Using Virtual Box & Vagrant)

# Step 1: Install Virtual Box

1. Download Virtual Box from the official website  
2. Run installer with default settings  
3. Restart system if prompted

![Oracle VirtualBox](virtualbox.png)


Oracle VirtualBox

https://www.virtualbox.org

# Oracle VirtualBox

VirtualBox is a general-purpose full virtualization software for x86_64 hardware with version 7.1 additionally for macOS/Arm and with version 7.2 also for ...

Downloads

Download VirtualBox. The VirtualBox Extension Pack is ...

Download VirtualBox for Linux ...

Download VirtualBox for Linux Hosts ¶ The VirtualBox base …

>

![](downloadvirtualbox.png)

# Step 2: Install Vagrant

1. Download Vagrant for Windows

![](Vagrant.png)

2. Install using default options  
3. Verify installation:

vagrant -version  
```batch
PS C:\WINDOWS\system32> cd C:\Users\HP\Desktop  
PS C:\Users\HP\Desktop> vagrant --version  
Vagrant 2.4.9
```

# Step 3: Create Ubuntu VM using Vagrant

1. Create a new directory:

mkdir vm-lab

cd vm-lab

2. Initialize Vagrant with Ubuntu box:

vagrant init ubuntu/jammy64

3.Start the Virtual Machine:

vagrant up


![](Vagrantup.png)


# 4. Access the VM:

# vagrant ssh

![](Vagrantssh.png)

# Step 4: Install Nginx inside VM

sudo apt update  
sudo apt install -y nginx  
sudo systemd start nginx

![](InstallNGINX.png)

# Step 5: Verify Nginx in VM

curl localhost

Nginx default HTML page confirms successful deployment.

![](Verifynginx.png)

# Step 6: Stop and Remove VM
![](stopremovevm.png)


# PART B: Container Setup using Docker inside WSL

# Step 1: Install WSL

ws1 --install

Reboot system after installation.

# Step 2: Install Ubuntu on WSL

wsl --install -d Ubuntu

```batch
PS C:\WINDOWS\system32> wsl --install -d Ubuntu  
Downloading: Ubuntu  
Installing: Ubuntu  
Distribution successfully installed. It can be launched via 'wsl.exe -d Ubuntu'  
Launching Ubuntu...  
Provisioning the new WSL instance Ubuntu  
This might take a while...  
Create a default Unix user account: mayank  
New password:  
Retype new password:  
passwd: password updated successfully  
To run a command as administrator (user "root"), use "sudo <command>".  
See "man sudo root" for details
```

# Step 3: Install Docker Engine inside WSL

sudo aptupdate

sudo apt install -y docker.io

```txt
mayank@DESKTOP-OC3UMDN:/mnt/c/WINDOWS/system32$ sudo apt install docker.io  
sudo systemdctl start docker  
[sudo] password for mayank:  
Sorry, try again.  
[sudo] password for mayank:  
Reading package lists... Done  
Building dependency tree... Done  
Reading state information... Done
```

sudo systemd start docker  
sudo usermod -aG docker $USER

![](images/30a71c921aa9b35f2be5104a709d39c339372b5c4e5dfe62a4011851139f541d.jpg)

Logout and login again to apply group changes.

# Step 4: Run Nginx Container

docker pullnginx  
```txt
mayank@DESKTOP-OC3UMDN:\~$ docker pull nginx  
Using default tag: latest  
latest: Pulling from library/nginx  
Digest: sha256:c881927c4077710ac4b1da63b83aa163937fb47457950c267d92f7e4dedf4aec  
Status: Image is up to date for nginx:latest  
docker.io/library/nginx:latest
```

docker run -d -p 8080:80 --namenginx-containernginx  
```txt
mayank@DESKTOP-OC3UMDN:\~\$ docker run -d -p 8080:80 --name nginx-container nginx  
4edbc7838396ad3d0d0a53f04bfo1a1bfbdc06fbdb66c968043aaf90a1afc0fc  
mayank@DESKTOP-OC3UMDN:\~\$ docker ps  
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES  
4edbc7838396 nginx "/docker-entrypoint..." 10 seconds ago Up 10 seconds 0.0.0.0:8880->80/tcp, [::]:8880->80/tcp nginx-container  
mayank@DESKTOP-OC3UMDN:\~$
```

Step 5: Verify Nginx Container curl localhost:8080  
```html
mayank@DESKTOP-OC3UMDN:\~$ curl localhost:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!\</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!\</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>
<For online documentation and support please refer to
<a href="http://nginx.org/"nginx.org</a>.<br />
Commercial support is available at
<a href="http://nginx.com/"nginx.com</a>.<p>
<Please thank you for using nginx.</p>
</body>
</html>
mayank@DESKTOP-OC3UMDN:\~$
```

Nginx default page confirms container deployment.

# Resource Utilization Observation

# VM Observation Commands

free -h

htop

systemd-analyze

# Container Observation Commands

docker stats

free -h



# Common Troubleshooting

# VirtualBox Issues

• VT-x / AMD-V not enabled  $\rightarrow$  Enable virtualization in BIOS  
Hyper-V conflict  $\rightarrow$  Disable Hyper-V in Windows

# Vagrant Issues

- Box download failure  $\rightarrow$  Check firewall  
- SSH timeout  $\rightarrow$  Run vagrant reload

# Docker Issues (WSL)

Permission denied  $\rightarrow$  Ensure user added to docker group  
Docker service not running:

sudo systemd start docker

# Result

The experiment successfully demonstrated that containers are lightweight, faster, and more resource-efficient than

virtual machines, while virtual machines provide stronger isolation and full OS abstraction.

exp1

# Conclusion

Containers are best suited for modern cloud-native and DevOps workflows due to their speed and efficiency, whereas Virtual Machines are preferred when full isolation and OS-level control are required.

# Viva-Voice Questions

1. What is the main difference between VM and container?  
2. Why do containers start faster than VMs?  
3. What role does a hypervisor play?  
4. Can containers run different OS kernels?  
5. Why is Docker considered lightweight?

# References

1. VirtualBox Documentation  
2. Vagrant Documentation  
3. Docker Official Documentation
