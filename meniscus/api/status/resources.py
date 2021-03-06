"""
The Status Resources module provides RESTful operations for managing
Worker status.  This includes the updating of a worker's status as well as the
retrieval of the status of a specified worker node, or all workers.
"""
import falcon

from meniscus import api
from meniscus.api.validator_init import get_validator
from meniscus.data.model.worker import SystemInfo
from meniscus.data.model import worker_util
from meniscus.data.model.worker import Worker


class WorkerStatusResource(api.ApiResource):
    """
    A resource for updating and retrieving data for a single worker node
    """

    @api.handle_api_exception(operation_name='WorkerStatus PUT')
    @falcon.before(get_validator('worker_status'))
    def on_put(self, req, resp, hostname, validated_body):
        """
        updates a worker's status or creates a new worker entry if not found
        """

        #load validated json payload in body
        body = validated_body['worker_status']

        #find the worker in db
        worker = worker_util.find_worker(hostname)

        if worker is None:
            #instantiate new worker object
            new_worker = Worker(**body)
            #persist the new worker
            worker_util.create_worker(new_worker)
            resp.status = falcon.HTTP_202
            return

        if 'status' in body:
            worker.status = body['status']

        if 'system_info' in body:
            worker.system_info = SystemInfo(**body['system_info'])

        worker_util.save_worker(worker)
        resp.status = falcon.HTTP_200

    @api.handle_api_exception(operation_name='WorkerStatus GET')
    def on_get(self, req, resp, hostname):
        """
        Retrieve the status of a specified worker node
        """
        #find the worker in db
        worker = worker_util.find_worker(hostname)

        if worker is None:
            api.abort(falcon.HTTP_404, 'Unable to locate worker.')

        resp.status = falcon.HTTP_200
        resp.body = api.format_response_body({'status': worker.get_status()})


class WorkersStatusResource(api.ApiResource):
    """
    A resource for retrieving data about all worker nodes in a meniscus cluster
    """

    @api.handle_api_exception(operation_name='WorkersStatus GET')
    def on_get(self, req, resp):
        """
        Retrieve the status of all workers in the meniscus cluster
        """

        workers = worker_util.retrieve_all_workers()

        workers_status = [
            worker.get_status()
            for worker in workers]

        resp.status = falcon.HTTP_200
        resp.body = api.format_response_body({'status': workers_status})
