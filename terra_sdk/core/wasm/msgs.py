"Wasm module messages."

from __future__ import annotations

import base64
import json
from typing import Optional, Union

import attr
from terra_proto.terra.wasm.v1beta1 import (
    MsgClearContractAdmin as MsgClearContractAdmin_pb,
)
from terra_proto.terra.wasm.v1beta1 import MsgExecuteContract as MsgExecuteContract_pb
from terra_proto.terra.wasm.v1beta1 import (
    MsgInstantiateContract as MsgInstantiateContract_pb,
)
from terra_proto.terra.wasm.v1beta1 import MsgMigrateCode as MsgMigrateCode_pb
from terra_proto.terra.wasm.v1beta1 import MsgMigrateContract as MsgMigrateContract_pb
from terra_proto.terra.wasm.v1beta1 import MsgStoreCode as MsgStoreCode_pb
from terra_proto.terra.wasm.v1beta1 import (
    MsgUpdateContractAdmin as MsgUpdateContractAdmin_pb,
)
from betterproto.lib.google.protobuf import Any as Any_pb

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg
from terra_sdk.util.remove_none import remove_none

__all__ = [
    "MsgStoreCode",
    "MsgMigrateCode",
    "MsgInstantiateContract",
    "MsgExecuteContract",
    "MsgMigrateContract",
    "MsgUpdateContractAdmin",
    "MsgClearContractAdmin",
]


def parse_msg(msg: Union[dict, str, bytes]) -> Union[dict, str]:
    if type(msg) is dict:
        return msg
    try:
        msg = json.loads(msg)
    except:
        return str(msg)


@attr.s
class MsgStoreCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain.

    Args:
        sender: address of sender
        wasm_byte_code: base64-encoded string containing bytecode
    """

    type_amino = "wasm/MsgStoreCode"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgStoreCode"
    """"""
    prototype = MsgStoreCode_pb
    """"""

    sender: AccAddress = attr.ib()
    wasm_byte_code: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {"sender": self.sender, "wasm_byte_code": self.wasm_byte_code},
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgStoreCode:
        return cls(sender=data["sender"], wasm_byte_code=data["wasm_byte_code"])

    def to_proto(self) -> MsgStoreCode_pb:
        return MsgStoreCode_pb(
            sender=self.sender, wasm_byte_code=base64.b64decode(self.wasm_byte_code)
        )

    @classmethod
    def from_proto(cls, proto: MsgStoreCode_pb) -> MsgStoreCode:
        return cls(sender=proto.sender, wasm_byte_code=base64.b64encode(proto.wasm_byte_code).decode())


@attr.s
class MsgMigrateCode(Msg):
    """Upload a new smart contract WASM binary to the blockchain, replacing an existing code ID.
    Can only be called once by creator of the contract, and is used for migrating from Col-4 to Col-5.

    Args:
        sender: address of sender
        code_id: reference to the code on the blockchain
        wasm_byte_code: base64-encoded string containing bytecode
    """

    type_amino = "wasm/MsgMigrateCode"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgMigrateCode"
    """"""
    prototype = MsgMigrateCode_pb
    """"""

    sender: AccAddress = attr.ib()
    code_id: int = attr.ib(converter=int)
    wasm_byte_code: str = attr.ib(converter=str)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "code_id": str(self.code_id),
                "wasm_byte_code": self.wasm_byte_code,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateCode:
        return cls(
            sender=data["sender"],
            code_id=data["code_id"],
            wasm_byte_code=data["wasm_byte_code"],
        )

    def to_proto(self) -> MsgMigrateCode_pb:
        return MsgMigrateCode_pb(
            sender=self.sender, code_id=self.code_id, wasm_byte_code=base64.b64decode(self.wasm_byte_code)
        )

    @classmethod
    def from_proto(cls, proto: MsgMigrateCode_pb) -> MsgMigrateCode:
        return cls(
            sender=proto.sender,
            code_id=proto.code_id,
            wasm_byte_code=base64.b64encode(proto.wasm_byte_code).decode(),
        )


@attr.s
class MsgInstantiateContract(Msg):
    """Creates a new instance of a smart contract from existing code on the blockchain.

    Args:
        sender: address of sender
        admin: address of contract admin
        code_id (int): code ID to use for instantiation
        init_msg (dict|str): InitMsg to initialize contract
        init_coins (Coins): initial amount of coins to be sent to contract
    """

    type_amino = "wasm/MsgInstantiateContract"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgInstantiateContract"
    """"""
    prototype = MsgInstantiateContract_pb
    """"""

    sender: AccAddress = attr.ib()
    admin: Optional[AccAddress] = attr.ib()
    code_id: int = attr.ib(converter=int)
    init_msg: Union[dict, str] = attr.ib()
    init_coins: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "admin": self.admin,
                "code_id": str(self.code_id),
                "init_msg": remove_none(self.init_msg),
                "init_coins": self.init_coins.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgInstantiateContract:
        return cls(
            sender=data.get("sender"),
            admin=data.get("admin"),
            code_id=data["code_id"],
            init_msg=parse_msg(data["init_msg"]),
            init_coins=Coins.from_data(data["init_coins"]),
        )

    def to_proto(self) -> MsgInstantiateContract_pb:
        return MsgInstantiateContract_pb(
            sender=self.sender,
            admin=self.admin,
            code_id=self.code_id,
            init_msg=bytes(json.dumps(self.init_msg), "utf-8"),
            init_coins=self.init_coins.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: MsgInstantiateContract_pb) -> MsgInstantiateContract:
        return cls(
            sender=proto.sender,
            admin=proto.admin,
            code_id=proto.code_id,
            init_msg=parse_msg(proto.init_msg),
            init_coins=Coins.from_proto(proto.init_coins),
        )


@attr.s
class MsgExecuteContract(Msg):
    """Execute a state-mutating function on a smart contract.

    Args:
        sender: address of sender
        contract: address of contract to execute function on
        execute_msg (dict|str): ExecuteMsg to pass
        coins: coins to be sent, if needed by contract to execute.
            Defaults to empty ``Coins()``
    """

    type_amino = "wasm/MsgExecuteContract"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgExecuteContract"
    """"""
    prototype = MsgExecuteContract_pb
    """"""

    sender: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    execute_msg: Union[dict, str] = attr.ib()
    coins: Coins = attr.ib(converter=Coins, factory=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "contract": self.contract,
                "execute_msg": remove_none(self.execute_msg),
                "coins": self.coins.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExecuteContract:
        return cls(
            sender=data["sender"],
            contract=data["contract"],
            execute_msg=parse_msg(data["execute_msg"]),
            coins=Coins.from_data(data["coins"]),
        )

    def to_proto(self) -> MsgExecuteContract_pb:
        return MsgExecuteContract_pb(
            sender=self.sender,
            contract=self.contract,
            execute_msg=bytes(json.dumps(self.execute_msg), "utf-8"),
            coins=self.coins.to_proto(),
        )

    @classmethod
    def from_proto(cls, proto: Any_pb) -> MsgExecuteContract:
        return cls(
            sender=proto.sender,
            contract=proto.contract,
            execute_msg=parse_msg(proto.execute_msg),
            coins=Coins.from_proto(proto.coins),
        )


@attr.s
class MsgMigrateContract(Msg):
    """Migrate the contract to a different code ID.

    Args:
        admin: address of contract admin
        contract: address of contract to migrate
        new_code_id (int): new code ID to migrate to
        migrate_msg (dict|str): MigrateMsg to execute
    """

    type_amino = "wasm/MsgMigrateContract"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgMigrateContract"
    """"""
    prototype = MsgMigrateContract_pb
    """"""

    admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()
    new_code_id: int = attr.ib(converter=int)
    migrate_msg: Union[dict, str] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "admin": self.admin,
                "contract": self.contract,
                "new_code_id": str(self.new_code_id),
                "migrate_msg": remove_none(self.migrate_msg),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgMigrateContract:
        return cls(
            admin=data["admin"],
            contract=data["contract"],
            new_code_id=data["new_code_id"],
            migrate_msg=parse_msg(data["migrate_msg"]),
        )

    def to_proto(self) -> MsgMigrateContract_pb:
        return MsgMigrateContract_pb(
            admin=self.admin,
            contract=self.contract,
            new_code_id=self.new_code_id,
            migrate_msg=bytes(json.dumps(self.migrate_msg), "utf-8"),
        )

    @classmethod
    def from_proto(cls, proto: MsgMigrateContract_pb) -> MsgMigrateContract:
        return cls(
            admin=proto.admin,
            contract=proto.contract,
            new_code_id=proto.new_code_id,
            migrate_msg=parse_msg(proto.migrate_msg),
        )


@attr.s
class MsgUpdateContractAdmin(Msg):
    """Update a smart contract's admin.

    Args:
        admin: address of current admin (sender)
        new_admin: address of new admin
        contract: address of contract to change
    """

    type_amino = "wasm/MsgUpdateContractAdmin"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgUpdateContractAdmin"
    """"""
    prototype = MsgUpdateContractAdmin_pb
    """"""

    admin: AccAddress = attr.ib()
    new_admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "admin": self.admin,
                "new_admin": self.new_admin,
                "contract": self.contract,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgUpdateContractAdmin:
        return cls(
            admin=data["admin"],
            new_admin=data["new_admin"],
            contract=data["contract"],
        )

    def to_proto(self) -> MsgUpdateContractAdmin_pb:
        return MsgUpdateContractAdmin_pb(
            admin=self.admin, new_admin=self.new_admin, contract=self.contract
        )

    @classmethod
    def from_proto(cls, proto: MsgUpdateContractAdmin_pb) -> MsgUpdateContractAdmin:
        return cls(
            admin=proto.admin,
            new_admin=proto.new_admin,
            contract=proto.contract,
        )


@attr.s
class MsgClearContractAdmin(Msg):
    """Clears the contract's admin field.

    Args:
        admin: address of current admin (sender)
        contract: address of contract to change
    """

    type_amino = "wasm/MsgClearContractAdmin"
    """"""
    type_url = "/terra.wasm.v1beta1.MsgClearContractAdmin"
    """"""
    prototype = MsgClearContractAdmin_pb
    """"""

    admin: AccAddress = attr.ib()
    contract: AccAddress = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {"admin": self.admin, "contract": self.contract},
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgClearContractAdmin:
        return cls(
            admin=data["admin"],
            contract=data["contract"],
        )

    def to_proto(self) -> MsgClearContractAdmin_pb:
        return MsgClearContractAdmin_pb(admin=self.admin, contract=self.contract)

    @classmethod
    def from_proto(cls, proto: MsgClearContractAdmin_pb) -> MsgClearContractAdmin:
        return cls(
            admin=proto.admin,
            contract=proto.contract,
        )
