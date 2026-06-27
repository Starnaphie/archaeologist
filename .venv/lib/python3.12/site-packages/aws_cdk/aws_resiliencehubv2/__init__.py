r'''
# AWS::ResilienceHubV2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_resiliencehubv2 as resiliencehub
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ResilienceHubV2 construct libraries](https://constructs.dev/search?q=resiliencehubv2)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ResilienceHubV2 resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResilienceHubV2.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ResilienceHubV2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResilienceHubV2.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_9df397a6,
    CfnTag as _CfnTag_f6864754,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    ITaggableV2 as _ITaggableV2_4e6798f8,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)
from ..interfaces.aws_resiliencehubv2 import (
    IPolicyRef as _IPolicyRef_8f29ce94,
    IServiceFunctionRef as _IServiceFunctionRef_176497fa,
    IServiceRef as _IServiceRef_7f44f4e1,
    ISystemRef as _ISystemRef_c37fa082,
    IUserJourneyRef as _IUserJourneyRef_ef12e386,
    PolicyReference as _PolicyReference_9fe32560,
    ServiceFunctionReference as _ServiceFunctionReference_766b969b,
    ServiceReference as _ServiceReference_4463a242,
    SystemReference as _SystemReference_71b63cdd,
    UserJourneyReference as _UserJourneyReference_d8b20a5a,
)


@jsii.implements(_IInspectable_c2943556, _IPolicyRef_8f29ce94, _ITaggableV2_4e6798f8)
class CfnPolicy(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnPolicy",
):
    '''Creates a resilience policy that defines availability and disaster recovery requirements.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html
    :cloudformationResource: AWS::ResilienceHubV2::Policy
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
        
        cfn_policy = resiliencehubv2.CfnPolicy(self, "MyCfnPolicy",
            name="name",
        
            # the properties below are optional
            availability_slo=resiliencehubv2.CfnPolicy.AvailabilitySloProperty(
                target=123
            ),
            data_recovery=resiliencehubv2.CfnPolicy.DataRecoveryTargetsProperty(
                time_between_backups_in_minutes=123
            ),
            description="description",
            kms_key_id="kmsKeyId",
            multi_az=resiliencehubv2.CfnPolicy.MultiAzTargetsProperty(
                disaster_recovery_approach="disasterRecoveryApproach",
                rpo_in_minutes=123,
                rto_in_minutes=123
            ),
            multi_region=resiliencehubv2.CfnPolicy.MultiRegionTargetsProperty(
                disaster_recovery_approach="disasterRecoveryApproach",
                rpo_in_minutes=123,
                rto_in_minutes=123
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        availability_slo: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.AvailabilitySloProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_recovery: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.DataRecoveryTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.MultiAzTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        multi_region: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.MultiRegionTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHubV2::Policy``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the policy.
        :param availability_slo: 
        :param data_recovery: 
        :param description: The description of the policy.
        :param kms_key_id: The KMS key ID for encrypting policy data.
        :param multi_az: 
        :param multi_region: 
        :param tags: Tags assigned to the policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e629fc4862e28e629f2d24cf4a00a9ca948681ba5b90659c1dcc6199c320f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPolicyProps(
            name=name,
            availability_slo=availability_slo,
            data_recovery=data_recovery,
            description=description,
            kms_key_id=kms_key_id,
            multi_az=multi_az,
            multi_region=multi_region,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForPolicy")
    @builtins.classmethod
    def arn_for_policy(cls, resource: "_IPolicyRef_8f29ce94") -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657ec34d9724a44984551b0d29a82d110c168db65580307fce1a2d5a4e955b62)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForPolicy", [resource]))

    @jsii.member(jsii_name="isCfnPolicy")
    @builtins.classmethod
    def is_cfn_policy(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnPolicy.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88419ea3bbf7ed00758b7eff5c807b3279da0bd13ec41e95b91b3dc4905c91b8)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnPolicy", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9281463bbddd5e6a5abcb1b418805af64867041de7188c8fcef204bbd56fba)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7931aad811d55f1c1d321f7f330caa12a52b96ab6cff5615e40053a2563812ee)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociatedServiceCount")
    def attr_associated_service_count(self) -> jsii.Number:
        '''The number of services associated with this policy.

        :cloudformationAttribute: AssociatedServiceCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAssociatedServiceCount"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the policy was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrPolicyArn")
    def attr_policy_arn(self) -> builtins.str:
        '''The ARN of the policy.

        :cloudformationAttribute: PolicyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the policy was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_TagManager_0a598cb3":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_TagManager_0a598cb3", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="policyRef")
    def policy_ref(self) -> "_PolicyReference_9fe32560":
        '''A reference to a Policy resource.'''
        return typing.cast("_PolicyReference_9fe32560", jsii.get(self, "policyRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the policy.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d259843c26b15a16dcbabd1e0e75fcbc09629b91a287d87104d92a18f19d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilitySlo")
    def availability_slo(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.AvailabilitySloProperty"]]:
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.AvailabilitySloProperty"]], jsii.get(self, "availabilitySlo"))

    @availability_slo.setter
    def availability_slo(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.AvailabilitySloProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a32bbfeaa8d459ff6083f2740f10c9ad8aca7eca836b39dc5f96859e83118f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilitySlo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataRecovery")
    def data_recovery(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.DataRecoveryTargetsProperty"]]:
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.DataRecoveryTargetsProperty"]], jsii.get(self, "dataRecovery"))

    @data_recovery.setter
    def data_recovery(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.DataRecoveryTargetsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876c6cdf83b364b06e9611ae74176173ca5e80eb30145b85d0a5866ba6f8bc5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRecovery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the policy.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3d4da539650d8938a395790f0d988b7ead316557ac6ead656ec0f538759099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key ID for encrypting policy data.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4b0d8affbccb5e5c84f1894869b877f9d0d3ed0d024461283c9760be1c47ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiAz")
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiAzTargetsProperty"]]:
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiAzTargetsProperty"]], jsii.get(self, "multiAz"))

    @multi_az.setter
    def multi_az(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiAzTargetsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8c8e4e3a2ca89f1c4516be1382bfe9a786ae265c976fe75df7b71606d23ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiAz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiRegion")
    def multi_region(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiRegionTargetsProperty"]]:
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiRegionTargetsProperty"]], jsii.get(self, "multiRegion"))

    @multi_region.setter
    def multi_region(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiRegionTargetsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b113d1c1a16d9a88d7758c26ad9a6eac43b4a8995ad9a6dfcb5c065a458e2aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the policy.'''
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["_CfnTag_f6864754"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a07e642dc63b7980c82a54120ed7d01ba6c8a726bdfc0589953ca23747bd214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnPolicy.AvailabilitySloProperty",
        jsii_struct_bases=[],
        name_mapping={"target": "target"},
    )
    class AvailabilitySloProperty:
        def __init__(self, *, target: typing.Optional[jsii.Number] = None) -> None:
            '''
            :param target: Availability target percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-availabilityslo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                availability_slo_property = resiliencehubv2.CfnPolicy.AvailabilitySloProperty(
                    target=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5fe061cf9d7a9f04783a913205c5eedecdc2480c89ff0f7834ff1a76b924fe0)
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def target(self) -> typing.Optional[jsii.Number]:
            '''Availability target percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-availabilityslo.html#cfn-resiliencehubv2-policy-availabilityslo-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AvailabilitySloProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnPolicy.DataRecoveryTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "time_between_backups_in_minutes": "timeBetweenBackupsInMinutes",
        },
    )
    class DataRecoveryTargetsProperty:
        def __init__(
            self,
            *,
            time_between_backups_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param time_between_backups_in_minutes: Time between backups in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-datarecoverytargets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                data_recovery_targets_property = resiliencehubv2.CfnPolicy.DataRecoveryTargetsProperty(
                    time_between_backups_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c006605f95c69f124beaad55ccd214823579d133c3345c18bfdbf66c77a8c6ac)
                check_type(argname="argument time_between_backups_in_minutes", value=time_between_backups_in_minutes, expected_type=type_hints["time_between_backups_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if time_between_backups_in_minutes is not None:
                self._values["time_between_backups_in_minutes"] = time_between_backups_in_minutes

        @builtins.property
        def time_between_backups_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''Time between backups in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-datarecoverytargets.html#cfn-resiliencehubv2-policy-datarecoverytargets-timebetweenbackupsinminutes
            '''
            result = self._values.get("time_between_backups_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataRecoveryTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnPolicy.MultiAzTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disaster_recovery_approach": "disasterRecoveryApproach",
            "rpo_in_minutes": "rpoInMinutes",
            "rto_in_minutes": "rtoInMinutes",
        },
    )
    class MultiAzTargetsProperty:
        def __init__(
            self,
            *,
            disaster_recovery_approach: typing.Optional[builtins.str] = None,
            rpo_in_minutes: typing.Optional[jsii.Number] = None,
            rto_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param disaster_recovery_approach: Multi-AZ disaster recovery approach.
            :param rpo_in_minutes: Recovery Point Objective in minutes.
            :param rto_in_minutes: Recovery Time Objective in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiaztargets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                multi_az_targets_property = resiliencehubv2.CfnPolicy.MultiAzTargetsProperty(
                    disaster_recovery_approach="disasterRecoveryApproach",
                    rpo_in_minutes=123,
                    rto_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dbe8843e5c0186207e785f6083fd070a090ff07a1de0f04ec95bb25b94450b0)
                check_type(argname="argument disaster_recovery_approach", value=disaster_recovery_approach, expected_type=type_hints["disaster_recovery_approach"])
                check_type(argname="argument rpo_in_minutes", value=rpo_in_minutes, expected_type=type_hints["rpo_in_minutes"])
                check_type(argname="argument rto_in_minutes", value=rto_in_minutes, expected_type=type_hints["rto_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disaster_recovery_approach is not None:
                self._values["disaster_recovery_approach"] = disaster_recovery_approach
            if rpo_in_minutes is not None:
                self._values["rpo_in_minutes"] = rpo_in_minutes
            if rto_in_minutes is not None:
                self._values["rto_in_minutes"] = rto_in_minutes

        @builtins.property
        def disaster_recovery_approach(self) -> typing.Optional[builtins.str]:
            '''Multi-AZ disaster recovery approach.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiaztargets.html#cfn-resiliencehubv2-policy-multiaztargets-disasterrecoveryapproach
            '''
            result = self._values.get("disaster_recovery_approach")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rpo_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''Recovery Point Objective in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiaztargets.html#cfn-resiliencehubv2-policy-multiaztargets-rpoinminutes
            '''
            result = self._values.get("rpo_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rto_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''Recovery Time Objective in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiaztargets.html#cfn-resiliencehubv2-policy-multiaztargets-rtoinminutes
            '''
            result = self._values.get("rto_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiAzTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnPolicy.MultiRegionTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disaster_recovery_approach": "disasterRecoveryApproach",
            "rpo_in_minutes": "rpoInMinutes",
            "rto_in_minutes": "rtoInMinutes",
        },
    )
    class MultiRegionTargetsProperty:
        def __init__(
            self,
            *,
            disaster_recovery_approach: typing.Optional[builtins.str] = None,
            rpo_in_minutes: typing.Optional[jsii.Number] = None,
            rto_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param disaster_recovery_approach: Multi-Region disaster recovery approach.
            :param rpo_in_minutes: Recovery Point Objective in minutes.
            :param rto_in_minutes: Recovery Time Objective in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiregiontargets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                multi_region_targets_property = resiliencehubv2.CfnPolicy.MultiRegionTargetsProperty(
                    disaster_recovery_approach="disasterRecoveryApproach",
                    rpo_in_minutes=123,
                    rto_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__487bb7bdb57d0212483b7ec1cee0412ed082324b11618e02e4ba649b339669aa)
                check_type(argname="argument disaster_recovery_approach", value=disaster_recovery_approach, expected_type=type_hints["disaster_recovery_approach"])
                check_type(argname="argument rpo_in_minutes", value=rpo_in_minutes, expected_type=type_hints["rpo_in_minutes"])
                check_type(argname="argument rto_in_minutes", value=rto_in_minutes, expected_type=type_hints["rto_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disaster_recovery_approach is not None:
                self._values["disaster_recovery_approach"] = disaster_recovery_approach
            if rpo_in_minutes is not None:
                self._values["rpo_in_minutes"] = rpo_in_minutes
            if rto_in_minutes is not None:
                self._values["rto_in_minutes"] = rto_in_minutes

        @builtins.property
        def disaster_recovery_approach(self) -> typing.Optional[builtins.str]:
            '''Multi-Region disaster recovery approach.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiregiontargets.html#cfn-resiliencehubv2-policy-multiregiontargets-disasterrecoveryapproach
            '''
            result = self._values.get("disaster_recovery_approach")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rpo_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''Recovery Point Objective in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiregiontargets.html#cfn-resiliencehubv2-policy-multiregiontargets-rpoinminutes
            '''
            result = self._values.get("rpo_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rto_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''Recovery Time Objective in minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-policy-multiregiontargets.html#cfn-resiliencehubv2-policy-multiregiontargets-rtoinminutes
            '''
            result = self._values.get("rto_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiRegionTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "availability_slo": "availabilitySlo",
        "data_recovery": "dataRecovery",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "multi_az": "multiAz",
        "multi_region": "multiRegion",
        "tags": "tags",
    },
)
class CfnPolicyProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        availability_slo: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.AvailabilitySloProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_recovery: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.DataRecoveryTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.MultiAzTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        multi_region: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnPolicy.MultiRegionTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPolicy``.

        :param name: The name of the policy.
        :param availability_slo: 
        :param data_recovery: 
        :param description: The description of the policy.
        :param kms_key_id: The KMS key ID for encrypting policy data.
        :param multi_az: 
        :param multi_region: 
        :param tags: Tags assigned to the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
            
            cfn_policy_props = resiliencehubv2.CfnPolicyProps(
                name="name",
            
                # the properties below are optional
                availability_slo=resiliencehubv2.CfnPolicy.AvailabilitySloProperty(
                    target=123
                ),
                data_recovery=resiliencehubv2.CfnPolicy.DataRecoveryTargetsProperty(
                    time_between_backups_in_minutes=123
                ),
                description="description",
                kms_key_id="kmsKeyId",
                multi_az=resiliencehubv2.CfnPolicy.MultiAzTargetsProperty(
                    disaster_recovery_approach="disasterRecoveryApproach",
                    rpo_in_minutes=123,
                    rto_in_minutes=123
                ),
                multi_region=resiliencehubv2.CfnPolicy.MultiRegionTargetsProperty(
                    disaster_recovery_approach="disasterRecoveryApproach",
                    rpo_in_minutes=123,
                    rto_in_minutes=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c906443be9003dedeed32d06ee8a6f0d9a43e95506b85846be31638078cafe)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument availability_slo", value=availability_slo, expected_type=type_hints["availability_slo"])
            check_type(argname="argument data_recovery", value=data_recovery, expected_type=type_hints["data_recovery"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument multi_region", value=multi_region, expected_type=type_hints["multi_region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if availability_slo is not None:
            self._values["availability_slo"] = availability_slo
        if data_recovery is not None:
            self._values["data_recovery"] = data_recovery
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if multi_region is not None:
            self._values["multi_region"] = multi_region
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_slo(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.AvailabilitySloProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-availabilityslo
        '''
        result = self._values.get("availability_slo")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.AvailabilitySloProperty"]], result)

    @builtins.property
    def data_recovery(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.DataRecoveryTargetsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-datarecovery
        '''
        result = self._values.get("data_recovery")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.DataRecoveryTargetsProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key ID for encrypting policy data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiAzTargetsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-multiaz
        '''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiAzTargetsProperty"]], result)

    @builtins.property
    def multi_region(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiRegionTargetsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-multiregion
        '''
        result = self._values.get("multi_region")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnPolicy.MultiRegionTargetsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-policy.html#cfn-resiliencehubv2-policy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556, _IServiceRef_7f44f4e1, _ITaggableV2_4e6798f8)
class CfnService(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService",
):
    '''Creates a resilience-managed service with associated systems, input sources, assertions, and service functions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html
    :cloudformationResource: AWS::ResilienceHubV2::Service
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
        
        cfn_service = resiliencehubv2.CfnService(self, "MyCfnService",
            name="name",
            regions=["regions"],
        
            # the properties below are optional
            assertions=[resiliencehubv2.CfnService.AssertionDefinitionProperty(
                text="text"
            )],
            associated_systems=[resiliencehubv2.CfnService.AssociatedSystemProperty(
                system_arn="systemArn",
        
                # the properties below are optional
                user_journey_ids=["userJourneyIds"]
            )],
            dependency_discovery="dependencyDiscovery",
            description="description",
            input_sources=[resiliencehubv2.CfnService.InputSourceDefinitionProperty(
                resource_configuration=resiliencehubv2.CfnService.ResourceConfigurationProperty(
                    cfn_stack_arn="cfnStackArn",
                    design_file_s3_url="designFileS3Url",
                    eks=resiliencehubv2.CfnService.EksSourceProperty(
                        cluster_arn="clusterArn",
                        namespaces=["namespaces"]
                    ),
                    resource_tags=[resiliencehubv2.CfnService.ResourceTagProperty(
                        key="key",
                        values=["values"]
                    )],
                    tf_state_file_url="tfStateFileUrl"
                )
            )],
            kms_key_id="kmsKeyId",
            permission_model=resiliencehubv2.CfnService.PermissionModelProperty(
                invoker_role_name="invokerRoleName",
        
                # the properties below are optional
                cross_account_role_arns=[resiliencehubv2.CfnService.CrossAccountRoleConfigurationProperty(
                    cross_account_role_arn="crossAccountRoleArn",
        
                    # the properties below are optional
                    external_id="externalId"
                )]
            ),
            policy_arn="policyArn",
            report_configuration=resiliencehubv2.CfnService.ServiceReportConfigurationProperty(
                report_output=[resiliencehubv2.CfnService.ReportOutputConfigurationProperty(
                    s3=resiliencehubv2.CfnService.S3ReportOutputConfigurationProperty(
                        bucket_owner="bucketOwner",
                        bucket_path="bucketPath"
                    )
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        regions: typing.Sequence[builtins.str],
        assertions: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.AssertionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        associated_systems: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.AssociatedSystemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        dependency_discovery: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        input_sources: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.InputSourceDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        permission_model: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.PermissionModelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_arn: typing.Optional[builtins.str] = None,
        report_configuration: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.ServiceReportConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHubV2::Service``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the service.
        :param regions: AWS regions for the service.
        :param assertions: Assertions associated with this service.
        :param associated_systems: Systems associated with this service.
        :param dependency_discovery: Dependency discovery state.
        :param description: The description of the service.
        :param input_sources: Input sources for this service.
        :param kms_key_id: The KMS key ID for encrypting service data.
        :param permission_model: 
        :param policy_arn: The ARN of the resilience policy to associate.
        :param report_configuration: Configuration for automatic report generation on a Service.
        :param tags: Tags assigned to the service.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6bdd32c65d4a9df22e965e380026f55b7e059ad2c4bb5b54867d27eceaea1e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceProps(
            name=name,
            regions=regions,
            assertions=assertions,
            associated_systems=associated_systems,
            dependency_discovery=dependency_discovery,
            description=description,
            input_sources=input_sources,
            kms_key_id=kms_key_id,
            permission_model=permission_model,
            policy_arn=policy_arn,
            report_configuration=report_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForService")
    @builtins.classmethod
    def arn_for_service(cls, resource: "_IServiceRef_7f44f4e1") -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4163076509fc819924f2189e2949bb93d4130966e24f7f0934cac260900582a)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForService", [resource]))

    @jsii.member(jsii_name="isCfnService")
    @builtins.classmethod
    def is_cfn_service(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnService.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec24122752db76055fe3823408f2737c9bdbd12aa457cdc9b0ce9fcde22579e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnService", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d3b1d949c49ce026994d9d4b0b0a1aeea5e5b94b475df0cbfd6d1f83fbce47)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a8bed735bc8fdf33d315032cfb56f7ad6fca0cd599641c370a480c562a9584)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the service was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEffectivePolicyValues")
    def attr_effective_policy_values(self) -> "_IResolvable_da3f097b":
        '''Effective policy values computed from the associated policy.

        :cloudformationAttribute: EffectivePolicyValues
        '''
        return typing.cast("_IResolvable_da3f097b", jsii.get(self, "attrEffectivePolicyValues"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceArn")
    def attr_service_arn(self) -> builtins.str:
        '''The ARN of the service.

        :cloudformationAttribute: ServiceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the service was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_TagManager_0a598cb3":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_TagManager_0a598cb3", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="serviceRef")
    def service_ref(self) -> "_ServiceReference_4463a242":
        '''A reference to a Service resource.'''
        return typing.cast("_ServiceReference_4463a242", jsii.get(self, "serviceRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the service.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40654003c72cad607c2285fc9007b24841372f07282d2e1e0074d9e53de8da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.List[builtins.str]:
        '''AWS regions for the service.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regions"))

    @regions.setter
    def regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964bfce08922c4fb735abcd9089af81bd138fd8a4ffbb49d7c1e1d6f1549576e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="assertions")
    def assertions(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssertionDefinitionProperty"]]]]:
        '''Assertions associated with this service.'''
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssertionDefinitionProperty"]]]], jsii.get(self, "assertions"))

    @assertions.setter
    def assertions(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssertionDefinitionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25bd9cec3047a0d0d7fe892cfb844e2cadbd370c4f6e00d03ec6668c3ae0bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assertions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="associatedSystems")
    def associated_systems(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssociatedSystemProperty"]]]]:
        '''Systems associated with this service.'''
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssociatedSystemProperty"]]]], jsii.get(self, "associatedSystems"))

    @associated_systems.setter
    def associated_systems(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssociatedSystemProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebf53f05f27c31f326af1fc62ded64873bc1a58da7e10b94706eae63e148fb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedSystems", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependencyDiscovery")
    def dependency_discovery(self) -> typing.Optional[builtins.str]:
        '''Dependency discovery state.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dependencyDiscovery"))

    @dependency_discovery.setter
    def dependency_discovery(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b9e7e595d6c6af07c6a42ca51a94cbaf992a9a6f55a97552f6367b986ebe2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencyDiscovery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0243afd562c00bc61ef677f20cecc4ac5705343dc87da0758a23a18fcdc47115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputSources")
    def input_sources(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.InputSourceDefinitionProperty"]]]]:
        '''Input sources for this service.'''
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.InputSourceDefinitionProperty"]]]], jsii.get(self, "inputSources"))

    @input_sources.setter
    def input_sources(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.InputSourceDefinitionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb607cafec82377097ae094d11f8506899ea08c36738456c1134887ead12e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key ID for encrypting service data.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242b39ff6b3b9a87071efd4aa5b82fb4561d7e0da10e88151ba434b99256230c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissionModel")
    def permission_model(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.PermissionModelProperty"]]:
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.PermissionModelProperty"]], jsii.get(self, "permissionModel"))

    @permission_model.setter
    def permission_model(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.PermissionModelProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f96997f389a164a9d59977b08fc63042a4bebad060235b2ad58734c1161867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyArn")
    def policy_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resilience policy to associate.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyArn"))

    @policy_arn.setter
    def policy_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2f304aa99feed1c072f06bf949b63b65fde2503fd90aaa86c7b1286b57e06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reportConfiguration")
    def report_configuration(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.ServiceReportConfigurationProperty"]]:
        '''Configuration for automatic report generation on a Service.'''
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.ServiceReportConfigurationProperty"]], jsii.get(self, "reportConfiguration"))

    @report_configuration.setter
    def report_configuration(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.ServiceReportConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4a4c62b7f037a37893fa13b7f13b0f1fabc51715e30be18ead891af7876e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reportConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the service.'''
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["_CfnTag_f6864754"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a377d29fac1c509599600752f1645f130ab40efe1400fd62790e225e015fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.AssertionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text"},
    )
    class AssertionDefinitionProperty:
        def __init__(self, *, text: builtins.str) -> None:
            '''An assertion about the service's resilience posture.

            :param text: The text of the assertion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-assertiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                assertion_definition_property = resiliencehubv2.CfnService.AssertionDefinitionProperty(
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d41432ca73fa194f691a78a5d7f3574e1e12d47aa621221155170fe576d5eea7)
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "text": text,
            }

        @builtins.property
        def text(self) -> builtins.str:
            '''The text of the assertion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-assertiondefinition.html#cfn-resiliencehubv2-service-assertiondefinition-text
            '''
            result = self._values.get("text")
            assert result is not None, "Required property 'text' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssertionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.AssociatedSystemProperty",
        jsii_struct_bases=[],
        name_mapping={"system_arn": "systemArn", "user_journey_ids": "userJourneyIds"},
    )
    class AssociatedSystemProperty:
        def __init__(
            self,
            *,
            system_arn: builtins.str,
            user_journey_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param system_arn: The system ARN.
            :param user_journey_ids: User journey IDs associated with this system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-associatedsystem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                associated_system_property = resiliencehubv2.CfnService.AssociatedSystemProperty(
                    system_arn="systemArn",
                
                    # the properties below are optional
                    user_journey_ids=["userJourneyIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__305b50b88f93c47a6df92c9050e81f812cf5cca69c6dfe6188aa63443c4a9012)
                check_type(argname="argument system_arn", value=system_arn, expected_type=type_hints["system_arn"])
                check_type(argname="argument user_journey_ids", value=user_journey_ids, expected_type=type_hints["user_journey_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "system_arn": system_arn,
            }
            if user_journey_ids is not None:
                self._values["user_journey_ids"] = user_journey_ids

        @builtins.property
        def system_arn(self) -> builtins.str:
            '''The system ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-associatedsystem.html#cfn-resiliencehubv2-service-associatedsystem-systemarn
            '''
            result = self._values.get("system_arn")
            assert result is not None, "Required property 'system_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_journey_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''User journey IDs associated with this system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-associatedsystem.html#cfn-resiliencehubv2-service-associatedsystem-userjourneyids
            '''
            result = self._values.get("user_journey_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociatedSystemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.CrossAccountRoleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cross_account_role_arn": "crossAccountRoleArn",
            "external_id": "externalId",
        },
    )
    class CrossAccountRoleConfigurationProperty:
        def __init__(
            self,
            *,
            cross_account_role_arn: builtins.str,
            external_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param cross_account_role_arn: ARN of the cross-account IAM role.
            :param external_id: External ID for cross-account access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-crossaccountroleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                cross_account_role_configuration_property = resiliencehubv2.CfnService.CrossAccountRoleConfigurationProperty(
                    cross_account_role_arn="crossAccountRoleArn",
                
                    # the properties below are optional
                    external_id="externalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ebe7293c74e1e49a5c894dc42cf632e3b58feccb2d4f9d9c5b6d9f1e2e089fa)
                check_type(argname="argument cross_account_role_arn", value=cross_account_role_arn, expected_type=type_hints["cross_account_role_arn"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cross_account_role_arn": cross_account_role_arn,
            }
            if external_id is not None:
                self._values["external_id"] = external_id

        @builtins.property
        def cross_account_role_arn(self) -> builtins.str:
            '''ARN of the cross-account IAM role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-crossaccountroleconfiguration.html#cfn-resiliencehubv2-service-crossaccountroleconfiguration-crossaccountrolearn
            '''
            result = self._values.get("cross_account_role_arn")
            assert result is not None, "Required property 'cross_account_role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''External ID for cross-account access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-crossaccountroleconfiguration.html#cfn-resiliencehubv2-service-crossaccountroleconfiguration-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossAccountRoleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.DisasterRecoverySourceProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_name": "policyName", "value": "value"},
    )
    class DisasterRecoverySourceProperty:
        def __init__(
            self,
            *,
            policy_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param policy_name: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-disasterrecoverysource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                disaster_recovery_source_property = resiliencehubv2.CfnService.DisasterRecoverySourceProperty(
                    policy_name="policyName",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27a8e661884ddb84edcb38679f978478b1d10209ff839e0e585f535402bf3884)
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_name is not None:
                self._values["policy_name"] = policy_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-disasterrecoverysource.html#cfn-resiliencehubv2-service-disasterrecoverysource-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-disasterrecoverysource.html#cfn-resiliencehubv2-service-disasterrecoverysource-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DisasterRecoverySourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.EffectivePolicyValuesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_slo": "availabilitySlo",
            "multi_az_dr_approach": "multiAzDrApproach",
            "multi_az_rpo": "multiAzRpo",
            "multi_az_rto": "multiAzRto",
            "multi_region_dr_approach": "multiRegionDrApproach",
            "multi_region_rpo": "multiRegionRpo",
            "multi_region_rto": "multiRegionRto",
        },
    )
    class EffectivePolicyValuesProperty:
        def __init__(
            self,
            *,
            availability_slo: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.SloSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            multi_az_dr_approach: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.DisasterRecoverySourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            multi_az_rpo: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.TargetSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            multi_az_rto: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.TargetSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            multi_region_dr_approach: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.DisasterRecoverySourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            multi_region_rpo: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.TargetSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            multi_region_rto: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.TargetSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Effective policy values computed from the associated policy.

            :param availability_slo: 
            :param multi_az_dr_approach: 
            :param multi_az_rpo: 
            :param multi_az_rto: 
            :param multi_region_dr_approach: 
            :param multi_region_rpo: 
            :param multi_region_rto: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                effective_policy_values_property = resiliencehubv2.CfnService.EffectivePolicyValuesProperty(
                    availability_slo=resiliencehubv2.CfnService.SloSourceProperty(
                        policy_name="policyName",
                        value=123
                    ),
                    multi_az_dr_approach=resiliencehubv2.CfnService.DisasterRecoverySourceProperty(
                        policy_name="policyName",
                        value="value"
                    ),
                    multi_az_rpo=resiliencehubv2.CfnService.TargetSourceProperty(
                        policy_name="policyName",
                        value=123
                    ),
                    multi_az_rto=resiliencehubv2.CfnService.TargetSourceProperty(
                        policy_name="policyName",
                        value=123
                    ),
                    multi_region_dr_approach=resiliencehubv2.CfnService.DisasterRecoverySourceProperty(
                        policy_name="policyName",
                        value="value"
                    ),
                    multi_region_rpo=resiliencehubv2.CfnService.TargetSourceProperty(
                        policy_name="policyName",
                        value=123
                    ),
                    multi_region_rto=resiliencehubv2.CfnService.TargetSourceProperty(
                        policy_name="policyName",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af3bf83c642b175e56cedcc2597cb09cfc5891dedf9b6e0c22b4876f003d65e9)
                check_type(argname="argument availability_slo", value=availability_slo, expected_type=type_hints["availability_slo"])
                check_type(argname="argument multi_az_dr_approach", value=multi_az_dr_approach, expected_type=type_hints["multi_az_dr_approach"])
                check_type(argname="argument multi_az_rpo", value=multi_az_rpo, expected_type=type_hints["multi_az_rpo"])
                check_type(argname="argument multi_az_rto", value=multi_az_rto, expected_type=type_hints["multi_az_rto"])
                check_type(argname="argument multi_region_dr_approach", value=multi_region_dr_approach, expected_type=type_hints["multi_region_dr_approach"])
                check_type(argname="argument multi_region_rpo", value=multi_region_rpo, expected_type=type_hints["multi_region_rpo"])
                check_type(argname="argument multi_region_rto", value=multi_region_rto, expected_type=type_hints["multi_region_rto"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_slo is not None:
                self._values["availability_slo"] = availability_slo
            if multi_az_dr_approach is not None:
                self._values["multi_az_dr_approach"] = multi_az_dr_approach
            if multi_az_rpo is not None:
                self._values["multi_az_rpo"] = multi_az_rpo
            if multi_az_rto is not None:
                self._values["multi_az_rto"] = multi_az_rto
            if multi_region_dr_approach is not None:
                self._values["multi_region_dr_approach"] = multi_region_dr_approach
            if multi_region_rpo is not None:
                self._values["multi_region_rpo"] = multi_region_rpo
            if multi_region_rto is not None:
                self._values["multi_region_rto"] = multi_region_rto

        @builtins.property
        def availability_slo(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.SloSourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-availabilityslo
            '''
            result = self._values.get("availability_slo")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.SloSourceProperty"]], result)

        @builtins.property
        def multi_az_dr_approach(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.DisasterRecoverySourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-multiazdrapproach
            '''
            result = self._values.get("multi_az_dr_approach")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.DisasterRecoverySourceProperty"]], result)

        @builtins.property
        def multi_az_rpo(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-multiazrpo
            '''
            result = self._values.get("multi_az_rpo")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]], result)

        @builtins.property
        def multi_az_rto(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-multiazrto
            '''
            result = self._values.get("multi_az_rto")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]], result)

        @builtins.property
        def multi_region_dr_approach(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.DisasterRecoverySourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-multiregiondrapproach
            '''
            result = self._values.get("multi_region_dr_approach")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.DisasterRecoverySourceProperty"]], result)

        @builtins.property
        def multi_region_rpo(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-multiregionrpo
            '''
            result = self._values.get("multi_region_rpo")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]], result)

        @builtins.property
        def multi_region_rto(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-effectivepolicyvalues.html#cfn-resiliencehubv2-service-effectivepolicyvalues-multiregionrto
            '''
            result = self._values.get("multi_region_rto")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.TargetSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EffectivePolicyValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.EksSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_arn": "clusterArn", "namespaces": "namespaces"},
    )
    class EksSourceProperty:
        def __init__(
            self,
            *,
            cluster_arn: builtins.str,
            namespaces: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param cluster_arn: ARN of the EKS cluster.
            :param namespaces: EKS namespaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-ekssource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                eks_source_property = resiliencehubv2.CfnService.EksSourceProperty(
                    cluster_arn="clusterArn",
                    namespaces=["namespaces"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8222153171bacb58425e667eddaf39b74006a9c713bec1af7ab5451917df746)
                check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
                check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cluster_arn": cluster_arn,
                "namespaces": namespaces,
            }

        @builtins.property
        def cluster_arn(self) -> builtins.str:
            '''ARN of the EKS cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-ekssource.html#cfn-resiliencehubv2-service-ekssource-clusterarn
            '''
            result = self._values.get("cluster_arn")
            assert result is not None, "Required property 'cluster_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def namespaces(self) -> typing.List[builtins.str]:
            '''EKS namespaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-ekssource.html#cfn-resiliencehubv2-service-ekssource-namespaces
            '''
            result = self._values.get("namespaces")
            assert result is not None, "Required property 'namespaces' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.InputSourceDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_configuration": "resourceConfiguration"},
    )
    class InputSourceDefinitionProperty:
        def __init__(
            self,
            *,
            resource_configuration: typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.ResourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''An input source for the service.

            :param resource_configuration: Resource configuration for an input source. Provide exactly one field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-inputsourcedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                input_source_definition_property = resiliencehubv2.CfnService.InputSourceDefinitionProperty(
                    resource_configuration=resiliencehubv2.CfnService.ResourceConfigurationProperty(
                        cfn_stack_arn="cfnStackArn",
                        design_file_s3_url="designFileS3Url",
                        eks=resiliencehubv2.CfnService.EksSourceProperty(
                            cluster_arn="clusterArn",
                            namespaces=["namespaces"]
                        ),
                        resource_tags=[resiliencehubv2.CfnService.ResourceTagProperty(
                            key="key",
                            values=["values"]
                        )],
                        tf_state_file_url="tfStateFileUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3b96172a11348626b3d426531adada00b779bda9de5fd5a2438e5760b0b948a)
                check_type(argname="argument resource_configuration", value=resource_configuration, expected_type=type_hints["resource_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_configuration": resource_configuration,
            }

        @builtins.property
        def resource_configuration(
            self,
        ) -> typing.Union["_IResolvable_da3f097b", "CfnService.ResourceConfigurationProperty"]:
            '''Resource configuration for an input source.

            Provide exactly one field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-inputsourcedefinition.html#cfn-resiliencehubv2-service-inputsourcedefinition-resourceconfiguration
            '''
            result = self._values.get("resource_configuration")
            assert result is not None, "Required property 'resource_configuration' is missing"
            return typing.cast(typing.Union["_IResolvable_da3f097b", "CfnService.ResourceConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSourceDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.PermissionModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invoker_role_name": "invokerRoleName",
            "cross_account_role_arns": "crossAccountRoleArns",
        },
    )
    class PermissionModelProperty:
        def __init__(
            self,
            *,
            invoker_role_name: builtins.str,
            cross_account_role_arns: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.CrossAccountRoleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param invoker_role_name: Name of the invoker IAM role.
            :param cross_account_role_arns: Cross-account role ARNs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-permissionmodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                permission_model_property = resiliencehubv2.CfnService.PermissionModelProperty(
                    invoker_role_name="invokerRoleName",
                
                    # the properties below are optional
                    cross_account_role_arns=[resiliencehubv2.CfnService.CrossAccountRoleConfigurationProperty(
                        cross_account_role_arn="crossAccountRoleArn",
                
                        # the properties below are optional
                        external_id="externalId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfe67ffbdc763fe6cc5eb3fd567392d6db437b5325ab8eada2e5ed14f605722d)
                check_type(argname="argument invoker_role_name", value=invoker_role_name, expected_type=type_hints["invoker_role_name"])
                check_type(argname="argument cross_account_role_arns", value=cross_account_role_arns, expected_type=type_hints["cross_account_role_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "invoker_role_name": invoker_role_name,
            }
            if cross_account_role_arns is not None:
                self._values["cross_account_role_arns"] = cross_account_role_arns

        @builtins.property
        def invoker_role_name(self) -> builtins.str:
            '''Name of the invoker IAM role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-permissionmodel.html#cfn-resiliencehubv2-service-permissionmodel-invokerrolename
            '''
            result = self._values.get("invoker_role_name")
            assert result is not None, "Required property 'invoker_role_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def cross_account_role_arns(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.CrossAccountRoleConfigurationProperty"]]]]:
            '''Cross-account role ARNs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-permissionmodel.html#cfn-resiliencehubv2-service-permissionmodel-crossaccountrolearns
            '''
            result = self._values.get("cross_account_role_arns")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.CrossAccountRoleConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PermissionModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.ReportOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class ReportOutputConfigurationProperty:
        def __init__(
            self,
            *,
            s3: typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.S3ReportOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Configuration for a report output destination.

            :param s3: S3 configuration for report output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-reportoutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                report_output_configuration_property = resiliencehubv2.CfnService.ReportOutputConfigurationProperty(
                    s3=resiliencehubv2.CfnService.S3ReportOutputConfigurationProperty(
                        bucket_owner="bucketOwner",
                        bucket_path="bucketPath"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e98098f1c2bd297b3d7e01e55079dd85f796e88178aeeb1b60467b04c1bdb28)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3": s3,
            }

        @builtins.property
        def s3(
            self,
        ) -> typing.Union["_IResolvable_da3f097b", "CfnService.S3ReportOutputConfigurationProperty"]:
            '''S3 configuration for report output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-reportoutputconfiguration.html#cfn-resiliencehubv2-service-reportoutputconfiguration-s3
            '''
            result = self._values.get("s3")
            assert result is not None, "Required property 's3' is missing"
            return typing.cast(typing.Union["_IResolvable_da3f097b", "CfnService.S3ReportOutputConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReportOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.ResourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cfn_stack_arn": "cfnStackArn",
            "design_file_s3_url": "designFileS3Url",
            "eks": "eks",
            "resource_tags": "resourceTags",
            "tf_state_file_url": "tfStateFileUrl",
        },
    )
    class ResourceConfigurationProperty:
        def __init__(
            self,
            *,
            cfn_stack_arn: typing.Optional[builtins.str] = None,
            design_file_s3_url: typing.Optional[builtins.str] = None,
            eks: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.EksSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_tags: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tf_state_file_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Resource configuration for an input source.

            Provide exactly one field.

            :param cfn_stack_arn: ARN of a CloudFormation stack.
            :param design_file_s3_url: S3 URL of a design file.
            :param eks: 
            :param resource_tags: Resource tags to discover resources.
            :param tf_state_file_url: URL of a Terraform state file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                resource_configuration_property = resiliencehubv2.CfnService.ResourceConfigurationProperty(
                    cfn_stack_arn="cfnStackArn",
                    design_file_s3_url="designFileS3Url",
                    eks=resiliencehubv2.CfnService.EksSourceProperty(
                        cluster_arn="clusterArn",
                        namespaces=["namespaces"]
                    ),
                    resource_tags=[resiliencehubv2.CfnService.ResourceTagProperty(
                        key="key",
                        values=["values"]
                    )],
                    tf_state_file_url="tfStateFileUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e35123fb3125dae56d99f98e2ba6dfd7915ea98d75d78550a3a8fb6dddb51352)
                check_type(argname="argument cfn_stack_arn", value=cfn_stack_arn, expected_type=type_hints["cfn_stack_arn"])
                check_type(argname="argument design_file_s3_url", value=design_file_s3_url, expected_type=type_hints["design_file_s3_url"])
                check_type(argname="argument eks", value=eks, expected_type=type_hints["eks"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
                check_type(argname="argument tf_state_file_url", value=tf_state_file_url, expected_type=type_hints["tf_state_file_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cfn_stack_arn is not None:
                self._values["cfn_stack_arn"] = cfn_stack_arn
            if design_file_s3_url is not None:
                self._values["design_file_s3_url"] = design_file_s3_url
            if eks is not None:
                self._values["eks"] = eks
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags
            if tf_state_file_url is not None:
                self._values["tf_state_file_url"] = tf_state_file_url

        @builtins.property
        def cfn_stack_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of a CloudFormation stack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourceconfiguration.html#cfn-resiliencehubv2-service-resourceconfiguration-cfnstackarn
            '''
            result = self._values.get("cfn_stack_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def design_file_s3_url(self) -> typing.Optional[builtins.str]:
            '''S3 URL of a design file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourceconfiguration.html#cfn-resiliencehubv2-service-resourceconfiguration-designfiles3url
            '''
            result = self._values.get("design_file_s3_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def eks(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.EksSourceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourceconfiguration.html#cfn-resiliencehubv2-service-resourceconfiguration-eks
            '''
            result = self._values.get("eks")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.EksSourceProperty"]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.ResourceTagProperty"]]]]:
            '''Resource tags to discover resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourceconfiguration.html#cfn-resiliencehubv2-service-resourceconfiguration-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.ResourceTagProperty"]]]], result)

        @builtins.property
        def tf_state_file_url(self) -> typing.Optional[builtins.str]:
            '''URL of a Terraform state file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourceconfiguration.html#cfn-resiliencehubv2-service-resourceconfiguration-tfstatefileurl
            '''
            result = self._values.get("tf_state_file_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            values: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param key: Tag key.
            :param values: Tag values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                resource_tag_property = resiliencehubv2.CfnService.ResourceTagProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be347aed89ea2bc55a6bbf8be865dc75dd68ec5e812c92564cd91af260bf24a6)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "values": values,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''Tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourcetag.html#cfn-resiliencehubv2-service-resourcetag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def values(self) -> typing.List[builtins.str]:
            '''Tag values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-resourcetag.html#cfn-resiliencehubv2-service-resourcetag-values
            '''
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.S3ReportOutputConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_owner": "bucketOwner", "bucket_path": "bucketPath"},
    )
    class S3ReportOutputConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_owner: builtins.str,
            bucket_path: builtins.str,
        ) -> None:
            '''S3 configuration for report output.

            :param bucket_owner: Account ID of the bucket owner.
            :param bucket_path: S3 bucket path where reports will be written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-s3reportoutputconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                s3_report_output_configuration_property = resiliencehubv2.CfnService.S3ReportOutputConfigurationProperty(
                    bucket_owner="bucketOwner",
                    bucket_path="bucketPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40aff8a4f02243bbfe3c7814df2330c297f01aab0fe5aff54214d747200a195d)
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument bucket_path", value=bucket_path, expected_type=type_hints["bucket_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_owner": bucket_owner,
                "bucket_path": bucket_path,
            }

        @builtins.property
        def bucket_owner(self) -> builtins.str:
            '''Account ID of the bucket owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-s3reportoutputconfiguration.html#cfn-resiliencehubv2-service-s3reportoutputconfiguration-bucketowner
            '''
            result = self._values.get("bucket_owner")
            assert result is not None, "Required property 'bucket_owner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_path(self) -> builtins.str:
            '''S3 bucket path where reports will be written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-s3reportoutputconfiguration.html#cfn-resiliencehubv2-service-s3reportoutputconfiguration-bucketpath
            '''
            result = self._values.get("bucket_path")
            assert result is not None, "Required property 'bucket_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReportOutputConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.ServiceReportConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"report_output": "reportOutput"},
    )
    class ServiceReportConfigurationProperty:
        def __init__(
            self,
            *,
            report_output: typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.ReportOutputConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Configuration for automatic report generation on a Service.

            :param report_output: Output destinations for generated reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-servicereportconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                service_report_configuration_property = resiliencehubv2.CfnService.ServiceReportConfigurationProperty(
                    report_output=[resiliencehubv2.CfnService.ReportOutputConfigurationProperty(
                        s3=resiliencehubv2.CfnService.S3ReportOutputConfigurationProperty(
                            bucket_owner="bucketOwner",
                            bucket_path="bucketPath"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e1877e39f31e88c69030d5a2056385fc2831e4fded6bcdf6989d30894bcbeab)
                check_type(argname="argument report_output", value=report_output, expected_type=type_hints["report_output"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "report_output": report_output,
            }

        @builtins.property
        def report_output(
            self,
        ) -> typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.ReportOutputConfigurationProperty"]]]:
            '''Output destinations for generated reports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-servicereportconfiguration.html#cfn-resiliencehubv2-service-servicereportconfiguration-reportoutput
            '''
            result = self._values.get("report_output")
            assert result is not None, "Required property 'report_output' is missing"
            return typing.cast(typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.ReportOutputConfigurationProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceReportConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.SloSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_name": "policyName", "value": "value"},
    )
    class SloSourceProperty:
        def __init__(
            self,
            *,
            policy_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param policy_name: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-slosource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                slo_source_property = resiliencehubv2.CfnService.SloSourceProperty(
                    policy_name="policyName",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d1a01abadfe4ca2d50d5f2a37c62ff834affb2cdaf557a3c420bed1eebfcb72)
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_name is not None:
                self._values["policy_name"] = policy_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-slosource.html#cfn-resiliencehubv2-service-slosource-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-slosource.html#cfn-resiliencehubv2-service-slosource-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SloSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnService.TargetSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_name": "policyName", "value": "value"},
    )
    class TargetSourceProperty:
        def __init__(
            self,
            *,
            policy_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param policy_name: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-targetsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
                
                target_source_property = resiliencehubv2.CfnService.TargetSourceProperty(
                    policy_name="policyName",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cdbacb4cdd0ec8ba002ccef6c12d3fd4bf6c9016ddbb8007adea5707a83e6cc5)
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_name is not None:
                self._values["policy_name"] = policy_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-targetsource.html#cfn-resiliencehubv2-service-targetsource-policyname
            '''
            result = self._values.get("policy_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehubv2-service-targetsource.html#cfn-resiliencehubv2-service-targetsource-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_c2943556, _IServiceFunctionRef_176497fa)
class CfnServiceFunction(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnServiceFunction",
):
    '''Creates a service function within a Resilience Hub service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-servicefunction.html
    :cloudformationResource: AWS::ResilienceHubV2::ServiceFunction
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
        
        cfn_service_function = resiliencehubv2.CfnServiceFunction(self, "MyCfnServiceFunction",
            criticality="criticality",
            name="name",
            service_arn="serviceArn",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        criticality: builtins.str,
        name: builtins.str,
        service_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHubV2::ServiceFunction``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param criticality: The criticality of the service function.
        :param name: The name of the service function.
        :param service_arn: The ARN of the parent service.
        :param description: The description of the service function.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba58da444dcd08a707fb324aff004e4b32bfca134f03c295b1ece6e0f79721f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceFunctionProps(
            criticality=criticality,
            name=name,
            service_arn=service_arn,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnServiceFunction")
    @builtins.classmethod
    def is_cfn_service_function(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnServiceFunction.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f631e142b10921a628478666b8c0179a080ee9d1c45e5429455b7ac77341e203)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnServiceFunction", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8eeeaac0063827f54de5f0ccdc0cbebf33d56abd28edf19ef157894f0c931b9)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4271c97d03f74cc10d121e95d72fdc31e40e9fd2d733c4441feedd03675ea07)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the service function was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceCount")
    def attr_resource_count(self) -> jsii.Number:
        '''The number of resources associated with this function.

        :cloudformationAttribute: ResourceCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrResourceCount"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceFunctionId")
    def attr_service_function_id(self) -> builtins.str:
        '''The server-generated service function ID.

        :cloudformationAttribute: ServiceFunctionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceFunctionId"))

    @builtins.property
    @jsii.member(jsii_name="attrSource")
    def attr_source(self) -> builtins.str:
        '''The source of the service function.

        :cloudformationAttribute: Source
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSource"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the service function was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="serviceFunctionRef")
    def service_function_ref(self) -> "_ServiceFunctionReference_766b969b":
        '''A reference to a ServiceFunction resource.'''
        return typing.cast("_ServiceFunctionReference_766b969b", jsii.get(self, "serviceFunctionRef"))

    @builtins.property
    @jsii.member(jsii_name="criticality")
    def criticality(self) -> builtins.str:
        '''The criticality of the service function.'''
        return typing.cast(builtins.str, jsii.get(self, "criticality"))

    @criticality.setter
    def criticality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3643f0336d27164481b5c125dd7f35ebe4b09dcebbf8c5b9480d51ac5f29deca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criticality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the service function.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beff5f5dafea49da6abc4de3e9b71a5f0d1e706b65cc44ef215efb19d4249452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''The ARN of the parent service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @service_arn.setter
    def service_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb383288f74ae56b541d028cdff4d06e0226c8285ee1cbe6070e370c47766cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service function.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed64e15fda69ee9dc3d694ecd60cf053a6a85cdec8ecf6c1c88eacf4db4c771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnServiceFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "criticality": "criticality",
        "name": "name",
        "service_arn": "serviceArn",
        "description": "description",
    },
)
class CfnServiceFunctionProps:
    def __init__(
        self,
        *,
        criticality: builtins.str,
        name: builtins.str,
        service_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceFunction``.

        :param criticality: The criticality of the service function.
        :param name: The name of the service function.
        :param service_arn: The ARN of the parent service.
        :param description: The description of the service function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-servicefunction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
            
            cfn_service_function_props = resiliencehubv2.CfnServiceFunctionProps(
                criticality="criticality",
                name="name",
                service_arn="serviceArn",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debf3e71098de7880e14b3dfae0cd423ae96d70fd7e348f99b576e63bfd50ab7)
            check_type(argname="argument criticality", value=criticality, expected_type=type_hints["criticality"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criticality": criticality,
            "name": name,
            "service_arn": service_arn,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def criticality(self) -> builtins.str:
        '''The criticality of the service function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-servicefunction.html#cfn-resiliencehubv2-servicefunction-criticality
        '''
        result = self._values.get("criticality")
        assert result is not None, "Required property 'criticality' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the service function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-servicefunction.html#cfn-resiliencehubv2-servicefunction-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_arn(self) -> builtins.str:
        '''The ARN of the parent service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-servicefunction.html#cfn-resiliencehubv2-servicefunction-servicearn
        '''
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-servicefunction.html#cfn-resiliencehubv2-servicefunction-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "regions": "regions",
        "assertions": "assertions",
        "associated_systems": "associatedSystems",
        "dependency_discovery": "dependencyDiscovery",
        "description": "description",
        "input_sources": "inputSources",
        "kms_key_id": "kmsKeyId",
        "permission_model": "permissionModel",
        "policy_arn": "policyArn",
        "report_configuration": "reportConfiguration",
        "tags": "tags",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        regions: typing.Sequence[builtins.str],
        assertions: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.AssertionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        associated_systems: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.AssociatedSystemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        dependency_discovery: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        input_sources: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Sequence[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.InputSourceDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        permission_model: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.PermissionModelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_arn: typing.Optional[builtins.str] = None,
        report_configuration: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnService.ServiceReportConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnService``.

        :param name: The name of the service.
        :param regions: AWS regions for the service.
        :param assertions: Assertions associated with this service.
        :param associated_systems: Systems associated with this service.
        :param dependency_discovery: Dependency discovery state.
        :param description: The description of the service.
        :param input_sources: Input sources for this service.
        :param kms_key_id: The KMS key ID for encrypting service data.
        :param permission_model: 
        :param policy_arn: The ARN of the resilience policy to associate.
        :param report_configuration: Configuration for automatic report generation on a Service.
        :param tags: Tags assigned to the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
            
            cfn_service_props = resiliencehubv2.CfnServiceProps(
                name="name",
                regions=["regions"],
            
                # the properties below are optional
                assertions=[resiliencehubv2.CfnService.AssertionDefinitionProperty(
                    text="text"
                )],
                associated_systems=[resiliencehubv2.CfnService.AssociatedSystemProperty(
                    system_arn="systemArn",
            
                    # the properties below are optional
                    user_journey_ids=["userJourneyIds"]
                )],
                dependency_discovery="dependencyDiscovery",
                description="description",
                input_sources=[resiliencehubv2.CfnService.InputSourceDefinitionProperty(
                    resource_configuration=resiliencehubv2.CfnService.ResourceConfigurationProperty(
                        cfn_stack_arn="cfnStackArn",
                        design_file_s3_url="designFileS3Url",
                        eks=resiliencehubv2.CfnService.EksSourceProperty(
                            cluster_arn="clusterArn",
                            namespaces=["namespaces"]
                        ),
                        resource_tags=[resiliencehubv2.CfnService.ResourceTagProperty(
                            key="key",
                            values=["values"]
                        )],
                        tf_state_file_url="tfStateFileUrl"
                    )
                )],
                kms_key_id="kmsKeyId",
                permission_model=resiliencehubv2.CfnService.PermissionModelProperty(
                    invoker_role_name="invokerRoleName",
            
                    # the properties below are optional
                    cross_account_role_arns=[resiliencehubv2.CfnService.CrossAccountRoleConfigurationProperty(
                        cross_account_role_arn="crossAccountRoleArn",
            
                        # the properties below are optional
                        external_id="externalId"
                    )]
                ),
                policy_arn="policyArn",
                report_configuration=resiliencehubv2.CfnService.ServiceReportConfigurationProperty(
                    report_output=[resiliencehubv2.CfnService.ReportOutputConfigurationProperty(
                        s3=resiliencehubv2.CfnService.S3ReportOutputConfigurationProperty(
                            bucket_owner="bucketOwner",
                            bucket_path="bucketPath"
                        )
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b8906af88284d1ba0ad97f215ad3c246bc5df190fa6886f254d66cb17c37cb9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument assertions", value=assertions, expected_type=type_hints["assertions"])
            check_type(argname="argument associated_systems", value=associated_systems, expected_type=type_hints["associated_systems"])
            check_type(argname="argument dependency_discovery", value=dependency_discovery, expected_type=type_hints["dependency_discovery"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument input_sources", value=input_sources, expected_type=type_hints["input_sources"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument permission_model", value=permission_model, expected_type=type_hints["permission_model"])
            check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
            check_type(argname="argument report_configuration", value=report_configuration, expected_type=type_hints["report_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "regions": regions,
        }
        if assertions is not None:
            self._values["assertions"] = assertions
        if associated_systems is not None:
            self._values["associated_systems"] = associated_systems
        if dependency_discovery is not None:
            self._values["dependency_discovery"] = dependency_discovery
        if description is not None:
            self._values["description"] = description
        if input_sources is not None:
            self._values["input_sources"] = input_sources
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if permission_model is not None:
            self._values["permission_model"] = permission_model
        if policy_arn is not None:
            self._values["policy_arn"] = policy_arn
        if report_configuration is not None:
            self._values["report_configuration"] = report_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regions(self) -> typing.List[builtins.str]:
        '''AWS regions for the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-regions
        '''
        result = self._values.get("regions")
        assert result is not None, "Required property 'regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def assertions(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssertionDefinitionProperty"]]]]:
        '''Assertions associated with this service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-assertions
        '''
        result = self._values.get("assertions")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssertionDefinitionProperty"]]]], result)

    @builtins.property
    def associated_systems(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssociatedSystemProperty"]]]]:
        '''Systems associated with this service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-associatedsystems
        '''
        result = self._values.get("associated_systems")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.AssociatedSystemProperty"]]]], result)

    @builtins.property
    def dependency_discovery(self) -> typing.Optional[builtins.str]:
        '''Dependency discovery state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-dependencydiscovery
        '''
        result = self._values.get("dependency_discovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_sources(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.InputSourceDefinitionProperty"]]]]:
        '''Input sources for this service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-inputsources
        '''
        result = self._values.get("input_sources")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", typing.List[typing.Union["_IResolvable_da3f097b", "CfnService.InputSourceDefinitionProperty"]]]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key ID for encrypting service data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission_model(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.PermissionModelProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-permissionmodel
        '''
        result = self._values.get("permission_model")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.PermissionModelProperty"]], result)

    @builtins.property
    def policy_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resilience policy to associate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-policyarn
        '''
        result = self._values.get("policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def report_configuration(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.ServiceReportConfigurationProperty"]]:
        '''Configuration for automatic report generation on a Service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-reportconfiguration
        '''
        result = self._values.get("report_configuration")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnService.ServiceReportConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-service.html#cfn-resiliencehubv2-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556, _ISystemRef_c37fa082, _ITaggableV2_4e6798f8)
class CfnSystem(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnSystem",
):
    '''Creates a system that represents a logical grouping of services.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-system.html
    :cloudformationResource: AWS::ResilienceHubV2::System
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
        
        cfn_system = resiliencehubv2.CfnSystem(self, "MyCfnSystem",
            name="name",
        
            # the properties below are optional
            description="description",
            kms_key_id="kmsKeyId",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHubV2::System``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the system.
        :param description: The description of the system.
        :param kms_key_id: The KMS key ID for encrypting system data.
        :param tags: Tags assigned to the system.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405b90698d86612452f0d03dd57e62240ba13029395a0d01bb77e8d66fb62b2d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSystemProps(
            name=name, description=description, kms_key_id=kms_key_id, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForSystem")
    @builtins.classmethod
    def arn_for_system(cls, resource: "_ISystemRef_c37fa082") -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50dcf6efaf23558cf735564897416ed26ff31b9e34792a2f1f3633ad52623c1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForSystem", [resource]))

    @jsii.member(jsii_name="isCfnSystem")
    @builtins.classmethod
    def is_cfn_system(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSystem.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879bbd55b067339d4f620dc8ba11d6032da579a1e8070b67f07bb501c154d31c)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSystem", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6c6793a6511f7329136ddd1d07d01c95d9539dc990d3683f66b563aa7b7b3a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b77e7133606f880ffb04c296d1943471ec4daf0ca1d1501eb29843b0c94f5e8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the system was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrSystemArn")
    def attr_system_arn(self) -> builtins.str:
        '''The ARN of the system.

        :cloudformationAttribute: SystemArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSystemArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSystemId")
    def attr_system_id(self) -> builtins.str:
        '''The system ID.

        :cloudformationAttribute: SystemId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSystemId"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the system was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_TagManager_0a598cb3":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_TagManager_0a598cb3", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="systemRef")
    def system_ref(self) -> "_SystemReference_71b63cdd":
        '''A reference to a System resource.'''
        return typing.cast("_SystemReference_71b63cdd", jsii.get(self, "systemRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the system.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c81be8218e696748585e9504afb71bfa95b2c885eabe9fec53ac7aad8500f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the system.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177bd08243f175ccd6578b9d15d7c0bc862e83d7846efe0b211a282efe7ea14e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key ID for encrypting system data.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f937a5a8a39f82303967ad20c105a8f63e81c586a41e86bfeac68e83d56db855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the system.'''
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["_CfnTag_f6864754"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fff15930170fd51f973d7a70c82cae6b8d0acb3e045d9c219267c24ab332b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "tags": "tags",
    },
)
class CfnSystemProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSystem``.

        :param name: The name of the system.
        :param description: The description of the system.
        :param kms_key_id: The KMS key ID for encrypting system data.
        :param tags: Tags assigned to the system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-system.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
            
            cfn_system_props = resiliencehubv2.CfnSystemProps(
                name="name",
            
                # the properties below are optional
                description="description",
                kms_key_id="kmsKeyId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9b127957de5f399d4f440f7958ad7824b1ac9311e507848fda8cf525c0755a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-system.html#cfn-resiliencehubv2-system-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-system.html#cfn-resiliencehubv2-system-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key ID for encrypting system data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-system.html#cfn-resiliencehubv2-system-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-system.html#cfn-resiliencehubv2-system-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556, _IUserJourneyRef_ef12e386)
class CfnUserJourney(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnUserJourney",
):
    '''Creates a user journey within a Resilience Hub system.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-userjourney.html
    :cloudformationResource: AWS::ResilienceHubV2::UserJourney
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
        
        cfn_user_journey = resiliencehubv2.CfnUserJourney(self, "MyCfnUserJourney",
            name="name",
            system_identifier="systemIdentifier",
        
            # the properties below are optional
            description="description",
            policy_arn="policyArn"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        system_identifier: builtins.str,
        description: typing.Optional[builtins.str] = None,
        policy_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ResilienceHubV2::UserJourney``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the user journey.
        :param system_identifier: The system ARN or system ID that owns this user journey.
        :param description: The description of the user journey.
        :param policy_arn: The ARN of the resilience policy to associate with this user journey.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83af87772206fde8fd7508052e09fcacc1009e2808ce7ba576660a693a9347d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserJourneyProps(
            name=name,
            system_identifier=system_identifier,
            description=description,
            policy_arn=policy_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnUserJourney")
    @builtins.classmethod
    def is_cfn_user_journey(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnUserJourney.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49778045cd8c93e126981d99436630b573dea373e3bd3091a65cdb93a91fb4c3)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnUserJourney", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c2955bcba8ae663e3a6aee140c9bea198b58adfb80824fa588264dd6828696)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9221ab3f24436a040dc223878cd8e8af4f92827155dbd30dc7361f28fa7e39b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the user journey was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the user journey was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUserJourneyId")
    def attr_user_journey_id(self) -> builtins.str:
        '''The server-generated user journey ID.

        :cloudformationAttribute: UserJourneyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUserJourneyId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="userJourneyRef")
    def user_journey_ref(self) -> "_UserJourneyReference_d8b20a5a":
        '''A reference to a UserJourney resource.'''
        return typing.cast("_UserJourneyReference_d8b20a5a", jsii.get(self, "userJourneyRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the user journey.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afa7030d035277e2d93e5ebaa3755a61fdb6c3c751239ac58139a6f27743bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemIdentifier")
    def system_identifier(self) -> builtins.str:
        '''The system ARN or system ID that owns this user journey.'''
        return typing.cast(builtins.str, jsii.get(self, "systemIdentifier"))

    @system_identifier.setter
    def system_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0d8d5961f0175df0b078d515edaa4f546437971daf23f9b5f722c88255961e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the user journey.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b59c36c1cc5c6ffc4f06475cc8b710f00dccfdc9ff46e08245f34f3c87b6696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyArn")
    def policy_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resilience policy to associate with this user journey.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyArn"))

    @policy_arn.setter
    def policy_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f14136224bd0bf550451b4284748c15dd38c68e1d9cdf14f8fc0548b03d219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyArn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_resiliencehubv2.CfnUserJourneyProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "system_identifier": "systemIdentifier",
        "description": "description",
        "policy_arn": "policyArn",
    },
)
class CfnUserJourneyProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        system_identifier: builtins.str,
        description: typing.Optional[builtins.str] = None,
        policy_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnUserJourney``.

        :param name: The name of the user journey.
        :param system_identifier: The system ARN or system ID that owns this user journey.
        :param description: The description of the user journey.
        :param policy_arn: The ARN of the resilience policy to associate with this user journey.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-userjourney.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_resiliencehubv2 as resiliencehubv2
            
            cfn_user_journey_props = resiliencehubv2.CfnUserJourneyProps(
                name="name",
                system_identifier="systemIdentifier",
            
                # the properties below are optional
                description="description",
                policy_arn="policyArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31b84d2608437c309b7f6ba8b5e3ed9df388d693c4ef8efee9ac70d196a669f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument system_identifier", value=system_identifier, expected_type=type_hints["system_identifier"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "system_identifier": system_identifier,
        }
        if description is not None:
            self._values["description"] = description
        if policy_arn is not None:
            self._values["policy_arn"] = policy_arn

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the user journey.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-userjourney.html#cfn-resiliencehubv2-userjourney-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def system_identifier(self) -> builtins.str:
        '''The system ARN or system ID that owns this user journey.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-userjourney.html#cfn-resiliencehubv2-userjourney-systemidentifier
        '''
        result = self._values.get("system_identifier")
        assert result is not None, "Required property 'system_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the user journey.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-userjourney.html#cfn-resiliencehubv2-userjourney-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resilience policy to associate with this user journey.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehubv2-userjourney.html#cfn-resiliencehubv2-userjourney-policyarn
        '''
        result = self._values.get("policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserJourneyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPolicy",
    "CfnPolicyProps",
    "CfnService",
    "CfnServiceFunction",
    "CfnServiceFunctionProps",
    "CfnServiceProps",
    "CfnSystem",
    "CfnSystemProps",
    "CfnUserJourney",
    "CfnUserJourneyProps",
]

publication.publish()

def _typecheckingstub__b2e629fc4862e28e629f2d24cf4a00a9ca948681ba5b90659c1dcc6199c320f1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    availability_slo: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.AvailabilitySloProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_recovery: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.DataRecoveryTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    multi_az: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.MultiAzTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_region: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.MultiRegionTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657ec34d9724a44984551b0d29a82d110c168db65580307fce1a2d5a4e955b62(
    resource: _IPolicyRef_8f29ce94,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88419ea3bbf7ed00758b7eff5c807b3279da0bd13ec41e95b91b3dc4905c91b8(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9281463bbddd5e6a5abcb1b418805af64867041de7188c8fcef204bbd56fba(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7931aad811d55f1c1d321f7f330caa12a52b96ab6cff5615e40053a2563812ee(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d259843c26b15a16dcbabd1e0e75fcbc09629b91a287d87104d92a18f19d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a32bbfeaa8d459ff6083f2740f10c9ad8aca7eca836b39dc5f96859e83118f(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnPolicy.AvailabilitySloProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876c6cdf83b364b06e9611ae74176173ca5e80eb30145b85d0a5866ba6f8bc5f(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnPolicy.DataRecoveryTargetsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3d4da539650d8938a395790f0d988b7ead316557ac6ead656ec0f538759099(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4b0d8affbccb5e5c84f1894869b877f9d0d3ed0d024461283c9760be1c47ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8c8e4e3a2ca89f1c4516be1382bfe9a786ae265c976fe75df7b71606d23ee5(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnPolicy.MultiAzTargetsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b113d1c1a16d9a88d7758c26ad9a6eac43b4a8995ad9a6dfcb5c065a458e2aa(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnPolicy.MultiRegionTargetsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a07e642dc63b7980c82a54120ed7d01ba6c8a726bdfc0589953ca23747bd214(
    value: typing.Optional[typing.List[_CfnTag_f6864754]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fe061cf9d7a9f04783a913205c5eedecdc2480c89ff0f7834ff1a76b924fe0(
    *,
    target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c006605f95c69f124beaad55ccd214823579d133c3345c18bfdbf66c77a8c6ac(
    *,
    time_between_backups_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbe8843e5c0186207e785f6083fd070a090ff07a1de0f04ec95bb25b94450b0(
    *,
    disaster_recovery_approach: typing.Optional[builtins.str] = None,
    rpo_in_minutes: typing.Optional[jsii.Number] = None,
    rto_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487bb7bdb57d0212483b7ec1cee0412ed082324b11618e02e4ba649b339669aa(
    *,
    disaster_recovery_approach: typing.Optional[builtins.str] = None,
    rpo_in_minutes: typing.Optional[jsii.Number] = None,
    rto_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c906443be9003dedeed32d06ee8a6f0d9a43e95506b85846be31638078cafe(
    *,
    name: builtins.str,
    availability_slo: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.AvailabilitySloProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_recovery: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.DataRecoveryTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    multi_az: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.MultiAzTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_region: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnPolicy.MultiRegionTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bdd32c65d4a9df22e965e380026f55b7e059ad2c4bb5b54867d27eceaea1e5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    regions: typing.Sequence[builtins.str],
    assertions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.AssertionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    associated_systems: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.AssociatedSystemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dependency_discovery: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    input_sources: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.InputSourceDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    permission_model: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.PermissionModelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_arn: typing.Optional[builtins.str] = None,
    report_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.ServiceReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4163076509fc819924f2189e2949bb93d4130966e24f7f0934cac260900582a(
    resource: _IServiceRef_7f44f4e1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec24122752db76055fe3823408f2737c9bdbd12aa457cdc9b0ce9fcde22579e(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d3b1d949c49ce026994d9d4b0b0a1aeea5e5b94b475df0cbfd6d1f83fbce47(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a8bed735bc8fdf33d315032cfb56f7ad6fca0cd599641c370a480c562a9584(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40654003c72cad607c2285fc9007b24841372f07282d2e1e0074d9e53de8da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964bfce08922c4fb735abcd9089af81bd138fd8a4ffbb49d7c1e1d6f1549576e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25bd9cec3047a0d0d7fe892cfb844e2cadbd370c4f6e00d03ec6668c3ae0bb1(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnService.AssertionDefinitionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebf53f05f27c31f326af1fc62ded64873bc1a58da7e10b94706eae63e148fb6(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnService.AssociatedSystemProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b9e7e595d6c6af07c6a42ca51a94cbaf992a9a6f55a97552f6367b986ebe2c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0243afd562c00bc61ef677f20cecc4ac5705343dc87da0758a23a18fcdc47115(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb607cafec82377097ae094d11f8506899ea08c36738456c1134887ead12e36(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnService.InputSourceDefinitionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242b39ff6b3b9a87071efd4aa5b82fb4561d7e0da10e88151ba434b99256230c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f96997f389a164a9d59977b08fc63042a4bebad060235b2ad58734c1161867(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnService.PermissionModelProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2f304aa99feed1c072f06bf949b63b65fde2503fd90aaa86c7b1286b57e06a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4a4c62b7f037a37893fa13b7f13b0f1fabc51715e30be18ead891af7876e50(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnService.ServiceReportConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a377d29fac1c509599600752f1645f130ab40efe1400fd62790e225e015fb1(
    value: typing.Optional[typing.List[_CfnTag_f6864754]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41432ca73fa194f691a78a5d7f3574e1e12d47aa621221155170fe576d5eea7(
    *,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305b50b88f93c47a6df92c9050e81f812cf5cca69c6dfe6188aa63443c4a9012(
    *,
    system_arn: builtins.str,
    user_journey_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebe7293c74e1e49a5c894dc42cf632e3b58feccb2d4f9d9c5b6d9f1e2e089fa(
    *,
    cross_account_role_arn: builtins.str,
    external_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a8e661884ddb84edcb38679f978478b1d10209ff839e0e585f535402bf3884(
    *,
    policy_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3bf83c642b175e56cedcc2597cb09cfc5891dedf9b6e0c22b4876f003d65e9(
    *,
    availability_slo: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.SloSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_az_dr_approach: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.DisasterRecoverySourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_az_rpo: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.TargetSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_az_rto: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.TargetSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_region_dr_approach: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.DisasterRecoverySourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_region_rpo: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.TargetSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    multi_region_rto: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.TargetSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8222153171bacb58425e667eddaf39b74006a9c713bec1af7ab5451917df746(
    *,
    cluster_arn: builtins.str,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b96172a11348626b3d426531adada00b779bda9de5fd5a2438e5760b0b948a(
    *,
    resource_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.ResourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe67ffbdc763fe6cc5eb3fd567392d6db437b5325ab8eada2e5ed14f605722d(
    *,
    invoker_role_name: builtins.str,
    cross_account_role_arns: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.CrossAccountRoleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e98098f1c2bd297b3d7e01e55079dd85f796e88178aeeb1b60467b04c1bdb28(
    *,
    s3: typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.S3ReportOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35123fb3125dae56d99f98e2ba6dfd7915ea98d75d78550a3a8fb6dddb51352(
    *,
    cfn_stack_arn: typing.Optional[builtins.str] = None,
    design_file_s3_url: typing.Optional[builtins.str] = None,
    eks: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.EksSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_tags: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tf_state_file_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be347aed89ea2bc55a6bbf8be865dc75dd68ec5e812c92564cd91af260bf24a6(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40aff8a4f02243bbfe3c7814df2330c297f01aab0fe5aff54214d747200a195d(
    *,
    bucket_owner: builtins.str,
    bucket_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1877e39f31e88c69030d5a2056385fc2831e4fded6bcdf6989d30894bcbeab(
    *,
    report_output: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.ReportOutputConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1a01abadfe4ca2d50d5f2a37c62ff834affb2cdaf557a3c420bed1eebfcb72(
    *,
    policy_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbacb4cdd0ec8ba002ccef6c12d3fd4bf6c9016ddbb8007adea5707a83e6cc5(
    *,
    policy_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba58da444dcd08a707fb324aff004e4b32bfca134f03c295b1ece6e0f79721f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    criticality: builtins.str,
    name: builtins.str,
    service_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f631e142b10921a628478666b8c0179a080ee9d1c45e5429455b7ac77341e203(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8eeeaac0063827f54de5f0ccdc0cbebf33d56abd28edf19ef157894f0c931b9(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4271c97d03f74cc10d121e95d72fdc31e40e9fd2d733c4441feedd03675ea07(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3643f0336d27164481b5c125dd7f35ebe4b09dcebbf8c5b9480d51ac5f29deca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beff5f5dafea49da6abc4de3e9b71a5f0d1e706b65cc44ef215efb19d4249452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb383288f74ae56b541d028cdff4d06e0226c8285ee1cbe6070e370c47766cbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed64e15fda69ee9dc3d694ecd60cf053a6a85cdec8ecf6c1c88eacf4db4c771(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debf3e71098de7880e14b3dfae0cd423ae96d70fd7e348f99b576e63bfd50ab7(
    *,
    criticality: builtins.str,
    name: builtins.str,
    service_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8906af88284d1ba0ad97f215ad3c246bc5df190fa6886f254d66cb17c37cb9(
    *,
    name: builtins.str,
    regions: typing.Sequence[builtins.str],
    assertions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.AssertionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    associated_systems: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.AssociatedSystemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dependency_discovery: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    input_sources: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.InputSourceDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    permission_model: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.PermissionModelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_arn: typing.Optional[builtins.str] = None,
    report_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnService.ServiceReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405b90698d86612452f0d03dd57e62240ba13029395a0d01bb77e8d66fb62b2d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50dcf6efaf23558cf735564897416ed26ff31b9e34792a2f1f3633ad52623c1(
    resource: _ISystemRef_c37fa082,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879bbd55b067339d4f620dc8ba11d6032da579a1e8070b67f07bb501c154d31c(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6c6793a6511f7329136ddd1d07d01c95d9539dc990d3683f66b563aa7b7b3a(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b77e7133606f880ffb04c296d1943471ec4daf0ca1d1501eb29843b0c94f5e8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c81be8218e696748585e9504afb71bfa95b2c885eabe9fec53ac7aad8500f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177bd08243f175ccd6578b9d15d7c0bc862e83d7846efe0b211a282efe7ea14e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f937a5a8a39f82303967ad20c105a8f63e81c586a41e86bfeac68e83d56db855(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fff15930170fd51f973d7a70c82cae6b8d0acb3e045d9c219267c24ab332b55(
    value: typing.Optional[typing.List[_CfnTag_f6864754]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9b127957de5f399d4f440f7958ad7824b1ac9311e507848fda8cf525c0755a(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83af87772206fde8fd7508052e09fcacc1009e2808ce7ba576660a693a9347d6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    system_identifier: builtins.str,
    description: typing.Optional[builtins.str] = None,
    policy_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49778045cd8c93e126981d99436630b573dea373e3bd3091a65cdb93a91fb4c3(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c2955bcba8ae663e3a6aee140c9bea198b58adfb80824fa588264dd6828696(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9221ab3f24436a040dc223878cd8e8af4f92827155dbd30dc7361f28fa7e39b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afa7030d035277e2d93e5ebaa3755a61fdb6c3c751239ac58139a6f27743bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0d8d5961f0175df0b078d515edaa4f546437971daf23f9b5f722c88255961e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b59c36c1cc5c6ffc4f06475cc8b710f00dccfdc9ff46e08245f34f3c87b6696(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f14136224bd0bf550451b4284748c15dd38c68e1d9cdf14f8fc0548b03d219(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31b84d2608437c309b7f6ba8b5e3ed9df388d693c4ef8efee9ac70d196a669f(
    *,
    name: builtins.str,
    system_identifier: builtins.str,
    description: typing.Optional[builtins.str] = None,
    policy_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
