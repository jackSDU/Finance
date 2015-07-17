#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Finance.settings")

    from multiprocessing import Process,freeze_support
    from Main import client
    #freeze_support()

    p=Process(name="daemon",target=client.daemon,args=(client.rcon,))
    p.daemon=True
    p.start()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
