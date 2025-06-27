INSERT INTO suppliers (name, address, bank_details)
VALUES 
		('mleko', 'Pipirkina,13', '394853485739475chiki-briki'),
		('slych', 'havai,340', '1353452345FGGEG-DDF'),
		('zabiy', 'lvivska,18', '7352623HHDDFV-ZABI'),
		('did_baba', 'didivska,69', '37845835873645DID-BABA'),
		('OBL_moloko', 'molochna,44', '6734763545345MOLO-KO'),
		('popki', 'chota,52', '66328648374DYP34-KI'),
		('lapki', 'lapkeri,1213', '3847388758475LI-HI'),
		('chyhpani', 'rozezd,87', '38648735RAZ-EZD'),
		('ROSHEN', 'pypypy,23', '38645435RAZ-EZD'),
		('tipyli', 'tipochkov,1', '7623476ROV-NIE');

INSERT INTO products (products_id, category, realization_date, weight, price, suppliers_name)
VALUES 
		(2, 'molochka', '2024-10-24', 2, 50, 'mleko'),	
		(3, 'kants', '2030-12-13', 0.05, 5, 'slych'),
		(4, 'miaso', '2024-10-20', 1, 120, 'zabiy'),
		(5, 'solodke', '2024-12-01', 0.5, 42, 'ROSHEN'),
		(6, 'kants', '2025-05-14', 0.1, 4.5, 'did_baba'),
		(7, 'kants', '2025-11-04', 0.3, 3, 'slych'),
		(8, 'molochka', '2024-10-24', 5, 325, 'OBL_moloko'),
		(9, 'miaso', '2024-10-15', 1.5, 675, 'zabiy'),
		(10, 'solodke', '2024-12-09', 0.3, 42, 'lapki'),
		(11, 'patsanache', '2024-12-01', 1, 1500, 'chyhpani');