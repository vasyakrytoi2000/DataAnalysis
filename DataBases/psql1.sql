CREATE TABLE suppliers(  --створив таблицю з назвою suppliers
	name TEXT NOT NULL PRIMARY KEY, --колонка 'name' і типом даних text, є первинним ключем не може бути без даних
	address TEXT NOT NULL, -- колонка 'address' тип text не може бути без даних
	bank_details VARCHAR(34) NOT NULL -- колонка 'bank_details' тип VARCHAR не може бути без даних
);

CREATE TABLE products( --створив таблицю з назвою products
	products_id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY,--автоматична нумерація																	
	category VARCHAR(128) NOT NULL,                                           
	realization_date DATE NOT NULL,                                            
	weight NUMERIC(18,3) NOT NULL,                                            
	price MONEY NOT NULL,                                                     
	suppliers_name TEXT NOT NULL,

	CONSTRAINT suppliers_name_fk FOREIGN KEY (suppliers_name) REFERENCES suppliers (name)
);--правило що колонка suppliers_name є зовнішнім ключем і посилається на колонку name таблиці suppliers