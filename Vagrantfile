# -*- mode: ruby -*-
# vi: set ft=ruby :


class Object
  def deep_symbolize_keys
    return self.inject({}){|memo,(k,v)| memo[k.to_sym] = v.deep_symbolize_keys; memo} if self.is_a? Hash
    return self.inject([]){|memo,v    | memo           << v.deep_symbolize_keys; memo} if self.is_a? Array
    return self
  end
end


conf = {
  :box_name => ENV['BOX_NAME'] || "trusty64",
  :box_url => ENV['BOX_URI'] || "http://files.xxxxx.com/trusty64.box",
  :host_port => (ENV['HOST_PORT'] || '8080').to_i,
}


user_conf_file = ENV.fetch('PROJECT_CONF', 'etc/vagrant.yaml')

if File.exist?(user_conf_file)
  require 'yaml'
  user_conf = YAML.load_file(user_conf_file)
  conf.deep_merge!(user_conf.deep_symbolize_keys)
end


# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Box
  config.vm.box = conf[:box_name]
  config.vm.box_url = conf[:box_url]

  if Vagrant.has_plugin?("vagrant-cachier")
    # Configure cached packages to be shared between instances of the same base box.
    # More info on http://fgrehm.viewdocs.io/vagrant-cachier/usage
    config.cache.scope = :box
  end

  # Network
  config.vm.hostname = 'dev.{{ project_name }}.com'.gsub('_', '-')
  config.vm.network :forwarded_port, guest: 80, host: conf[:host_port]

  # Share for django
  config.vm.synced_folder "./", "/home/vagrant/{{ project_name }}"

  ## For masterless, mount your file roots file root
  config.vm.synced_folder "salt/roots/", "/srv/"

  # Custom the box
  config.vm.provider :virtualbox do |vb|
    vb.name = '{{ project_name }}'
    vb.customize ["modifyvm", :id, "--memory", 512]
  end

  ## Set your salt configs here
  config.vm.provision :salt do |salt|
    # Custom pillar from yaml file
    salt.pillar(conf)

    salt.verbose = true
    salt.log_level = 'info'
    salt.colorize = true

    ## Minion config is set to ``file_client: local`` for masterless
    salt.minion_config = "salt/minion"

    ## Installs our formula in "salt/roots/salt"
    salt.run_highstate = true

  end

end
