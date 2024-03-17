from invoke import task
import subprocess
import os

if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f.readlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            var, value = line.strip().split("=", 1)
            os.environ.setdefault(var, value)

env = os.environ.copy()

DEFAULT_MACHINE_SOURCE = "ubuntu"
DEFAULT_MACHINE_NAME = "ubuntu-machine"
DEFAULT_MACHINE_INIT_SCRIPT = "init-ubuntu-machine"


def create_machine():
    cmd = f"orb create {env.get('MACHINE_SOURCE', DEFAULT_MACHINE_SOURCE)} {env.get('MACHINE_NAME', DEFAULT_MACHINE_NAME)}"
    return cmd.split(" ")


def init_machine():
    cmd = f"orb -m {env.get('MACHINE_NAME', DEFAULT_MACHINE_NAME)} ./{env.get('MACHINE_INIT_SCRIPT', DEFAULT_MACHINE_INIT_SCRIPT)}"
    return cmd.split(" ")


def setup_machine():
    subprocess.run(create_machine())
    subprocess.run(init_machine())


def destroy_machine():
    cmd = f"orb delete {env.get('MACHINE_NAME', DEFAULT_MACHINE_NAME)} --force"
    subprocess.run(cmd.split(" "))


def start_machine():
    cmd = f"orb start {env.get('MACHINE_NAME', DEFAULT_MACHINE_NAME)}"
    subprocess.run(cmd.split(" "))


def stop_machine():
    cmd = f"orb stop {env.get('MACHINE_NAME', DEFAULT_MACHINE_NAME)}"
    subprocess.run(cmd.split(" "))


@task
def build(context):
    setup_machine()


@task
def destroy(context):
    destroy_machine()


@task
def start(context):
    start_machine()


@task
def stop(context):
    stop_machine()
