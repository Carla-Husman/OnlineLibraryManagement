--                                                          VERIFICARI LEGATE DE UPDATEURI (MODIFICARI)
--RETURNARI

--Returnare Carla astazi: cartea luata in biblioteca in stare buna
Select id_inchiriere, stare_inchiriere, inchirieri.id_scaun, disponibilitate from inchirieri, sali_lectura where sali_lectura.id_scaun = 7 and inchirieri.id_scaun = 7;

UPDATE sali_lectura set disponibilitate = 1 where id_scaun = 7; 
UPDATE inchirieri set stare_inchiriere = 'buna', id_scaun = NULL where id_scaun = 7;

Select id_inchiriere, stare_inchiriere, inchirieri.id_scaun, disponibilitate from inchirieri, sali_lectura where sali_lectura.id_scaun = 7 and nr_card = 7777771 and id_carte = 101 and data_inchiriere = TO_CHAR(SYSDATE,'DD-MM-YYYY');
ROLLBACK;   
    
--Returnare Carla astazi: carte luata cu deplasare in stare pierduta
select inchirieri.id_carte, exemplare 
    from inchirieri, carti 
    where nr_card = 7777771 and inchirieri.id_carte = 100 and data_inchiriere = TO_CHAR(SYSDATE - 3,'DD-MM-YYYY') and inchirieri.id_carte = carti.id_carte;  
    
UPDATE inchirieri set stare_inchiriere = 'pierduta', data_returnare = TO_CHAR(SYSDATE,'DD-MM-YYYY') where nr_card = 7777771 and id_carte = 100 and data_inchiriere = TO_CHAR(SYSDATE - 3,'DD-MM-YYYY');
UPDATE carti set exemplare = exemplare - 1 where id_carte = 100; --decrementarea unei carti de pe stoc

select inchirieri.id_carte, exemplare 
    from inchirieri, carti 
    where nr_card = 7777771 and inchirieri.id_carte = 100 and data_inchiriere = TO_CHAR(SYSDATE - 3,'DD-MM-YYYY') and inchirieri.id_carte = carti.id_carte;   

--Returnare Stefana astazi: 1 carte in stare uzata citite in biblioteca
Select id_inchiriere, stare_inchiriere, inchirieri.id_scaun, disponibilitate from inchirieri, sali_lectura where sali_lectura.id_scaun = 1 and inchirieri.id_scaun = 1;

UPDATE sali_lectura set disponibilitate = 1 where id_scaun = 1; 
UPDATE inchirieri set stare_inchiriere = 'uzata', id_scaun = NULL where id_scaun = 1;

Select id_inchiriere, stare_inchiriere, inchirieri.id_scaun, disponibilitate from inchirieri, sali_lectura where sali_lectura.id_scaun = 1 and nr_card = 7777772 and id_carte = 103 and data_inchiriere = TO_CHAR(SYSDATE,'DD-MM-YYYY');


-- PRELUNGIRE DATA DE INCHIRIERE

--Stefana doreste prelungirea perioadei de inchiriere cu 2 zile pentru cartea cu id ul 104
Select id_inchiriere, data_returnare from inchirieri where nr_card = 7777772 and id_carte = 104 and data_inchiriere = TO_CHAR(SYSDATE,'DD-MM-YYYY') ;

UPDATE inchirieri set data_returnare = TO_CHAR(data_returnare + 2,'DD-MM-YYYY') where nr_card = 7777772 and id_carte = 104 and data_inchiriere = TO_CHAR(SYSDATE,'DD-MM-YYYY');

Select id_inchiriere, data_returnare from inchirieri where nr_card = 7777772 and id_carte = 104 and data_inchiriere = TO_CHAR(SYSDATE,'DD-MM-YYYY') ;


--                                                                          AFISARE

-- afisarea clientilor si detaliilor acestora
SELECT clienti.nr_card, nume, clienti.id_cnp, serie_numar, telefon
FROM clienti, detalii_clienti
WHERE clienti.id_cnp = detalii_clienti.id_cnp;

--afisarea cartilor donate si informatiile despre donatori
select nume_carte, nume_donator, telefon_donator
from carti, donatori
where carti.id_donator = donatori.id_donator;

--afisarea cartilor care nu sunt donate si informatiile despre donatori
select *
from carti
where id_donator is NULL;

-- afisarea inchirierilor 
select id_inchiriere, stare_inchiriere, data_inchiriere, data_returnare, id_scaun, nume_carte, inchirieri.nr_card, nume
from clienti, inchirieri, carti
where inchirieri.nr_card = clienti.nr_card and inchirieri.id_carte = carti.id_carte;

-- numarul total de carti de la o editura
select id_nume_editura, Count(id_nume_editura) "Editura Paralela"
from carti
where id_nume_editura = 'Paralela'
group by id_nume_editura;

--numarul total de carti din biblioteca
select sum(exemplare) "Numarul total de carti din biblioteca"
from carti;

-- afisarea tuturor cartilor inchiriate
select nume_carte "Carti inchiriate"
from inchirieri, carti
where inchirieri.id_carte = carti.id_carte;

-- cel mai fidel client 
with
    inch as (select nume, count(inchirieri.nr_card) nr_inc
                from inchirieri, clienti
                where inchirieri.nr_card = clienti.nr_card
                group by nume),
    maxim as (select max(nr_inc) M from inch) 
select clienti.nume, M
from inch, maxim, clienti
where inch.nume = clienti.nume and M = nr_inc;

-- cel care a inchiriat cel mai rar
with
    inch as (select nume, count(inchirieri.nr_card) nr_inc
                from inchirieri, clienti
                where inchirieri.nr_card = clienti.nr_card
                group by nume),
    minim as (select min(nr_inc) M from inch) 
select clienti.nume, M
from inch, minim, clienti
where inch.nume = clienti.nume and M = nr_inc;

-- cartea cea mai inchiriata
with
    carti_cnt as (select nume_carte titlu, count(inchirieri.id_carte) numar
                        from inchirieri, carti
                        where inchirieri.id_carte = carti.id_carte
                        group by nume_carte),
    cmi as (select max(numar) M from carti_cnt)
SELECT titlu, M
FROM carti_cnt, cmi 
WHERE numar = M;

-- afisarea cartilor care mai pot fi inchiriate
select nume_carte
from carti
where disponibilitate(id_carte) is not null;

-- afisarea tutoror cartilor de fictiune
select nume_carte 
from carti
where gen = 'fictiune';

--afisarea cartilor, a anului de aparitie si a starii returnate de dinainte de anul 2000
select nume_carte, an_aparitie, stare_inchiriere
from carti, inchirieri
where an_aparitie < 2000 and carti.id_carte = inchirieri.id_carte;

--afisarea cartilor care au fost inchiriate de catre Carla
select nume_carte
from carti, inchirieri
where inchirieri.nr_card = (select nr_card from clienti where nume LIKE '%Carla')
        and carti.id_carte = inchirieri.id_carte;
        
--afisarea cartilor care nu au an de aparitie si 
--a caror autor are numele terminat in litera 'u'
--si ordonarea acestora in ordine crescatoare
--dupa nume, apoi descrescatoare dupa numarul de exemplare
select nume_carte, autor, an_aparitie, exemplare
from carti
where an_aparitie is not null and autor LIKE '%u'
order by nume_carte asc, exemplare desc;

--sa se afiseze numele clientilor din Iasi care au facut inchirieri
select distinct(nume)
from detalii_clienti dc, clienti c, inchirieri i
where dc.id_cnp = c.id_cnp and i.nr_card = c.nr_card and serie_numar LIKE 'IS%';


--                                                                  VERIFICAREA CHECKURILOR

--check DETALII CLIENTI
update detalii_clienti set id_cnp = 12345;
update detalii_clienti set id_cnp = '1234567890123';
update detalii_clienti set serie_numar = 'IS123456';
update detalii_clienti set telefon = '076481233';

--check CLIENTI
UPDATE clienti set nume = '123H';
UPDATE clienti SET nr_card = 123456;

--check SALI_LECTURA
UPDATE sali_lectura set disponibilitate = 3; 

--check EDITURI
update edituri set id_nume_editura = 'H123' where id_nume_editura = 'Nemira';
update edituri set telefon_editura = '076481232a';
update edituri set adresa = 'Str. Pantelimon, Nr16;';

--check DONATORI
UPDATE donatori set nume_donator = '123H';
update donatori set telefon_donator = '07648123';

--check CARTI
update carti set autor = 'Ionel 2';
update carti set gen = 'sf.';
update carti set an_aparitie = 800;
update carti set exemplare = -1;

--check INCHIRIERI
update inchirieri set stare_inchiriere = 'patata';



--                                                                ADAUGARE DE COLOANA
--Sa se adauge coloana Tip_coperta in tabela CARTI, de tip VARCHAR2(9)
--si sa i se adauge o constrangere care sa limiteze inregistrarile pentru aceasta
--coloana la urmatoarele valori: brosata, dura, cartonata, 
ALTER TABLE carti ADD tip_coperta VARCHAR2(9) 
    CONSTRAINT inchirieri_coperta_ck CHECK  (tip_coperta in ('cartonata', 'brosata', 'dura'));



--                                                               STERGERE DE INREGISTRARE
--Stergeti inregistrarea din tabela INCHIRIERI pentru cartea Soarele 
--care a fost tinuta inchiriata mai mult de 7 zile
DELETE FROM inchirieri
WHERE id_carte = (SELECT  id_carte
                    FROM carti 
                    WHERE nume_carte = 'Soarele')
    AND data_returnare - data_inchiriere > 7;
