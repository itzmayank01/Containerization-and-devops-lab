# Experiment 8: Chef - Configuration Management

**Name:** Mayank Thakur
**Subject:** Containerization and DevOps

---

## Problem Statement

Managing infrastructure manually across multiple servers leads to configuration drift, inconsistent environments, and time-consuming repetitive tasks. While Ansible solves this with agentless SSH, Chef offers a pull-based approach where nodes regularly check in with a central server, ensuring continuous compliance even when network connections are intermittent.

---

## 1. What is Chef?

Chef is an automation platform that transforms infrastructure into code using **Ruby-based DSL** (Domain Specific Language). It follows a **pull-based model** where agents (Chef clients) periodically pull configurations from a central Chef server.

**Key Difference from Ansible:** Chef requires an agent on managed nodes and a central server, but offers more powerful dependency management and scales better for large enterprises.

---

## 2. How Chef Solves the Problem

- **Pull-based Model:** Nodes check in with Chef server regularly, ensuring consistent state
- **Idempotent Resources:** Resources ensure desired state regardless of how many times applied
- **Infrastructure as Code:** All configurations version-controlled and testable
- **Community Cookbooks:** Reusable configurations for common applications

---

## 3. Key Concepts

| Term | Description |
|------|-------------|
| **Chef Server** | Central repository for cookbooks, policies, and node data |
| **Chef Workstation** | Development machine where cookbooks are created and tested |
| **Chef Node** | Managed machine with Chef client installed |
| **Cookbook** | Collection of recipes, attributes, templates, and files |
| **Recipe** | Ruby-based file containing resource declarations |
| **Resource** | Building blocks (`package`, `service`, `file`, `template`, etc.) |
| **Run List** | Ordered list of recipes applied to a node |
| **Ohai** | System profiling tool that collects node attributes |

---

## 4. How Chef Works — Architecture

```
CHEF SERVER ARCHITECTURE
─────────────────────────────────────────────────────

  WORKSTATION              CHEF SERVER (Port 443)
  ┌──────────────┐         ┌──────────────────────┐
  │ • Cookbooks  │─────────▶ • Cookbooks (versioned)│
  │ • Roles      │  knife   │ • Node Data          │
  │ • Environments│  upload │ • Client Auth Keys   │
  │ • Data Bags  │         │ • Search Indexes      │
  └──────────────┘         └──────────────────────┘
                                      │
                              Pull (every 30 min)
                                      │
                           ┌──────────▼──────────┐
                           │    MANAGED NODES     │
                           │  Chef Client (Agent) │
                           │  Chef Client (Agent) │
                           └─────────────────────┘
```

---

## 5. Benefits of Chef

- **Pull-based Architecture:** Nodes check in regularly, ensuring compliance
- **Powerful Ruby DSL:** More expressive than YAML for complex logic
- **Large Community:** 4000+ community cookbooks
- **Test Kitchen:** Built-in testing framework
- **Compliance:** Continuous auditing capabilities

---

## Part A: Chef Solo (Simpler — No Server Required)

### Architecture

```
CHEF SOLO ARCHITECTURE
──────────────────────────────────────────────

  CONTROL NODE (Your Machine)    MANAGED NODES
  ┌─────────────────────┐        ┌───────────────────┐
  │ • Cookbooks         │──ssh──▶│ Chef Client       │
  │ • Recipes           │  scp   │ (Local Mode)      │
  │ • Attributes        │        └───────────────────┘
  │ • Templates         │
  └─────────────────────┘
  No central server needed — runs in local mode
```

---

### Step 1: Install Chef Workstation

```bash
# Ubuntu/Debian installation
wget https://packages.chef.io/files/stable/chef-workstation/24.10.1144/ubuntu/22.04/chef-workstation_24.10.1144-1_amd64.deb
sudo dpkg -i chef-workstation_24.10.1144-1_amd64.deb

# Verify installation
chef --version
# Expected: Chef Workstation version: 24.10.1144

# Install Chef Client on managed nodes (Docker containers)
docker exec server1 apt-get update
docker exec server1 apt-get install -y curl
docker exec server1 curl -L https://omnitruck.chef.io/install.sh | bash
```
![alt text](exp8%20screenshots/image.png)
---

### Step 2: Setup Lab Environment (Docker Containers)

```bash
# Create network
docker network create chef-lab

# Create SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/chef-key -N ""

# Build Chef-ready Docker image
cat > Dockerfile.chef << 'EOF'
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 openssh-server sudo curl systemd && \
    apt-get clean

RUN mkdir -p /var/run/sshd && \
    echo 'root:chef' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
COPY ~/.ssh/chef-key.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
EOF

# Build image
docker build -f Dockerfile.chef -t chef-node .

# Create 4 test nodes
for i in {1..4}; do
  docker run -d \
    --name node${i} \
    --network chef-lab \
    -p 222${i}:22 \
    chef-node
  echo "Node${i} created with SSH on port 222${i}"
done

# Copy SSH key to nodes
for i in {1..4}; do
  docker exec node${i} mkdir -p /root/.ssh
  docker cp ~/.ssh/chef-key.pub node${i}:/root/.ssh/authorized_keys
  docker exec node${i} chmod 600 /root/.ssh/authorized_keys
done
```
![alt text](exp8%20screenshots/image-2.png)
![alt text](exp8%20screenshots/image-1.png)
![alt text](exp8%20screenshots/image-3.png)
---

### Step 3: Create First Cookbook

```bash
mkdir -p ~/chef-repo/cookbooks
cd ~/chef-repo

chef generate cookbook cookbooks/basics

cat > cookbooks/basics/metadata.rb << 'EOF'
name 'basics'
maintainer 'DevOps Lab'
maintainer_email 'lab@example.com'
license 'Apache-2.0'
description 'Installs/Configures basic system settings'
version '0.1.0'
chef_version '>= 16.0'
depends 'apt'
EOF
```
![alt text](exp8%20screenshots/image-4.png)
---

### Step 4: Create Recipes

**Default Recipe** — `cookbooks/basics/recipes/default.rb`

```ruby
include_recipe 'basics::packages'
include_recipe 'basics::files'
include_recipe 'basics::services'
```
![alt text](exp8%20screenshots/image-6.png)
**Packages Recipe** — `cookbooks/basics/recipes/packages.rb`

```ruby
apt_update 'update' do
  action :update
  frequency 86400
end

%w(vim htop wget curl git net-tools).each do |pkg|
  package pkg do
    action :install
  end
end

package 'python3' do
  action :install
  version '3.10.*'
end
```
![alt text](exp8%20screenshots/image-7.png)
**Files Recipe** — `cookbooks/basics/recipes/files.rb`

```ruby
directory '/opt/chef-demo' do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

file '/opt/chef-demo/README.md' do
  content <<~EOH
    # Chef Managed System
    ======================
    Hostname: #{node['hostname']}
    IP Address: #{node['ipaddress']}
    OS: #{node['platform']} #{node['platform_version']}
    Managed by: Chef
    Last Converged: #{Time.now}
  EOH
  mode '0644'
  action :create
end

cookbook_file '/opt/chef-demo/welcome.txt' do
  source 'welcome.txt'
  mode '0644'
  action :create
end
```

**Services Recipe** — `cookbooks/basics/recipes/services.rb`

```ruby
service 'ssh' do
  action [:enable, :start]
end

template '/etc/systemd/system/demo.service' do
  source 'demo.service.erb'
  owner 'root'
  group 'root'
  mode '0644'
  notifies :run, 'execute[systemctl daemon-reload]', :immediately
end

execute 'systemctl daemon-reload' do
  command 'systemctl daemon-reload'
  action :nothing
end

service 'demo' do
  action [:enable, :start]
  subscribes :restart, 'template[/etc/systemd/system/demo.service]'
end
```

---

### Step 5: Create Templates and Files

**Service Template** — `cookbooks/basics/templates/demo.service.erb`

```ini
[Unit]
Description=Chef Demo Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do echo "Chef Demo Service: $(date)" >> /var/log/demo.log; sleep 60; done'
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```
![alt text](exp8%20screenshots/image-8.png)
**Welcome File** — `cookbooks/basics/files/welcome.txt`

```
=====================================
Welcome to Chef Managed System
=====================================
This system is configured using Chef.
All changes should be made through cookbooks.
=====================================
```

---

### Step 6: Create Node Inventory

```bash
cat > nodes.json << 'EOF'
{
  "node1": { "run_list": ["recipe[basics]"] },
  "node2": { "run_list": ["recipe[basics]"] },
  "node3": { "run_list": ["recipe[basics]"] },
  "node4": { "run_list": ["recipe[basics]"] }
}
EOF

mkdir -p ~/chef-repo/.chef
cat > ~/chef-repo/.chef/config.rb << 'EOF'
current_dir = File.dirname(__FILE__)
node_name 'workstation'
client_key "#{current_dir}/workstation.pem"
chef_repo_path "#{current_dir}/.."
cookbook_path ["#{current_dir}/../cookbooks"]
EOF

cat > ~/chef-repo/run-chef.sh << 'EOF'
#!/bin/bash
for i in {1..4}; do
  echo "====================================="
  echo "Configuring node${i}"
  echo "====================================="
  ssh -i ~/.ssh/chef-key -o StrictHostKeyChecking=no root@localhost -p 222${i} "mkdir -p /opt/chef/cookbooks"
  scp -i ~/.ssh/chef-key -P 222${i} -r ~/chef-repo/cookbooks root@localhost:/opt/chef/
  ssh -i ~/.ssh/chef-key -p 222${i} root@localhost << 'ENDSSH'
cd /opt/chef
chef-client --local-mode --runlist 'recipe[basics]'
ENDSSH
  echo "Node${i} configured successfully"
done
EOF
chmod +x ~/chef-repo/run-chef.sh
```

---

### Step 7: Run Chef Solo

```bash
cd ~/chef-repo
./run-chef.sh

# Verify changes on nodes
for i in {1..4}; do
  echo "=== Node${i} ==="
  ssh -i ~/.ssh/chef-key -p 222${i} root@localhost "cat /opt/chef-demo/README.md"
  echo ""
done
```
![alt text](exp8%20screenshots/image-9.png)
---

## Part B: Chef Server (Full Enterprise Setup)

### Step 1: Setup Chef Server

```bash
docker pull chef/chef-server:latest

docker run -d \
  --name chef-server \
  --network chef-lab \
  -p 443:443 \
  -v chef-server-data:/var/opt/opscode \
  chef/chef-server:latest

docker logs -f chef-server

docker exec chef-server chef-server-ctl user-create \
  admin "Admin" "User" admin@example.com 'admin123' \
  --filename /tmp/admin.pem

docker exec chef-server chef-server-ctl org-create \
  devops "DevOps Lab" --association admin \
  --filename /tmp/devops-validator.pem

docker cp chef-server:/tmp/admin.pem ~/chef-repo/.chef/
docker cp chef-server:/tmp/devops-validator.pem ~/chef-repo/.chef/
```

---
![alt text](image.png)

### Step 2: Configure Knife

```bash
cat > ~/chef-repo/.chef/knife.rb << 'EOF'
current_dir = File.dirname(__FILE__)
log_level :info
log_location STDOUT
node_name "admin"
client_key "#{current_dir}/admin.pem"
validation_client_name "devops-validator"
validation_key "#{current_dir}/devops-validator.pem"
chef_server_url "https://chef-server/organizations/devops"
cookbook_path ["#{current_dir}/../cookbooks"]
ssl_verify_mode :verify_none
EOF

cd ~/chef-repo
knife ssl check
knife client list
```

---
![alt text](image-1.png)

### Step 3: Create Advanced Cookbook (webapp)

```bash
chef generate cookbook cookbooks/webapp
```

**Default Recipe**

```ruby
include_recipe 'webapp::webserver'
include_recipe 'webapp::app'
```

**Webserver Recipe**

```ruby
package 'nginx' do
  action :install
end

template '/etc/nginx/sites-available/webapp' do
  source 'webapp.conf.erb'
  owner 'root'
  group 'root'
  mode '0644'
  notifies :reload, 'service[nginx]'
end

link '/etc/nginx/sites-enabled/webapp' do
  to '/etc/nginx/sites-available/webapp'
  notifies :reload, 'service[nginx]'
end

file '/etc/nginx/sites-enabled/default' do
  action :delete
  notifies :reload, 'service[nginx]'
end

service 'nginx' do
  action [:enable, :start]
end
```
![alt text](image-2.png)
**App Recipe**

```ruby
apt_repository 'nodejs' do
  uri 'https://deb.nodesource.com/node_16.x'
  components ['main']
  key 'https://deb.nodesource.com/gpgkey/nodesource.gpg.key'
  action :add
end

package 'nodejs' do
  action :install
end

directory '/opt/webapp' do
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

git '/opt/webapp' do
  repository 'https://github.com/chef-training/sample-node-app.git'
  revision 'main'
  action :sync
  notifies :run, 'execute[npm install]', :immediately
end

execute 'npm install' do
  cwd '/opt/webapp'
  command 'npm install --production'
  action :nothing
end

template '/etc/systemd/system/webapp.service' do
  source 'webapp.service.erb'
  owner 'root'
  group 'root'
  mode '0644'
  notifies :run, 'execute[systemctl daemon-reload]', :immediately
  notifies :restart, 'service[webapp]'
end

execute 'systemctl daemon-reload' do
  command 'systemctl daemon-reload'
  action :nothing
end

service 'webapp' do
  action [:enable, :start]
end
```

---
![alt text](image-3.png)
### Step 4: Create Templates

**Nginx Config** — `cookbooks/webapp/templates/webapp.conf.erb`

```nginx
server {
    listen 80;
    server_name <%= node['hostname'] %>;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
![alt text](image-4.png)
**Webapp Service** — `cookbooks/webapp/templates/webapp.service.erb`

```ini
[Unit]
Description=Node.js Web Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/webapp
ExecStart=/usr/bin/node server.js
Restart=on-failure
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

---

### Step 5: Bootstrap Nodes

```bash
for i in {1..4}; do
  docker exec node${i} curl -L https://omnitruck.chef.io/install.sh | bash
  docker cp ~/chef-repo/.chef/devops-validator.pem node${i}:/etc/chef/
  docker exec node${i} bash -c "cat > /etc/chef/client.rb << 'EOF'
log_level :info
log_location STDOUT
chef_server_url 'https://chef-server/organizations/devops'
validation_client_name 'devops-validator'
validation_key '/etc/chef/devops-validator.pem'
node_name 'node${i}'
ssl_verify_mode :verify_none
EOF"
done
```

---

### Step 6: Upload Cookbook and Bootstrap

```bash
cd ~/chef-repo
knife cookbook upload webapp

for i in {1..4}; do
  knife bootstrap localhost \
    --ssh-user root \
    --ssh-port 222${i} \
    --ssh-identity-file ~/.ssh/chef-key \
    --node-name node${i} \
    --run-list 'recipe[webapp]'
done

knife node list
knife status
```

---

### Step 7: Verify Configuration

```bash
knife node show node1
knife search node "platform:ubuntu"

knife ssh "name:node1" "chef-client" \
  --ssh-user root \
  --ssh-identity-file ~/.ssh/chef-key \
  --attribute ipaddress

for i in {1..4}; do
  echo "=== Node${i} ==="
  curl -s http://localhost:222${i} || echo "Service not accessible"
done
```

---
![alt text](image-6.png)
![alt text](image-7.png)

## 6. Comparison: Chef Solo vs Chef Server

| Aspect | Chef Solo (Part A) | Chef Server (Part B) |
|--------|-------------------|---------------------|
| Complexity | Low | High |
| Setup Time | ~15 minutes | ~45 minutes |
| Server Required | No | Yes |
| Scalability | Manual per node | Centralized |
| Node Management | Direct SSH | Chef Server |
| Search Capabilities | No | Yes |
| Role-Based Config | Limited | Full support |
| Best For | Learning, small setups | Production, enterprises |

---

## 7. Chef vs Ansible Comparison

| Feature | Chef | Ansible |
|---------|------|---------|
| Architecture | Pull-based (agent) | Push-based (agentless) |
| Language | Ruby DSL | YAML |
| Learning Curve | Steep | Gentle |
| Setup Complexity | High | Low |
| Idempotency | Yes | Yes |
| Real-time Changes | Delayed (pull interval) | Immediate (push) |
| Scaling | Excellent (5000+ nodes) | Good (up to 2000 nodes) |
| Community | Mature, 4000+ cookbooks | Largest, 3000+ collections |
| Use Case | Large enterprises | Small to medium, cloud |


---

## 9. Cleanup

```bash
for i in {1..4}; do docker rm -f node${i}; done
docker rm -f chef-server
rm -rf ~/chef-repo
```

---

## 10. Optional Read — Chef Solo vs Ansible Deep Dive

### What was Chef Solo?

Chef Solo allowed running Chef **without a central server**. It ran locally on a machine, with cookbooks and JSON configs provided manually — essentially *"a script executor with idempotency"*.

**Key limitations:**
- No centralized state management
- No node discovery or inventory management
- No orchestration across nodes
- No API or UI

### Core Conceptual Difference

| | Chef Solo | Ansible |
|--|-----------|---------|
| Agent required | No | No |
| Central control | No | Yes |
| Multi-node orchestration | No | Yes |
| Config delivery | Manual copy per machine | Push from control node |
| Node awareness | None | Global inventory view |

### Why Chef Solo Never Became Dominant

It lacked what modern DevOps needed — infrastructure orchestration, central visibility, easy scaling, and simplicity. Ansible solved all of these without requiring agents.

### Evolution Timeline

```
Chef (classic)  →  Heavy, enterprise, agent-based
Chef Solo       →  Lightweight but very limited
Ansible         →  Agentless + centralized (sweet spot)
```

### Simple Analogy

- **Chef with server:** Manager giving instructions via a central system
- **Chef Solo:** Giving each worker a USB stick with instructions
- **Ansible:** A remote control system managing all workers live

---

## 11. Observations

- Chef uses a **pull-based model** — nodes periodically converge to desired state
- **Idempotency** is core — running the same recipe multiple times produces the same result
- Chef Solo is ideal for learning; Chef Server is production-grade and enterprise-ready
- `knife` is the primary CLI for interacting with Chef Server
- Recipes written in Ruby DSL are more powerful but steeper to learn than Ansible's YAML
- Docker-based lab setup simplifies node provisioning for learning purposes

---

## 12. Result

Successfully studied and implemented Chef configuration management:
- **Part A (Chef Solo):** Local mode cookbook execution across Docker nodes via SSH
- **Part B (Chef Server):** Full enterprise setup with `knife` bootstrapping and centralized cookbook management
- Compared Chef Solo vs Chef Server and Chef vs Ansible in terms of architecture, scalability, and use cases

---

## 13. Viva Questions

**Q1. What is the difference between Chef Solo and Chef Server?**
Chef Solo runs locally without a central server — cookbooks are manually pushed to nodes. Chef Server provides centralized management where nodes pull their configurations automatically every ~30 minutes.

**Q2. What is a Cookbook in Chef?**
A Cookbook is the fundamental unit of configuration — it contains recipes, attributes, templates, files, and metadata defining how a node should be configured.

**Q3. What is idempotency in Chef?**
Idempotency means applying a recipe multiple times always results in the same system state. Chef resources only make changes when the current state differs from the desired state.

**Q4. What is `knife` in Chef?**
`knife` is the CLI tool used to interact with the Chef Server — uploading cookbooks, bootstrapping nodes, running remote commands, and querying node data.

**Q5. What is Ohai?**
Ohai is Chef's system discovery tool that automatically collects node attributes (hostname, IP, OS, memory, etc.) and makes them available in recipes as `node['attribute']`.

**Q6. Why is Chef pull-based while Ansible is push-based?**
In Chef, the Chef client on each node periodically contacts the Chef Server and pulls its configuration. In Ansible, the control node pushes commands to managed nodes via SSH — no agent is needed.

**Q7. What is a Run List?**
A Run List is an ordered list of recipes and roles assigned to a node, defining what configurations will be applied during a Chef client run.

---

## 14. Key Takeaways

- Chef transforms infrastructure into code using **Ruby DSL**
- **Pull-based model** ensures nodes continuously converge to desired state
- Chef Solo = no server, manual delivery; Chef Server = centralized, scalable
- Ansible is simpler and agentless — better for small/medium environments
- Chef excels in **large enterprises** needing complex dependency management
- Always use Chef's credentials mechanisms — **never hardcode secrets** in recipes

---

## 15. References

- Official Website: [https://www.chef.io](https://www.chef.io)
- Documentation: [https://docs.chef.io](https://docs.chef.io)
- Chef Supermarket: [https://supermarket.chef.io](https://supermarket.chef.io)
- Learn Chef: [https://learn.chef.io](https://learn.chef.io)

---

*Experiment completed as part of Containerization and DevOps Lab.*
