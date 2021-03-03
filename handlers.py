import kopf
import kubernetes
import yaml
import os
import requests
import json
import time
from datetime import datetime, timedelta
from kubernetes.client.rest import ApiException

#@kopf.on.startup()
#def configure(settings: kopf.OperatorSettings, **_):
#    settings.posting.level = logging.WARNING
#    settings.watching.connect_timeout = 1 * 60
#    settings.watching.server_timeout = 10 * 60

@kopf.on.create('jbaldwin.org', 'v1', 'elevatepermissions')
def create_fn(meta, spec, namespace, logger, body, **kwargs):
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']

    # check if servicenow has an open incident for this - this needs testing!
    # https://gallery.technet.microsoft.com/scriptcenter/Get-all-open-ServiceNow-16142d9a
    servicenow_url = "https://myservicenow.ruffer.local/"
    servicenow_inc = "INC1234567"
    get_servicenow_incident_url = servicenow_url + "/api/now/v1/table/incident?sysparm_query=number=" + servicenow_inc
    #get_servicenow_incident_response = requests.get(get_servicenow_incident_url, auth=('myusername', 'mybasicpass'))
    #if get_servicenow_incident_response.status_code != 200:
    #    logger.error("Failed to retrieve ServiceNow Inc")
    #    exit
    
    #json_data = json.loads(get_servicenow_incident_response.json())
    #if json_data['active'] != "true":
    #    logger.error()
    #https://stackoverflow.com/questions/35283649/error-in-creating-an-incident-in-servicenow


    batch_api = kubernetes.client.BatchV1beta1Api()
    #cron_job = batch_api.create_namespaced_cron_job(body=data, namespace=namespace)
    #kopf.adopt(cron_job, owner=body)
    #logger.info(f"asdasdasd: %s", cron_job)

    # create role (one-off setup per namespace)
    path = os.path.join(os.path.dirname(__file__), '/templates/role.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(namespace="default")
    data = yaml.safe_load(text)
    batch_api = kubernetes.client.RbacAuthorizationV1Api()
    try:
        batch_api.create_namespaced_role(body=data, namespace=namespace)
    except ApiException as e:
        if (e.status == 409): # conflict
            logger.debug("Role has already been created in this namespace, handling this exception...")

    # create rolebinding to elevate user's permissions
    path = os.path.join(os.path.dirname(__file__), '/templates/rolebinding.yaml')
    tmpl = open(path, 'rt').read()
    now=int(datetime.timestamp(datetime.now()))
    expiry=int(datetime.timestamp(datetime.now() + timedelta(hours=body['spec']['lease-hours'])))
    incident_ticket=body['spec']['incident-ticket']
    rb_name = "kube-elevate-rb-readwrite-" + body['spec']['incident-ticket'] + "-" + str(int(time.time()))
    text = tmpl.format(user=body['spec']['username'], 
                       namespace=body['spec']['username'], 
                       expirytime=expiry, 
                       rolebindingname=rb_name)
    rb = yaml.safe_load(text)
    kopf.adopt(rb, owner=body)
    roleBinding = batch_api.create_namespaced_role_binding(body=rb, namespace=namespace)
    return {'message': 'Rolebinding created'}

@kopf.on.delete('jbaldwin.org', 'v1', 'elevatepermissions')
def delete(body, **kwargs):
    msg = f"Database {body['metadata']['name']} and its Pod / Service children deleted"
    return {'message': msg}