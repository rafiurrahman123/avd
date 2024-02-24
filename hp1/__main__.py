import pulumi
import pulumi_azure_native as azure_native

# Create an Azure resource group
resource_group = azure_native.resources.ResourceGroup('myResourceGroup')

# Create an Azure Virtual Desktop host pool
host_pool = azure_native.desktopvirtualization.HostPool(
    'myHostPool',
    host_pool_type=azure_native.desktopvirtualization.HostPoolType.PERSONAL,
    load_balancer_type=azure_native.desktopvirtualization.LoadBalancerType.BREADTH_FIRST,
    personal_desktop_assignment_type=azure_native.desktopvirtualization.PersonalDesktopAssignmentType.AUTOMATIC,
    preferred_app_group_type=azure_native.desktopvirtualization.PreferredAppGroupType.DESKTOP,
    resource_group_name=resource_group.name,
)

# Export the host pool's name
pulumi.export('hostPoolName', host_pool.name)