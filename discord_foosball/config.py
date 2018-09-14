from dotenv import load_dotenv
import environ

__all__ = ['config']


@environ.config(prefix='DISCORD')
class AppConfig:
    # this is overkill for this application but I wanted to test it out
    token = environ.var()
    command_prefix = environ.var(default='!')
    roll_timeout = environ.var(default=180, converter=int)


print('Loading environment configuration...')
load_dotenv()
config: AppConfig = environ.to_config(AppConfig)
