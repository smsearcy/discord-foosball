from dotenv import load_dotenv
import environ

__all__ = ['config']


@environ.config(prefix='DISCORD')
class AppConfig:
    token = environ.var()


load_dotenv()
config = environ.to_config(AppConfig)
