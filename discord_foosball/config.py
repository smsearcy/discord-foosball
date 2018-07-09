from dotenv import load_dotenv
import environ

__all__ = ['config']


@environ.config(prefix='DISCORD')
class AppConfig:
    # this is overkill for this application but I wanted to test it out
    token = environ.var()
    command_prefix = environ.var(default='!')


load_dotenv()
config = environ.to_config(AppConfig)
