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

from ..._jsii import *

import constructs as _constructs_77d1e7e8
from .. import IEnvironmentAware as _IEnvironmentAware_f39049ee


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.IPolicyRef")
class IPolicyRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Policy.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="policyRef")
    def policy_ref(self) -> "PolicyReference":
        '''(experimental) A reference to a Policy resource.

        :stability: experimental
        '''
        ...


class _IPolicyRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Policy.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_resiliencehubv2.IPolicyRef"

    @builtins.property
    @jsii.member(jsii_name="policyRef")
    def policy_ref(self) -> "PolicyReference":
        '''(experimental) A reference to a Policy resource.

        :stability: experimental
        '''
        return typing.cast("PolicyReference", jsii.get(self, "policyRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPolicyRef).__jsii_proxy_class__ = lambda : _IPolicyRefProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.IServiceFunctionRef"
)
class IServiceFunctionRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ServiceFunction.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="serviceFunctionRef")
    def service_function_ref(self) -> "ServiceFunctionReference":
        '''(experimental) A reference to a ServiceFunction resource.

        :stability: experimental
        '''
        ...


class _IServiceFunctionRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ServiceFunction.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_resiliencehubv2.IServiceFunctionRef"

    @builtins.property
    @jsii.member(jsii_name="serviceFunctionRef")
    def service_function_ref(self) -> "ServiceFunctionReference":
        '''(experimental) A reference to a ServiceFunction resource.

        :stability: experimental
        '''
        return typing.cast("ServiceFunctionReference", jsii.get(self, "serviceFunctionRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServiceFunctionRef).__jsii_proxy_class__ = lambda : _IServiceFunctionRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.IServiceRef")
class IServiceRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Service.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="serviceRef")
    def service_ref(self) -> "ServiceReference":
        '''(experimental) A reference to a Service resource.

        :stability: experimental
        '''
        ...


class _IServiceRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Service.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_resiliencehubv2.IServiceRef"

    @builtins.property
    @jsii.member(jsii_name="serviceRef")
    def service_ref(self) -> "ServiceReference":
        '''(experimental) A reference to a Service resource.

        :stability: experimental
        '''
        return typing.cast("ServiceReference", jsii.get(self, "serviceRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServiceRef).__jsii_proxy_class__ = lambda : _IServiceRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.ISystemRef")
class ISystemRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a System.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="systemRef")
    def system_ref(self) -> "SystemReference":
        '''(experimental) A reference to a System resource.

        :stability: experimental
        '''
        ...


class _ISystemRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a System.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_resiliencehubv2.ISystemRef"

    @builtins.property
    @jsii.member(jsii_name="systemRef")
    def system_ref(self) -> "SystemReference":
        '''(experimental) A reference to a System resource.

        :stability: experimental
        '''
        return typing.cast("SystemReference", jsii.get(self, "systemRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISystemRef).__jsii_proxy_class__ = lambda : _ISystemRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.IUserJourneyRef")
class IUserJourneyRef(
    _constructs_77d1e7e8.IConstruct,
    _IEnvironmentAware_f39049ee,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a UserJourney.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="userJourneyRef")
    def user_journey_ref(self) -> "UserJourneyReference":
        '''(experimental) A reference to a UserJourney resource.

        :stability: experimental
        '''
        ...


class _IUserJourneyRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_IEnvironmentAware_f39049ee), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a UserJourney.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_resiliencehubv2.IUserJourneyRef"

    @builtins.property
    @jsii.member(jsii_name="userJourneyRef")
    def user_journey_ref(self) -> "UserJourneyReference":
        '''(experimental) A reference to a UserJourney resource.

        :stability: experimental
        '''
        return typing.cast("UserJourneyReference", jsii.get(self, "userJourneyRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUserJourneyRef).__jsii_proxy_class__ = lambda : _IUserJourneyRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.PolicyReference",
    jsii_struct_bases=[],
    name_mapping={"policy_arn": "policyArn"},
)
class PolicyReference:
    def __init__(self, *, policy_arn: builtins.str) -> None:
        '''A reference to a Policy resource.

        :param policy_arn: The PolicyArn of the Policy resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_resiliencehubv2 as interfaces_resiliencehubv2
            
            policy_reference = interfaces_resiliencehubv2.PolicyReference(
                policy_arn="policyArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a007d8e198e6f822e26c396ff3716496b7b041cded37b1f7f464e3b301c7fc)
            check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_arn": policy_arn,
        }

    @builtins.property
    def policy_arn(self) -> builtins.str:
        '''The PolicyArn of the Policy resource.'''
        result = self._values.get("policy_arn")
        assert result is not None, "Required property 'policy_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.ServiceFunctionReference",
    jsii_struct_bases=[],
    name_mapping={
        "service_arn": "serviceArn",
        "service_function_id": "serviceFunctionId",
    },
)
class ServiceFunctionReference:
    def __init__(
        self,
        *,
        service_arn: builtins.str,
        service_function_id: builtins.str,
    ) -> None:
        '''A reference to a ServiceFunction resource.

        :param service_arn: The ServiceArn of the ServiceFunction resource.
        :param service_function_id: The ServiceFunctionId of the ServiceFunction resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_resiliencehubv2 as interfaces_resiliencehubv2
            
            service_function_reference = interfaces_resiliencehubv2.ServiceFunctionReference(
                service_arn="serviceArn",
                service_function_id="serviceFunctionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1286d322b3e1a516344aeac96ddfd9acb339feba042b5c929bd444cbb4e414d)
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument service_function_id", value=service_function_id, expected_type=type_hints["service_function_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_arn": service_arn,
            "service_function_id": service_function_id,
        }

    @builtins.property
    def service_arn(self) -> builtins.str:
        '''The ServiceArn of the ServiceFunction resource.'''
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_function_id(self) -> builtins.str:
        '''The ServiceFunctionId of the ServiceFunction resource.'''
        result = self._values.get("service_function_id")
        assert result is not None, "Required property 'service_function_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFunctionReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.ServiceReference",
    jsii_struct_bases=[],
    name_mapping={"service_arn": "serviceArn"},
)
class ServiceReference:
    def __init__(self, *, service_arn: builtins.str) -> None:
        '''A reference to a Service resource.

        :param service_arn: The ServiceArn of the Service resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_resiliencehubv2 as interfaces_resiliencehubv2
            
            service_reference = interfaces_resiliencehubv2.ServiceReference(
                service_arn="serviceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611ac533e7d1aba1a0093f92ce8b75d27c931e9118288b4abb36126c806e72a9)
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_arn": service_arn,
        }

    @builtins.property
    def service_arn(self) -> builtins.str:
        '''The ServiceArn of the Service resource.'''
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.SystemReference",
    jsii_struct_bases=[],
    name_mapping={"system_arn": "systemArn"},
)
class SystemReference:
    def __init__(self, *, system_arn: builtins.str) -> None:
        '''A reference to a System resource.

        :param system_arn: The SystemArn of the System resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_resiliencehubv2 as interfaces_resiliencehubv2
            
            system_reference = interfaces_resiliencehubv2.SystemReference(
                system_arn="systemArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486ce6f06dbdc0e80607a818825851bfeb2233a8bc89f06744345ce20bd09d28)
            check_type(argname="argument system_arn", value=system_arn, expected_type=type_hints["system_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "system_arn": system_arn,
        }

    @builtins.property
    def system_arn(self) -> builtins.str:
        '''The SystemArn of the System resource.'''
        result = self._values.get("system_arn")
        assert result is not None, "Required property 'system_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SystemReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_resiliencehubv2.UserJourneyReference",
    jsii_struct_bases=[],
    name_mapping={
        "system_identifier": "systemIdentifier",
        "user_journey_id": "userJourneyId",
    },
)
class UserJourneyReference:
    def __init__(
        self,
        *,
        system_identifier: builtins.str,
        user_journey_id: builtins.str,
    ) -> None:
        '''A reference to a UserJourney resource.

        :param system_identifier: The SystemIdentifier of the UserJourney resource.
        :param user_journey_id: The UserJourneyId of the UserJourney resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_resiliencehubv2 as interfaces_resiliencehubv2
            
            user_journey_reference = interfaces_resiliencehubv2.UserJourneyReference(
                system_identifier="systemIdentifier",
                user_journey_id="userJourneyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9d6b2f843fd6d8785834a6a7ea16acb108739a88bb53e00691596a06b37124)
            check_type(argname="argument system_identifier", value=system_identifier, expected_type=type_hints["system_identifier"])
            check_type(argname="argument user_journey_id", value=user_journey_id, expected_type=type_hints["user_journey_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "system_identifier": system_identifier,
            "user_journey_id": user_journey_id,
        }

    @builtins.property
    def system_identifier(self) -> builtins.str:
        '''The SystemIdentifier of the UserJourney resource.'''
        result = self._values.get("system_identifier")
        assert result is not None, "Required property 'system_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_journey_id(self) -> builtins.str:
        '''The UserJourneyId of the UserJourney resource.'''
        result = self._values.get("user_journey_id")
        assert result is not None, "Required property 'user_journey_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserJourneyReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IPolicyRef",
    "IServiceFunctionRef",
    "IServiceRef",
    "ISystemRef",
    "IUserJourneyRef",
    "PolicyReference",
    "ServiceFunctionReference",
    "ServiceReference",
    "SystemReference",
    "UserJourneyReference",
]

publication.publish()

def _typecheckingstub__a9a007d8e198e6f822e26c396ff3716496b7b041cded37b1f7f464e3b301c7fc(
    *,
    policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1286d322b3e1a516344aeac96ddfd9acb339feba042b5c929bd444cbb4e414d(
    *,
    service_arn: builtins.str,
    service_function_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611ac533e7d1aba1a0093f92ce8b75d27c931e9118288b4abb36126c806e72a9(
    *,
    service_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486ce6f06dbdc0e80607a818825851bfeb2233a8bc89f06744345ce20bd09d28(
    *,
    system_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9d6b2f843fd6d8785834a6a7ea16acb108739a88bb53e00691596a06b37124(
    *,
    system_identifier: builtins.str,
    user_journey_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IPolicyRef, IServiceFunctionRef, IServiceRef, ISystemRef, IUserJourneyRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
