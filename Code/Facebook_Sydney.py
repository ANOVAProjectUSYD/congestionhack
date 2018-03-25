import urllib, facebook, requests, json, datetime, csv, time
from urllib.request import urlopen


def initial_write(name):
    '''Create and write first entry in file.'''
    csv_file = name + '.csv'
    write_file = open(csv_file, 'w')
    writer = csv.writer(write_file)
    writer.writerow(["event_name", "attendance_count",
                     "interested_count", "no_reply_count",
                     "total_invited_count", "description",
                     "start_time", "place" ])
    write_file.close()


def read_data(token):
    '''Open CSV file and pass group into FB'''

    facebook_groups = ["cityofsydney", "spiritualeventsinsydney", "magiccitysydney", "TimeOutSydney", "OpmSydney", "AFL", "sydneyafl", "nrl", "ForsythBarrStadium", "anzstadium", "SydShowground", "qudosbankarena", "ICCSyd", "gaymardigras"]
    initial_write('gaymardigras')
    scrape_api(token, "gaymardigras", 'gaymardigras') # scrapes info about the group


def scrape_api(token, group, file_name):
    '''Scraping FB data.'''
    base = "https://graph.facebook.com/v2.12/"
    url = "?fields=events.limit(5000)%7Bname%2Cattending_count%2Cinterested_count%2Cnoreply_count%2Cdescription%2Cstart_time%2Cplace%7D&access_token="
    link = base + group + url + token
    data = json.loads(urlopen(link).read())
    #print(data['events']['data'][0])

    csv_file = file_name + '.csv'
    write_file = open(csv_file, 'a')
    writer = csv.writer(write_file)
    # collects all the data regarding events
    for i in range(0, len(data['events']['data'])):
        try:
            # what this return is a dictionary in a list in a nested dict.
            data_obj = data['events']['data'][i]
            name = data_obj['name']
            attendance_count = data_obj['attending_count']
            interested_count = data_obj['interested_count']
            no_reply_count = data_obj['noreply_count']
            total_invited_count = attendance_count + interested_count + no_reply_count
            description = data_obj['description']
            start_time = data_obj['start_time']
            place = data_obj['place']['name']

            # Check if event has further info
            writer.writerow([name, attendance_count, interested_count,
                             no_reply_count,
                             total_invited_count, description, start_time,
                             place])
            print("Wrote a row")
        except Exception as e:
            print(e)
            writer.writerow([name, attendance_count, interested_count,
                             no_reply_count,
                             total_invited_count, description, start_time,
                             None])
            continue

    write_file.close()
    print("Done scraping!")


def main():
    token = 'EAACEdEose0cBAIb2jVFn51M5K29eW9SaZAw1ZCt5r0oyCcEdqW24VsrkZBbhpBpatn98dSm1SXyHZBd4F1FfHi2C3kuKsYYVI1vxo3e74sZAWiJdDnBA5DqJgMOhva9Rk9tSbP15mDQZBCV44OYnCTGp5QiDZCWU8d0oV7idqksfZCIWTZCEXQr7cJovTJERYCnI18f9uRwHQWQZDZD'
    read_data(token)


if __name__ == "__main__":
    main()
