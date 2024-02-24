import pulumi
from pulumi_azure import network, compute

# Create an Azure Resource Group
resource_group = network.ResourceGroup('my-resource-group')

# Create an Azure Virtual Network
virtual_network = network.VirtualNetwork('my-vnet',
    resource_group_name=resource_group.name,
    address_spaces=['10.0.0.0/16'])

# Create a subnet
subnet = network.Subnet('my-subnet',
    resource_group_name=resource_group.name,
    virtual_network_name=virtual_network.name,
    address_prefixes=['10.0.1.0/24'])

# Create a network interface for the VM
network_interface = network.NetworkInterface('my-nic',
    resource_group_name=resource_group.name,
    ip_configurations=[{
        "name": "webserveripcfg",
        "subnet_id": subnet.id,
        "privateIpAddressAllocation": "Dynamic",
    }])

# Now create the VM
vm = compute.VirtualMachine('my-vm',
    resource_group_name=resource_group.name,
    network_interface_ids=[network_interface.id],
    vm_size='Standard_DS1_v2',
    delete_data_disks_on_termination=True,
    delete_os_disk_on_termination=True,
    os_profile={
        "computer_name": "hostname",
        "admin_username": "testadmin",
        "admin_password": "Password1234!",
    },
    os_profile_linux_config={
        "disable_password_authentication": False,
    },
    storage_os_disk={
        "create_option": "FromImage",
        "name": "myosdisk1",
    },
    storage_image_reference={
        "publisher": "Canonical",
        "offer": "UbuntuServer",
        "sku": "16.04-LTS",
        "version": "latest"
    })

# Export the public IP of the VM
pulumi.export('public_ip', network_interface.private_ip)