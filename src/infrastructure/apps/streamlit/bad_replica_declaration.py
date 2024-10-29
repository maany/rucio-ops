import streamlit as st
from rucio.common.types import InternalScope, InternalAccount
from rucio.core import replica
import pandas as pd
from core.entity import BadReplicaDeclaration
import logging
import pandas as pd
import threading
from queue import Queue
import datetime
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel

st.title("# SEAL - Bad replica declaration Monitor")
st.write("## This app is used to declare bad replicas in SEAL")


