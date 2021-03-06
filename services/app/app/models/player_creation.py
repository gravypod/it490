import pprint
from app.models.login import Login  # noqa: F401,E501


class PlayerCreation(dict):
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
        'username': 'str',
        'password': 'str',
        'location_name': 'str'
    }

    attribute_map = {
        'username': 'username',
        'password': 'password',
        'location_name': 'locationName'
    }

    def __init__(self, username=None, password=None, location_name=None):  # noqa: E501
        """PlayerCreation - a model defined in Swagger"""  # noqa: E501

        self._username = None
        self._password = None
        self._location_name = None
        self.discriminator = None

        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if location_name is not None:
            self.location_name = location_name

    @property
    def username(self):
        """Gets the username of this Login.  # noqa: E501


        :return: The username of this Login.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this Login.


        :param username: The username of this Login.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this Login.  # noqa: E501


        :return: The password of this Login.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this Login.


        :param password: The password of this Login.  # noqa: E501
        :type: str
        """
        if password is not None and len(password) > 127:
            raise ValueError("Invalid value for `password`, length must be less than or equal to `127`")  # noqa: E501
        if password is not None and len(password) < 0:
            raise ValueError("Invalid value for `password`, length must be greater than or equal to `0`")  # noqa: E501

        self._password = password

    @property
    def location_name(self):
        """Gets the location_name of this PlayerCreation.  # noqa: E501

        Name of the location the user is in  # noqa: E501

        :return: The location_name of this PlayerCreation.  # noqa: E501
        :rtype: str
        """
        return self._location_name

    @location_name.setter
    def location_name(self, location_name):
        """Sets the location_name of this PlayerCreation.

        Name of the location the user is in  # noqa: E501

        :param location_name: The location_name of this PlayerCreation.  # noqa: E501
        :type: str
        """

        self._location_name = location_name

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
        if issubclass(PlayerCreation, dict):
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
        if not isinstance(other, PlayerCreation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
