'''
Lecture: COMPSCI 1026A 002
Name: Jocelyn Chang

This code generates an output.txt with information about universities in a selected country. This code provides information related to rankings and scores.
'''


def loadCVSData(filename1, filename2):  # function to clean files and convert information into a list
    info = []
    capitalUni = []  # will temporarily hold the used content of filename2

    try:
        with open(filename1, "r", encoding='utf8') as unis, open(filename2, "r", encoding='utf8') as capitals:
            unis.readline()  # gets rid of header
            line = unis.readline()
            while line != "":
                line = line.rstrip("\n")
                uniList = line.split(",")
                del uniList[4:8]  # delete content that will not be used
                info.append(uniList)
                line = unis.readline()
            unis.close()

            capitals.readline()
            line = capitals.readline()
            while line != "":
                line = line.rstrip("\n")
                capitalList = line.split(",")
                del capitalList[2:5]
                capitalUni.append(capitalList)
                line = capitals.readline()
            capitals.close()
    except IOError:
        print("file not found")
        quit()

    for item1 in capitalUni:
        for item2 in info:
            if item2[2] == item1[0]:  # matches the country from filename1 with filename2
                item2.append(item1[1].upper())
                item2.append(item1[2].upper())
                item2[1] = item2[1].upper()
                item2[2] = item2[2].upper()
    return info


def uniCount(info):  # function to count university entries
    number = len(info)
    line = 'Total number of universities => %d\n' % number
    print(line)
    return line


def availCountries(info):  # function to output all the countries in filename1
    countryList = []
    for item in info:
        country = item[2]
        if country not in countryList:  # adds new countries to list
            countryList.append(country)
    line = "Available countries => "
    for country in countryList:  # for loop to format output
        if country == countryList[-1]:
            line += country + "\n"
        else:
            line += country + ", "
    return line


def availContinents(info):  # function will output all the continents if filename2 that have countries in filename1
    continentList = []
    for item in info:
        continent = item[6]
        if continent not in continentList:  # adds new continents to list
            continentList.append(continent)
    line = "Available continents => "
    for continent in continentList:  # for loop to format output
        if continent == continentList[-1]:
            line += continent + "\n"
        else:
            line += continent + ", "
    return line


def internationalRank(info, selectedCountry):  # function finds the university with the best international rank in selected country
    rank = 0
    school = ""
    for item in info:
        if selectedCountry in item:
            rank = int(item[0])  # sets beginning values to compare with other values later
            school = item[1]
            break
    for item in info:
        if selectedCountry in item:
            if int(item[0]) < rank:
                rank = int(item[0])
                school = item[1]
    line = f'At international rank => %d the university name is => %s\n' % (rank, school)
    return line


def nationalRank(info, selectedCountry):  # function finds the university with the best national rank in selected country
    rank = 0
    school = ""
    for item in info:
        if selectedCountry in item:
            rank = int(item[3])  # sets beginning values to compare with other values later
            school = item[1]
            break
    for item in info:
        if selectedCountry in item:
            if int(item[3]) < rank:
                rank = int(item[3])
                school = item[1]
    line = f'At national rank => %d the university name is => %s\n' % (rank, school)
    return line


def avgScore(info, selectedCountry):  # function calculates the average score of all the universities in selected country
    sum = 0.00
    num = 0.00
    for item in info:
        if selectedCountry in item:
            sum += float(item[4])  # sum of the scores of all the universities in selected country
            num += 1  # number of universities in selected country
    avg = sum / num
    line = f'The average score => %.2f%%\n' % avg
    return line


def relativeScore(info, selectedCountry):  # function calculates the continent relative score; divides average by highest score
    highestScore = 0.00
    continent = ""
    for item in info:  # finds continent
        if selectedCountry in item:
            continent = item[-1]
    for item in info:  # finds top score
        if continent in item:
            if float(item[4]) > highestScore:
                highestScore = float(item[4])
    sum = 0.00
    num = 0.00
    for item in info:  # finds average score
        if selectedCountry in item:
            sum += float(item[4])
            num += 1
    avg = sum / num
    relative = (avg / highestScore) * 100.00
    line = f'The relative score to the top university in %s is => (%.2f / %.2f) x 100%% = %.2f%%\n' % (continent, avg, highestScore, relative)
    return line


def capitalCity(info, selectedCountry):  # function finds the capital city of the selected country
    capital = ""
    for item in info:
        if selectedCountry in item:
            capital = item[5]
            break
    line = f'The capital is => %s\n' % capital
    return line


def holdCapital(info, selectedCountry):  # function finds all the universities in a selected country that hold its capitals name
    uniList = []
    for item in info:
        if selectedCountry in item:
            capital = item[5]
            uni = item[1]
            if capital in uni:  # checks if the capital is in the institution name
                uniList.append(uni)
    line = "The universities that contain the capital name =>\n"
    count = 1
    HASHTAG = '#'  # constant value
    for uni in uniList:  # for loop to help format the output
        line += f'%5s%s' % (HASHTAG, count)
        line += f' %s\n' % uni
        count += 1
    return line


def getInformation(selectedCountry, rankingFileName, capitalsFileName):  # function will output all the information calculated by the other functions
    selectedCountry = selectedCountry.upper()  # to undo case-sensitivity
    filename1 = rankingFileName
    filename2 = capitalsFileName

    info = list(loadCVSData(filename1, filename2))

    amount = uniCount(info)
    countries = availCountries(info)
    continents = availContinents(info)
    international = internationalRank(info, selectedCountry)
    national = nationalRank(info, selectedCountry)
    average = avgScore(info, selectedCountry)
    relative = relativeScore(info, selectedCountry)
    capital = capitalCity(info, selectedCountry)
    hold = holdCapital(info, selectedCountry)

    new = open("output.txt", "w")
    new.write(str(amount) + str(countries) + str(continents) + str(international) + str(national) + str(average) + str(relative) + str(capital) + str(hold))
    new.close()

