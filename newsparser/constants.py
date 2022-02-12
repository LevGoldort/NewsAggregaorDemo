import os
import pwd
import pathlib

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Path to parent folder
USERNAME = pwd.getpwuid(os.getuid())[0]  # System username


# Startup data:

#
# asap = Subscription(
#         short_name='ASAP',
#         long_name='News sent maximum after 10 minutes they gone live',
#         cron_setting='10 * * * *'
#
#     )
#
# daily7pm = Subscription(
#         short_name='Daily7PM',
#         long_name='News sent every day at 7PM',
#         cron_setting='0 19 * * *'
#
#     )
#
# daily10pm = Subscription(
#         short_name='Daily10PM',
#         long_name='News sent every day at 10PM',
#         cron_setting='0 22 * * *'
#     )
#
# weeklyfriday10am = Subscription(
#         short_name='WeeklyFriday10AM',
#         long_name='News sent every week at Friday at 10AM',
#         cron_setting='0 10 * * 5'
#     )
#
# weeklysunday7am = Subscription(
#         short_name='WeeklySunday7AM',
#         long_name='News sent every week at Sunday at 7AM',
#         cron_setting='0 7 * * 7'
#     )