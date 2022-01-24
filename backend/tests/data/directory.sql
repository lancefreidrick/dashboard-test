BEGIN;
  INSERT INTO directory.person(
    person_id,
    email_address,
    first_name,
    last_name,
    system_role,
    hashed_password,
    is_account_confirmed,
    is_enabled
  )
  VALUES
    (1000000, 'caesar@qwikwire.com', 'Julius', 'Caesar', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000001, 'marius@qwikwire.com', 'Gaius', 'Marius', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000002, 'brutus@qwikwire.com', 'Lucius Junius', 'Brutus', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000003, 'cincinnatus@qwikwire.com', 'Lucius Quinctius', 'Cincinnatus', 'sysadmin'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000004, 'augustus@qwikwire.com', 'Gaius Octavius', 'Thurinus', 'finance'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000005, 'vercingetorix@qwikwire.com', 'Vercingetorix', 'Celtillus', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000006, 'hannibal@qwikwire.com', 'Hannibal', 'Barca', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000007, 'genghis@qwikwire.com', 'Genghis', 'Adolphus', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000008, 'napoleon@qwikwire.com', 'Napoleon', 'Bonaparte', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, false),
    (1000009, 'scipio@qwikwire.com', 'Scipio', 'Africanus', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', false, true),
    (1000010, 'marcus@qwikwire.com', 'Marcus', 'Aurelius', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', false, true),
    (1000011, 'elizabeth@qwikwire.com', 'Elizabeth', 'the Queen', 'payer'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000012, 'maximus@qwikwire.com', 'Maximus Decimus', 'Meridius', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, false),
    (1000013, 'lapu@qwikwire.com', 'Lapu', 'Lapu', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, false),
    (1000014, 'rizal@qwikwire.com', 'Jose', 'Rizal', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true),
    (1000015, 'mabini@qwikwire.com', 'Apolinario', 'Mabini', 'user'::directory.system_role, '$2b$05$u3lmMYzdeXbb8Ml1mAUxrOxD6B9DQz9DsuYyA533z8/gABkEAY04u', true, true)
  ;

  INSERT INTO directory.merchant(
    merchant_id,
    merchant_code,
    merchant_name,
    invoicing_mode,
    merchant_category_id,
    address_one,
    address_two,
    address_three,
    config,
    portal3_config,
    portal_url,
    is_public,
    is_active,
    merchant_timezone,
    owner_id
  )
  VALUES
    (90000, 'rome', 'Roman Empire', 'project', 2, 'Palace of the Emperor', 'Rome', 'Roman Empire', '{}', '{}', '#', true, true, 'Asia/Manila', 1000000),
    (90001, 'parthia', 'Parthia', 'project', 2, 'Taq Kasra', 'Ctesiphon', 'Parthia', '{}', '{}', '#', true, true, 'Asia/Manila', null),
    (90002, 'gaul', 'Gaul', 'default', 1, 'Chief Tribal Council', 'Alesia', 'Gaul', '{}', '{}', '#', true, true, 'Asia/Manila', null),
    (90003, 'carthage', 'Carthage', 'default', 2, 'Carthago', 'Qarthago', 'Carthage', '{}', '{}', '#', true, true, 'Asia/Manila', null),
    (90004, 'macedon', 'Macedonia', 'project', 3, 'Pella', 'Macedonia', 'Macedonia', '{}', '{}', '#', true, true, 'Asia/Manila', null),
    (90005, 'greeks', 'Greek City-States', 'project', 2, 'Athens', 'Athenai', 'Greece', '{}', '{}', '#', true, true, 'Asia/Manila', null),
    (90006, 'mongols', 'Mongolian Empire', 'project', 2, 'Mongolia', 'Mongolia', 'Mongolia', '{}', '{}', '#', true, true, 'Asia/Manila', null)
  ;

  INSERT INTO directory.merchant_member(person_id, merchant_id, merchant_role_id, is_active, can_receive_daily_transaction_emails, can_receive_portals_payment_emails, can_receive_settlement_emails)
  VALUES
    (1000000, 90000, 10, true, true, true, true),
    (1000001, 90000, 20, true, false, true, false),
    (1000002, 90000, 30, true, false, true, false),
    (1000005, 90005, 10, true, true, true, true),
    (1000006, 90000, 10, true, true, true, false),
    (1000006, 90003, 10, false, true, true, true),
    (1000008, 90005, 10, true, true, true, true),
    (1000009, 90000, 10, true, false, true, true),
    (1000010, 90000, 10, false, false, true, false),
    (1000011, 90000, 10, false, false, true, false),
    (1000013, 90000, 10, true, true, true, true),
    (1000014, 90002, 10, true, true, true, true),
    (1000014, 90006, 20, true, true, true, true),
    (1000014, 90004, 30, true, true, true, true),
    (1000015, 90002, 30, true, true, true, true)
  ;

  INSERT INTO directory.merchant_project (
    merchant_project_id,
    merchant_id,
    project_name,
    project_key,
    project_category,
    project_description,
    project_fields,
    project_source,
    is_active,
    is_enabled
  )
  VALUES
    (100000, 90000, 'Colosseum', 'colosseum', 'amphitheatre', NULL, '{"fields": []}', 'test', true, true),
    (100001, 90000, 'Pantheon', 'pantheon', 'temple', NULL, '{"fields": []}', 'test', true, true),
    (100002, 90000, 'Hadrian''s Wall', 'hadrian-wall', 'wall', NULL, '{}', 'test', true, true),
    (100003, 90000, 'Aqueduct', 'aqueduct', 'wall', NULL, '{}', 'test', true, true),
    (100004, 90000, 'Roma Forum', 'forum', 'forum', NULL, '{}', 'test', true, true),
    (100005, 90005, 'Parthenon', 'parthenon', 'temple', NULL, '{}', 'test', true, true),
    (100006, 90005, 'Temple of Artemis', 'artemis', 'temple', NULL, '{}', 'test', true, true),
    (100007, 90005, 'Colossus of Rhodes', 'colossus', 'statue', NULL, '{}', 'test', true, true),
    (100009, 90000, 'Luneta Park of Rome', 'luneta', 'park', NULL, '{}', 'test', true, true),
    (100010, 90000, 'Temple of Jupiter', 'temple-jupiter', 'temple', NULL, '{}', 'test', true, true),
    (100011, 90000, 'Temple of Venus', 'temple-venus', 'temple', NULL, '{}', 'test', true, true),
    (100012, 90000, 'Temple of Mars', 'temple-mars', 'temple', NULL, '{}', 'test', true, true),
    (100013, 90000, 'Temple of Mercury', 'temple-mercury', 'temple', NULL, '{}', 'test', true, true),
    (100014, 90000, 'Temple of Neptune', 'temple-neptune', 'temple', NULL,
      '{"fields": [{"text": "Built On", "name": "builtOn", "value": "20 Nov"},{"text": "Company Code", "name": "companyCode", "value": "2000"}, {"text": "Status", "name": "status", "value": 1}]}',
      'test', true, true),
    (100015, 90000, 'Temple of Pluto', 'temple-pluto', 'temple', NULL,
      '{"fields": [{"text": "Built On", "name": "builtOn", "value": "08 Dec"},{"text": "Company Code", "name": "companyCode", "value": "4000"}, {"text": "Status", "name": "status", "value": 2}]}',
      'test', false, true),
    (100016, 90000, 'Roma Bridge', 'roman-bridge', 'temple', NULL, '{}', 'test', true, false),
    -- Test for disable project
    (100017, 90000, 'Aqueduct 1', 'aqueduct-1', 'aqueduct', NULL, '{}', 'test', true, true),
    (100018, 90000, 'Aqueduct 2', 'aqueduct-2', 'aqueduct', NULL, '{}', 'test', true, true),
    (100019, 90000, 'Aqueduct 3', 'aqueduct-3', 'aqueduct', NULL, '{}', 'test', true, true),
    (100020, 90000, 'Aqueduct 4', 'aqueduct-4', 'aqueduct', NULL, '{}', 'test', true, true),
    (100021, 90000, 'Aqueduct 5', 'aqueduct-5', 'aqueduct', NULL, '{}', 'test', true, true),
    (100022, 90000, 'Aqueduct 6', 'aqueduct-6', 'aqueduct', NULL, '{}', 'test', true, true),
    (100023, 90000, 'Aqueduct 7', 'aqueduct-7', 'aqueduct', NULL, '{}', 'test', true, true),
    (100024, 90000, 'Aqueduct 8', 'aqueduct-8', 'aqueduct', NULL, '{}', 'test', false, true),
    -- Test for publish project
    (100025, 90000, 'Aqueduct 9', 'aqueduct-9', 'aqueduct', NULL, '{}', 'test', false, true),
    (100026, 90000, 'Aqueduct 10', 'aqueduct-10', 'aqueduct', NULL, '{}', 'test', false, true),
    (100027, 90000, 'Aqueduct 11', 'aqueduct-11', 'aqueduct', NULL, '{}', 'test', false, true),
    (100028, 90000, 'Aqueduct 12', 'aqueduct-12', 'aqueduct', NULL, '{}', 'test', false, true),
    (100029, 90000, 'Aqueduct 13', 'aqueduct-13', 'aqueduct', NULL, '{}', 'test', false, true),
    (100030, 90000, 'Aqueduct 14', 'aqueduct-14', 'aqueduct', NULL, '{}', 'test', false, true),
    (100031, 90000, 'Aqueduct 15', 'aqueduct-15', 'aqueduct', NULL, '{}', 'test', false, true),
    (100032, 90000, 'Aqueduct 16', 'aqueduct-16', 'aqueduct', NULL, '{}', 'test', true, true),
    -- Test for delete project
    (100033, 90000, 'Aqueduct 17', 'aqueduct-17', 'aqueduct', NULL, '{}', 'test', true, true),
    (100034, 90000, 'Aqueduct 18', 'aqueduct-18', 'aqueduct', NULL, '{}', 'test', true, true),
    (100035, 90000, 'Aqueduct 19', 'aqueduct-19', 'aqueduct', NULL, '{}', 'test', true, true),
    (100036, 90000, 'Aqueduct 20', 'aqueduct-20', 'aqueduct', NULL, '{}', 'test', true, true),
    (100037, 90000, 'Aqueduct 21', 'aqueduct-21', 'aqueduct', NULL, '{}', 'test', true, true),
    (100038, 90000, 'Aqueduct 22', 'aqueduct-22', 'aqueduct', NULL, '{}', 'test', true, true),
    (100039, 90000, 'Aqueduct 23', 'aqueduct-23', 'aqueduct', NULL, '{}', 'test', true, true),
    (100040, 90000, 'Aqueduct 24', 'aqueduct-24', 'aqueduct', NULL, '{}', 'test', false, true),
    (100041, 90000, 'Aqueduct 25', 'aqueduct-25', 'aqueduct', NULL, '{}', 'test', true, true),
    (100042, 90000, 'Aqueduct 26', 'aqueduct-26', 'aqueduct', NULL, '{}', 'test', true, true)
  ;

  INSERT INTO directory.payment_mode (
    payment_mode_id,
    payment_mode_code,
    payment_mode_name
  )
  VALUES
    (20000, 'ROMA-CL', 'Collatio lustralis'),
    (20001, 'ROMA-AU', 'Aes uxorium')
  ;

  INSERT INTO directory.payment_type (
    payment_type_id,
    payment_type_code,
    payment_type_name
  )
  VALUES
    (20000, 'ROMA-VL', 'Vicesima libertatis'),
    (20001, 'ROMA-VG', 'Vectigal'),
    (20002, 'GREEK-ES', 'Eisphorá'),
    (20003, 'GREEK-KAP', 'Kápêloi')
  ;

  INSERT INTO directory.merchant_payment_mode (merchant_id, payment_mode_id)
  VALUES
  (90000, 20000),
  (90000, 20001);

  INSERT INTO directory.merchant_payment_type (merchant_id, payment_type_id)
  VALUES
  (90000, 20000),
  (90000, 20001),
  (90005, 20002),
  (90005, 20003);

  INSERT INTO directory.merchant_payment_method (
    merchant_payment_method_id,
    merchant_id,
    method_code,
    method_mode,
    currency,
    payment_processor,
    rate_markup,
    rate_fixed_amount,
    conversion_markup,
    conversion_fixed_amount,
    is_auto_debit_enabled,
    metadata,
    is_enabled
  )
  VALUES
    (100000, 90000, 'card', 'tiered', 'USD', 'BT', 1, 0, 1.04, 0, true, '{}', true),
    (100001, 90000, 'card', 'formula', 'PHP', 'MB', 1.029, 0, 1.04, 0, false, '{}', true),
    (100002, 90000, 'ach', 'formula', 'USD', 'BT', 1, 0, 1.04, 0, false, '{}', false),
    (100003, 90000, 'ewallet', 'formula', 'PHP', 'PMG', 1, 0, 1.04, 0, false, '{"channels" : [{"name" : "Grab", "code" : "grab_pay"}, {"name" : "GCash", "code" : "gcash"}]}', false),
    (100004, 90000, 'directDebit', 'formula', 'PHP', 'XD', 1, 0, 1.04, 0, false, '{"channels" : [{"name" : "UnionBank", "code" : "BA_UBP"}, {"name" : "BPI", "code" : "BA_BPI"}, {"name" : "BDO", "code" : "BA_BDO"}]}', false),
    (100005, 90000, 'ideal', 'tiered', 'EUR', 'BT', 1, 0, 1.04, 0, false, '{}', false),
    (100006, 90000, 'applepay', 'tiered', 'USD', 'BT', 1, 0, 1.04, 0, false, '{}', false),
    (100007, 90000, 'alipay', 'formula', 'RMB', 'AL', 1.029, 10, 1.04, 0, true, '{}', true),
    (100008, 90000, 'wechatpay', 'formula', 'RMB', 'WC', 1.029, 10, 1.04, 0, true, '{}', true),
    (100009, 90000, 'googlepay', 'tiered', 'USD', 'BT', 1, 0, 1.04, 0, true, '{}', true),
    (100010, 90000, 'mspay', 'tiered', 'USD', 'BT', 1, 0, 1.04, 0, true, '{}', true),
    (100011, 90000, 'sepa', 'tiered', 'EUR', 'BT', 1, 0, 1.04, 0, true, '{}', true),
    (100012, 90000, 'sofort', 'tiered', 'EUR', 'BT', 1, 0, 1.04, 0, true, '{}', true),
    (100013, 90000, 'cartes', 'tiered', 'EUR', 'BT', 1, 0, 1.04, 0, true, '{}', true)
  ;

  SELECT setval('directory.person_person_id_seq',
    COALESCE((SELECT MAX(person_id) + 1 FROM directory.person), 1), false);
  SELECT setval('directory.merchant_merchant_id_seq',
    COALESCE((SELECT MAX(merchant_id) + 1 FROM directory.merchant), 1), false);
  SELECT setval('directory.payment_mode_payment_mode_id_seq',
    COALESCE((SELECT MAX(payment_mode_id) + 1 FROM directory.payment_mode), 1), false);
  SELECT setval('directory.payment_type_payment_type_id_seq',
    COALESCE((SELECT MAX(payment_type_id) + 1 FROM directory.payment_type), 1), false);
  SELECT setval('directory.merchant_project_merchant_project_id_seq',
    COALESCE((SELECT MAX(merchant_project_id) + 1 FROM directory.merchant_project), 1), false);
  SELECT setval('directory.merchant_payment_method_merchant_payment_method_id_seq',
    COALESCE((SELECT MAX(merchant_payment_method_id) + 1 FROM directory.merchant_payment_method), 1), false);

COMMIT;
