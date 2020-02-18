#!/usr/bin/env python3

from aws_cdk import core

from vpc_cdk_sample.vpc_cdk_sample_stack import VpcCdkSampleStack


app = core.App()
VpcCdkSampleStack(app, "vpc-cdk-sample")

app.synth()
