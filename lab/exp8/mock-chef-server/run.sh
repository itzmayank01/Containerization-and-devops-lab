#!/bin/bash
echo "Starting mock Chef-Server..."

# Run chef-zero inside thin or weasel etc for SSL.
# wait, chef-zero itself supports SSL via WEBrick when we pass --ssl
# But WEBrick is a bit slow. Still, chef-zero handles it natively.
# Let's generate a self-signed cert first to make sure it doesn't fail.
# chef-zero can generate its own keys if we pass --generate-keys or --ssl

chef-zero -H 0.0.0.0 -p 443 --ssl --generate-keys
