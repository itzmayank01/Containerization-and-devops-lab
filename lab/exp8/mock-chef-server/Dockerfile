FROM ruby:3.2-alpine

RUN apk add --no-cache bash openssl curl jq build-base \
    && gem install chef-zero

COPY run.sh /usr/bin/run.sh
COPY chef-server-ctl /usr/bin/chef-server-ctl

RUN chmod +x /usr/bin/run.sh /usr/bin/chef-server-ctl \
    && mkdir -p /var/opt/opscode

EXPOSE 443

CMD ["/usr/bin/run.sh"]
