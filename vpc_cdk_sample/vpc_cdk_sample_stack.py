from aws_cdk import (
    aws_s3 as s3,
    aws_ec2 as ec2,
    core
)


class VpcCdkSampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cidr = '10.0.0.0/16'

        vpc = ec2.Vpc(self, "TheVPC",
                      cidr=cidr,
                      max_azs=3,
                      subnet_configuration=[ec2.SubnetConfiguration(
                          subnet_type=ec2.SubnetType.PUBLIC,
                          name="Ingress",
                          cidr_mask=24
                      ), ec2.SubnetConfiguration(
                          cidr_mask=24,
                          name="Application",
                          subnet_type=ec2.SubnetType.PRIVATE
                      ), ec2.SubnetConfiguration(
                          cidr_mask=28,
                          name="Database",
                          subnet_type=ec2.SubnetType.ISOLATED,
                          reserved=True
                      )
                      ]
                      )

        security_group = ec2.SecurityGroup(
            self,
            id='test-security-group',
            vpc=vpc,
            security_group_name='test-security-group'
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(cidr),
            connection=ec2.Port.tcp(22),
        )

        image_id = ec2.AmazonLinuxImage(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2).get_image(self).image_id

        ec2.CfnInstance(
            self,
            id='test-instance',
            availability_zone="ap-northeast-1a",
            image_id=image_id,
            instance_type="t2.micro",
            key_name='test-ssh-key',
            security_group_ids=[security_group.security_group_id],
            subnet_id=vpc.private_subnets[0].subnet_id,
            tags=[{
                "key": "Name",
                "value": "test-instance"
            }]
        )
