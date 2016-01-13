import endpoints

from progress.api import ProgressApi

APPLICATION = endpoints.api_server([ProgressApi], restricted=False)
