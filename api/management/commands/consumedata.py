from django.core.management.base import BaseCommand, CommandError
import requests
from api.models import RawData, ParsedData
from api.serializers import RawDataSerializer
from django.db import transaction

class Command(BaseCommand):
    help = 'Consumes data from the /api/rawdata/ endpoint'

    def add_arguments(self, parser):
        '''
            Set the command argument "--token"
            This command it is mandatory because is it used to
            authenticate the user in api app
        '''
        parser.add_argument(
            '--token',
            action='append',
            type=str,
            help='Must be string.',
        )

        '''
            Set the command argument "--pageSize"
            This argument it is used to set the number of the result that will
            be taken from the redis cache and then executed to be moved in db
        '''
        parser.add_argument(
            '--pageSize',
            action='append',
            type=int,
            help='Must be an integer.',
        )

        '''
            Set the command argument "--updateMode"
            This argument was created to handle the update action
            More specific when this command argument was pasted the rendom
            data generator it will create data that are in db in that moment
            and it will be executed the update data action
        '''
        parser.add_argument(
            '--updateMode',
            action='append',
            type=int,
            help='1',
        )

    def handle(self, *args, **options):
        # check the token argument if is set else return error
        if not options['token']:
            self.stderr.write(self.style.ERROR(f"It is necessary to send the --token parameter with a valid token"))
            return

        # check if the page size argument is set else set a default value
        pageSize = 10000
        if options['pageSize']:
            pageSize = options['pageSize'][0]

        # set the update mode
        updateMode = False

        # check if the update mode argument is set and change the update mode
        if options['updateMode']:
            if options['updateMode'][0] != 1:
                # display log error if the update mode it is not allowed
                self.stderr.write(self.style.ERROR(f"UPDATE MODE IS NOT VALID. MUST BE 1"))
                return
            else:
                updateMode = 1

        # send the request to get the page size data fom redis cache
        r = requests.get(
            f"http://127.0.0.1:3000/api/rawdata/?pageSize={pageSize}",
            headers={
                "Authorization":f"Token {options['token'][0]}"
            }
        )

        # check the request status else return the status error code
        if r.status_code != 200:
            self.stderr.write(self.style.ERROR(f"ERROR. HTTP CODE: {r.status_code}"))
            return

        # convert the request response to json data
        data = r.json()

        # check the request result and return error or send them to the db
        if len(data['results']) == 0:
            # display the log where it is specified that the 50000 results was created
            self.stdout.write(self.style.SUCCESS(f"GENERATED 50000 RESULTS WITH A PAGE SIZE: {pageSize}, REMAINING: {data['remaining']}"))
        else:
            # display log with the number of data that will be executed
            self.stdout.write(self.style.SUCCESS(f"GOT: {len(data['results'])}, PAGE SIZE: {pageSize}, REMAINING: {data['remaining']}"))

            with transaction.atomic():
                # set the model obj holder
                rawDataList = []

                # create the obj
                for item in data['results']:
                    serializer = RawDataSerializer(data=item)
                    if serializer.is_valid():
                        rawData = serializer.create(serializer.validated_data)
                        rawDataList.append(rawData)

                # insert the model obj data to db table rowdata
                RawData.objects.bulk_create(rawDataList)

                # display log for this action
                self.stdout.write(self.style.SUCCESS(f"SAVED {len(rawDataList)} ENTRIES IN RAW DATA TABLE"))

                # get the db entries and send them to parsed data table
                lastEntries = RawData.objects.order_by('-id')[:len(data['results'])]

                # set the model obj holder
                parsedDataList = []

                # create the obj
                for item in lastEntries:
                    parsedData = ParsedData(
                        id = item,
                        app=item.network_app,
                        campaign=item.network_campaign,
                        ad_group=item.network_adgroup,
                        clicks=item.taps,
                        impressions=item.views,
                        ad_spend=item.cost,
                        revenues=item.earnings,
                    )
                    parsedDataList.append(parsedData)

                # insert the model obj to db table parseddata
                ParsedData.objects.bulk_create(parsedDataList)

                # display log for this action
                self.stdout.write(self.style.SUCCESS(f"SAVED {len(parsedDataList)} ENTRIES IN PARSED DATA TABLE"))


