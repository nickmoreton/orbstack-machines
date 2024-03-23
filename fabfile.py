from invoke import task
import yaml

from orb.models import OrbManager, UiManager


config = yaml.safe_load(open("config.yaml"))
orb_manager = OrbManager(config)
ui_manager = UiManager(orb_manager)


@task
def build(c):
    ui_manager.list_groups()

    group_index = input("Enter group index: ")
    if not group_index.isdigit():
        print("Invalid index")
        return

    group_index = int(group_index) - 1  # convert to 0-based index

    group = ui_manager.groups[int(group_index)]
    print(f"You have selected: {group.name}")

    build = input("Do you want to continue? (y/n): ")
    if build.lower() != "y":
        return

    orb_manager.build_machines_for_group(group)


@task
def destroy(c):
    ui_manager.list_groups()

    group_index = input("Enter group index: ")
    if not group_index.isdigit():
        print("Invalid index")
        return

    group_index = int(group_index) - 1  # convert to 0-based index

    group = ui_manager.groups[int(group_index)]
    print(f"You have selected: {group.name}")

    destroy = input("Do you want to continue? (y/n): ")
    if destroy.lower() != "y":
        return

    orb_manager.destroy_machines_for_group(group)


@task
def status(c):
    ui_manager.status()


@task
def info(c):
    ui_manager.info()
