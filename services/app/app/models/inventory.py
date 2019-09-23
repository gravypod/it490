import pprint

from app.models.item_stack import ItemStack  # noqa: F401,E501


class Inventory(object):
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
        'id': 'str',
        'player_id': 'str',
        'item_stacks': 'list[ItemStack]'
    }

    attribute_map = {
        'id': 'id',
        'player_id': 'playerId',
        'item_stacks': 'itemStacks'
    }

    def __init__(self, id=None, player_id=None, item_stacks=None):  # noqa: E501
        """Inventory - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._player_id = None
        self._item_stacks = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if player_id is not None:
            self.player_id = player_id
        if item_stacks is not None:
            self.item_stacks = item_stacks

    @property
    def id(self):
        """Gets the id of this Inventory.  # noqa: E501

        ID of this inventory  # noqa: E501

        :return: The id of this Inventory.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Inventory.

        ID of this inventory  # noqa: E501

        :param id: The id of this Inventory.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def player_id(self):
        """Gets the player_id of this Inventory.  # noqa: E501

        Player that owns this inventory.  # noqa: E501

        :return: The player_id of this Inventory.  # noqa: E501
        :rtype: str
        """
        return self._player_id

    @player_id.setter
    def player_id(self, player_id):
        """Sets the player_id of this Inventory.

        Player that owns this inventory.  # noqa: E501

        :param player_id: The player_id of this Inventory.  # noqa: E501
        :type: str
        """

        self._player_id = player_id

    @property
    def item_stacks(self):
        """Gets the item_stacks of this Inventory.  # noqa: E501


        :return: The item_stacks of this Inventory.  # noqa: E501
        :rtype: list[ItemStack]
        """
        return self._item_stacks

    @item_stacks.setter
    def item_stacks(self, item_stacks):
        """Sets the item_stacks of this Inventory.


        :param item_stacks: The item_stacks of this Inventory.  # noqa: E501
        :type: list[ItemStack]
        """

        self._item_stacks = item_stacks

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
        if issubclass(Inventory, dict):
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
        if not isinstance(other, Inventory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other