# Experiment 9 — Ansible: Configuration Management and Automation

## Theory

### Problem Statement

Managing infrastructure manually across multiple servers leads to configuration drift, inconsistent environments, and time-consuming repetitive tasks. Scaling from one server to hundreds becomes nearly impossible with manual SSH-based administration.

### What is Ansible?

Ansible is an open-source automation tool for **configuration management**, **application deployment**, and **orchestration**. It follows an **agentless architecture** — using SSH for Linux and WinRM for Windows — and uses YAML-based **playbooks** to define automation tasks.

Ansible has become the standard choice among enterprise automation solutions because it is simple yet powerful, agentless, community-powered, predictable, and secure.

### How Ansible Solves the Problem

| Problem | Ansible Solution |
|---|---|
| Agent installation on every server | Agentless — uses SSH only |
| Running playbooks twice breaks things | Idempotency — same result every time |
| Imperative scripts hard to read | Declarative YAML — describe desired state |
| Waiting for changes to propagate | Push-based — initiates from control node immediately |

---

## Key Concepts

| Component | Description |
|---|---|
| **Control Node** | Machine with Ansible installed — where you run commands |
| **Managed Nodes** | Target servers — no Ansible agent needed |
| **Inventory** | File listing all managed nodes (EC2 instances, servers, etc.) |
| **Playbooks** | YAML files containing a sequence of automation steps |
| **Tasks** | Individual actions in playbooks (e.g., installing a package) |
| **Modules** | Built-in functionality to perform tasks (e.g., `apt`, `yum`, `service`) |
| **Roles** | Pre-defined reusable automation scripts |

### How Ansible Works

Ansible connects from the **control node** to the **managed nodes** via SSH, sending commands and instructions. The units of code it executes are called **modules**. Each module is invoked by a **task**, and an ordered list of tasks forms a **playbook**. The managed machines are listed in an **inventory file** grouped into categories.

```
Control Node (Ansible installed)
        │
        │ SSH
        ├──────────── Managed Node 1
        ├──────────── Managed Node 2
        └──────────── Managed Node 3
```

No extra agents required on managed nodes — just a terminal and a text editor to get started.

---

## Part A — Hands-On Lab

### Step 1: Install Ansible

**Via pip (recommended for macOS/Linux):**

```bash
pip install ansible
ansible --version
```

**Via apt (Ubuntu/Debian):**

```bash
sudo apt update -y
sudo apt install ansible -y
ansible --version
```

**Post-installation check:**

```bash
ansible localhost -m ping
```

**Expected output:**

```
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

---

### Step 2: Create SSH Key Pair

Ansible uses SSH key-based authentication to connect to managed nodes without passwords.

```bash
ssh-keygen -t rsa -b 4096
# Accept all defaults — keys saved to ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub
```

Copy keys to the current working directory (needed for building the Docker image):

```bash
cp ~/.ssh/id_rsa.pub .
cp ~/.ssh/id_rsa .
```

**Key placement explained:**

| File | Location | Purpose |
|---|---|---|
| `id_rsa` (Private Key) | Control node only | Used to authenticate when connecting — **never share this** |
| `id_rsa.pub` (Public Key) | Remote server `~/.ssh/authorized_keys` | Grants access to anyone with the matching private key |

---

### Step 3: Create the Docker Image (Ubuntu SSH Server)

Create a `Dockerfile` that builds a custom Ubuntu image with OpenSSH pre-configured and our public key baked in:

```dockerfile
FROM ubuntu

RUN apt update -y
RUN apt install -y python3 python3-pip openssh-server
RUN mkdir -p /var/run/sshd

# Configure SSH
RUN mkdir -p /run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Create .ssh directory and set proper permissions
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh

# Copy SSH keys into the image
COPY id_rsa /root/.ssh/id_rsa
COPY id_rsa.pub /root/.ssh/authorized_keys

# Set proper permissions
RUN chmod 600 /root/.ssh/id_rsa && \
    chmod 644 /root/.ssh/authorized_keys

# Fix for SSH login
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

# Expose SSH port
EXPOSE 22

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]
```

Build the image:

```bash
docker build -t ubuntu-server .
```

---
![alt text](screenshots/dockerfile.png)
### Step 4: Launch 4 Server Containers

```bash
for i in {1..4}; do
    echo -e "\n Creating server${i}\n"
    docker run -d --rm -p 220${i}:22 --name server${i} ubuntu-server
    echo -e "IP of server${i} is $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server${i})"
done
```

**Expected output:**

```
Creating server1
IP of server1 is 172.17.0.2

Creating server2
IP of server2 is 172.17.0.3

Creating server3
IP of server3 is 172.17.0.4

Creating server4
IP of server4 is 172.17.0.5
```

---

### Step 5: Create Ansible Inventory

This script auto-generates `inventory.ini` with the real container IPs:

```bash
echo "[servers]" > inventory.ini
for i in {1..4}; do
    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server${i} >> inventory.ini
done

cat << EOF >> inventory.ini

[servers:vars]
ansible_user=root
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
EOF
```

Review the generated file:

```bash
cat inventory.ini
```

**Expected `inventory.ini` content:**

![alt text](image-2.png)

### Step 6: Test Connectivity

Manual SSH test to confirm keys work:

```bash
ssh -i ~/.ssh/id_rsa root@172.17.0.2
```

Ansible ping test across all servers:

```bash
ansible all -i inventory.ini -m ping
```

**Expected output:**

```
172.17.0.2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
172.17.0.3 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
172.17.0.4 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
172.17.0.5 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
![alt text](image-3.png)
For verbose output (useful for debugging):





### Step 7: Create and Run Playbook (`update.yml`)


```yaml
---
- name: Update and configure servers
  hosts: all
  become: yes
  tasks:

    - name: Update apt packages
      apt:
        update_cache: yes
        upgrade: dist

    - name: Install required packages
      apt:
        name: ["vim", "htop", "wget"]
        state: present

    - name: Create test file
      copy:
        dest: /root/ansible_test.txt
        content: "Configured by Ansible on {{ inventory_hostname }}"
```
![alt text](image-4.png)
Run the playbook:

```bash
ansible-playbook -i inventory.ini update.yml
```

**Expected output:**

```
PLAY [Update and configure servers] ********************************************

TASK [Gathering Facts] *********************************************************
ok: [172.17.0.2]
ok: [172.17.0.3]
ok: [172.17.0.4]
ok: [172.17.0.5]

TASK [Update apt packages] *****************************************************
changed: [172.17.0.2]
changed: [172.17.0.3]
...

TASK [Install required packages] ***********************************************
changed: [172.17.0.2]
...

TASK [Create test file] ********************************************************
changed: [172.17.0.2]
...

PLAY RECAP *********************************************************************
172.17.0.2  : ok=4  changed=3  unreachable=0  failed=0
172.17.0.3  : ok=4  changed=3  unreachable=0  failed=0
172.17.0.4  : ok=4  changed=3  unreachable=0  failed=0
172.17.0.5  : ok=4  changed=3  unreachable=0  failed=0
```

---
![alt text](screenshots/imagecopy.png)

### Step 8: Create Advanced Playbook (`playbook1.yml`)

```yaml
---
- name: Configure multiple servers
  hosts: servers
  become: yes
  tasks:

    - name: Update apt package index
      apt:
        update_cache: yes

    - name: Install Python 3 (latest available)
      apt:
        name: python3
        state: latest

    - name: Create test file with content
      copy:
        dest: /root/test_file.txt
        content: |
          This is a test file created by Ansible
          Server name: {{ inventory_hostname }}
          Current date: {{ ansible_date_time.date }}

    - name: Display system information
      command: uname -a
      register: uname_output

    - name: Show disk space
      command: df -h
      register: disk_space

    - name: Print results
      debug:
        msg:
          - "System info: {{ uname_output.stdout }}"
          - "Disk space: {{ disk_space.stdout_lines }}"
```

Run it:

```bash
ansible-playbook -i inventory.ini playbook1.yml
```

---

### Step 9: Verify Changes

Using Ansible to read the created file across all servers:

```bash
ansible all -i inventory.ini -m command -a "cat /root/ansible_test.txt"
```
![alt text](image.png)
Using Docker exec directly:

```bash
for i in {1..4}; do
    docker exec server${i} cat /root/ansible_test.txt
done
```
![alt text](image-1.png)
**Expected output on each server:**

```
Configured by Ansible on 172.17.0.2
Configured by Ansible on 172.17.0.3
Configured by Ansible on 172.17.0.4
Configured by Ansible on 172.17.0.5
```

---


### Step 10: Cleanup

Stop all server containers:

```bash
for i in {1..4}; do
    docker rm -f server${i}
done
```

---



## Complete Workflow Summary

```
1. Setup SSH keys
        ↓
2. Build ubuntu-server Docker image
        ↓
3. Launch 4 containers (server1–server4)
        ↓
4. Generate inventory.ini with container IPs
        ↓
5. Test connectivity (ansible -m ping)
        ↓
6. Run playbook (ansible-playbook)
        ↓
7. Verify changes
        ↓
8. Cleanup (docker rm -f)
```

---

## Key Takeaways

1. **Agentless** — Ansible only needs SSH on managed nodes, no extra software to install
2. **Idempotent** — running the same playbook twice produces the same result, no unintended side effects
3. **Declarative** — you describe *what* you want (nginx installed, file present), not *how* to do it step by step
4. **Inventory** — the single source of truth for all managed nodes, supports groups and variables
5. **Modules** — 3000+ built-in modules cover everything from `apt`/`yum` to AWS/Azure/GCP resources
6. **`register` + `debug`** — capture command output and print it back, useful for auditing and troubleshooting
7. **Playbooks scale** — the same playbook that ran on 4 Docker containers runs identically on 400 EC2 instances

---

## Screenshots

>  All screenshots are stored in the `screenshots/` folder.


## References

- [Ansible Official Documentation](https://docs.ansible.com/)
- [Ansible Tutorial — Spacelift](https://spacelift.io/blog/ansible-tutorial)
- [Ansible Official Website](https://www.ansible.com/)
- [Ansible Tower GUI](https://ansible.github.io/lightbulb/decks/intro-to-ansible-tower.html)
- [Ansible Tower Tutorial — GeeksforGeeks](https://www.geeksforgeeks.org/devops/ansible-tower/)

---

*Experiment 9 | Containerization and DevOps Lab | UPES Dehradun*
