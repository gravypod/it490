import pprint

from app.models.ability import Ability  # noqa: F401,E501
from app.models.attribute import Attribute  # noqa: F401,E501


class Stats(object):
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
        'abilities': 'list[Ability]',
        'attributes': 'list[Attribute]',
        'level': 'int'
    }

    attribute_map = {
        'abilities': 'abilities',
        'attributes': 'attributes',
        'level': 'level'
    }

    def __init__(self, abilities=None, attributes=None, level=None):  # noqa: E501
        """Stats - a model defined in Swagger"""  # noqa: E501

        self._abilities = None
        self._attributes = None
        self._level = None
        self.discriminator = None

        if abilities is not None:
            self.abilities = abilities
        if attributes is not None:
            self.attributes = attributes
        if level is not None:
            self.level = level

    @property
    def abilities(self):
        """Gets the abilities of this Stats.  # noqa: E501


        :return: The abilities of this Stats.  # noqa: E501
        :rtype: list[Ability]
        """
        return self._abilities

    @abilities.setter
    def abilities(self, abilities):
        """Sets the abilities of this Stats.


        :param abilities: The abilities of this Stats.  # noqa: E501
        :type: list[Ability]
        """

        self._abilities = abilities

    @property
    def attributes(self):
        """Gets the attributes of this Stats.  # noqa: E501


        :return: The attributes of this Stats.  # noqa: E501
        :rtype: list[Attribute]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this Stats.


        :param attributes: The attributes of this Stats.  # noqa: E501
        :type: list[Attribute]
        """

        self._attributes = attributes

    @property
    def level(self):
        """Gets the level of this Stats.  # noqa: E501


        :return: The level of this Stats.  # noqa: E501
        :rtype: int
        """
        return self._level

    @level.setter
    def level(self, level):
        """Sets the level of this Stats.


        :param level: The level of this Stats.  # noqa: E501
        :type: int
        """
        if level is not None and level > 100:  # noqa: E501
            raise ValueError("Invalid value for `level`, must be a value less than or equal to `100`")  # noqa: E501
        if level is not None and level < 0:  # noqa: E501
            raise ValueError("Invalid value for `level`, must be a value greater than or equal to `0`")  # noqa: E501

        self._level = level

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
        if issubclass(Stats, dict):
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
        if not isinstance(other, Stats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other