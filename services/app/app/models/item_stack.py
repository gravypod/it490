import pprint

from app.models.item import Item  # noqa: F401,E501


class ItemStack(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'item': 'Item',
        'quantity': 'int'
    }

    attribute_map = {
        'item': 'item',
        'quantity': 'quantity'
    }

    def __init__(self, item=None, quantity=None):  # noqa: E501
        """ItemStack - a model defined in Swagger"""  # noqa: E501

        self._item = None
        self._quantity = None
        self.discriminator = None

        if item is not None:
            self.item = item
        if quantity is not None:
            self.quantity = quantity

    @property
    def item(self):
        """Gets the item of this ItemStack.  # noqa: E501


        :return: The item of this ItemStack.  # noqa: E501
        :rtype: Item
        """
        return self._item

    @item.setter
    def item(self, item):
        """Sets the item of this ItemStack.


        :param item: The item of this ItemStack.  # noqa: E501
        :type: Item
        """

        self._item = item

    @property
    def quantity(self):
        """Gets the quantity of this ItemStack.  # noqa: E501


        :return: The quantity of this ItemStack.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this ItemStack.


        :param quantity: The quantity of this ItemStack.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.swagger_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ItemStack, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ItemStack):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other