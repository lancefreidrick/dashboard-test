BEGIN;
  DELETE FROM auditing.activity_log WHERE person_id >= 1000000;
  DELETE FROM invoicing.transaction_invoice_log WHERE invoice_id IN (
    SELECT invoice_id FROM invoicing.invoice WHERE transaction_id >= 9000000
  );

  DELETE FROM invoicing.settlement_invoice WHERE settlement_id >= 90000;
  UPDATE invoicing.settlement_file SET settlement_id = NULL WHERE settlement_id >= 90000;
  DELETE FROM invoicing.settlement_file WHERE settlement_file_id >= 80000;
  DELETE FROM invoicing.settlement WHERE settlement_id >= 90000;

  DELETE FROM invoicing.invoice WHERE transaction_id >= 9000000;
  DELETE FROM invoicing.transaction WHERE transaction_id >= 9000000;
  DELETE FROM invoicing.payment_method WHERE payment_method_id >= 9000000;

  DELETE FROM directory.merchant_payment_mode WHERE payment_mode_id >= 20000;
  DELETE FROM directory.merchant_payment_type WHERE payment_type_id >= 20000;

  DELETE FROM directory.payment_mode WHERE payment_mode_id >= 20000;
  DELETE FROM directory.payment_type WHERE payment_type_id >= 20000;
  DELETE FROM directory.merchant_project WHERE merchant_id >= 90000;
  DELETE FROM directory.merchant_payment_method WHERE merchant_id >= 90000;
  DELETE FROM directory.merchant_member WHERE person_id >= 100000;
  DELETE FROM directory.merchant WHERE merchant_id >= 90000;
  DELETE FROM directory.session WHERE person_id >= 1000000;
  DELETE FROM directory.person WHERE person_id >= 1000000;

COMMIT;

