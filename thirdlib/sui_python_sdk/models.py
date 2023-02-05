from typing import Optional, Union, List, Any


class Tx:
    pass


class TransferObjectTransaction(Tx):
    def __init__(self,
                 object_id: str,
                 recipient: str,
                 gas_budget: int,
                 gas_payment: Optional[str] = None):
        self.object_id = object_id
        self.gas_payment = gas_payment
        self.gas_budget = gas_budget
        self.recipient = recipient


class TransferSuiTransaction(Tx):
    def __init__(self,
                 sui_object_id: str,
                 recipient: str,
                 gas_budget: int,
                 amount: Optional[int] = None):
        self.sui_object_id = sui_object_id
        self.recipient = recipient
        self.gas_budget = gas_budget
        self.amount = amount


class MoveCallTransaction(Tx):
    def __init__(self,
                 package_object_id: str,
                 module: str,
                 function: str,
                 type_arguments: Union[List[str], List[Any]],
                 arguments: List[Union[bool, int, str, List[Any]]],
                 gas_budget: int,
                 gas_payment: Optional[str] = None):
        self.package_object_id = package_object_id
        self.module = module
        self.function = function
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.gas_budget = gas_budget
        self.gas_payment = gas_payment
