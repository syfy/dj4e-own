import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from unesco.models import Iso,Category,Region,States,Site



Iso.objects.all().delete()
Category.objects.all().delete()
Region.objects.all().delete()
States.objects.all().delete()

fhand = open('unesco/whc-sites-2018-clean.csv')
reader = csv.reader(fhand)
next(reader)  # Advance past the header
for row in reader:
    #row[7] = category
    #row[8] = state
    #row[9] = region
    #row[10] = iso
   # print(row[10])
    try:
        category, created_category = Category.objects.get_or_create(name=row[7])
    except:
       print("creating Categorey")
    try:
        y = int(row[3])
    except:
        y = None
    try:
        validate_hectares = float(row[6])
    except:
        validate_hectares = 0
    try:
        iso, created_iso = Iso.objects.get_or_create(name=row[10])
    except:
       #iso = Iso(name=row[10])
       #  iso.save()
        print(iso)

    try:
        region, created_region = Region.objects.get_or_create(name=row[9])
    except:
        #region =Region(name=row[9])
        #region.save()
        print("creating region")
    try:
        state, created_state = States.objects.get_or_create(name=row[8],region=region)
    except:
        #state= States(name = row[8],region=region)
        #state.save()
        print("creating sate")

    site = Site(name=row[0],description = row[1],justification=row[2],year=y,longitude=row[4],latitude=row[5],area_hectares=validate_hectares,category = category,iso = iso,state=state)
    site.save()


