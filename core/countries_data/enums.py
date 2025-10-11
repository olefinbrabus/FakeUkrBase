from enum import Enum


class ExtendedPaymentCardBrand(str, Enum):

    amex = 'American Express'
    mastercard = 'Mastercard'
    visa = 'Visa'
    mir = 'Mir'
    maestro = 'Maestro'
    discover = 'Discover'
    verve = 'Verve'
    dankort = 'Dankort'
    troy = 'Troy'
    unionpay = 'UnionPay'
    jcb = 'JCB'
    diners_club = 'Diners Club'
    other = 'other'
    """They were taken by [`PaymentCardBrand`][pydantic_extra_types.payment.PaymentCardBrand]."""
    prostir = 'Prostir'


    def __str__(self) -> str:
        return self.value

class TypeCreditCard(str, Enum):
    credit = 'credit'
    debit = 'debit'

    def __str__(self) -> str:
        return self.value