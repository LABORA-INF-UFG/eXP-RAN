import os
import gdown

id = "1S7OwQZEvCwPEQxL7dm7Zz14YN1bOo2mX"
gdown.download(id=id, output='expran.zip', quiet=False)

os.system("unzip expran.zip && rm expran.zip")