# Simple PagerDuty CLI

There's a [go-pagerduty](https://github.com/PagerDuty/go-pagerduty), but, I don't really like it. I just wanted something simple to keep from needing that browser tab/window open while on call.

The `pagerduty-cli.py` script is basically just using `requests` and the [PagerDuty v2 REST API](https://v2.developer.pagerduty.com/v2/page/api-reference#!/Incidents/get\_incidents).

All you need is the stuff in `requirements.txt` and a couple of environment variables.

The stuff below uses Python Virtualenv, but on my laptop I just installed the packages at the system-level.

```bash
$ env | grep PAGERDUTY
PAGERDUTY_USERID=P46... # find it in PD (check the url after you log in, look for something like assignedToUser=P46...
PAGERDUTY_APIKEY=aCG...

$ virtualenv venv # or not, if you are okay with installing the package system-wide

$ source venv/bin/activate # or not, if you are okay with installing the package system-wide

$ pip install -r requirements.txt

$ ln -s pagerduty-cli.py /usr/local/bin/pd # for like, convenience or something

$ /usr/local/bin/pd # or just pd if /usr/local/bin is in your path
+-------+-------------------------------------------------------+--------------+---------------------------------------+
|   #   |                         Title                         |    Status    |                Pending                |
+=======+=======================================================+==============+=======================================+
| 70397 | CRITICAL: 'CONNTRACK' on '....................        | acknowledged | unacknowledge at 2018-12-08T20:33:38Z |
|       | ..................'                                   |              | resolve at 2018-12-09T00:33:38Z       |
|       | https://..........pagerduty.com/incidents/P1OS40E     |              |                                       |
+-------+-------------------------------------------------------+--------------+---------------------------------------+
| 70405 | Host '....................' is ....                   | acknowledged | unacknowledge at 2018-12-08T20:33:38Z |
|       | https://..........pagerduty.com/incidents/PVIHAEI     |              | resolve at 2018-12-09T00:33:38Z       |
|       |                                                       |              |                                       |
+-------+-------------------------------------------------------+--------------+---------------------------------------+
| 70415 | CRITICAL: 'CONNTRACK' on '....................        | acknowledged | unacknowledge at 2018-12-08T20:33:38Z |
|       | ..................'                                   |              | resolve at 2018-12-09T00:33:38Z       |
|       | https://..........pagerduty.com/incidents/PPO8EQG     |              |                                       |
+-------+-------------------------------------------------------+--------------+---------------------------------------+
...

$ /usr/local/bin/pd oncalls
+-----------------------------------------------------------+--------------------------+
|                          Policy                           |         Schedule         |
+===========================================================+==========================+
| Some Escalation Policy                                    |                          |
+-----------------------------------------------------------+--------------------------+
|                                                           | 1 Jane Doe               |
|                                                           | 2 ..... ........         |
+-----------------------------------------------------------+--------------------------+
...
```
