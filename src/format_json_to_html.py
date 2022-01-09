""" Utility script to convert describe change set json results to HTML formatted table """
import json
import sys

DEFAULT = "-"


class ChangeSet:
    """ Change Set structure"""
    changes = None

    def __init__(self, changes):
        """ Constructor """
        self.changes = changes

    def action(self):
        """ Return Image placeholder and action"""
        action = self.changes['ResourceChange']['Action']
        color = ""
        if self.changes['ResourceChange']['Action'] == "Modify":
            color = "<img src=\"https://via.placeholder.com//12/0073bb/0073bb?text=+\" />"
        elif self.changes['ResourceChange']['Action'] == "Add":
            color = "<img src=\"https://via.placeholder.com//12/1d8102/1d8102?text=+\" />"
        elif self.changes['ResourceChange']['Action'] == "Remove":
            color = "<img src=\"https://via.placeholder.com/12/d13212/d13212?text=+\" />"
        return f"{color} {action}"

    def logical_resource_id(self):
        """ Return logical resource id"""
        return self.changes['ResourceChange']['LogicalResourceId']

    def physical_resource_id(self):
        """ Return physical resource id """
        resource_id = DEFAULT
        if 'PhysicalResourceId' in self.changes['ResourceChange']:
            resource_id = self.changes['ResourceChange']['PhysicalResourceId']
        return resource_id

    def resource_type(self):
        """ Return resource type """
        return self.changes['ResourceChange']['ResourceType']

    def replacement(self):
        """ is Replacement """
        replaced = DEFAULT
        if 'Replacement' in self.changes['ResourceChange']:
            replaced = self.changes['ResourceChange']['Replacement']
        return replaced

    def details(self):
        """ Returns details of change set"""
        arr = []
        for detail in self.changes['ResourceChange']['Details']:
            if detail['Target']['Attribute'] != 'Properties':
                continue
            arr.append(f"- {detail['Target']['Name']}")
        return "<br>".join(arr)


def execute(stack, change_set_path, env):
    """ Execute Processing """
    with open(change_set_path, 'rb') as file:
        data = json.load(file)

    if env:
        body = f"<h1>Change Set for {env}</h1>"
    else:
        body = "<h1>Change Set</h1>"

    body += f"<h2>Stack Name: {stack}</h2><br>"

    if data['Changes']:
        body += "<table><tr><th>Action&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>" \
                "<th>Logical ID</th><th>Physical " \
                "Resource ID</th><th>Type</th><th>Replacement</th><th>Changed Properties</th></tr> "
        for change in data['Changes']:
            body += "<tr>"
            change_set = ChangeSet(change)
            body += f"<td>{change_set.action()}</td>"
            body += f"<td>{change_set.logical_resource_id()}</td>"
            body += f"<td>{change_set.physical_resource_id()}</td>"
            body += f"<td>{change_set.resource_type()}</td>"
            body += f"<td>{change_set.replacement()}</td>"
            body += f"<td>{change_set.details()}</td>"
            body += "</tr>"
        body += "</table>"
    else:
        body += "no change."

    return body


if __name__ == '__main__':
    print(execute(sys.argv[1], sys.argv[2], sys.argv[3]))
