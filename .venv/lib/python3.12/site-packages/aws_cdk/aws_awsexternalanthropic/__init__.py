r'''
# AWS::AWSExternalAnthropic Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_awsexternalanthropic as awsexternalanthropic
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AWSExternalAnthropic construct libraries](https://constructs.dev/search?q=awsexternalanthropic)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AWSExternalAnthropic resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AWSExternalAnthropic.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AWSExternalAnthropic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AWSExternalAnthropic.html).

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
from ..interfaces.aws_awsexternalanthropic import (
    IWorkspaceRef as _IWorkspaceRef_00d45939,
    WorkspaceReference as _WorkspaceReference_ec14a59a,
)


@jsii.implements(_IInspectable_c2943556, _IWorkspaceRef_00d45939, _ITaggableV2_4e6798f8)
class CfnWorkspace(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_awsexternalanthropic.CfnWorkspace",
):
    '''Resource type definition for AWS::AWSExternalAnthropic::Workspace.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-awsexternalanthropic-workspace.html
    :cloudformationResource: AWS::AWSExternalAnthropic::Workspace
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_awsexternalanthropic as awsexternalanthropic
        
        cfn_workspace = awsexternalanthropic.CfnWorkspace(self, "MyCfnWorkspace",
            name="name",
        
            # the properties below are optional
            data_residency=awsexternalanthropic.CfnWorkspace.DataResidencyProperty(
                allowed_inference_geos=["allowedInferenceGeos"],
                default_inference_geo="defaultInferenceGeo",
                workspace_geo="workspaceGeo"
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
        data_residency: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnWorkspace.DataResidencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AWSExternalAnthropic::Workspace``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the workspace.
        :param data_residency: Data residency configuration for the workspace. WorkspaceGeo is immutable after creation.
        :param tags: An array of key-value pairs to apply to this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7972f9f230d9d32fca9aef341b3151dbcd7cfe39372c1c214af568bf845011)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceProps(name=name, data_residency=data_residency, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForWorkspace")
    @builtins.classmethod
    def arn_for_workspace(cls, resource: "_IWorkspaceRef_00d45939") -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01d28f1f33d0230df73c2724c2b8bec4908e395e44c76954b725eaf7baa1a70)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForWorkspace", [resource]))

    @jsii.member(jsii_name="isCfnWorkspace")
    @builtins.classmethod
    def is_cfn_workspace(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnWorkspace.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fb67a04f352dd374eb3bbf1c8774c50b909e14adc1cf96bda2a2342022d770)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnWorkspace", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85b761a2db1c50aa0842d08bc02df6d76481e9bdaa8ba78e620f10c264e1b1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1525cef69a762a224d976ca2d368314dc3817cb05ef8e29fbdb6220196218714)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the workspace.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the workspace was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier of the workspace.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

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
    @jsii.member(jsii_name="workspaceRef")
    def workspace_ref(self) -> "_WorkspaceReference_ec14a59a":
        '''A reference to a Workspace resource.'''
        return typing.cast("_WorkspaceReference_ec14a59a", jsii.get(self, "workspaceRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the workspace.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229b507e8aa5d72857ead27961ce095a691116c6c8d5954013478f4467650245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataResidency")
    def data_residency(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnWorkspace.DataResidencyProperty"]]:
        '''Data residency configuration for the workspace.'''
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnWorkspace.DataResidencyProperty"]], jsii.get(self, "dataResidency"))

    @data_residency.setter
    def data_residency(
        self,
        value: typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnWorkspace.DataResidencyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e13b4d8e24c1a46a50f2ed8345092e33a01c63355d9f7348d84b87ac883c634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataResidency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''An array of key-value pairs to apply to this resource.'''
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["_CfnTag_f6864754"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555038c93a8c4c5472ce094be0e4c8705faa9abc90e46165a5e6713c472ee0ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_awsexternalanthropic.CfnWorkspace.DataResidencyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_inference_geos": "allowedInferenceGeos",
            "default_inference_geo": "defaultInferenceGeo",
            "workspace_geo": "workspaceGeo",
        },
    )
    class DataResidencyProperty:
        def __init__(
            self,
            *,
            allowed_inference_geos: typing.Optional[typing.Sequence[builtins.str]] = None,
            default_inference_geo: typing.Optional[builtins.str] = None,
            workspace_geo: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Data residency configuration for the workspace.

            WorkspaceGeo is immutable after creation.

            :param allowed_inference_geos: Permitted inference geo values. Omit to allow all geos (the service default of 'unrestricted'); otherwise list specific geos.
            :param default_inference_geo: Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of AllowedInferenceGeos unless AllowedInferenceGeos is omitted.
            :param workspace_geo: Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-awsexternalanthropic-workspace-dataresidency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_awsexternalanthropic as awsexternalanthropic
                
                data_residency_property = awsexternalanthropic.CfnWorkspace.DataResidencyProperty(
                    allowed_inference_geos=["allowedInferenceGeos"],
                    default_inference_geo="defaultInferenceGeo",
                    workspace_geo="workspaceGeo"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed6b39c230431b9e74d34d832a0f3e909f9ee14b5cb700e6937b386678bed504)
                check_type(argname="argument allowed_inference_geos", value=allowed_inference_geos, expected_type=type_hints["allowed_inference_geos"])
                check_type(argname="argument default_inference_geo", value=default_inference_geo, expected_type=type_hints["default_inference_geo"])
                check_type(argname="argument workspace_geo", value=workspace_geo, expected_type=type_hints["workspace_geo"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_inference_geos is not None:
                self._values["allowed_inference_geos"] = allowed_inference_geos
            if default_inference_geo is not None:
                self._values["default_inference_geo"] = default_inference_geo
            if workspace_geo is not None:
                self._values["workspace_geo"] = workspace_geo

        @builtins.property
        def allowed_inference_geos(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Permitted inference geo values.

            Omit to allow all geos (the service default of 'unrestricted'); otherwise list specific geos.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-awsexternalanthropic-workspace-dataresidency.html#cfn-awsexternalanthropic-workspace-dataresidency-allowedinferencegeos
            '''
            result = self._values.get("allowed_inference_geos")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def default_inference_geo(self) -> typing.Optional[builtins.str]:
            '''Default inference geo applied when requests omit the parameter.

            Defaults to 'global' if omitted. Must be a member of AllowedInferenceGeos unless AllowedInferenceGeos is omitted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-awsexternalanthropic-workspace-dataresidency.html#cfn-awsexternalanthropic-workspace-dataresidency-defaultinferencegeo
            '''
            result = self._values.get("default_inference_geo")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workspace_geo(self) -> typing.Optional[builtins.str]:
            '''Geographic region for workspace data storage.

            Immutable after creation. Defaults to 'us' if omitted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-awsexternalanthropic-workspace-dataresidency.html#cfn-awsexternalanthropic-workspace-dataresidency-workspacegeo
            '''
            result = self._values.get("workspace_geo")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataResidencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_awsexternalanthropic.CfnWorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "data_residency": "dataResidency", "tags": "tags"},
)
class CfnWorkspaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        data_residency: typing.Optional[typing.Union["_IResolvable_da3f097b", typing.Union["CfnWorkspace.DataResidencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspace``.

        :param name: The name of the workspace.
        :param data_residency: Data residency configuration for the workspace. WorkspaceGeo is immutable after creation.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-awsexternalanthropic-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_awsexternalanthropic as awsexternalanthropic
            
            cfn_workspace_props = awsexternalanthropic.CfnWorkspaceProps(
                name="name",
            
                # the properties below are optional
                data_residency=awsexternalanthropic.CfnWorkspace.DataResidencyProperty(
                    allowed_inference_geos=["allowedInferenceGeos"],
                    default_inference_geo="defaultInferenceGeo",
                    workspace_geo="workspaceGeo"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60f15552610df14aaf729bcf9b16161b7e8222e8a4fce4e3e68e52e08ec2036)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data_residency", value=data_residency, expected_type=type_hints["data_residency"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if data_residency is not None:
            self._values["data_residency"] = data_residency
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-awsexternalanthropic-workspace.html#cfn-awsexternalanthropic-workspace-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_residency(
        self,
    ) -> typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnWorkspace.DataResidencyProperty"]]:
        '''Data residency configuration for the workspace.

        WorkspaceGeo is immutable after creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-awsexternalanthropic-workspace.html#cfn-awsexternalanthropic-workspace-dataresidency
        '''
        result = self._values.get("data_residency")
        return typing.cast(typing.Optional[typing.Union["_IResolvable_da3f097b", "CfnWorkspace.DataResidencyProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-awsexternalanthropic-workspace.html#cfn-awsexternalanthropic-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnWorkspace",
    "CfnWorkspaceProps",
]

publication.publish()

def _typecheckingstub__7d7972f9f230d9d32fca9aef341b3151dbcd7cfe39372c1c214af568bf845011(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    data_residency: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnWorkspace.DataResidencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01d28f1f33d0230df73c2724c2b8bec4908e395e44c76954b725eaf7baa1a70(
    resource: _IWorkspaceRef_00d45939,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fb67a04f352dd374eb3bbf1c8774c50b909e14adc1cf96bda2a2342022d770(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85b761a2db1c50aa0842d08bc02df6d76481e9bdaa8ba78e620f10c264e1b1b(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1525cef69a762a224d976ca2d368314dc3817cb05ef8e29fbdb6220196218714(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229b507e8aa5d72857ead27961ce095a691116c6c8d5954013478f4467650245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e13b4d8e24c1a46a50f2ed8345092e33a01c63355d9f7348d84b87ac883c634(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnWorkspace.DataResidencyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555038c93a8c4c5472ce094be0e4c8705faa9abc90e46165a5e6713c472ee0ce(
    value: typing.Optional[typing.List[_CfnTag_f6864754]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6b39c230431b9e74d34d832a0f3e909f9ee14b5cb700e6937b386678bed504(
    *,
    allowed_inference_geos: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_inference_geo: typing.Optional[builtins.str] = None,
    workspace_geo: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60f15552610df14aaf729bcf9b16161b7e8222e8a4fce4e3e68e52e08ec2036(
    *,
    name: builtins.str,
    data_residency: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnWorkspace.DataResidencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
