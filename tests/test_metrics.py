import sys, json, unittest, re, time
import librato
from mock_connection import MockRequest

librato.connection.requests = MockRequest()

"""tell me if two dics have the same contents """
def dicts_match(x, truth):
  shared_items              = set(x.items()) & set(truth.items())
  same_length               = len(x) == len(truth)
  same_overlap_shared_items = len(shared_items) == len(truth)
  if same_length and same_overlap_shared_items:
    return True
  else:
    print "--x:     "; print json.dumps(x)
    print "--truth: "; print json.dumps(truth)
    return False


class TestMetrics(unittest.TestCase):
  def setUp(self):
    self.api = librato.Connection('drio', 'abcdef')
    self.my_gauge = librato.Gauge(self.api, name='home_temp', description='Temp. at home')

    # Create a metric(gauge) and add a couple of measurements
    self.now = 1356802172
    g = self.my_gauge
    g.add(20.2, source="upstairs")
    g.add(20.0, name="dummy", source="downstairs", measure_time=self.now)

    # Load truth for some POST requests
    fd                = open("tests/fixtures/post_measurements_1.json")
    self.truth_post_1 = json.loads(fd.read())['gauges']
    fd.close()
    # TODO: try counters ...

  def tearDown(self):
    pass

  def test_add_measurements(self):
    g = self.my_gauge
    m = g.measurements # measurements
    truth = self.truth_post_1

    assert len(g.measurements) == 2
    assert dicts_match(truth[0], m[0].__dict__)
    assert dicts_match(truth[1], m[1].__dict__)

  def test_checking_type_of_metric(self):
    g = self.my_gauge
    assert g.what_type() == 'gauges'

  def test_submit_measurements(self):
    g = self.my_gauge
    g.submit()

    assert g.payload.has_key('gauges')
    m = g.payload['gauges'] # the measurements
    assert len(m) == 2

    # contents
    truth = self.truth_post_1
    assert dicts_match(m[0], truth[0])
    assert dicts_match(m[1], truth[1])