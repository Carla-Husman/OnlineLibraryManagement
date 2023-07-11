from datetime import datetime, date
# Create your views here.
import cx_Oracle
import re
from django.http import HttpResponse
from django.template import loader
from Biblioteca.connect import connect_to_oracle
from Biblioteca.config import username, password, dsn, encoding

connect_to_oracle()

connection = cx_Oracle.connect(
    username,
    password,
    dsn,
    encoding=encoding)


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


def clienti(request):
    template = loader.get_template('clienti.html')

    clienti = []

    cur = connection.cursor()
    cur.execute('select * from clienti')
    for result in cur:
        client = {}
        client['nr_card'] = result[0]
        client['nume'] = result[1]
        client['id_cnp'] = result[2]
        clienti.append(client)

    cur.close()

    context = {
        'client': clienti,
    }

    return HttpResponse(template.render(context, request))


def detalii(request, id_cnp):
    template = loader.get_template('detalii.html')

    cur1 = connection.cursor()
    sql = "select nume, serie_numar, telefon " \
          "from detalii_clienti, clienti " \
          "where detalii_clienti.id_cnp=clienti.id_cnp " \
          "and clienti.id_cnp=" + str(id_cnp)
    cur1.execute(sql)

    detalii = []
    for result in cur1:
        detaliu = {}
        detaliu['nume'] = result[0]
        detaliu['serie_numar'] = result[1]
        detaliu['telefon'] = result[2]
        detaliu['id_cnp'] = id_cnp
        detalii.append(detaliu)

    context = {
        'detalii': detalii,
    }
    cur1.close()

    return HttpResponse(template.render(context, request))


def carti(request):
    template = loader.get_template('carti.html')

    carti = []

    cur = connection.cursor()
    cur.execute('select * from carti')
    for result in cur:
        carte = {}
        carte['id_carte'] = result[0]
        carte['nume_carte'] = result[1]
        carte['autor'] = result[2]
        carte['gen'] = result[3]
        carte['an_aparitie'] = result[4]
        carte['exemplare'] = result[5]
        carte['id_nume_editura'] = result[6]
        carti.append(carte)

    cur.close()

    context = {
        'carte': carti,
    }

    return HttpResponse(template.render(context, request))


def inchirieri(request):
    template = loader.get_template('inchirieri.html')

    inchirieri = []

    cur = connection.cursor()
    cur.execute('select * from inchirieri')
    for result in cur:
        inchiriere = {}
        inchiriere['id_inchiriere'] = result[0]
        inchiriere['stare_returnare'] = result[1]
        inchiriere['data_inchiriere'] = result[2].strftime("%d") + "-" + result[2].strftime("%m") + "-" + result[
            2].strftime("%Y")
        inchiriere['data_returnare'] = result[3].strftime("%d") + "-" + result[3].strftime("%m") + "-" + result[
            3].strftime("%Y")
        inchiriere['id_carte'] = result[4]
        inchiriere['nr_card'] = result[5]
        inchirieri.append(inchiriere)
    cur.close()

    context = {
        'inchiriere': inchirieri,
    }

    return HttpResponse(template.render(context, request))


def carte(request, id_carte):
    template = loader.get_template('carte.html')
    inchirieri = []

    cur = connection.cursor()
    cur.execute(
        'select nume_carte,autor,gen,an_aparitie,exemplare,id_nume_editura from carti where id_carte=' + str(id_carte))
    for result in cur:
        inchiriere = {}
        inchiriere['nume_carte'] = result[0]
        inchiriere['autor'] = result[1]
        inchiriere['gen'] = result[2]
        inchiriere['an_aparitie'] = result[3]
        inchiriere['exemplare'] = result[4]
        inchiriere['id_nume_editura'] = result[5]
        inchirieri.append(inchiriere)
    cur.close()

    context = {
        'carte': inchirieri,
    }

    return HttpResponse(template.render(context, request))


def client(request, nr_card):
    template = loader.get_template('client.html')
    clts = []

    cur = connection.cursor()
    cur.execute(
        'select nume,clienti.id_cnp,serie_numar,telefon from clienti,detalii_clienti where clienti.id_cnp=detalii_clienti.id_cnp and nr_card=' + str(
            nr_card))
    for result in cur:
        clt = {}
        clt['nume'] = result[0]
        clt['cnp'] = result[1]
        clt['serie_numar'] = result[2]
        clt['telefon'] = result[3]
        clt['card'] = nr_card
        clts.append(clt)
    cur.close()

    context = {
        'client': clts,
    }

    return HttpResponse(template.render(context, request))


def edituri(request):
    template = loader.get_template('edituri.html')

    edituri = []

    cur = connection.cursor()
    cur.execute('select * from edituri')
    for result in cur:
        editura = {}
        editura['nume'] = result[0]
        editura['adresa'] = result[1]
        editura['telefon'] = result[2]
        edituri.append(editura)

    cur.close()

    context = {
        'edituri': edituri,
    }

    return HttpResponse(template.render(context, request))


def stergereInchiriere(request, id_inchiriere):
    template = loader.get_template('stergereInchiriere.html')

    mesaj = "Operatiune efectuata cu success!"

    cur = connection.cursor()
    cur.execute('delete from inchirieri where id_inchiriere=' + str(id_inchiriere))
    cur.execute('commit')

    context = {
        'mesaj': mesaj,
    }

    return HttpResponse(template.render(context, request))


def stergereClient(request, nr_card):
    template = loader.get_template('stergereClient.html')

    cur = connection.cursor()
    try:
        cur.execute('select id_cnp from clienti where nr_card=' + str(nr_card))
        for result in cur:
            cnp = result[0]
        cur.execute('delete from clienti where nr_card=' + str(nr_card))
        cur.execute('delete from detalii_clienti where id_cnp=' + str(cnp))
        cur.execute('commit')
        mesaj = "Operatiune efectuata cu success!"
    except:
        mesaj = "ACTIUNE INVALIDA! Stergerea nu a reusit." \
                " Clientul pe care doriti sa-l stergeti este in baza de " \
                "date a inchirierilor."

    cur.close()

    context = {
        'mesaj': mesaj,
    }

    return HttpResponse(template.render(context, request))


def stergereCarte(request, id_carte):
    template = loader.get_template('stergereCarte.html')

    cur = connection.cursor()
    try:
        cur.execute('select id_nume_editura from carti where id_carte=' + str(id_carte))
        for result in cur:
            editura = result[0]

        cur.execute('delete from carti where id_carte=' + str(id_carte))

        cur.execute('select id_nume_editura from carti')

        count = 0

        for result in cur:
            if str(result[0]) == str(editura):
                count = count + 1

        if count == 0:
            elem = "'" + str(editura) + "'"
            cur.execute("delete from edituri where id_nume_editura =" + elem)
            cur.execute('commit')
        mesaj = "Operatiune efectuata cu success!"
    except:
        mesaj = "ACTIUNE INVALIDA! Stergerea nu a reusit. Cartea pe care doriti sa o stergeti este in baza de date a inchirierilor."

    cur.close()

    context = {
        'mesaj': mesaj,
    }

    return HttpResponse(template.render(context, request))


def stergereEditura(request, id_editura):
    template = loader.get_template('stergereEditura.html')

    cur = connection.cursor()
    mesaj = ''
    try:
        var = "'" + id_editura + "'"
        cur.execute('delete from edituri where id_nume_editura=' + var)
        cur.execute('commit')
        mesaj = "Operatiune efectuata cu success!"
    except:
        mesaj = "ACTIUNE INVALIDA! Avem contract in prezent cu aceasta editura."

    cur.close()

    context = {
        'mesaj': mesaj,
    }

    return HttpResponse(template.render(context, request))


def editareClient(request, nr_card):
    template = loader.get_template('editareClient.html')
    flag = 1
    cur = connection.cursor()
    detaliu = {}

    cur.execute(
        'select nume, serie_numar, telefon from clienti,detalii_clienti where clienti.id_cnp = detalii_clienti.id_cnp and nr_card=' + str(
            nr_card))
    for result in cur:
        detaliu['nr_card'] = nr_card
        detaliu['nume'] = result[0]
        detaliu['serie_numar'] = result[1]
        detaliu['telefon'] = result[2]

    mesaj = ''
    if request.method == 'POST':
        nume = request.POST.get('your_name')
        serie = request.POST.get('serie')
        telefon = request.POST.get('telefon')

        if nume != detaliu['nume']:
            var = "'" + nume + "'"
            try:
                cur.execute('update clienti set nume=' + var + ' where nr_card=' + str(nr_card))
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Numele trebuie sa contina doar litere si spatii.'
                flag = 0

        if serie != detaliu['serie_numar']:
            var = "'" + serie.upper() + "'"
            try:
                cur.execute(
                    'update detalii_clienti set serie_numar=' + var + ' where id_cnp=(select id_cnp from clienti where nr_card=' + str(
                        nr_card) + ')')
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Seria si numarul trebuie sa contina 6 cifre, un spatiu si 2 litere. (unic)'
                flag = 0

        if telefon != detaliu['telefon']:
            var = "'" + telefon + "'"
            try:
                cur.execute(
                    'update detalii_clienti set telefon=' + var + ' where id_cnp=(select id_cnp from clienti where nr_card=' + str(
                        nr_card) + ')')
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Telefonul este introdus gresit!'
                flag = 0

    detaliu = {}

    cur.execute(
        'select nr_card, nume, clienti.id_cnp, serie_numar, telefon from clienti,detalii_clienti where clienti.id_cnp = detalii_clienti.id_cnp and nr_card=' + str(
            nr_card))
    for result in cur:
        detaliu = {}
        detaliu['nr_card'] = result[0]
        detaliu['nume'] = result[1]
        detaliu['cnp'] = result[2]
        detaliu['serie_numar'] = result[3]
        detaliu['telefon'] = result[4]

    context = {
        'mesaj': mesaj,
        'detaliu': detaliu,
        'flag': flag,
    }

    cur.close()

    return HttpResponse(template.render(context, request))


def editareCarte(request, id_carte):
    template = loader.get_template('editareCarte.html')

    mesaj = ''

    cur = connection.cursor()
    carte = {}

    cur.execute('select * from carti where id_carte=' + str(id_carte))
    for result in cur:
        carte['nume_carte'] = result[1]
        carte['autor'] = result[2]
        carte['gen'] = result[3]
        carte['an'] = result[4]
        carte['exemplare'] = result[5]
        carte['editura'] = result[6]

    edituri = []

    cur.execute('select id_nume_editura from edituri')
    for result in cur:
        editura = {}
        editura['nume'] = result[0]
        edituri.append(editura)

    flag = 1
    if request.method == 'POST':
        denumire = request.POST.get('nume')
        autor = request.POST.get('autor')
        gen = request.POST.get('gen')
        an = request.POST.get('an')
        exemplare = request.POST.get('exemplare')
        editura = request.POST.get('editura')

        if denumire != carte['nume_carte']:
            var = "'" + denumire + "'"
            try:
                cur.execute('update carti set nume_carte=' + var + ' where id_carte=' + str(id_carte))
                cur.execute('commit')
                mesaj = 'Operatiune completa23!'
            except:
                mesaj = 'Editarea nu a reusit.'
                flag = 0
        if autor != carte['autor']:
            var = "'" + autor + "'"
            try:
                cur.execute('update carti set autor=' + var + ' where id_carte=' + str(id_carte))
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Numele autorului trebuie sa contina doar litere si spatii.'
                flag = 0

        if gen != carte['gen']:
            var = "'" + gen + "'"
            try:
                cur.execute('update carti set gen=' + var + ' where id_carte=' + str(id_carte))
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Genul trebuie sa contina doar litere.'
                flag = 0

        if an != carte['an']:
            try:
                if an == '':
                    cur.execute('update carti set an_aparitie=NULL where id_carte=' + str(id_carte))
                else:
                    cur.execute('update carti set an_aparitie=' + str(an) + ' where id_carte=' + str(id_carte))
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Anul trebuie sa contina doar cifre si sa fie cuprins intre 1000 si 2023'
                flag = 0

        if exemplare != carte['exemplare']:
            try:
                cur.execute('update carti set exemplare=' + str(exemplare) + ' where id_carte=' + str(id_carte))
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Numarul de exemplare trebuie sa fie mai mare sau egal cu 0.'
                flag = 0

        if editura != carte['editura']:
            try:
                var = "'" + str(editura) + "'"
                cur.execute('update carti set id_nume_editura=' + var + ' where id_carte=' + str(id_carte))
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Nu avem contract cu aceasta editura!'
                flag = 0

    carte = {}

    cur.execute('select * from carti where id_carte=' + str(id_carte))
    for result in cur:
        carte['nume_carte'] = result[1]
        carte['autor'] = result[2]
        carte['gen'] = result[3]
        carte['an'] = result[4]
        carte['exemplare'] = result[5]
        carte['editura'] = result[6]

    edituri = []

    cur.execute('select id_nume_editura from edituri')
    for result in cur:
        editura = {}
        editura['nume'] = result[0]
        edituri.append(editura)

    context = {
        'mesaj': mesaj,
        'carte': carte,
        'edituri': edituri,
        'flag': flag,
    }

    cur.close()

    return HttpResponse(template.render(context, request))


def editareInchiriere(request, id_inchiriere):
    template = loader.get_template('editareInchiriere.html')

    cur = connection.cursor()
    inchiriere = {}

    cur.execute('select * from inchirieri where id_inchiriere=' + str(id_inchiriere))
    for result in cur:
        inchiriere['stare'] = result[1]
        var = result[2].strftime("%Y") + "-" + result[2].strftime("%m") + "-" + result[2].strftime("%d")
        inchiriere['data_inchiriere'] = var
        var = result[3].strftime("%Y") + "-" + result[3].strftime("%m") + "-" + result[3].strftime("%d")
        inchiriere['data_returnare'] = var
        inchiriere['carte'] = result[4]
        inchiriere['card'] = result[5]

    carti = []

    cur.execute('select id_carte,nume_carte from carti')
    for result in cur:
        carte = {}
        carte['id'] = result[0]
        carte['nume'] = result[1]
        carti.append(carte)

    clienti = []

    cur.execute('select nr_card,nume from clienti')
    for result in cur:
        client = {}
        client['card'] = result[0]
        client['nume'] = result[1]
        clienti.append(client)

    mesaj = ''
    flag = 1

    if request.method == 'POST':
        stare = request.POST.get('stare')
        dataI = request.POST.get('dataI')
        dataR = request.POST.get('dataR')
        carte_id = request.POST.get('id')
        card = request.POST.get('card')

        if stare != inchiriere['stare']:
            var = "'" + stare + "'"
            try:
                cur.execute(
                    'update inchirieri set stare_inchiriere=' + var + ' where id_inchiriere=' + str(id_inchiriere))
                cur.execute('commit')
                if stare == 'pierduta':
                    cur.execute(
                        'update carti set exemplare=exemplare-1 where id_carte=(select id_carte from inchirieri where id_inchiriere=' + str(
                            id_inchiriere) + ')')
                    cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Starea negasita!'
                flag = 0

        data_str1 = datetime.strptime(dataI, '%Y-%m-%d').date()
        data_str2 = datetime.strptime(dataR, '%Y-%m-%d').date()
        if data_str1 <= data_str2:
            if dataR != inchiriere['data_returnare']:
                data_str = datetime.strptime(dataR, '%Y-%m-%d').date()
                temp = str(data_str.strftime("%d")) + "-" + str(data_str.strftime("%m")) + "-" + str(
                        data_str.strftime("%Y"))
                var = "'" + temp + "'"
                convert = "'dd-mm-YYYY'"
                try:
                    cur.execute(
                            'update inchirieri set data_returnare=TO_DATE(' + var + ',' + convert + ') where id_inchiriere=' + str(
                                id_inchiriere))
                    cur.execute('commit')

                    mesaj = 'Operatiune completa!'
                except:
                    mesaj = 'Editarea nu a reusit. Data invalida!'
                    flag = 0
        else:
            mesaj = 'Operatiune invalida! Data de returnare trebuie sa fie dupa data inchirierii!'
            flag = 0

    inchiriere = {}

    cur.execute('select * from inchirieri where id_inchiriere=' + str(id_inchiriere))
    for result in cur:
        inchiriere['stare'] = result[1]
        var = result[2].strftime("%Y") + "-" + result[2].strftime("%m") + "-" + result[2].strftime("%d")
        inchiriere['data_inchiriere'] = var
        var = result[3].strftime("%Y") + "-" + result[3].strftime("%m") + "-" + result[3].strftime("%d")
        inchiriere['data_returnare'] = var
        inchiriere['carte'] = result[4]
        inchiriere['card'] = result[5]

    carti = []

    cur.execute('select id_carte,nume_carte from carti')
    for result in cur:
        carte = {}
        carte['id'] = result[0]
        carte['nume'] = result[1]
        carti.append(carte)

    clienti = []

    cur.execute('select nr_card,nume from clienti')
    for result in cur:
        client = {}
        client['card'] = result[0]
        client['nume'] = result[1]
        clienti.append(client)

    cur.close()

    context = {
        'mesaj': mesaj,
        'inchiriere': inchiriere,
        'clienti': clienti,
        'carti': carti,
        'flag': flag,
    }

    return HttpResponse(template.render(context, request))


def editareEditura(request, id_editura):
    template = loader.get_template('editareEditura.html')

    cur = connection.cursor()
    editura = {}

    var = "'" + id_editura + "'"
    cur.execute('select * from edituri where id_nume_editura=' + var)
    for result in cur:
        editura['nume'] = result[0]
        editura['adresa'] = result[1]
        editura['telefon'] = result[2]

    mesaj = ''
    flag = 1

    if request.method == 'POST':
        adresa = request.POST.get('adresa')
        telefon = request.POST.get('telefon')

        if adresa != editura['adresa']:
            var = "'" + adresa + "'"
            var2 = "'" + id_editura + "'"
            try:
                cur.execute(
                    'update edituri set adresa=' + var +
                    ' where id_nume_editura=' + var2)
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Adresa invalida!'
                flag = 0

        if telefon != editura['telefon']:
            var = "'" + telefon + "'"
            var2 = "'" + id_editura + "'"
            try:
                cur.execute(
                    'update edituri set telefon_editura=' + var +
                    ' where id_nume_editura=' + var2)
                cur.execute('commit')
                mesaj = 'Operatiune completa!'
            except:
                mesaj = 'Editarea nu a reusit. Telefonul este introdus gresit!'
                flag = 0

    var = "'" + id_editura + "'"
    cur.execute('select * from edituri where id_nume_editura=' + var)
    for result in cur:
        editura['nume'] = result[0]
        editura['adresa'] = result[1]
        editura['telefon'] = result[2]

    context = {
        'mesaj': mesaj,
        'flag': flag,
        'editura': editura,
    }

    return HttpResponse(template.render(context, request))


def adaugareClient(request):
    template = loader.get_template('adaugareClient.html')

    mesaj = ''
    flag = 1

    mesajTelefon = ''
    mesajCnp = ''
    mesajCard = ''
    mesajNume = ''
    mesajSerie = ''

    cur = connection.cursor()
    if request.method == 'POST':
        card = request.POST.get('card')
        nume = request.POST.get('nume')
        serie = request.POST.get('serie')
        cnp = request.POST.get('cnp')
        telefon = request.POST.get('telefon')

        pat = re.compile(r"^[a-zA-Z_]+( [a-zA-Z_]+)*$")
        if re.fullmatch(pat, nume):
            mesajNume = ''
        else:
            mesajNume = 'Doar litere si spatii'
            flag = 0

        pat = re.compile(r"^([0-9]{7})$")
        if re.fullmatch(pat, card):
            mesajCard = ''
        else:
            mesajCard = 'Format invalid. Doar 7 cifre.'
            flag = 0

        pat = re.compile(r"^(([A-Z]){2}|B)( )([0-9]){6}$")
        if re.fullmatch(pat, serie):
            mesajSerie = ''
        else:
            mesajSerie = 'Format invalid'
            flag = 0

        cur.execute('select id_cnp from detalii_clienti')
        UNIQUE = 1
        for result in cur:
            var = str(result[0])
            if var == cnp:
                UNIQUE = 0

        pat = re.compile(r"^[1-9]{1}[0-9]{12}$")
        if UNIQUE == 0:
            mesajCnp = 'Ati introdus un CNP existent'
            flag = 0
        elif re.fullmatch(pat, cnp):
            mesajCnp = ''
        else:
            mesajCnp = 'Format invalid'
            flag = 0

        pat = re.compile(r"^((07)([0-9]){8})$")
        if re.fullmatch(pat, telefon):
            mesajTelefon = ''
        else:
            mesajTelefon = 'Introduceti doar 10 cifre (07..)'
            flag = 0

        if flag == 1:
            mesaj = 'Inserare completa!'
            var1 = "'" + serie + "'"
            var2 = "'" + telefon + "'"
            cur.execute('INSERT INTO detalii_clienti '
                        'VALUES (' + str(cnp) + ',' + var1 + ',' + var2 + ')')
            var1 = "'" + nume + "'"
            cur.execute('INSERT INTO clienti '
                        'VALUES (' + str(card) + ',' + var1 + ',' + str(cnp) + ')')
            cur.execute('commit')
        else:
            mesaj = 'Inserarea a esuat!'

    cur.close()

    context = {
        'mesaj': mesaj,
        'mesajTelefon': mesajTelefon,
        'mesajCnp': mesajCnp,
        'mesajNume': mesajNume,
        'mesajCard': mesajCard,
        'mesajSerie': mesajSerie,
        'flag': flag,
    }

    return HttpResponse(template.render(context, request))


def adaugareEditura(request):
    template = loader.get_template('adaugareEditura.html')

    mesaj = ''
    flag = 1
    mesajNume = ''
    mesajStrada = ''
    mesajNr = ''
    mesajJudet = ''
    mesajOras = ''
    mesajTelefon = ''

    cur = connection.cursor()
    if request.method == 'POST':
        nume = request.POST.get('nume')
        strada = request.POST.get('strada')
        nr = request.POST.get('nr')
        judet = request.POST.get('judet')
        oras = request.POST.get('oras')
        telefon = request.POST.get('telefon')

        cur.execute('select id_nume_editura from edituri')
        UNIQUE = 1
        for result in cur:
            var = str(result[0])
            if var == nume:
                UNIQUE = 0

        pat = re.compile(r"^[A-z]*$")
        if UNIQUE == 0:
            mesajNume = 'Editura existenta!'
            flag = 0
        elif re.fullmatch(pat, nume):
            mesajNume = ''
        else:
            mesajNume = 'Format invalid! Doar litere'
            flag = 0

        pat = re.compile(r"^((07)([0-9]){8})$")
        if re.fullmatch(pat, telefon):
            mesajTelefon = ''
        else:
            mesajTelefon = 'Introduceti doar 10 cifre (07..)'
            flag = 0

        # construire adresa
        adresaCompleta = 'Str. '
        pat = re.compile(r"^[a-zA-Z_ \\.]*$")
        if re.fullmatch(pat, strada):
            mesajStrada = ''
            adresaCompleta = adresaCompleta + str(strada)
        else:
            mesajStrada = 'Format invalid! (Ex: Sf. Gheorghe)'
            flag = 0

        adresaCompleta = adresaCompleta + ', '
        pat = re.compile(r"^[0-9]*$")
        if re.fullmatch(pat, nr):
            mesajNr = ''
            adresaCompleta = adresaCompleta + nr
        else:
            mesajNr = 'Format invalid! (Ex: 5))'
            flag = 0

        adresaCompleta = adresaCompleta + ', '
        pat = re.compile(r"^[a-zA-Z]*$")
        if re.fullmatch(pat, judet):
            mesajJudet = ''
            adresaCompleta = adresaCompleta + str(judet)
        else:
            mesajJudet = 'Format invalid! (Ex: Iasi))'
            flag = 0

        if oras != '':
            adresaCompleta = adresaCompleta + ', '
            pat = re.compile(r"^[a-zA-Z]*$")
            if re.fullmatch(pat, oras):
                mesajOras = ''
                adresaCompleta = adresaCompleta + str(oras)
            else:
                mesajOras = 'Format invalid! (Ex: Raducaneni))'
                flag = 0

        if flag == 1:
            mesaj = 'Inserare completa!'
            var1 = "'" + adresaCompleta + "'"
            var2 = "'" + telefon + "'"
            var3 = "'" + nume + "'"
            cur.execute('INSERT INTO edituri VALUES (' + var3 + ',' + var1 + ',' + var2 + ')')
            cur.execute('commit')
        else:
            mesaj = 'Inserarea a esuat!'

    cur.close()

    context = {
        'mesaj': mesaj,
        'flag': flag,
        'mesajNume': mesajNume,
        'mesajStrada': mesajStrada,
        'mesajNr': mesajNr,
        'mesajJudet': mesajJudet,
        'mesajOras': mesajOras,
        'mesajTelefon': mesajTelefon,
    }

    return HttpResponse(template.render(context, request))


def adaugareCarte(request):
    template = loader.get_template('adaugareCarte.html')

    cur = connection.cursor()
    edituri = []

    cur.execute('select id_nume_editura from edituri')
    for result in cur:
        editura = {}
        editura['nume'] = result[0]
        edituri.append(editura)

    mesajNume = ''
    mesajAutor = ''
    mesajGen = ''
    mesajAn = ''
    mesajEx = ''

    mesaj = ''
    flag = 1

    if request.method == 'POST':
        nume = request.POST.get('nume')
        autor = request.POST.get('autor')
        gen = request.POST.get('gen')
        an = request.POST.get('an')
        exemplare = request.POST.get('exemplare')
        editura = request.POST.get('editura')

        pat = re.compile(r"^[a-zA-Z_ 0-9\\,.!*]*$")
        if re.fullmatch(pat, nume):
            mesajNume = ''
        else:
            mesajNume = 'Format invalid!'
            flag = 0

        if autor != '':
            pat = re.compile(r"^[a-zA-Z_ \\.]*$")
            if re.fullmatch(pat, autor):
                mesajAutor = ''
            else:
                mesajAutor = 'Ex. Mc. Ailey'
                flag = 0

        pat = re.compile(r"^[A-z]*$")
        if re.fullmatch(pat, gen):
            mesajGen = ''
        else:
            mesajGen = 'Doar litere!'
            flag = 0

        pat = re.compile(r"^[1-2]{1}[0-9]{3}$")
        anNumber = int(an)
        if re.fullmatch(pat, an):
            if (anNumber > 1000) and (anNumber < 2024):
                mesajAn = ''
            else:
                mesajAn = 'Interval (1000,2024)'
        else:
            mesajAn = 'Interval (1000,2024)'
            flag = 0

        pat = re.compile(r"^[0-9]$")
        exNumber = int(exemplare)
        if re.fullmatch(pat, exemplare):
            if (exNumber > 0) and (exNumber < 100):
                mesajEx = ''
            else:
                mesajEx = 'Interval [0,100)'
        else:
            mesajEx = 'Format invalid!'
            flag = 0

        if flag == 1:
            mesaj = 'Inserare completa!'
            var1 = "'" + nume + "'"
            var2 = "'" + autor + "'"
            var3 = "'" + gen + "'"
            var4 = "'" + editura + "'"
            cur.execute('INSERT INTO carti (nume_carte, autor, gen, an_aparitie, exemplare, id_nume_editura) '
                        'VALUES (' + var1 + ',' + var2 + ',' + var3 + ',' + an + ',' + exemplare + ',' + var4 + ')')
            cur.execute('commit')
        else:
            mesaj = 'Inserarea a esuat!'

    cur.close()

    context = {
        'mesaj': mesaj,
        'flag': flag,
        'edituri': edituri,
        'mesajNume': mesajNume,
        'mesajEx': mesajEx,
        'mesajAn': mesajAn,
        'mesajGen': mesajGen,
        'mesajAutor': mesajAutor,
    }

    return HttpResponse(template.render(context, request))


def adaugareInchiriere(request):
    template = loader.get_template('adaugareInchiriere.html')

    mesaj = ''
    flag = 1

    cur = connection.cursor()

    carti = []
    cur.execute('select distinct(nume_carte) from carti')
    for result in cur:
        carte = {}
        carte['nume'] = result[0]
        carti.append(carte)

    genuri = []
    cur.execute('select distinct(gen) from carti')
    for result in cur:
        gen = {}
        gen['gen'] = result[0]
        genuri.append(gen)

    autori = []
    cur.execute('select distinct(autor) from carti')
    for result in cur:
        autor = {}
        autor['autor'] = result[0]
        autori.append(autor)

    carduri = []
    cur.execute('select nr_card from clienti')
    for result in cur:
        card = {}
        card['card'] = result[0]
        carduri.append(card)

    if request.method == 'POST':
        carte = request.POST.get('carte')
        autor = request.POST.get('autor')
        gen = request.POST.get('gen')
        card = request.POST.get('card')
        stare = request.POST.get('stare')
        dataI = request.POST.get('dataI')
        temp1 = datetime.strptime(dataI, '%Y-%m-%d').date()  # asta e pentru testare
        data_inchiriere = "'" + str(temp1.strftime("%d")) + "-" + str(temp1.strftime("%m")) \
                          + "-" + str(temp1.strftime("%Y")) + "'"  # asta o introduci in baza de date
        dataR = request.POST.get('dataR')
        temp2 = datetime.strptime(dataR, '%Y-%m-%d').date()  # asta e pentru testare
        data_returnare = "'" + str(temp2.strftime("%d")) + "-" + str(temp2.strftime("%m")) \
                         + "-" + str(temp2.strftime("%Y")) + "'"  # asta o introduci in baza de date

        if temp1 > date.today():
            mesaj = mesaj + '\n' \
                            'Data de inchiriere nu poate fi din viitor.'
            flag = 0

        if temp2 < temp1:
            mesaj = mesaj + '\n' \
                            'Data returnare nu poate fi inaintea celei de inchiriere.'
            flag = 0

        if stare == 'error':
            stare = ''
        if stare == 'error':
            autor = ''

        if flag == 0:
            mesaj = mesaj + '\nTranzactie esuata!'
        elif carte == 'error' or gen == 'error' or card == 'error':
            mesaj = '\nTranzactie esuata!'
            flag = 0
        elif flag == 1:
            # alegere id carte
            var1 = "'" + carte + "'"
            var2 = "'" + autor + "'"
            var3 = "'" + gen + "'"
            try:
                cur.execute(
                    'select id_carte from carti where nume_carte=' + var1 + ' and autor =' + var2 + " and gen=" + var3);
                id_carte = ''
                for result in cur:
                    id_carte = result[0]
                convert = "'dd-mm-YYYY'"
                # cur.execute('BEGIN');
                if stare == '':
                    try:
                        cur.execute('INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card)'
                                    'VALUES(TO_DATE(' + data_inchiriere + ',' + convert + '), ' +
                                    'TO_DATE(' + data_returnare + ',' + convert + '),disponibilitate(' + str(
                            id_carte) + ")," + str(card) + ')')
                        cur.execute('commit')
                        mesaj = '\nTranzactie finalizata cu succes!'
                    except:
                        flag = 0
                        mesaj = '\nNu mai avem carti disponibile! Toate exemplarele sunt date spre inchiriere.'
                else:
                    stare = "'" + stare + "'"
                    try:
                        cur.execute(
                            'INSERT INTO inchirieri (stare_inchiriere, data_inchiriere, data_returnare, id_carte, nr_card)'
                            'VALUES(' + stare + ',TO_DATE(' + data_inchiriere + ',' + convert + '), ' +
                            'TO_DATE(' + data_returnare + ',' + convert + '),disponibilitate(' + str(
                                id_carte) + ")," + str(card) + ')')
                        cur.execute('commit')
                        mesaj = '\nTranzactie finalizata cu succes!'
                    except:
                        flag = 0
                        mesaj = '\nNu mai avem carti disponibile! Toate exemplarele sunt date spre inchiriere.'
            except:
                flag = 0
                mesaj = '\nCarte negasita!'

    cur.close()

    context = {
        'mesaj': mesaj,
        'flag': flag,
        'carti': carti,
        'autori': autori,
        'genuri': genuri,
        'carduri': carduri,
    }

    return HttpResponse(template.render(context, request))
