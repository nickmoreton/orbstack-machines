from dataclasses import dataclass

import pprint
from re import sub
import subprocess
import json
import tempfile
import os


@dataclass
class Machine:
    name: str
    distro: str = ""
    version: str = ""
    arch: str = ""
    status: str = ""
    exists: bool = ""
    build_vars: str = ""
    init: list[str] = None
    orb_id: str = ""

    @property
    def create_command(self):
        cmd = f"orb create {self.distro} {self.name}"
        return cmd.split(" ")

    @property
    def destroy_command(self):
        cmd = f"orb delete {self.name}"
        return cmd.split(" ")


@dataclass
class Group:
    name: str
    machines: list[Machine]


@dataclass
class OrbManager:
    """Orb class to manage orb machines.

    Only interested in machines in our config file.
    """

    config: dict
    machines: list[Machine] = None

    def __post_init__(self):
        self.machines = self._parse_machines()
        self._update_machines()

    def _parse_machines(self):
        # machine available in config file
        machines = []
        for item in self.config:
            if item.get("machine"):
                machines.append(
                    Machine(
                        name=item.get("machine").get("name"),
                        distro=item.get("machine").get("distro"),
                        version=item.get("machine").get("version"),
                        arch=item.get("machine").get("arch"),
                        build_vars=item.get("machine").get("build_vars"),
                        init=item.get("machine").get("init"),
                    )
                )
        return machines

    def _update_machines(self):
        # only update the machine found in orb

        for machine in self.machines:
            with subprocess.Popen(
                f"orb info {machine.name} -f json".split(" "),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as p:
                response, error = p.communicate()
                if not error:
                    data = json.loads(response)
                    # print(data)
                    if data.get("name") == machine.name:
                        machine.status = data.get("state")
                        machine.exists = "found"
                        machine.orb_id = data.get("id")
                        machine.distro = data.get("image").get("distro")
                        machine.version = data.get("image").get("version")
                        machine.arch = data.get("image").get("arch")
                else:
                    machine.exists = "not found"

    @property
    def get_machine(self, name):
        for machine in self.machines:
            if machine.name == name:
                return machine
        return None

    @property
    def get_all_machines(self):
        return self.machines

    @property
    def get_running_machines(self):
        return [machine for machine in self.machines if machine.status == "running"]

    @property
    def get_stopped_machines(self):
        return [machine for machine in self.machines if machine.status == "stopped"]

    def start_machine(self, name):
        machine = self.get_machine(name)
        if machine:
            cmd = f"orb start {machine.name}"
            subprocess.run(cmd.split(" "))
        else:
            print(f"Machine {name} not found")

    def stop_machine(self, name):
        machine = self.get_machine(name)
        if machine:
            cmd = f"orb stop {machine.name}"
            subprocess.run(cmd.split(" "))
        else:
            print(f"Machine {name} not found")


    def create_machine(self, name, distro, version, arch, vars, init):
        arch = "" if not arch else f"--arch {arch}"
        distro = f"{distro}" if not version else f"{distro}:{version}"
        cmd = f"orb create {distro} {name} {arch}"
        subprocess.run(cmd, shell=True)
        
        # load init and write to a temporary file
        if init:
            if not vars:
                vars = ""
            init = init.replace("{{ build_vars }}", vars)

            tmp_file = tempfile.NamedTemporaryFile()
            with open(tmp_file.name, "w") as f:
                f.write(init)
                        
            cmd = f"orb push -m {name} {tmp_file.name} /tmp/init.sh"
            subprocess.run(cmd, shell=True)
            subprocess.run(f"orb -m {name} sh /tmp/init.sh -a", shell=True)
            print(f"Machine {name} created successfully")
            print(f"{vars}")
            

    def destroy_machine(self, name):
        cmd = f"orb delete {name} -f"
        subprocess.run(cmd.split(" "))

    def build_machines_for_group(self, group):
        print(f"Building machines for group {group.name}")
        for machine in group.machines:
            if machine.exists == "not found":
                self.create_machine(machine.name, machine.distro, machine.version, machine.arch, machine.build_vars, machine.init)
            else:
                print(f"Machine {machine.name} already exists")

    def destroy_machines_for_group(self, group):
        print(f"Destroying machines for group {group.name}")
        for machine in group.machines:
            if machine.exists == "found":
                # print(f"Deleting machine {machine.name}")
                self.destroy_machine(machine.name)
            else:
                print(f"Machine {machine.name} not found")


@dataclass
class UiManager:
    orb_manager: OrbManager
    groups: list[Group] = None

    def __post_init__(self):
        self.machines = self._parse_machines()
        self.groups = self._parse_groups()

    def _parse_groups(self):
        groups = []

        for item in self.orb_manager.config:
            if item.get("group"):  # ignore the machines here
                group = Group(item.get("group").get("name"), [])
                for machine in self.orb_manager.machines:
                    if machine.name in item.get("group").get("machines"):
                        group.machines.append(machine)
                groups.append(group)
        return groups

    def _parse_machines(self):
        machines = []
        for item in self.orb_manager.config:
            if item.get("machine"):  # ignore the groups here
                machines.append(
                    Machine(
                        name=item.get("machine").get("name"),
                        distro=item.get("machine").get("distro"),
                        version=item.get("machine").get("version"),
                        arch=item.get("machine").get("arch"),
                        build_vars=item.get("machine").get("build_vars"),
                        init=item.get("machine").get("init"),
                    )
                )
        return machines

    def list_groups(self):
        for i, group in enumerate(self.groups, start=1):
            print(f"[{i}] {group.name}")
            print("--- Machines ---")
            for machine in group.machines:
                print(f"    {machine.name}")
            print()

    def list_machines(self):
        for i, machine in enumerate(self.machines):
            print(
                f"[{i}] {machine.name}-{machine.distro} | {machine.status} | {machine.exists}"
            )

    def status(self):
        print("Orb Status")
        print("-----------")
        print(f"Total Machines: {len(self.orb_manager.machines)}")
        print(f"Running Machines: {len(self.orb_manager.get_running_machines)}")
        print(f"Stopped Machines: {len(self.orb_manager.get_stopped_machines)}")

    def info(self):
        for machine in self.orb_manager.machines:
            print(f"Machine: {machine.name}")
            print(f"Status: {machine.status}")
            print(f"Exists: {machine.exists}")
            print(f"Orb ID: {machine.orb_id}")
            print(f"Distro: {machine.distro}")
            print(f"Version: {machine.version}")
            print(f"Arch: {machine.arch}")
            print(f"Init: {machine.init}")
            print(f"Env: {machine.env}")
            print()
