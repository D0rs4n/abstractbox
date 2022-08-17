# Copyright 2022-present D0rs4n
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import nox
from nox import options

PATH_TO_PROJECT = os.path.join(".", "abstractbox")
SCRIPT_PATHS = [
    PATH_TO_PROJECT,
    "noxfile.py",
]

options.sessions = ["format_fix", "mypy"]


@nox.session()
def format_fix(session: nox.Session):
    session.install("black")
    session.install("isort")
    session.run("python", "-m", "black", *SCRIPT_PATHS)
    session.run("python", "-m", "isort", *SCRIPT_PATHS)


# noinspection PyShadowingBuiltins
@nox.session()
def format(session: nox.Session):
    session.install("-U", "black")
    session.run("python", "-m", "black", *SCRIPT_PATHS, "--check")


@nox.session()
def mypy(session: nox.Session):
    session.run("poetry", "config", "virtualenvs.create", "false", external=True)
    session.run("poetry", "install", "-n", "--no-dev", external=True, silent=True)
    session.run("poetry", "config", "virtualenvs.create", "true", external=True)
    session.install("-U", "mypy")
    session.run("python", "-m", "mypy", PATH_TO_PROJECT)
