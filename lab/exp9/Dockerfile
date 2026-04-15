FROM ubuntu

RUN apt update -y
RUN apt install -y python3 python3-pip openssh-server sudo

RUN mkdir -p /var/run/sshd

# Enable root login + SSH config
RUN echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# SSH folder setup
RUN mkdir -p /root/.ssh
RUN chmod 700 /root/.ssh

# Copy keys (IMPORTANT)
COPY id_rsa.pub /root/.ssh/authorized_keys

RUN chmod 600 /root/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
