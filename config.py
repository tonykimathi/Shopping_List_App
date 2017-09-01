class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True



class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}