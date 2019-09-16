FROM rabbitmq:3.7.17-management

# development login credentials
ENV RABBITMQ_DEFAULT_USER=root \
    RABBITMQ_DEFAULT_PASS=root

# Enable plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management

