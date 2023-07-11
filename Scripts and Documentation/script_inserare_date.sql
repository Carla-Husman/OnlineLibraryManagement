-- DETALII CLIENTI & CLIENTI
INSERT INTO detalii_clienti VALUES (1234567890001, 'BT 000001', '0760000001');
INSERT INTO clienti VALUES (7777771, 'Aluculesei Georgiana', 1234567890001);

INSERT INTO detalii_clienti VALUES (1234567890002, 'IS 000001', '0760000002');
INSERT INTO clienti VALUES (7777772, 'Hriscu Stefana', 1234567890002);

INSERT INTO detalii_clienti VALUES (1234567890003, 'IS 000002', '0760000003');
INSERT INTO clienti VALUES (7777773, 'Rosca Madalina', 1234567890003);

INSERT INTO detalii_clienti VALUES (1234567890004, 'BT 000002', '0760000004');
INSERT INTO clienti VALUES (7777774, 'Birbiliu Larisa', 1234567890004);

INSERT INTO detalii_clienti VALUES (1234567890005, 'IS 000003', '0760000004');
INSERT INTO clienti VALUES (7777775, 'Gania Andreea', 1234567890005);

-- EDITURI
INSERT INTO edituri values ('Globo', 'Bulevardul Poitiers 6, Iasi', '0761111111');
INSERT INTO edituri values ('Libra', 'Bulevardul Nicolae Balcescu 20, Cluj', '0761111112');
INSERT INTO edituri values ('Arthur', 'Str. Cotroceni nr. 26, Bucuresti', '0761111113');
INSERT INTO edituri values ('Paralela', 'Strada Sfantul Lazar nr. 27, Iasi', '0761111114');
INSERT INTO edituri values ('Litera', 'Bulevardul Carol I 3, Iasi ', '0761111115');
INSERT INTO edituri values ('Bloomsbury', 'Bulevardul Pantelimon 54, Iasi ', '0761111225');

-- CARTI --
INSERT INTO carti (nume_carte, autor, gen, an_aparitie, exemplare, id_nume_editura) 
    values ('Intelepciunea psihopatilor', 'Kevin Dutton', 'psihologie', 2013, 1, 'Globo');
INSERT INTO carti (nume_carte, autor, gen, an_aparitie, exemplare, id_nume_editura) 
    values ('Legendele Olimpului', 'Alexandru Mitru', 'mitologie', 1960, 2, 'Libra');
INSERT INTO carti (nume_carte, autor, gen, exemplare, id_nume_editura) 
    values ('Morometii Vol.1', 'Marin Preda', 'social', 4, 'Arthur');
INSERT INTO carti (nume_carte, autor, gen, an_aparitie, exemplare, id_nume_editura) 
    values ('Harry Potter Vol.1', 'J. K. Rowling', 'fantastic', 1997, 3, 'Bloomsbury');
INSERT INTO carti (nume_carte, gen, exemplare, id_nume_editura) 
    values ('Intelepciunea lui Confucius', 'cugetari', 5,'Paralela');
INSERT INTO carti (nume_carte, autor, gen, exemplare, id_nume_editura) 
    values ('Emma!', 'Owens Aly', 'mister', 2, 'Paralela');


--INCHIRIERI
--Tranzactie Madalina acum 3 zile (REUSESTE)
Begin
    INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card) 
        VALUES (TO_CHAR (SYSDATE - 3, 'dd-mm-YYYY'), TO_CHAR (SYSDATE + 4, 'dd-mm-YYYY'), disponibilitate(100), 7777773);      
    commit;
end;  
/

--Tranzactie Madalina astazi (REUSESTE)
Begin
    INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card) 
        VALUES (TO_CHAR (SYSDATE, 'dd-mm-YYYY'), TO_CHAR (SYSDATE + 7, 'dd-mm-YYYY'), disponibilitate(101), 7777773);
    commit;
end; 
/

--Tranzactii Stefana astazi (NU REUSESTE pentru ca nu mai am pe stoc, e inchiriata de catre Madalina) 
Begin
    INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card) 
        VALUES (TO_CHAR (SYSDATE, 'dd-mm-YYYY'), TO_CHAR (SYSDATE + 7, 'dd-mm-YYYY'), disponibilitate(100), 7777772);
COMMIT;
END; 
/

--Tranzactie Georgiana cu 2 carti ieri si astazi (REUSESTE)
Begin 
INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card) 
    VALUES (TO_CHAR (SYSDATE-1, 'dd-mm-YYYY'), TO_CHAR (SYSDATE + 6, 'dd-mm-YYYY'), disponibilitate(104), 7777771);
    commit;
END;
/
Begin
    INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card) 
    VALUES (TO_CHAR (SYSDATE, 'dd-mm-YYYY'), TO_CHAR (SYSDATE + 7, 'dd-mm-YYYY'), disponibilitate(105), 7777771);
    commit;
end;
/

--Tranzactie Larisa astazi (REUSESTE)
Begin INSERT INTO inchirieri (data_inchiriere, data_returnare, id_carte, nr_card) 
    VALUES (TO_CHAR (SYSDATE, 'dd-mm-YYYY'), TO_CHAR (SYSDATE + 7, 'dd-mm-YYYY'), disponibilitate(105), 7777774);
    commit;
END;
/