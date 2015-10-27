import os
from datetime import datetime, time

def execute(time, typename):
    alter = """sed -i "/%s/c $(sed -n '/%s/p' ~/content.txt | sed 's/[0-9]\+/%s/')" ~/content.txt"""%(typename, typename, time)
    print alter
    os.system(alter)
