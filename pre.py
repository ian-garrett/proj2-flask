"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """
    field = None
    entry = { }
    cooked = [ ] 

    #i = number of weeks to add
    i = 0
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                startdate = content
                base = arrow.get(content)
                splitdate = content.split("/")
                weekdate = arrow.get(int(splitdate[2]),int(splitdate[0]),int(splitdate[1]))
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }

            #set current week and next week
            currentWeek = weekdate.replace(weeks=+(i))
            newWeek = weekdate.replace(weeks=+i+1)
            #by default, a week is considered to not be the current week. This saves an extra line of code that would result from an else statement
            entry['now'] = "false"
            #process marking current week
            if currentWeek < arrow.now() < newWeek:
                entry['now'] = "true"
                #make a swithc, and when this condition is true, flip is to mark this week

            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = "Week "+content+": "
            entry['weekdate'] = currentWeek.format('MM-DD')
            i += 1
            #Advance current week by i (number of weeks so far +1)
            currentWeek = currentWeek.replace(weeks=+i)

        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    return cooked


def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
