current_dir = File.dirname(__FILE__)
log_level :info
log_location STDOUT
node_name "admin"
client_key "#{current_dir}/admin.pem"
validation_client_name "devops-validator"
validation_key "#{current_dir}/devops-validator.pem"
chef_server_url "https://127.0.0.1"
cookbook_path ["#{current_dir}/../cookbooks"]
ssl_verify_mode :verify_none
