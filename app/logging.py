from fastapi import Depends

from app.database import get_session
from .models import Trace
from colorama import Fore # type: ignore
import logging

FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
from sqlalchemy.orm import Session

# Logs both to the console and
# As the simulation proceeds, create entries in the 'Trace' file which can be accesed via an endpoint

def report(level, simulation_id, message, db: Session):
    """
    Prints a message on the terminal (or other output if designated).  
    Exports it to the Trace database.  

        Level: depth within the simulation.  
        Simulation_id - which simulation this refers to.  

    Does not commit the change. Assumes this will be done by the caller.
    """
    match level:
        case 1:
            colour = Fore.YELLOW
        case 2:
            colour = Fore.RED
        case 3:
            colour = Fore.GREEN
        case 4:
            colour= Fore.BLUE
        case 5:
            colour=Fore.LIGHTRED_EX

    user_message = " " * level + f"Level {level}: {message}"
    log_message = " " * level+colour + message + Fore.WHITE
    # logging.info(log_message)
    entry = Trace(
        simulation_id=simulation_id,
        level=level,
        time_stamp=1,
        message=user_message,
    )
    db.add(entry)
    # db.commit()
