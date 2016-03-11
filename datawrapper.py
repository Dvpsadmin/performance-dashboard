import codecs
import datetime as dt
from datetime import timedelta
import logging

from serverdensity.wrapper import Device
from serverdensity.wrapper import Tag
from serverdensity.wrapper import Metrics


# summing lists map(sum, izip(a,b))

class DataWrapper(object):

    def __init__(self, token, conf):
        self.token = token
        self.conf = conf
        self.historic_data = None

        self.device = Device(self.token)
        self.tag = Tag(self.token)
        self.metrics = Metrics(self.token)

        self._validation()
        self._load_historic_data()

    def _validation(self):
        """Check the following
        - metric for every piece in infrastructure
        -
        """

    def _get_devices(self, infra_conf):
        """Takes the configuration part for each infrastructure"""
        raw_devices = self.device.list()

        if infra_conf.get('tag'):
            tags = self.tag.list()
            tag_id =[tag['_id'] for tag in tags if tag['name'] == infra_conf['tag']]
            if not tag_id:
                available_tags = '\n'.join(list(set([tag['name'] for tag in tags])))
                message = 'There is no tag with the name "{}". Try one of these: \n{}'.format(infra_conf['tag'], available_tags)
                raise Exception(message)
            else:
                tag_id = tag_id[0]

            devices = [device for device in raw_devices if tag_id in device.get('tags')]
            if not devices:
                available_tags = '\n'.join(list(set([tag['name'] for tag in tags])))
                raise Exception('There is no device with this tag name. Try one of these: \n{}'.format(available_tags))
        elif infra_conf.get('group'):
            group = infra_conf.get('group')
            devices = [device for device in raw_devices if group == device.get('group')]
            if not devices:
                groups = set([device['group'] for device in raw_devices
                             if not device['group'] is None])
                groups = '\n'.join(list(groups))
                raise Exception('There is no device with this group name. The following groups are available:\n {}'.format(groups))
        else:
            raise Exception('You have to provide either group or tag for each part of your infrastructure.')
        return devices

    def _get_metrics(self, metric, devices):
        """For all devices associated with the group or device"""
        metric = metric.split('.')
        metric_filter = self.metric_filter(metric)
        end = dt.datetime.now()
        start = end - timedelta(hours=24)
        data_entries = []
        for device in devices:
            data = self.metrics.get(device['_id'], start, end, metric_filter)
            data = self._data_node(data)
            if data['data']:
                data_entries.append(data)
        if not data_entries:
            metric = '.'.join(metric)
            # Append zero data to avoid zerodivison error
            data_entries.append({'data': [{'x': 0, 'y': 0}]})
            logging.warning('No server in this group has any data on {}'.format(metric))
        return data_entries

    def _data_node(self, data, names=None):
        """Inputs the data from the metrics endpoints and returns
        the node that has contains the data + names of the metrics."""

        if not names:
            names = []
        for d in data:
            if d.get('data') or d.get('data') == []:
                names.append(d.get('name'))
                d['full_name'] = names
                return d
            else:
                names.append(d.get('name'))
                return self._data_node(d.get('tree'), names)

    def _get_data_points(self, data_entries):
        data_points = []
        for data in data_entries:
            points = [point['y'] for point in data['data']]
            data_points += points
        return data_points

    def _round(self, number):
        if number < 1:
            return round(number, self.conf['general'].get('round', 2))
        else:
            return int(round(number, 0))

    def calc_average(self, data_entries):
        data_points = self._get_data_points(data_entries)
        return self._round(sum(data_points)/len(data_points))

    def calc_max(self, data_entries):
        data_points = self._get_data_points(data_entries)
        return self._round(max(data_points))

    def calc_min(self, data_entries):
        return self._round(min(self._get_data_points(data_entries)))

    def calc_median(self, data_entries):
        data_points = self._get_data_points(data_entries)
        data_points.sort()
        start = len(data_points) // 2.0
        if len(data_points) % 2 > 0:
            result = (data_points[start] + data_points[start+1]) / 2.0
        else:
            result = self._round(data_points[start] // 2.0)
        return result

    def calc_sum(self, data_entries):
        return self._round(sum(self._get_data_points(data_entries)))

    def calc_raw_average(self, data_entries):
        pass

    def gather_data(self):
        infrastructure = self.conf['infrastructure']
        for infra_conf in infrastructure:
            devices = self._get_devices(infra_conf)
            for metric_conf in infra_conf['metrics']:
                metric = metric_conf['metrickey']
                data_entries = self._get_metrics(metric, devices)
                for method in metric_conf['calculation']:
                    result = getattr(self, 'calc_{}'.format(method))(data_entries)
                    metric_conf['{}_stat'.format(method)] = result
        return self.conf



    def _load_historic_data(self):
        pass

    def metric_filter(self, metrics, filter=None):
        """from a list of metrics ie ['cpuStats', 'CPUs', 'usr'] it constructs
        a dictionary that can be sent to the metrics endpoint for consumption"""

        metrics = list(metrics)
        if not filter:
            filter = {}
            filter[metrics.pop()] = 'all'
            return self.metric_filter(metrics, filter)
        else:
            try:
                metric = metrics.pop()
                dic = {metric: filter}
                return self.metric_filter(metrics, dic)
            except IndexError:
                return filter

    def available(self):
        """Assumes that all metrics are the same for a group or a tag"""
        infrastructure = self.conf['infrastructure']
        md = '# Available metrics for all your groups\n\n'

        for infra_conf in infrastructure:
            devices = self._get_devices(infra_conf)
            device = devices[0]
            end = dt.datetime.now()
            start = end - timedelta(hours=2)
            available = self.metrics.available(device['_id'], start, end)
            metrics = self.flatten(available)
            try:
                md += '##{}\n'.format(infra_conf['title'])
            except KeyError:
                raise KeyError('Each section need a title, go on fill one in and try again.')
            for metric in metrics:
                title = ' '.join([tup[0] for tup in metric])
                metric = '.'.join([tup[1] for tup in metric])
                entry = '###{}\nmetrickey: {}\n\n'.format(title, metric)
                md += entry
        with codecs.open('available.md', 'w') as f:
            f.write(md)


    def flatten(self, lst):
        """Get all the keys when calling available"""
        for dct in lst:
            key = dct['key']
            name = dct['name']
            if 'tree' not in dct:
                yield [(name, key)]  # base case
            else:
                for result in self.flatten(dct["tree"]):  # recursive case
                    yield [(name, key)] + result

