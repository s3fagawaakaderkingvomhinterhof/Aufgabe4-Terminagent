#########################
# Logic Class of Client #
#########################

def parse_string_to_calendar_array(data):
    calendar = []
    b = data.replace("[[", "").replace("]]", "")
    for line in b.split('], ['):
        row = list(map(int, line.split(
            ',')))
        calendar.append(row)
    return calendar
